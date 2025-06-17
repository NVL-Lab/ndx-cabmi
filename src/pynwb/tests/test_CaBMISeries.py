from ndx_cabmi import CaBMISeries


import numpy as np
from datetime import datetime
from pynwb import NWBHDF5IO

from pynwb.testing import TestCase, remove_test_file
from pynwb.testing.mock.file import mock_NWBFile



class TestCaBMISeriesConstructor(TestCase):
    #Unit test for constructing CaBMI Series

    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())

    def test_constructor(self):
        cabmiseries = CaBMISeries(
            name = "test_cabmiseries",
            about = "test about",
            self_hit_counter = 1,
            stim_hit_counter = 1,
            self_reward_counter = 1,
            stim_reward_counter = 1,
            scheduled_stim_counter = 1,
            scheduled_reward_counter = 1,
            trial_counter = 1,
            number_of_hits = 1, 
            number_of_misses = 1,
            last_frame = 100,
            target = np.arange(2, dtype=float),
            cursor = np.arange(2, dtype=float),
            cursor_audio = np.arange(2, dtype=int),
            raw_activity = np.arange(4*10).reshape(4,10),
            baseline_vector = np.arange(4*10).reshape(4,10),
            self_hits = np.ones(10, dtype=bool),
            stim_hits = np.ones(10, dtype=bool),
            self_reward = np.ones(10, dtype=bool),
            stim_reward = np.ones(10, dtype=bool),
            stim_delivery = np.ones(10, dtype=bool),
            trial_start = np.ones(10, dtype=bool),
            time_vector = np.arange(10, dtype=float),
            scheduled_stim = np.arange(10, dtype=int),
            scheduled_reward = np.arange(10, dtype=int),
        )

        self.assertEqual(cabmiseries.name, "test_cabmiseries")
        self.assertEqual(cabmiseries.about, 'test about')
        self.assertEqual(cabmiseries.self_hit_counter, 1)
        self.assertEqual(cabmiseries.stim_hit_counter, 1)
        self.assertEqual(cabmiseries.self_reward_counter, 1)
        self.assertEqual(cabmiseries.stim_reward_counter, 1)
        self.assertEqual(cabmiseries.scheduled_stim_counter, 1)
        self.assertEqual(cabmiseries.scheduled_reward_counter, 1)
        self.assertEqual(cabmiseries.trial_counter, 1)
        self.assertEqual(cabmiseries.number_of_hits, 1)
        self.assertEqual(cabmiseries.number_of_misses, 1)
        self.assertEqual(cabmiseries.last_frame, 100)
        np.testing.assert_array_equal(cabmiseries.target, np.arange(2, dtype=float))
        np.testing.assert_array_equal(cabmiseries.cursor, np.arange(2, dtype=float))
        np.testing.assert_array_equal(cabmiseries.cursor_audio, np.arange(2, dtype=int))
        np.testing.assert_array_equal(cabmiseries.raw_activity, np.arange(4*10).reshape(4,10))
        np.testing.assert_array_equal(cabmiseries.baseline_vector, np.arange(4*10).reshape(4,10))
        np.testing.assert_array_equal(cabmiseries.self_hits, np.ones(10, dtype=bool))
        np.testing.assert_array_equal(cabmiseries.stim_hits, np.ones(10, dtype=bool))
        np.testing.assert_array_equal(cabmiseries.self_reward, np.ones(10, dtype=bool))
        np.testing.assert_array_equal(cabmiseries.stim_reward, np.ones(10, dtype=bool))
        np.testing.assert_array_equal(cabmiseries.stim_delivery, np.ones(10, dtype=bool))
        np.testing.assert_array_equal(cabmiseries.trial_start, np.ones(10, dtype=bool))
        np.testing.assert_array_equal(cabmiseries.time_vector,  np.arange(10, dtype=float))
        np.testing.assert_array_equal(cabmiseries.scheduled_stim,  np.arange(10, dtype=int))
        np.testing.assert_array_equal(cabmiseries.scheduled_reward,  np.arange(10, dtype=int))


class TestCaBMISeriesRoundtrip(TestCase):
    #Roundtrip test for CaBMI Series
    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())
        self.path = "test_cabmi_series.nwb"
    
    def tearDown(self):
        remove_test_file(self.path)
    
    def test_roundtrip(self):
        cabmiseries = CaBMISeries(
            name = "test_cabmiseries",
            about = "test about",
            self_hit_counter = 1,
            stim_hit_counter = 1,
            self_reward_counter = 1,
            stim_reward_counter = 1,
            scheduled_stim_counter = 1,
            scheduled_reward_counter = 1,
            trial_counter = 1,
            number_of_hits = 1, 
            number_of_misses = 1,
            last_frame = 100,
            target = np.arange(2, dtype=float),
            cursor = np.arange(2, dtype=float),
            cursor_audio = np.arange(2, dtype=int),
            raw_activity = np.arange(4*10, dtype=float).reshape(4,10),
            baseline_vector = np.arange(4*10, dtype=float).reshape(4,10),
            self_hits = np.ones(10, dtype=bool),
            stim_hits = np.ones(10, dtype=bool),
            self_reward = np.ones(10, dtype=bool),
            stim_reward = np.ones(10, dtype=bool),
            stim_delivery = np.ones(10, dtype=bool),
            trial_start = np.ones(10, dtype=bool),
            time_vector = np.arange(10, dtype=float),
            scheduled_stim = np.arange(10, dtype=int),
            scheduled_reward = np.arange(10, dtype=int),
        )

        self.nwbfile.add_acquisition(cabmiseries)

        # Write to file

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)


        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            read_cabmi = read_nwbfile.acquisition["test_cabmiseries"]
            self.assertContainerEqual(cabmiseries, read_cabmi)
    