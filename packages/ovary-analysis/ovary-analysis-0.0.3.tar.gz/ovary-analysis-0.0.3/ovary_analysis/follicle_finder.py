import argparse
import os
from typing import Any, Dict, List, Optional, Tuple

try:
    from aydin.restoration.denoise.noise2selffgr import noise2self_fgr

    AYDIN_INSTALLED = True
except ImportError:
    AYDIN_INSTALLED = False
import numpy as np
from pytorch3dunet.predict import run_predictions
from pytorch3dunet.unet3d.config import get_device
import yaml


from .io.hdf5_io import load_im_from_hdf, write_multi_dataset_hdf
from .measure.vol_measure import measure_image
from .post_process.follicles import post_process_follicles
from .post_process.ovary import post_process_ovary
from .utils.image import crop_raw_image, pad_image


def segment_follicles(
    raw_image: np.ndarray,
    ovary_seg_config: Dict[str, Any],
    follicle_seg_config: Dict[str, Any],
    ovary_probability_threshold: float = 0.8,
    ovary_dilation_size: int = 10,
    min_follicle_im_shape: List[int] = [80, 80, 80],
    follicle_probability_thresh: float = 0.6,
    follicle_volume_thresh: int = 30,
    follicle_prediction_index: int = 1,
) -> Tuple[np.ndarray, np.ndarray]:

    # denoise the image
    if AYDIN_INSTALLED is True:
        print("denoising")
        denoised_image = noise2self_fgr(raw_image)
    else:
        denoised_image = raw_image.copy()

    print("ovary prediction")
    # predict the ovary
    ovary_prediction = run_predictions(
        ovary_seg_config, raw_dataset=[denoised_image]
    )[0]["predictions"]

    # apply sigmoid to the predictions
    ovary_prediction = 1 / (1 + np.exp(-ovary_prediction))

    # segment the ovary
    ovary_segmentation = post_process_ovary(
        ovary_prediction=ovary_prediction[1, ...],
        raw_im=denoised_image,
        threshold=ovary_probability_threshold,
        dilation_size=ovary_dilation_size,
        mask_padding=False,
    )

    # extract the ovary
    cropped_raw, reference_shape, offset = crop_raw_image(
        denoised_image,
        ovary_segmentation,
        min_shape=min_follicle_im_shape,
        mask_periphery=False,
    )
    cropped_ovary_seg, _, _ = crop_raw_image(
        ovary_segmentation,
        ovary_segmentation,
        min_shape=min_follicle_im_shape,
        mask_periphery=False,
    )

    print("follicle prediction")
    # run the follicles prediction
    follicle_prediction_im = run_predictions(
        follicle_seg_config, raw_dataset=[cropped_raw]
    )[0]["predictions"]

    # Post process follicles
    follicle_labels = post_process_follicles(
        follicle_prediction=follicle_prediction_im,
        ovary_seg=cropped_ovary_seg,
        prob_threshold=follicle_probability_thresh,
        volume_threshold=follicle_volume_thresh,
        prediction_index=follicle_prediction_index,
    )

    follicle_labels = pad_image(follicle_labels, reference_shape, offset)

    return follicle_labels, ovary_segmentation


module_path = os.path.dirname(os.path.abspath(__file__))
MODELS_PATH = os.path.join(module_path, "predict", "models")
CONFIGS_PATH = os.path.join(module_path, "predict", "configs")


def _load_ovary_config(
    config_path: str, model_path: Optional[str] = None
) -> Dict[str, Any]:
    """Load pytorch3dunet ovary prediction configuration yaml file.

    Parameters
    ----------
    user_dir : Path
        Path to the user follicle tracker directory in their home directory.
    config_name : str
        Name of the config YAML file to load. (Loaded from the configs dir)
    Returns
    -------
    config: dict
        Configuration Dictionary.
    """
    if config_path == "":
        config_path = os.path.join(CONFIGS_PATH, "ovary_3dunet_config.yaml")
    config = yaml.safe_load(open(config_path))

    config["device"] = get_device(config.get("device", None))

    if model_path is None or model_path == "":
        model_path = os.path.join(MODELS_PATH, "ovary_3dunet.pytorch")
    config["model_path"] = model_path

    return config


def _load_follicles_config(
    config_path: str, model_path: Optional[str] = None
) -> Dict[str, Any]:
    """Load pytorch3dunet follicles prediction configuration yaml file.

    Parameters
    ----------
    user_dir : Path
        Path to the user follicle tracker directory in their home directory.
    config_name : str
        Name of the config YAML file to load. (Loaded from the configs dir)
    Returns
    -------
    config: dict
        Configuration Dictionary.
    """
    if config_path == "":
        config_path = os.path.join(CONFIGS_PATH, "follicle_3dunet_config.yaml")
    config = yaml.safe_load(open(config_path))

    config["device"] = get_device(config.get("device", None))

    if model_path is None or model_path == "":
        model_path = os.path.join(MODELS_PATH, "follicle_3dunet.pytorch")
    config["model_path"] = model_path

    return config


def _parse_arguments():
    parser = argparse.ArgumentParser(
        description="", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-i", "--image", dest="image_path", help="raw image path"
    )
    parser.add_argument(
        "--image-key",
        dest="image_key",
        type=str,
        default="raw_rescaled",
        help="raw image key",
    )
    parser.add_argument(
        "--ovary-seg-config",
        dest="ovary_seg_config",
        type=str,
        default="",
        help="path to the ovary segmentation configuration file",
    )
    parser.add_argument(
        "--follicle-seg-config",
        dest="follicle_seg_config",
        type=str,
        default="",
        help="path to the follicle segmentation configuration file",
    )
    parser.add_argument(
        "--ovary-model",
        dest="ovary_model",
        type=str,
        default="",
        help="path to the ovary model.  if not provided, built-in model is used.",
    )
    parser.add_argument(
        "--follicle-model",
        dest="follicle_model",
        type=str,
        default="",
        help="path to the follicle model. if not provided, built-in model is used.",
    )
    parser.add_argument(
        "--ovary-probability-threshold",
        dest="ovary_probability_threshold",
        type=float,
        default=0.8,
        help="probabilty threshold for binarizing ovary prediction",
    )
    parser.add_argument(
        "--ovary-dilation-size",
        dest="ovary_dilation_size",
        type=int,
        default=10,
        help="size of the dilation to perform on the ovary segmentation",
    )
    parser.add_argument(
        "--follicle-probability-threshold",
        dest="follicle_probability_threshold",
        type=float,
        default=0.5,
        help="probabilty threshold for binarizing follicle prediction",
    )
    parser.add_argument(
        "--follicle-volume-threshold",
        dest="follicle_volume_threshold",
        type=int,
        default=30,
        help="minimum volume (# voxels) for a follicle to be included ",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_directory",
        help="output directory path",
        default="",
    )
    args = parser.parse_args()
    return args


def cli():
    # parse arguments
    args = _parse_arguments()

    # load the image
    raw_image = load_im_from_hdf(args.image_path, args.image_key)

    # load the configs
    ovary_config = _load_ovary_config(args.ovary_seg_config, args.ovary_model)
    follicle_config = _load_follicles_config(
        args.follicle_seg_config, args.follicle_model
    )

    # perform the segmentation
    follicle_labels, ovary_segmentation = segment_follicles(
        raw_image=raw_image,
        ovary_seg_config=ovary_config,
        follicle_seg_config=follicle_config,
        ovary_probability_threshold=args.ovary_probability_threshold,
        ovary_dilation_size=args.ovary_dilation_size,
        min_follicle_im_shape=[80, 80, 80],
        follicle_probability_thresh=args.follicle_probability_threshold,
        follicle_volume_thresh=args.follicle_volume_threshold,
        follicle_prediction_index=1,
    )

    # make measurements
    measurements_df = measure_image(follicle_labels.astype(int))

    # save the image
    if args.output_directory == "":
        output_directory = os.getcwd()
    else:
        output_directory = args.output_directory

    output_path = os.path.join(output_directory, "segmentation.h5")
    write_multi_dataset_hdf(
        file_path=output_path,
        compression="gzip",
        follicles=follicle_labels,
        ovary=ovary_segmentation,
    )

    # save the measurements
    measurements_path = os.path.join(output_directory, "measurements.csv")
    measurements_df.to_csv(measurements_path)
