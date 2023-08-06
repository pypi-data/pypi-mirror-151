"""
init for nn
"""
from .parameter import Parameter
from .batch_norm import BatchNorm1d, BatchNorm2d
from .activation import Sigmoid, ReLu, LeakyReLu, Softmax, Softplus, Softsign, HardSigmoid, ELU, Tanh
from .pooling import MaxPool1D, MaxPool2D, AvgPool1D, AvgPool2D
from .linear import Linear
from .conv import Conv2D, Conv1D, ConvT2D
from .module import Module
from .loss import CategoricalCrossEntropy, BinaryCrossEntropy, SoftmaxCrossEntropy, MeanSquaredError
from .embedding import Embedding
from .layer_norm import LayerNorm1d, LayerNorm2d
from .dropout import Dropout
from .spectral_norm import Spectral_Norm
from .self_attention import Self_Conv_Attention
