from ndx_cabmi import ROI_metadata

import numpy as np
from datetime import datetime
from pynwb import NWBHDF5IO

from pynwb.testing import TestCase, remove_test_file
from pynwb.testing.mock.file import mock_NWBFile


class TestROIMetadataConstructor(TestCase):
    # Unit test for constructing parameters Metadata

    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())

    def test_constructor(self):
        roi = ROI_metadata(
            name='test_ROI_metadata',
            description='ROI metadata for my experiment',
            category='test category',
            about='test about',
            image_mask_roi=np.ones((3, 3)),
            center_rois=np.ones((4, 5, 6, 7)),
            pixel_rois=np.ones((4, 5, 6))

        )

        self.assertEqual(roi.name, 'test_ROI_metadata')
        self.assertEqual(roi.description, 'ROI metadata for my experiment')
        self.assertEqual(roi.category, 'test category')
        self.assertEqual(roi.about, 'test about')
        np.testing.assert_array_equal(roi.image_mask_roi, np.ones((4, 4)))
        np.testing.assert_array_equal(roi.center_rois, np.ones((4, 5, 6, 7)))
        np.testing.assert_array_equal(roi.pixel_rois, np.ones((4, 5, 6)))


class TestROIMetadataRoundtrip(TestCase):
    # Roundtrip test for Calibration Metadata
    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())
        self.path = 'test_roi_metadata.nwb'

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        roi = ROI_metadata(
            name='test_ROI_metadata',
            description='roi metadata for my experiment',
            category='test category',
            about='test about',
            image_mask_roi=np.ones((3, 3)),
            center_rois=np.ones((4, 5, 6, 7)),
            pixel_rois=np.ones((4, 5, 6))
        )

        self.nwbfile.add_acquisition(roi)

        # Write to temporary file

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_roi = read_nwbfile.acquisition['test_ROI_metadata']
            self.assertContainerEqual(roi, read_roi)
