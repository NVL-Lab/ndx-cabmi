import numpy as np
import numpy.typing as npt
import ndx_cabmi
from typing import Optional
from pynwb.testing.mock.utils import name_generator

def mock_Calibration_metadata (
      *,
      name: Optional[str] = None,
      description: str = "mock metadata for Calibration",
      category: str = "mock metadata",
      additional_data: str = "mock additional data",
      feedback_flag: bool,
      ensemble_indexes: npt.NDArray[np.int32] = np.arange(10),
      decoder: npt.NDArray[np.float64] = np.arange(10),
      target: npt.NDArray[np.float64] = np.arange(2),
      feedback_target: npt.NDArray[np.float64] = np.arange(2),
      ensemble_mean: npt.NDArray[np.float64] = np.arange(10),
      ensemble_sd: npt.NDArray[np.int32] = np.arange(10)
      ) -> ndx_cabmi.Calibration_metadata: # type: ignore
    calibration_metadata = ndx_cabmi.Calibration_metadata(
        name=name or name_generator("Calibration_metadata"),
        description=description,
        category=category,
        additional_data=additional_data,
        feedback_flag=feedback_flag,
        ensemble_indexes=ensemble_indexes,
        decoder=decoder,
        target=target,
        feedback_target=feedback_target,
        feedback_flag=feedback_flag,
        ensemble_mean=ensemble_mean,
        ensemble_sd=ensemble_sd
    )
    return calibration_metadata

def mock_Parameters_BMI (
        
):
    return

def mock_CaBMISeries (
        
):
    return

def mock_Calibration_metadata (
        
):
    return

def mock_ROI_metadata (
        
):
    return
