# -*- coding: utf-8 -*-


import jax.lax
import brainpy.math as bm
from brainpy.initialize import XavierNormal, ZeroInit, init_param
from brainpy.nn.base import Node

__all__ = [
  'GeneralConv',
  'Conv1D',
  'Conv2D',
  'Conv3D'
]


def _check_tuple(v):
  if isinstance(v, (tuple, list)):
    return tuple(v)
  elif isinstance(v, int):
    return (v, v)
  else:
    raise ValueError


def _conv_dimension_numbers(input_shape):
  """Computes the dimension numbers based on the input shape."""
  ndim = len(input_shape)
  lhs_spec = (0, ndim - 1) + tuple(range(1, ndim - 1))
  rhs_spec = (ndim - 1, ndim - 2) + tuple(range(0, ndim - 2))
  out_spec = lhs_spec
  return jax.lax.ConvDimensionNumbers(lhs_spec, rhs_spec, out_spec)


class GeneralConv(Node):
  """Applies a convolution to the inputs.

  Args:
    out_channels: integer
      number of output channels.
    kernel_size: sequence[int]
      shape of the convolutional kernel. For 1D convolution,
      the kernel size can be passed as an integer. For all other cases, it must
      be a sequence of integers.
    strides: sequence[int]
      an integer or a sequence of `n` integers, representing the inter-window strides (default: 1).
    padding: str, sequence[int]
      either the string `'SAME'`, the string `'VALID'`, the string
      `'CIRCULAR'` (periodic boundary conditions), or a sequence of `n` `(low,
      high)` integer pairs that give the padding to apply before and after each
      spatial dimension. A single int is interpeted as applying the same padding
      in all dims and passign a single int in a sequence causes the same padding
      to be used on both sides.
    input_dilation: integer, sequence[int]
      an integer or a sequence of `n` integers, giving the
      dilation factor to apply in each spatial dimension of `inputs`
      (default: 1). Convolution with input dilation `d` is equivalent to
      transposed convolution with stride `d`.
    kernel_dilation: integer, sequence[int]
      an integer or a sequence of `n` integers, giving the
      dilation factor to apply in each spatial dimension of the convolution
      kernel (default: 1). Convolution with kernel dilation
      is also known as 'atrous convolution'.
    groups: integer, default 1.
      If specified divides the input
      features into groups.
    kernel_init: brainpy.init.Initializer
      initializer for the convolutional kernel.
    bias_init: brainpy.init.Initializer
      initializer for the bias.
  """

  def __init__(self, out_channels, kernel_size, strides=None, padding='SAME',
               input_dilation=None, kernel_dilation=None, groups=1, w_init=XavierNormal(), b_init=ZeroInit(), **kwargs):
    super(GeneralConv, self).__init__(**kwargs)

    self.out_channels = out_channels
    self.kernel_size = kernel_size
    self.strides = strides
    self.padding = padding
    self.input_dilation = input_dilation
    self.kernel_dilation = kernel_dilation
    self.groups = groups
    self.w_init = w_init
    self.b_init = b_init
    self.dimension_numbers = None
    self.trainable = True

    if isinstance(padding, str):
      assert padding in ['SAME', 'VALID']
    elif isinstance(padding, tuple):
      for k in padding:
        assert isinstance(k, int)
    else:
      raise ValueError

    assert out_channels % self.groups == 0, '"nout" should be divisible by groups'

  def _check_input_dim(self):
    pass

  def init_ff_conn(self):
    input_shapes = self.feedforward_shapes
    in_channels = int(input_shapes[-1])
    assert in_channels % self.groups == 0, '"nin" should be divisible by groups'
    kernel_shape = _check_tuple(self.kernel_size) + (in_channels // self.groups, self.out_channels)
    self.w = init_param(self.w_init, kernel_shape)
    self.b = init_param(self.b_init, (1,) * len(self.kernel_size) + (self.out_channels,))
    if self.trainable:
      self.w = bm.TrainVar(self.w)
      self.b = bm.TrainVar(self.b)

    if self.strides is None:
      self.strides = (1,) * (len(input_shapes) - 2)

    output_shapes = jax.lax.conv_transpose_shape_tuple(
      input_shapes, kernel_shape, self.strides, self.padding, dimension_numbers=self.dimension_numbers)
    self.set_output_shape(output_shapes)

  def init_fb_conn(self):
    fb_input_shapes = self.feedback_shapes
    ff_input_shapes = self.feedforward_shapes
    ff_spatial_axes = ff_input_shapes[1:-1]  # only first (batch) and last (channel) dimension are not spatial dims
    fb_spatial_axes = fb_input_shapes[1:-1]
    assert ff_spatial_axes == fb_spatial_axes, f"Feedback input spatial dimensions {fb_spatial_axes} are not aligned " \
                                               f"with feedforward input spatial dimensions {ff_spatial_axes}. "

    in_channels = int(ff_input_shapes[-1] + fb_input_shapes[-1])
    assert in_channels % self.groups == 0, '"nin" should be divisible by groups'
    kernel_shape = _check_tuple(self.kernel_size) + (in_channels // self.groups, self.out_channels)
    self.w = init_param(self.w_init, kernel_shape)
    self.b = init_param(self.b_init, (1,) * len(self.kernel_size) + (self.out_channels,))
    if self.trainable:
      self.w = bm.TrainVar(self.w)
      self.b = bm.TrainVar(self.b)

    if self.strides is None:
      self.strides = (1,) * (len(ff_input_shapes) - 2)

  def forward(self, ff, fb=None, **shared_kwargs):
    if fb is not None:
      data = bm.concatenate((ff, fb), axis=-1)
    else:
      data = ff
    y = jax.lax.conv_general_dilated(lhs=data.value if isinstance(data, bm.JaxArray) else ff,
                                     rhs=self.w.value,
                                     window_strides=self.strides,
                                     padding=self.padding,
                                     lhs_dilation=self.input_dilation,
                                     rhs_dilation=self.kernel_dilation,
                                     feature_group_count=self.groups,
                                     dimension_numbers=self.dimension_numbers)
    if self.b is None:
      return y
    return y + self.b.value


class Conv1D(GeneralConv):
  def __init__(self, out_channels, kernel_size, **kwargs):
    super(Conv1D, self).__init__(out_channels, kernel_size, **kwargs)

    self.dimension_numbers = ('NWC', 'WIO', 'NWC')

  def _check_input_dim(self):
    ndim = len(self.feedforward_shapes)
    if ndim != 3:
      raise ValueError(
        "expected 3D input (got {}D input)".format(ndim)
      )

    assert len(self.kernel_size) == 1, "expected 1D kernel size (got {}D input)".format(self.kernel_size)


class Conv2D(GeneralConv):
  def __init__(self, out_channels, kernel_size, **kwargs):
    super(Conv2D, self).__init__(out_channels, kernel_size, **kwargs)

    self.dimension_numbers = ('NHWC', 'HWIO', 'NHWC')

  def _check_input_dim(self):
    ndim = len(self.feedforward_shapes)
    if ndim != 4:
      raise ValueError(
        "expected 4D input (got {}D input)".format(ndim)
      )

    assert len(self.kernel_size) == 2, "expected 2D kernel size (got {}D input)".format(self.kernel_size)


class Conv3D(GeneralConv):
  def __init__(self, out_channels, kernel_size, **kwargs):
    super(Conv3D, self).__init__(out_channels, kernel_size, **kwargs)

    self.dimension_numbers = ('NHWDC', 'HWDIO', 'NHWDC')

  def _check_input_dim(self):
    ndim = len(self.feedforward_shapes)
    if ndim != 5:
      raise ValueError(
        "expected 5D input (got {}D input)".format(ndim)
      )

    assert len(self.kernel_size) == 3, "expected 3D kernel size (got {}D input)".format(self.kernel_size)
