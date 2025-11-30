# ============================================================================
# Objective 5: Tensors - Working with Tensors
# ============================================================================
# Understanding PyTorch tensors and tensor operations

from llm_fundamentals_support import (
    LLMFundamentalsSupport, ModelLoader, TextProcessor, EmbeddingExtractor,
    Formatter, StateManager, DeviceDetector
)
import torch

support = LLMFundamentalsSupport()
formatter = Formatter()
state_mgr = StateManager()
device_detector = DeviceDetector()

print(formatter.header("OBJECTIVE 5: TENSORS"))
print(formatter.learning_intro(
    concept="Tensors",
    description="Tensors are multi-dimensional arrays that store all data in neural networks. They are the fundamental data structure in PyTorch.",
    what_we_learn=[
        "What tensors are (multi-dimensional arrays)",
        "Tensor shapes and dimensions [batch, seq, features]",
        "Common tensor operations (element-wise, matrix multiply, reductions)",
        "GPU vs CPU tensors and device management",
        "Tensor broadcasting for operations on different shapes"
    ],
    what_we_do=[
        "Create tensors of different dimensions (0D, 1D, 2D, 3D)",
        "Inspect tensor shapes, sizes, and memory usage",
        "Perform tensor operations (add, multiply, matrix multiply)",
        "Move tensors between CPU and GPU",
        "Understand broadcasting with different shapes"
    ],
    hands_on=[
        "Create scalar (0D), vector (1D), matrix (2D), 3D tensors",
        "Create embedding tensor: [batch=2, seq=5, hidden=768]",
        "Perform operations: a + b, a * b, a @ b",
        "Reductions: sum(), mean(), max()",
        "Indexing: a[0], a[:, 0], a[0, 1]",
        "Move tensor to GPU/MPS if available"
    ]
))

# Part 1: Creating and Manipulating Tensors
print(formatter.section("Part 1: Creating and Manipulating Tensors - Hands-On Code"))

try:
    print("\n📦 Creating Tensors:")
    scalar = torch.tensor(5.0)
    vector = torch.tensor([1.0, 2.0, 3.0])
    matrix = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    tensor_3d = torch.randn(2, 3, 4)
    
    print(f"   Scalar: {scalar}, shape: {scalar.shape}, dims: {scalar.dim()}")
    print(f"   Vector: {vector}, shape: {vector.shape}, dims: {vector.dim()}")
    print(f"   Matrix: shape {matrix.shape}, dims: {matrix.dim()}")
    print(f"   3D Tensor: shape {tensor_3d.shape}, dims: {tensor_3d.dim()}")
    
    print(f"\n🔧 Common Creation Methods:")
    zeros = torch.zeros(3, 4)
    ones = torch.ones(2, 3)
    rand = torch.rand(2, 3)
    randn = torch.randn(2, 3)
    
    print(f"   zeros(3,4): shape {zeros.shape}")
    print(f"   ones(2,3): shape {ones.shape}")
    print(f"   rand(2,3): shape {rand.shape}, range [0,1)")
    print(f"   randn(2,3): shape {randn.shape}, mean≈0, std≈1")
    
    print(formatter.output_summary([
        "Tensors can be 0D (scalar), 1D (vector), 2D (matrix), or ND (higher dimensions)",
        "Shape determines dimensions: (3, 4) = 3 rows × 4 columns",
        "Common creation: zeros(), ones(), rand(), randn()",
        "rand() = uniform [0,1), randn() = normal distribution"
    ]))
except Exception as e:
    print(f"❌ Error: {e}")

# Part 2: Tensor Shapes and Dimensions
print(formatter.section("Part 2: Tensor Shapes and Dimensions - Real Example"))

try:
    batch_size, seq_len, hidden_dim = 2, 5, 768
    embedding_tensor = torch.randn(batch_size, seq_len, hidden_dim)
    
    print(f"\n📊 Example: Embedding Tensor")
    print(f"   Shape: {embedding_tensor.shape}")
    print(f"   Dimensions: {embedding_tensor.dim()}D")
    print(f"   Size: {embedding_tensor.numel()} elements")
    print(f"   Memory: ~{embedding_tensor.numel() * 4 / 1024:.2f} KB (float32)")
    
    print(f"\n🔍 Dimension Breakdown:")
    print(f"   [0] Batch dimension: {embedding_tensor.shape[0]} samples")
    print(f"   [1] Sequence dimension: {embedding_tensor.shape[1]} tokens")
    print(f"   [2] Feature dimension: {embedding_tensor.shape[2]} features")
    
    print(f"\n🔄 Reshaping:")
    flattened = embedding_tensor.view(-1, hidden_dim)
    print(f"   Original: {embedding_tensor.shape}")
    print(f"   Flattened: {flattened.shape} (batch*seq, hidden)")
    
    print(formatter.output_summary([
        f"Embedding tensor shape [2, 5, 768] = 2 batches × 5 tokens × 768 features",
        f"Total elements: {embedding_tensor.numel():,} = 2 × 5 × 768",
        f"Memory usage: ~{embedding_tensor.numel() * 4 / 1024:.2f} KB (float32)",
        "Can reshape: view(-1, 768) flattens batch and sequence dimensions",
        "Shape determines how data is organized and processed"
    ]))
except Exception as e:
    print(f"❌ Error: {e}")

# Part 3: Common Tensor Operations
print(formatter.section("Part 3: Common Tensor Operations - Math Operations"))

try:
    a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    b = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
    
    print(f"\n🧮 Basic Operations:")
    print(f"   a + b (element-wise):\n{a + b}")
    print(f"   a * b (element-wise):\n{a * b}")
    print(f"   a @ b (matrix multiply):\n{a @ b}")
    
    print(f"\n📐 Reduction Operations:")
    print(f"   a.sum(): {a.sum().item()}")
    print(f"   a.mean(): {a.mean().item()}")
    print(f"   a.max(): {a.max().item()}")
    print(f"   a.sum(dim=0): {a.sum(dim=0)} (sum along rows)")
    print(f"   a.sum(dim=1): {a.sum(dim=1)} (sum along columns)")
    
    print(f"\n🔀 Indexing and Slicing:")
    print(f"   a[0]: {a[0]} (first row)")
    print(f"   a[:, 0]: {a[:, 0]} (first column)")
    print(f"   a[0, 1]: {a[0, 1].item()} (element at [0,1])")
    
    print(formatter.output_summary([
        "Element-wise ops: +, -, *, / work on same shape tensors",
        "Matrix multiply (@): [m,n] @ [n,p] = [m,p]",
        "Reductions: sum(), mean(), max() can operate on specific dimensions",
        "Indexing: a[0] = first row, a[:, 0] = first column, a[0,1] = element"
    ]))
except Exception as e:
    print(f"❌ Error: {e}")

# Part 4: GPU vs CPU Tensors
print(formatter.section("Part 4: GPU vs CPU Tensors - Device Management"))

try:
    device = device_detector.detect()
    print(f"\n🖥️  Available Devices:")
    print(f"   CPU: ✅ Always available")
    
    if torch.cuda.is_available():
        print(f"   CUDA: ✅ Available ({torch.cuda.get_device_name(0)})")
    else:
        print(f"   CUDA: ❌ Not available")
    
    if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        print(f"   MPS (Apple Silicon): ✅ Available")
    else:
        print(f"   MPS (Apple Silicon): ❌ Not available")
    
    tensor_cpu = torch.randn(3, 3)
    print(f"\n📦 Tensor on CPU:")
    print(f"   Device: {tensor_cpu.device}")
    
    if device != "cpu":
        tensor_device = tensor_cpu.to(device)
        print(f"   Moved to {device.upper()}: {tensor_device.device}")
    
    print(formatter.output_summary([
        f"Current device: {device}",
        "Tensors default to CPU, can be moved to GPU/MPS",
        "GPU/MPS tensors enable faster computation",
        "Operations between tensors must be on same device"
    ]))
except Exception as e:
    print(f"❌ Error: {e}")

# Part 5: Tensor Broadcasting
print(formatter.section("Part 5: Tensor Broadcasting - Shape Compatibility"))

try:
    a = torch.randn(3, 1, 5)
    b = torch.randn(1, 4, 5)
    
    print(f"\n📡 Broadcasting:")
    print(f"   a shape: {a.shape}")
    print(f"   b shape: {b.shape}")
    
    c = a + b
    print(f"   a + b shape: {c.shape}")
    print(f"   ✅ PyTorch automatically broadcasts compatible dimensions")
    
    print(f"\n💡 Broadcasting Rules:")
    print(f"   1. Dimensions are aligned from the right")
    print(f"   2. Size 1 dimensions are broadcast")
    print(f"   3. Missing dimensions are added as size 1")
    
    print(formatter.output_summary([
        f"Broadcasting: [3,1,5] + [1,4,5] = [3,4,5]",
        "Size 1 dimensions are expanded to match",
        "Enables operations on tensors with compatible but different shapes",
        "Saves memory (no need to explicitly expand)"
    ]))
except Exception as e:
    print(f"❌ Error: {e}")

# Part 6: Real Example - Model Embeddings
print(formatter.section("Part 6: Real Example - Model Embeddings"))

loader = ModelLoader()
try:
    tokenizer, model = loader.load_both(globals())
    if 'tokenizer' in globals() and 'model' in globals():
        processor = TextProcessor(tokenizer)
        extractor = EmbeddingExtractor(model, tokenizer)
        
        text = "Hello world"
        embeddings = extractor.get_embeddings(text)
        
        print(f"\n📊 Model Output Tensor:")
        print(f"   Shape: {embeddings.shape}")
        print(f"   Dtype: {embeddings.dtype}")
        print(f"   Device: {embeddings.device}")
        print(f"   Requires grad: {embeddings.requires_grad}")
        print(f"   Memory: ~{embeddings.numel() * embeddings.element_size() / 1024:.2f} KB")
        
        print(formatter.output_summary([
            f"Model produces embeddings tensor: {embeddings.shape}",
            f"Data type: {embeddings.dtype} (float32 or float16)",
            f"Device: {embeddings.device} (where computation happens)",
            f"Memory: ~{embeddings.numel() * embeddings.element_size() / 1024:.2f} KB",
            "All model inputs/outputs are tensors"
        ]))
except Exception as e:
    print(f"⚠️  Could not demonstrate with model: {e}")

# Summary
takeaways = [
    "Tensors are multi-dimensional arrays (0D to ND)",
    "Shape determines dimensions: [batch, seq, features]",
    "Operations: element-wise, matrix multiply, reductions",
    "Devices: CPU, CUDA (GPU), MPS (Apple Silicon)",
    "Broadcasting enables operations on different shapes"
]
print(formatter.summary("Objective 5 Complete: Tensors", takeaways, "Objective 6 - Parameters (Model Weights & Config)"))

# Save state
if 'model' in locals() and 'tokenizer' in locals():
    state_mgr.save_to_globals(globals(), model=model, tokenizer=tokenizer)
    print("\n💾 Model and tokenizer saved for next objective")
