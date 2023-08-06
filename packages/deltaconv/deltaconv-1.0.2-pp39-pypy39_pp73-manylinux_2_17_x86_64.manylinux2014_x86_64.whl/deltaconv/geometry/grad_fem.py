import torch
import torch.linalg as LA

def build_grad_div(pos, faces):
    grad = build_grad(pos, faces)
    div = grad.T
    return grad, div

def build_grad(pos, face):
    """Builds an intrinsic gradient matrix from point positions and faces (triangles).
    The output gradient matrix is a [2N_F, N_V] sparse matrix that computes
    a tangent vector per face pointint in the direction of the gradient.

    Args:
        pos (Tensor): point positions in a [N, 3] tensor.
        face (Tensor): list of face indices in a [3, N] tensor.
    """

    v0 = pos[face[0]]
    v1 = pos[face[1]]
    v2 = pos[face[2]]

    v01 = v1 - v0
    v12 = v2 - v1
    v20 = v0 - v2

    double_area = LA.norm(LA.cross(v01, v12))
    
    l01 = LA.norm(v01, dim=-1, keepdim=True)
    l12 = LA.norm(v12, dim=-1, keepdim=True)
    l20 = LA.norm(v20, dim=-1, keepdim=True)

    
