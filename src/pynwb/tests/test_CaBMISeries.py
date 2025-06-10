from ndx_cabmi import CaBMISeries

import tempfile
import numpy as np
from datetime import datetime
from pynwb import NWBHDF5IO

from pynwb.testing import TestCase, remove_test_file
from pynwb.testing import TestCase
from pynwb.testing.mock.file import mock_NWBFile
from datetime import datetime
import unittest

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


class TestCaBMISeriesRoundtrip(unittest.TestCase):
    #Roundtrip test for Calibration Metadata
    def setUp(self):
        self.nwbfile = mock_NWBFile(session_start_time=datetime.now().astimezone())
    
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

        # Write to temporary file
        with tempfile.NamedTemporaryFile(suffix='.nwb', delete=True) as tmp:
            with NWBHDF5IO(tmp.name, mode='w') as io:
                io.write(self.nwbfile)

        
            with NWBHDF5IO(tmp.name, mode='r', load_namespaces=True) as io:
                read_nwbfile = io.read()
                print("\n=== LabMetaData Contents ===")
                for name, meta in read_nwbfile.acquisition.items():
                    
                    print(f"CaBMISeries Name: {name}")
                    print(f"About: {meta.about}")
                    print(f"Self hit counter: {meta.self_hit_counter}")
                    print(f"Stim hit counter: {meta.stim_hit_counter}\n")
                    print(f"Self reward counter: {meta.self_reward_counter}")
                    print(f"Stim reward counter: {meta.stim_reward_counter}")
                    print(f"Scheduled stim counter: {meta.scheduled_stim_counter}\n")
                    print(f"Scheduled reward counter: {meta.scheduled_reward_counter}")
                    print(f"Trial counter: {meta.trial_counter}\n")
                    print(f"Number of hits: {meta.number_of_hits}\n")
                    print(f"Number of misses: {meta.number_of_misses}")
                    print(f"Last frame: {meta.last_frame}\n")
                    print(f"Target: {meta.target}\n")
                    print(f"Cursor: {meta.cursor}")
                    print(f"Cursor Audio: {meta.cursor_audio}")
                    print(f"Raw activity: {meta.raw_activity}")
                    print(f"Baseline vector: {meta.baseline_vector}\n")
                    print(f"Self hits: {meta.self_hits}")
                    print(f"Stim hits: {meta.stim_hits}")
                    print(f"Self reward: {meta.self_reward}\n")
                    print(f"Stim reward: {meta.stim_reward}")
                    print(f"Stim delivery: {meta.stim_delivery}\n")
                    print(f"Trial start: {meta.trial_start}\n")
                    print(f"Time vector: {meta.time_vector}")
                    print(f"Scheduled stim: {meta.scheduled_stim}\n")
                    print(f"Scheduled reward: {meta.scheduled_reward}\n")        