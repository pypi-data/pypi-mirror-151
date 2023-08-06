# fvbitcore

Fork from [this repository](https://github.com/facebookresearch/fvcore) from Facebook. Fvcore offers operation level
FLOP estimation. This repository adapts this tool to take into account quantization when calculating
model flops and size.

This tool can be used together with [bitorch](https://github.com/hpi-xnor/bitorch) to create and evaluate quantized deep learning models.
The documentation may not yet be up-to-date yet.
Read more about the [original project](https://github.com/facebookresearch/fvcore) below.

### about the original fvcore project

fvcore is a light-weight core library that provides the most common and essential
functionality shared in various computer vision frameworks developed in FAIR,
such as [Detectron2](https://github.com/facebookresearch/detectron2/),
[PySlowFast](https://github.com/facebookresearch/SlowFast), and
[ClassyVision](https://github.com/facebookresearch/ClassyVision).
All components in this library are type-annotated, tested, and benchmarked.

The computer vision team in FAIR is responsible for maintaining [fvcore](https://github.com/facebookresearch/fvcore).

## Features:

Besides some basic utilities, fvcore includes the following features:

- Common pytorch layers, functions and losses in [fvcore.nn](fvcore/nn/).
- A hierarchical per-operator flop counting tool: see [this note for details](./docs/flop_count.md).
- Recursive parameter counting: see [API doc](https://detectron2.readthedocs.io/en/latest/modules/fvcore.html#fvcore.nn.parameter_count).
- Recompute BatchNorm population statistics: see its [API doc](https://detectron2.readthedocs.io/en/latest/modules/fvcore.html#fvcore.nn.update_bn_stats).
- A stateless, scale-invariant hyperparameter scheduler: see its [API doc](https://detectron2.readthedocs.io/en/latest/modules/fvcore.html#fvcore.common.param_scheduler.ParamScheduler).

## Install:

fvbitcore requires pytorch and python >= 3.6.

Use one of the following ways to install:

### 1. Install from PyPI (updated nightly)

```
pip install -U fvbitcore
```

### 2. Install from Anaconda Cloud (updated nightly)

(Not yet supported.)

```
conda install -c fvbitcore -c iopath -c conda-forge fvbitcore
```

### 3. Install latest from GitHub

```
pip install -U 'git+https://github.com/hpi-xnor/fvbitcore'
```

### 4. Install from a local clone

```
git clone https://github.com/hpi-xnor/fvbitcore
pip install -e fvbitcore
```

## License

This library is released under the [Apache 2.0 license](LICENSE).
