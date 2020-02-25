# AUTOGENERATED! DO NOT EDIT! File to edit: 01_ResnetTrick_model.ipynb (unless otherwise specified).

__all__ = ['NewResBlock', 'Model']

# Cell
from kornia.contrib import MaxBlurPool2d

# Cell
from fastai.basic_train import *
from fastai.vision import *
from fastai.script import *
from model_constructor.net import *
from model_constructor.layers import SimpleSelfAttention, ConvLayer

# Cell
import math
import torch
from torch.optim.optimizer import Optimizer, required
import itertools as it

# Cell
from .train_utils import *

# Cell
class NewResBlock(Module):
    def __init__(self, expansion, ni, nh, stride=1,
                 conv_layer=ConvLayer, act_fn=act_fn,
                 pool=nn.AvgPool2d(2, ceil_mode=True), sa=False,sym=False, zero_bn=True):
        nf,ni = nh*expansion,ni*expansion
        self.reduce = noop if stride==1 else pool
        layers  = [(f"conv_0", conv_layer(ni, nh, 3, stride=stride, act_fn=act_fn)),
                   (f"conv_1", conv_layer(nh, nf, 3, zero_bn=zero_bn, act=False))
        ] if expansion == 1 else [
                   (f"conv_0",conv_layer(ni, nh, 1, act_fn=act_fn)),
                   (f"conv_1",conv_layer(nh, nh, 3, stride=1, act_fn=act_fn)), #!!!
                   (f"conv_2",conv_layer(nh, nf, 1, zero_bn=zero_bn, act=False))
        ]
        if sa: layers.append(('sa', SimpleSelfAttention(nf,ks=1,sym=sym)))
        self.convs = nn.Sequential(OrderedDict(layers))
        self.idconv = noop if ni==nf else conv_layer(ni, nf, 1, act=False)
        self.merge =act_fn

    def forward(self, x):
        o = self.reduce(x)
        return self.merge(self.convs(o) + self.idconv(o))

# Cell
class Model(Net):
    def __init__(self):
        super().__init__()
        self.name = 'xresnet50_trick'
        self.c_out = 10
        self.expansion=4
        self.layers=[3, 4,  6, 3]
        self.stem_sizes = [3,32,64,64]
        self.act_fn= Mish()
        self.sa = True
        self.pool = MaxBlurPool2d(3, True)
        self.stem_pool = self.pool
        self.block = NewResBlock