import torch 
import torch.nn as nn 

from dataclasses import dataclass
from typing_extensions import dataclass_transform


@dataclass_transform(eq_default=False, kw_only_default=True)
class DataclassModule(nn.Module):
    def __new__(cls, *_, **__):
        obj = super().__new__(cls)
        nn.Module.__init__(obj)
        return obj

    def __init_subclass__(cls) -> None:
        dataclass(eq=False, kw_only=True)(cls)
        return super().__init_subclass__()

    def __str__(self):
        return nn.Module.__repr__(self)

