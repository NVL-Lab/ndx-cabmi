from datetime import datetime
import numpy as np
import numpy.typing as npt
import ndx_cabmi
from typing import Optional


from pytz import UTC
import pytest

import pynwb
from pynwb.testing import TestCase as pynwb_TestCase
from pynwb.testing.mock.file import mock_NWBFile
from pynwb.testing.mock.utils import name_generator



def mock_Calibration_metadata (
      *,
      name: Optional[str] = None,
      description: str = "mock metadata for Calibration",
      category: str = "mock metadata",
      #help: str = "mock help",
      feedback_flag: bool = True,
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
        #help=help,
        feedback_flag=feedback_flag,
        ensemble_indexes=ensemble_indexes,
        decoder=decoder,
        target=target,
        feedback_target=feedback_target,
        ensemble_mean=ensemble_mean,
        ensemble_sd=ensemble_sd
    )
    return calibration_metadata

class TestCalibrationMetadata(pynwb_TestCase):
    """Simple roundtrip test for PlanarMicroscopySeries."""

    def setUp(self):
        self.nwbfile_path = "test_planar_microscopy_series_roundtrip.nwb"

    def tearDown(self):
        pynwb.testing.remove_test_file(self.nwbfile_path)

    def test_roundtrip(self):
        nwbfile = mock_NWBFile(session_start_time=datetime(2000, 1, 1, tzinfo=UTC))
        calibration = mock_Calibration_metadata(name="Calibration")
        nwbfile.add_acquisition(nwbdata=calibration)
    
        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="w") as io:
            io.write(nwbfile)
        
        with pynwb.NWBHDF5IO(path=self.nwbfile_path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()

            self.assertContainerEqual(calibration, read_nwbfile.acquisition["Calibration"])