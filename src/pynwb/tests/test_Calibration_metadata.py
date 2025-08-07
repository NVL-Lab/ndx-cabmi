from ndx_cabmi import Calibration_metadata

import numpy as np
from datetime import datetime
from pynwb import NWBHDF5IO

from pynwb.testing import TestCase, remove_test_file
from pynwb.testing.mock.file import mock_NWBFile


class TestCalibrationMetadataConstructor(TestCase):
    # Unit test for constructing Calibration Metadata

    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())

    def test_constructor(self):
        calibration = Calibration_metadata(
            name='test_calibration',
            description='calibration metadata for my experiment',
            category='test category',
            about='test about',
            feedback_flag=True,
            ensemble_indexes=np.arange(4, dtype=int),
            decoder=np.arange(4, dtype=float),
            target=np.arange(2, dtype=float),
            feedback_target=np.arange(2, dtype=float),
            ensemble_mean=np.arange(4, dtype=float),
            ensemble_sd=np.arange(4, dtype=float)
        )

        self.assertEqual(calibration.name, 'test_calibration')
        self.assertEqual(calibration.description, 'calibration metadata for my experiment')
        self.assertEqual(calibration.category, 'test category')
        self.assertEqual(calibration.about, 'test about')
        self.assertEqual(calibration.feedback_flag, True)
        np.testing.assert_array_equal(calibration.ensemble_indexes, np.arange(4, dtype=int))
        np.testing.assert_array_equal(calibration.decoder, np.arange(4, dtype=float), )
        np.testing.assert_array_equal(calibration.target, np.arange(2, dtype=float))
        np.testing.assert_array_equal(calibration.feedback_target, np.arange(2, dtype=float))
        np.testing.assert_array_equal(calibration.ensemble_mean, np.arange(4, dtype=float))
        np.testing.assert_array_equal(calibration.ensemble_sd, np.arange(4, dtype=float))


class TestCalibrationMetadataRoundtrip(TestCase):
    # Roundtrip test for Calibration Metadata
    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())
        self.path = 'test_calibration_metadata.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        calibration = Calibration_metadata(
            name='test_calibration',
            description='calibration metadata for my experiment',
            category='test category',
            about='test about',
            feedback_flag=True,
            ensemble_indexes=np.arange(4, dtype=int),
            decoder=np.arange(4, dtype=float),
            target=np.arange(2, dtype=float),
            feedback_target=np.arange(2, dtype=float),
            ensemble_mean=np.arange(4, dtype=float),
            ensemble_sd=np.arange(4, dtype=float)
        )
        self.nwbfile.add_lab_meta_data(lab_meta_data=calibration)

        # Write to file
        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_calibration = read_nwbfile.lab_meta_data['test_calibration']
            self.assertContainerEqual(calibration, read_calibration)
