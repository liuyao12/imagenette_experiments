# AUTOGENERATED! DO NOT EDIT! File to edit: 01_ResnetTrick_model.ipynb (unless otherwise specified).

__all__ = ['Model']

# Cell
from kornia.contrib import MaxBlurPool2d

# Cell
# hide
from nbdev.showdoc import *

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