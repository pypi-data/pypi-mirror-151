# ovary-analysis

`ovary-analysis` is a python package for analysis of ovarian follicles from ultrasound images. `ovary-analysis` contains 
the `follicle-finder` pipeline for the automated segmentation and measurement of ovarian follicles.

## Graphical User Interface
If you would like a graphical user interface for the `follicle-finder` segmentation pipeline, please see our 
[`follicle-tracker` napari plugin.](https://github.com/leopold-franz/follicle-tracker).

## Usage
### Segmentation and measurement
You can perform automated segmentation and measurement via the FollicleFinder command line interface. To see options 
of FollicleFinder you can type `follicle-finder --help` in your terminal (you must first activate your 
`follicle-finder environment).

```bash
$ follicle-finder --help
usage: follicle-finder [-h] [-i IMAGE_PATH] [--image-key IMAGE_KEY] [--ovary-seg-config OVARY_SEG_CONFIG]
                       [--follicle-seg-config FOLLICLE_SEG_CONFIG] [--ovary-model OVARY_MODEL]
                       [--follicle-model FOLLICLE_MODEL]
                       [--ovary-probability-threshold OVARY_PROBABILITY_THRESHOLD]
                       [--ovary-dilation-size OVARY_DILATION_SIZE]
                       [--follicle-probability-threshold FOLLICLE_PROBABILITY_THRESHOLD]
                       [--follicle-volume-threshold FOLLICLE_VOLUME_THRESHOLD] [-o OUTPUT_DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE_PATH, --image IMAGE_PATH
                        raw image path (default: None)
  --image-key IMAGE_KEY
                        raw image key (default: raw_rescaled)
  --ovary-seg-config OVARY_SEG_CONFIG
                        path to the ovary segmentation configuration file (default: )
  --follicle-seg-config FOLLICLE_SEG_CONFIG
                        path to the follicle segmentation configuration file (default: )
  --ovary-model OVARY_MODEL
                        path to the ovary model. if not provided, built-in model is used. (default: )
  --follicle-model FOLLICLE_MODEL
                        path to the follicle model. if not provided, built-in model is used. (default: )
  --ovary-probability-threshold OVARY_PROBABILITY_THRESHOLD
                        probabilty threshold for binarizing ovary prediction (default: 0.8)
  --ovary-dilation-size OVARY_DILATION_SIZE
                        size of the dilation to perform on the ovary segmentation (default: 10)
  --follicle-probability-threshold FOLLICLE_PROBABILITY_THRESHOLD
                        probabilty threshold for binarizing follicle prediction (default: 0.5)
  --follicle-volume-threshold FOLLICLE_VOLUME_THRESHOLD
                        minimum volume (# voxels) for a follicle to be included (default: 30)
  -o OUTPUT_DIRECTORY, --output OUTPUT_DIRECTORY
                        output directory path (default: )
```
To perform segmentation with the default options you can enter the following into your terminal

```bash
$ follicle-finder --image /path/to/image --output /path/to/output/directory
```
where `/path/to/image` is the path to your image to be segmented and `/path/to/output/directory` is the path to the 
directory in which the results will be saved. Following the completion of the pipeline, you find two files in your 
output directory:
- `segmentation.h5`: the segmentated image with the follicles in the `follicles` key and the ovary in the `ovary` key.
- `measurements.csv`: the table of measurements for each detected follicle.

If you would like to perform segmentation with your own model (see instructions for training below), you can use the 
following command:

```bash
$ follicle-finder --image /path/to/image --ovary-model /path/to/ovary/model --follicle-model /path/to/follicle/model 
--output /path/to/output/directory
```
where `/path/to/ovary/model` and `path/to/follicle/model` are the paths to the ovary and follicle models, respectively.

### Training a model 
We have included example scripts for training and performing cross validation in the `examples` directory. Due to 
the compute time of training and cross validation, we have designed these scripts for usage with a scientific 
compute cluster with an LSF job queue. Please file an issue if you would like help running on a different computing 
setup.

- ovary model: `examples/make_ovary_cross_validation.py`
- follicle model: `examples/make_follicle_cross_validation.py`

## Installation
### Pre-requisites
- computer with an nvidia GPU. We have tested on a P1000, P4000, and RTX2080Ti.
- CUDA > 11.3 installed on the computer
- anaconda or miniconda python

### Installation with conda
You can install `follicle-finder` via our conda environment file. To do so, first install anaconda or miniconda on 
your computer. Then, download the [`environment_denoise.yml file`](https://git.bsse.ethz.ch/iber/ovary-analysis/-/raw/master/environment_denoise.yml?inline=false) (right click the link and "Save as..."). In 
your terminal, 
navigate to the directory you downloaded the `environment_denoise.yml` file to:

```bash
cd <path/to/downloaded/environment_denoise.yml>
```

Then create the `follicle-finder` environment and 

```bash
conda env create -f environment.yml
```

Once the environment has been created, you can activate it and use `follicle-finder` as described below.

```bash
conda activate follicle-finder
```

## Development installation

You can set up your development environment with our conda dev environment file. To do so, first install 
anaconda or miniconda on your computer. Then, download the [`environment_dev.yml file`](https://git.bsse.ethz.ch/iber/ovary-analysis/-/raw/master/environment_dev.yml?inline=false) (right click the link and "Save as..."). In your 
terminal, navigate to the directory you downloaded the `environment_dev.yml` file to:

```bash
cd <path/to/downloaded/environment_dev.yml>
```

Then create the `follicle-tracker` environment and 

```bash
conda env create -f environment_dev.yml
```

Once the environment has been created, you can activate it and install `follicle-finder` as described below.

```bash
conda activate follice_tracker
```

Navigate to the directory you would like to download the `ovary-analysis` repository to and then clone the 
follicle-tracker repository.

```bash
cd /path/to/repo/parent/directory
git clone git@git.bsse.ethz.ch:iber/ovary-analysis.git
```

Navigate into the `ovary-analysis` directory and install in editable mode with all dependencies.

```bash
cd ovary-analysis
pip install -e .
```

We use pre-commit to ensure code style is uniform across the repository. To set up pre-commit, run the following in 
your terminal.

```bash
pre-commit install
```
