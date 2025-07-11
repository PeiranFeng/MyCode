import torch
import numpy as np
from einops import rearrange, einsum

D = torch.rand((2,3,4), dtype=torch.float32)
A = torch.randn((4,4), dtype=torch.float32)

print('D:', D)
print('A:', A)
Y = D @ A.T
print('Y:', Y)
Y = einsum(D, A, "batch sequence d_in, d_out d_in -> batch sequence d_out")
print('Y with einsum:', Y)
Y = einsum(D, A, "... d_in, d_out d_in -> ... d_out")
print('Y with einsum and ellipsis:', Y)

images = torch.randn(64, 128, 128, 3) # (batch, height, width, channels)
dim_by = torch.linspace(start=0, end=1.0, steps=10)
print('dim_by:', dim_by)
print('dim_by shape:', dim_by.shape)
dim_value = rearrange(dim_by, "dim_value  -> 1 dim_value 1 1 1")
print('dim_value:', dim_value.shape)
images_rearr = rearrange(images, "batch height width channel -> batch 1 height width channel")
print('images_rearr:', images_rearr.shape)
dimmed_images = images_rearr * dim_value
print('dimmed_images:', dimmed_images.shape)
dimmed_images = einsum(
    dim_by, 
    images, 
    "dim_value, batch height width channel -> batch dim_value height width channel")
print('dimmed_images with rearrange:', dimmed_images.shape)


A = torch.randn(2,3,4,5)
B = torch.randn(2,3,4,5)
C = einsum(A, B, 'b t1 head c, b t2 head c -> b head t1 t2')
print('A:', A)
print('B:', B)
print('C:', C)
