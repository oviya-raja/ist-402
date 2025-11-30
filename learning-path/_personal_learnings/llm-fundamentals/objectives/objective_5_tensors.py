# ============================================================================
# Objective 5: Tensors - Working with Tensors
# ============================================================================
# Understanding PyTorch tensors and tensor operations

import torch
import numpy as np

print("=" * 80)
print("OBJECTIVE 5: TENSORS")
print("=" * 80)
print("\n🧠 Learning Goal: Understand tensors and tensor operations")
print("   Tensors are multi-dimensional arrays used in deep learning.\n")

# ============================================================================
# Part 1: Creating and Manipulating Tensors
# ============================================================================
print("\n" + "-" * 80)
print("Part 1: Creating and Manipulating Tensors")
print("-" * 80)

try:
    # Create different types of tensors
    print("\n📦 Creating Tensors:")
    
    # Scalar (0D)
    scalar = torch.tensor(5.0)
    print(f"   Scalar: {scalar}, shape: {scalar.shape}, dims: {scalar.dim()}")
    
    # Vector (1D)
    vector = torch.tensor([1.0, 2.0, 3.0])
    print(f"   Vector: {vector}, shape: {vector.shape}, dims: {vector.dim()}")
    
    # Matrix (2D)
    matrix = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    print(f"   Matrix: shape {matrix.shape}, dims: {matrix.dim()}")
    
    # 3D Tensor
    tensor_3d = torch.randn(2, 3, 4)  # [batch, height, width]
    print(f"   3D Tensor: shape {tensor_3d.shape}, dims: {tensor_3d.dim()}")
    
    # Common tensor creation methods
    print(f"\n🔧 Common Creation Methods:")
    zeros = torch.zeros(3, 4)
    ones = torch.ones(2, 3)
    rand = torch.rand(2, 3)  # Uniform [0, 1)
    randn = torch.randn(2, 3)  # Normal distribution
    
    print(f"   zeros(3,4): shape {zeros.shape}")
    print(f"   ones(2,3): shape {ones.shape}")
    print(f"   rand(2,3): shape {rand.shape}, range [0,1)")
    print(f"   randn(2,3): shape {randn.shape}, mean≈0, std≈1")
    
except Exception as e:
    print(f"❌ Error: {e}")

# ============================================================================
# Part 2: Tensor Shapes and Dimensions
# ============================================================================
print("\n" + "-" * 80)
print("Part 2: Tensor Shapes and Dimensions")
print("-" * 80)

try:
    # Example: Embedding tensor (like from a model)
    batch_size = 2
    seq_len = 5
    hidden_dim = 768
    
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
    
    # Reshaping
    print(f"\n🔄 Reshaping:")
    flattened = embedding_tensor.view(-1, hidden_dim)
    print(f"   Original: {embedding_tensor.shape}")
    print(f"   Flattened: {flattened.shape} (batch*seq, hidden)")
    
except Exception as e:
    print(f"❌ Error: {e}")

# ============================================================================
# Part 3: Common Tensor Operations
# ============================================================================
print("\n" + "-" * 80)
print("Part 3: Common Tensor Operations")
print("-" * 80)

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
    
except Exception as e:
    print(f"❌ Error: {e}")

# ============================================================================
# Part 4: GPU vs CPU Tensors
# ============================================================================
print("\n" + "-" * 80)
print("Part 4: GPU vs CPU Tensors")
print("-" * 80)

try:
    # Check device availability
    device_cpu = torch.device("cpu")
    device_cuda = torch.device("cuda") if torch.cuda.is_available() else None
    device_mps = torch.device("mps") if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available() else None
    
    print(f"\n🖥️  Available Devices:")
    print(f"   CPU: ✅ Always available")
    if device_cuda:
        print(f"   CUDA: ✅ Available ({torch.cuda.get_device_name(0)})")
    else:
        print(f"   CUDA: ❌ Not available")
    if device_mps:
        print(f"   MPS (Apple Silicon): ✅ Available")
    else:
        print(f"   MPS (Apple Silicon): ❌ Not available")
    
    # Create tensor on CPU
    tensor_cpu = torch.randn(3, 3)
    print(f"\n📦 Tensor on CPU:")
    print(f"   Device: {tensor_cpu.device}")
    
    # Move to GPU if available
    if device_cuda:
        tensor_gpu = tensor_cpu.to(device_cuda)
        print(f"   Moved to CUDA: {tensor_gpu.device}")
    elif device_mps:
        tensor_mps = tensor_cpu.to(device_mps)
        print(f"   Moved to MPS: {tensor_mps.device}")
    else:
        print(f"   GPU not available, staying on CPU")
    
except Exception as e:
    print(f"❌ Error: {e}")

# ============================================================================
# Part 5: Tensor Broadcasting
# ============================================================================
print("\n" + "-" * 80)
print("Part 5: Tensor Broadcasting")
print("-" * 80)

try:
    # Broadcasting example
    a = torch.randn(3, 1, 5)  # Shape: [3, 1, 5]
    b = torch.randn(1, 4, 5)  # Shape: [1, 4, 5]
    
    print(f"\n📡 Broadcasting:")
    print(f"   a shape: {a.shape}")
    print(f"   b shape: {b.shape}")
    
    c = a + b  # Broadcasts to [3, 4, 5]
    print(f"   a + b shape: {c.shape}")
    print(f"   ✅ PyTorch automatically broadcasts compatible dimensions")
    
    print(f"\n💡 Broadcasting Rules:")
    print(f"   1. Dimensions are aligned from the right")
    print(f"   2. Size 1 dimensions are broadcast")
    print(f"   3. Missing dimensions are added as size 1")
    
except Exception as e:
    print(f"❌ Error: {e}")

# ============================================================================
# Part 6: Real Example - Model Embeddings
# ============================================================================
print("\n" + "-" * 80)
print("Part 6: Real Example - Model Embeddings")
print("-" * 80)

if 'model' in globals() and 'tokenizer' in globals():
    try:
        text = "Hello world"
        token_ids = tokenizer.encode(text, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model(token_ids)
            embeddings = outputs.last_hidden_state
        
        print(f"\n📊 Model Output Tensor:")
        print(f"   Shape: {embeddings.shape}")
        print(f"   Dtype: {embeddings.dtype}")
        print(f"   Device: {embeddings.device}")
        print(f"   Requires grad: {embeddings.requires_grad}")
        print(f"   Memory: ~{embeddings.numel() * embeddings.element_size() / 1024:.2f} KB")
        
    except Exception as e:
        print(f"⚠️  Could not demonstrate with model: {e}")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("✅ Objective 5 Complete: Tensors")
print("=" * 80)
print("\n📚 Key Takeaways:")
print("  1. Tensors are multi-dimensional arrays (0D to ND)")
print("  2. Shape determines dimensions: [batch, seq, features]")
print("  3. Operations: element-wise, matrix multiply, reductions")
print("  4. Devices: CPU, CUDA (GPU), MPS (Apple Silicon)")
print("  5. Broadcasting enables operations on different shapes")
print("\n➡️  Next: Objective 6 - Parameters (Model Weights & Config)")

# Store for next objective
if 'model' in globals():
    globals()['model'] = model
if 'tokenizer' in globals():
    globals()['tokenizer'] = tokenizer
print("\n💾 Model and tokenizer saved for next objective")
