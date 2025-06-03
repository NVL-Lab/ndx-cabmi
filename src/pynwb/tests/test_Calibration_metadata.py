from ndx_cabmi import Calibration_metadata

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
            help = "test help",
            feedback_flag = True,
            ensemble_indexes = [1, 2, 3, 4],
            decoder = [0.1, 0.2, 0.3, 0.4],
            target = [1, 2],
            feedback_target = [440, 890],
            ensemble_mean = [1, 2, 3, 4], 
            ensemble_sd = [4, 3, 2, 1]
        )

        self.assertEqual(calibration.name, "test_calibration")
        self.assertEqual(calibration.description, 'calibration metadata for my experiment')
        self.assertEqual(calibration.category, 'test category')
        self.assertEqual(calibration.help, "test help")
        self.assertEqual(calibration.feedback_flag, True)
        self.assertEqual(calibration.ensemble_indexes, [1, 2, 3, 4])
        self.assertEqual(calibration.decoder, [0.1, 0.2, 0.3, 0.4])
        self.assertEqual(calibration.target, [1, 2])
        self.assertEqual(calibration.feedback_target, [440, 890])
        self.assertEqual(calibration.ensemble_mean, [1, 2, 3, 4])
        self.assertEqual(calibration.ensemble_sd, [4, 3, 2, 1])


class TestCalibrationMetadataRoundtrip(unittest.TestCase):
    #Roundtrip test for Calibration Metadata
    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())
        self.path = "test_calibration.nwb"
    
    def test_roundtrip(self):
        calibration = Calibration_metadata(
            name = "test_calibration",
            description='calibration metadata for my experiment',
            category = "test category",
            help = "test help",
            feedback_flag = True,
            ensemble_indexes = [1, 2, 3, 4],
            decoder = [0.1, 0.2, 0.3, 0.4],
            target = [1, 2],
            feedback_target = [440, 890],
            ensemble_mean = [1, 2, 3, 4], 
            ensemble_sd = [4, 3, 2, 1]
        )

        self.nwbfile.add_acquisition(nwbdata=calibration)

        # Write to file
        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        
        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            print("\n=== LabMetaData Contents ===")
            for name, meta in read_nwbfile.lab_meta_data.items():
                
                print(f"Calibration Name: {name}")
                print(f"Description: {meta.description}")
                print(f"  Category: {meta.category}")
                print(f"  Help: {meta.help}")
                print(f"  Feedback Flag: {meta.feedback_flag}")
                print(f"  Ensemble Indexes: {meta.ensemble_indexes}\n")
                print(f"  Decoder: {meta.decoder}")
                print(f"  Target: {meta.target}")
                print(f"  Feedback Target: {meta.feedback_target}\n")
                print(f"  Ensamble Mean: {meta.ensemble_mean}")
                print(f"  Ensemble SD: {meta.ensemble_sd}\n")
    

        