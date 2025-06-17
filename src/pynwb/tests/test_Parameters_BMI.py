from ndx_cabmi import Parameters_BMI

import numpy as np
from datetime import datetime
from pynwb import NWBHDF5IO

from pynwb.testing import TestCase, remove_test_file
from pynwb.testing.mock.file import mock_NWBFile
from datetime import datetime


class TestParametersBMIConstructor(TestCase):
    #Unit test for constructing parameters Metadata

    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())

    def test_constructor(self):
        parameters = Parameters_BMI(
            name = "test_parameters_BMI",
            description = "BMI parameters for my experiment",
            category = "test category",
            about = "test about",
            back_to_baseline_frames = 10,
            prefix_window_frames = 11,
            dff_baseline_window_frames = 12,
            smooth_window_frames = 13,
            cursor_zscore_bool = True,
            relaxation_window_frames = 2, 
            timelimit_frames = 3,
            timeout_window_frames = 4,
            back_to_baseline_threshold = [4.1, 4.1],
            conditions_target = [150.2, 120.1],
            seconds_per_reward_range = [0, 120]
            
        )

        self.assertEqual(parameters.name, "test_parameters_BMI")
        self.assertEqual(parameters.description, 'BMI parameters for my experiment')
        self.assertEqual(parameters.category, 'test category')
        self.assertEqual(parameters.about, "test about")
        self.assertEqual(parameters.back_to_baseline_frames, 10)
        self.assertEqual(parameters.prefix_window_frames, 11)
        self.assertEqual(parameters.dff_baseline_window_frames, 12)
        self.assertEqual(parameters.smooth_window_frames, 13)
        self.assertEqual(parameters.cursor_zscore_bool, True)
        self.assertEqual(parameters.relaxation_window_frames, 2)
        self.assertEqual(parameters.timelimit_frames, 3)
        self.assertEqual(parameters.timeout_window_frames, 4)
        self.assertEqual(parameters.back_to_baseline_threshold, [4.1, 4.1])
        self.assertEqual(parameters.conditions_target, [150.2, 120.1])
        self.assertEqual(parameters.seconds_per_reward_range, [0, 120])



class TestParametersBMIRoundtrip(TestCase):
    #Roundtrip test for Parameters BMI
    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())
        self.path = "test_parameter_bmi.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        parameters = Parameters_BMI(
            name = "test_parameters_BMI",
            description = "BMI parameters for my experiment",
            category = "test category",
            about = "test about",
            back_to_baseline_frames = 10,
            prefix_window_frames = 11,
            dff_baseline_window_frames = 12,
            smooth_window_frames = 13,
            cursor_zscore_bool = True,
            relaxation_window_frames = 2, 
            timelimit_frames = 3,
            timeout_window_frames = 4,
            back_to_baseline_threshold = [4.1, 4.1],
            conditions_target = [150.2, 120.1],
            seconds_per_reward_range = [0, 120]
            
        )

        self.nwbfile.add_lab_meta_data(lab_meta_data=parameters)

        # Write to file

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

    
        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_parameters = read_nwbfile.lab_meta_data["test_parameters_BMI"]
            self.assertContainerEqual(parameters, read_parameters)

