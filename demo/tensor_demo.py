"""

    结论：
    - transpose后 storage没变 改变了stride和shape
        - 具体的方式为获取dim0 dim1两个参数 将stride和shape两个维度对应位置的值对调
            如例子中base.shape (2,2,3); base.stride (6,3,1)
            当transpose(1,2)时 分别交换shape和stride索引1和索引2位置的元素
            即 base.transpose(1,2).shape (2,3,2); base.transpose(1,2).stride (6,1,3)
        - 由于交换了stride 逻辑顺序和物理顺序不一致 discontiguous
    - permute 可以实现和transpose一样的效果
        - discontiguous
    - expand 可以将指定的dimension(require dim equals 1)扩展为指定的值 行为是复制该维度上的值
        - 如对[1,2,3]进行unsqueeze(-1) 并 expand -1维度至3:
            unsqueeze(-1): [1, 2, 3] => [[1], [2], [3]]; <shape, (3)> => <shape, (3,1)>
            expand(-1, 3): [[1], [2], [3]] => [[1,1,1],[2,2,2],[3,3,3]]; <shape, (3,1)> => <shape, (3,3)>
            组合使用两个method的本质是将从某维度起的后续维度复制n次
        - create view of tensor
        - 复制某维度时没有开辟新的内存 逻辑地址与物理地址出现差异 discontiguous
        - expand_as(other: Tensor) is equivalent to expand(other.size()) 
    - as_stride create a view of the tensor with special size, stride and storage offset.
    - stride stride是长度等于维度的tuple 每个维度上的数字决定了在该维度上获取下一个元素时,需要在物理上跳过的索引间隔,即某个维度上两元素之间的'物理距离'
    - slice
"""

import torch

base = torch.tensor([
    [[1,2,3], [4,5,6]],
    [[7,8,9], [10,11,12]]
])

# print(torch.Size(tuple(base.size()).__add__((9,))))
# print(base.expand(torch.Size((10,))+base.size()).size())
# print(base.unsqueeze(0))
# print(base.mean(dim=2, dtype=float))
print(base.dtype)
base = base.to(dtype=float)

print(torch.Size([1,2,3])+torch.Size([4,5]))

assert base.shape == torch.Size([2, 2, 3])
assert base.stride() == (6, 3, 1)
assert base.transpose(1,2).stride() == base.permute(0,2,1).stride()
assert base.transpose(1,2).size() == base.permute(0,2,1).size()
U = torch.randn((8,3), dtype=torch.float64)
D = torch.randn((8,), dtype=torch.float64)
D = D * D
diag = (torch.linalg.vecdot(U,U,dim=-1)+D).unsqueeze(dim=-1)
for idx, tensor in enumerate([
    # base.view(1,12),                           
    # base.reshape([1,12]),                                   
    # base[:],                                        
    # base.transpose(0,1),                            
    # base.transpose(0,2),                        
    # base.transpose(1,2),
    # base.permute(0,1,2),
    # base.permute(0,2,1),
    # base.permute(1,0,2),
    # base.permute(1,2,0),
    # base.squeeze(),
    # base.unsqueeze(0),
    # base.unsqueeze(-1),
    # base.unsqueeze(-1).expand(-1, -1, -1, 3),
    # base.unsqueeze(-2).expand(-1, -1, 3, -1),
    # base.select(0, 1),
    # base.mean(dim=1, dtype=float)
    # base.mean(dim=1,dtype=float).unsqueeze(1)
    # torch.matmul(base.unsqueeze(-1),base.unsqueeze(-2)).sum(-1),
    # torch.linalg.vecdot(base, base, dim=-1).unsqueeze(-1),
    # torch.randn((8,3), dtype=torch.float64),
    # base * torch.tensor([2,2,2])**2,
    # torch.linalg.vecdot(base, torch.ones((2,2,3),dtype=float), dim=-1),
    # torch.tensor([[1.0,2.0],[3.0,4.0]])
]):
    print('\n[',idx,']', tensor, '\n')
    # assert base.untyped_storage().data_ptr() == tensor.untyped_storage().data_ptr()
    if not tensor.is_contiguous():
        print('\t', tensor, 'is discontiguous\n')
        assert tensor.contiguous().untyped_storage().data_ptr() != base.untyped_storage().data_ptr()
        assert tensor.contiguous().is_contiguous()
    print('\tstride', tensor.stride(), 'is' if tensor.stride()==base.stride() else 'not', 'equals base')
    print('\tshape', tensor.shape, 'is' if tensor.shape==base.shape else 'not', 'equals base')