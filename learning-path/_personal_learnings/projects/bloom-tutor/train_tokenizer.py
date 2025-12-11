# train_tokenizer.py
"""
Tokenizer training code (BPE over your notes)
"""

from tokenizers import Tokenizer, models, trainers, pre_tokenizers
from pathlib import Path

notes_path = Path("notes.txt")
assert notes_path.exists(), "Create notes.txt with your learning notes."

tokenizer = Tokenizer(models.BPE(unk_token="[UNK]"))
tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

trainer = trainers.BpeTrainer(
    vocab_size=16000,
    min_frequency=2,
    special_tokens=["[PAD]", "[UNK]", "[BOS]", "[EOS]"]
)

tokenizer.train([str(notes_path)], trainer)
tokenizer.save("tokenizer.json")

print("Saved tokenizer.json with vocab size:", tokenizer.get_vocab_size())



