from ndx_cabmi import Calibration_metadata

import tempfile
import numpy as np
from datetime import datetime
from pynwb import NWBHDF5IO

from pynwb.testing import TestCase, remove_test_file
from pynwb.testing import TestCase
from pynwb.testing.mock.file import mock_NWBFile
from datetime import datetime
import unittest

class TestCalibrationMetadataConstructor(TestCase):
    #Unit test for constructing Calibration Metadata

    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())

    def test_constructor(self):
        calibration = Calibration_metadata(
            name = "test_calibration",
            description = "calibration metadata for my experiment",
            category = "test category",
            about = "test about",
            feedback_flag = True,
            ensemble_indexes = np.arange(4, dtype=int),
            decoder = np.arange(4, dtype=float),
            target = np.arange(2, dtype=float),
            feedback_target = np.arange(2, dtype=float),
            ensemble_mean = np.arange(4, dtype=float), 
            ensemble_sd = np.arange(4, dtype=float)
        )

        self.assertEqual(calibration.name, "test_calibration")
        self.assertEqual(calibration.description, 'calibration metadata for my experiment')
        self.assertEqual(calibration.category, 'test category')
        self.assertEqual(calibration.about, "test about")
        self.assertEqual(calibration.feedback_flag, True)
        np.testing.assert_array_equal(calibration.ensemble_indexes, np.arange(4, dtype=int))
        np.testing.assert_array_equal(calibration.decoder, np.arange(4, dtype=float),)
        np.testing.assert_array_equal(calibration.target, np.arange(2, dtype=float))
        np.testing.assert_array_equal(calibration.feedback_target, np.arange(2, dtype=float))
        np.testing.assert_array_equal(calibration.ensemble_mean, np.arange(4, dtype=float))
        np.testing.assert_array_equal(calibration.ensemble_sd, np.arange(4, dtype=float))


class TestCalibrationMetadataRoundtrip(unittest.TestCase):
    #Roundtrip test for Calibration Metadata
    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())
    
    def test_roundtrip(self):
        calibration = Calibration_metadata(
            name = "test_calibration",
            description = "calibration metadata for my experiment",
            category = "test category",
            about = "test about",
            feedback_flag = True,
            ensemble_indexes = np.arange(4, dtype=int),
            decoder = np.arange(4, dtype=float),
            target = np.arange(2, dtype=float),
            feedback_target = np.arange(2, dtype=float),
            ensemble_mean = np.arange(4, dtype=float), 
            ensemble_sd = np.arange(4, dtype=float)
        )

        self.nwbfile.add_lab_meta_data(lab_meta_data=calibration)

        # Write to temporary file
        with tempfile.NamedTemporaryFile(suffix='.nwb', delete=True) as tmp:
            with NWBHDF5IO(tmp.name, mode='w') as io:
                io.write(self.nwbfile)

        
            with NWBHDF5IO(tmp.name, mode='r', load_namespaces=True) as io:
                read_nwbfile = io.read()
                print("\n=== LabMetaData Contents ===")
                for name, meta in read_nwbfile.lab_meta_data.items():
                    
                    print(f"Calibration Name: {name}")
                    print(f"Description: {meta.description}")
                    print(f"Category: {meta.category}")
                    print(f"About: {meta.about}")
                    print(f"Feedback Flag: {meta.feedback_flag}")
                    print(f"Ensemble Indexes: {meta.ensemble_indexes}\n")
                    print(f"Decoder: {meta.decoder}")
                    print(f"Target: {meta.target}")
                    print(f"Feedback Target: {meta.feedback_target}\n")
                    print(f"Ensamble Mean: {meta.ensemble_mean}")
                    print(f"Ensemble SD: {meta.ensemble_sd}\n")
    

        