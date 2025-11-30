# bloom_mini_gpt.py
"""
Real small model from scratch (mini GPT for your notes)
This is a non-toy but still small GPT-style model (~10–20M params depending on config).
You can plug in your own tokenizer (trained in step 3) or use an existing one.
"""

import math
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path
from typing import Tuple, Optional

# ---------------- CONFIG ----------------
block_size = 256  # max context length
n_embd = 256  # embedding dim
n_head = 8  # attention heads
n_layer = 6  # transformer layers
batch_size = 32
learning_rate = 2e-4
max_steps = 50_000  # adjust as needed
eval_interval = 1000

# Get script directory for relative paths
SCRIPT_DIR = Path(__file__).parent.absolute()

device = "mps" if torch.backends.mps.is_available() else "cpu"
torch.set_float32_matmul_precision("high")
print("Using device:", device)

# ------------- TOKENIZER HOOKS ----------
# Option A: use existing tokenizer (e.g. GPT-2) via transformers
# Option B: use your own BPE tokenizer.json from step 3

def load_tokenizer(tokenizer_path: Optional[str] = None):
    """Load tokenizer from file or fallback to GPT-2."""
    if tokenizer_path is None:
        tokenizer_path_obj = SCRIPT_DIR / "tokenizer.json"
    else:
        tokenizer_path_obj = Path(tokenizer_path)
    
    if tokenizer_path_obj.exists():
        try:
            from tokenizers import Tokenizer
            tokenizer = Tokenizer.from_file(str(tokenizer_path_obj))
            print(f"Loaded custom tokenizer from {tokenizer_path_obj}")
            return tokenizer
        except Exception as e:
            print(f"Failed to load custom tokenizer: {e}")
            print("Falling back to GPT-2 tokenizer...")
    
    # Fallback to GPT-2 tokenizer
    try:
        from transformers import GPT2Tokenizer
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        print("Using GPT-2 tokenizer as fallback")
        return tokenizer
    except ImportError:
        raise ImportError(
            "Please install transformers: pip install transformers\n"
            "Or train a tokenizer first: python train_tokenizer.py"
        )


tokenizer = load_tokenizer()


def encode(text: str):
    """Encode text to token IDs."""
    if hasattr(tokenizer, 'encode'):
        # HuggingFace tokenizer
        return tokenizer.encode(text, return_tensors=None)
    else:
        # tokenizers library
        return tokenizer.encode(text).ids


def decode(ids):
    """Decode token IDs to text."""
    if isinstance(ids, torch.Tensor):
        ids = ids.tolist()
    if hasattr(tokenizer, 'decode'):
        # HuggingFace tokenizer
        return tokenizer.decode(ids, skip_special_tokens=True)
    else:
        # tokenizers library
        return tokenizer.decode(ids)


# ------------- DATA LOADING -------------
# Put all your learning notes in notes.txt (large as you want)
data_path = SCRIPT_DIR / "notes.txt"
if not data_path.exists():
    raise FileNotFoundError(
        f"notes.txt not found at {data_path}\n"
        "Please create notes.txt with your learning notes in the same directory."
    )

raw_text = data_path.read_text()
ids = encode(raw_text)
if isinstance(ids, list):
    ids = torch.tensor(ids, dtype=torch.long)
else:
    ids = ids if isinstance(ids, torch.Tensor) else torch.tensor(ids, dtype=torch.long)

data = ids

n = int(0.9 * len(data))
train_data = data[:n]
val_data = data[n:]


def get_batch(split: str) -> Tuple[torch.Tensor, torch.Tensor]:
    """Get a batch of training or validation data."""
    source = train_data if split == "train" else val_data
    if len(source) < block_size + 1:
        raise ValueError(f"Data too short: need at least {block_size + 1} tokens, got {len(source)}")
    ix = torch.randint(len(source) - block_size - 1, (batch_size,))
    x = torch.stack([source[i:i+block_size] for i in ix])
    y = torch.stack([source[i+1:i+block_size+1] for i in ix])
    return x.to(device), y.to(device)


# Get vocab size
if hasattr(tokenizer, 'vocab_size'):
    vocab_size = tokenizer.vocab_size
elif hasattr(tokenizer, 'get_vocab_size'):
    vocab_size = tokenizer.get_vocab_size()
else:
    # Fallback: estimate from data
    vocab_size = int(data.max().item() + 1)
    print(f"Warning: Could not determine vocab size, using {vocab_size} from data")

print("Vocab size:", vocab_size)

# ------------- MODEL --------------------


class CausalSelfAttention(nn.Module):
    def __init__(self, n_embd, n_head):
        super().__init__()
        assert n_embd % n_head == 0
        self.n_head = n_head
        self.key = nn.Linear(n_embd, n_embd, bias=False)
        self.query = nn.Linear(n_embd, n_embd, bias=False)
        self.value = nn.Linear(n_embd, n_embd, bias=False)
        self.proj = nn.Linear(n_embd, n_embd, bias=False)
        mask = torch.tril(torch.ones(block_size, block_size)).view(1, 1, block_size, block_size)
        self.register_buffer("mask", mask)

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x).view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        q = self.query(x).view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        v = self.value(x).view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) / math.sqrt(C // self.n_head)
        # Apply causal mask - self.mask is a registered buffer (torch.Tensor)
        causal_mask: torch.Tensor = self.mask  # type: ignore
        mask = causal_mask[:, :, :T, :T]
        att = att.masked_fill(mask == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        y = self.proj(y)
        return y


class Block(nn.Module):
    def __init__(self, n_embd, n_head):
        super().__init__()
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)
        self.attn = CausalSelfAttention(n_embd, n_head)
        self.mlp = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.GELU(),
            nn.Linear(4 * n_embd, n_embd),
        )

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x


class MiniBloomGPT(nn.Module):
    def __init__(self, vocab_size, n_embd, n_head, n_layer, block_size):
        super().__init__()
        self.block_size = block_size
        self.tok_emb = nn.Embedding(vocab_size, n_embd)
        self.pos_emb = nn.Embedding(block_size, n_embd)
        self.blocks = nn.ModuleList([Block(n_embd, n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size, bias=False)
        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, (nn.Linear, nn.Embedding)):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
        if isinstance(module, nn.Linear) and module.bias is not None:
            nn.init.zeros_(module.bias)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        assert T <= self.block_size
        pos = torch.arange(0, T, device=idx.device).unsqueeze(0)
        x = self.tok_emb(idx) + self.pos_emb(pos)
        for blk in self.blocks:
            x = blk(x)
        x = self.ln_f(x)
        logits = self.lm_head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(
                logits.view(-1, logits.size(-1)),
                targets.view(-1),
            )
        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=0.8, top_k=40):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.block_size:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] / temperature
            if top_k is not None:
                v, _ = torch.topk(logits, top_k)
                logits[logits < v[:, [-1]]] = -float("inf")
            probs = F.softmax(logits, dim=-1)
            next_id = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, next_id), dim=1)
        return idx


def main():
    """Main training function."""
    print("\n" + "="*60)
    print("Bloom Mini GPT - Training")
    print("="*60)
    
    model = MiniBloomGPT(vocab_size, n_embd, n_head, n_layer, block_size).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.1)
    
    print(f"\nModel parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
    print(f"Training data: {len(train_data):,} tokens")
    print(f"Validation data: {len(val_data):,} tokens")
    print(f"Total steps: {max_steps:,}\n")

    def estimate_loss():
        model.eval()
        out = {}
        with torch.no_grad():
            for split in ("train", "val"):
                losses = []
                for _ in range(20):
                    xb, yb = get_batch(split)
                    _, loss = model(xb, yb)
                    losses.append(loss.item())
                out[split] = sum(losses) / len(losses)
        model.train()
        return out

    # Training loop
    for step in range(max_steps):
        xb, yb = get_batch("train")
        logits, loss = model(xb, yb)
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        if step % eval_interval == 0:
            losses = estimate_loss()
            print(f"step {step:6d}: train {losses['train']:.3f}, val {losses['val']:.3f}")

    # Save model
    model_path = SCRIPT_DIR / "bloom_mini_gpt.pt"
    torch.save(model.state_dict(), model_path)
    print(f"\nModel saved to {model_path}")

    # Quick sample generation
    print("\n" + "="*60)
    print("Sample Generation")
    print("="*60)
    context_text = "Explain backpropagation: "
    ctx_ids = torch.tensor([encode(context_text)], dtype=torch.long).to(device)
    out_ids = model.generate(ctx_ids, max_new_tokens=200)[0].tolist()
    print("\nPrompt:", context_text)
    print("\nGenerated:")
    print(decode(out_ids))
    print()


if __name__ == "__main__":
    main()

