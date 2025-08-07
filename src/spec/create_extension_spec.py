# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec


# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name='''ndx-cabmi''',
        version='''0.1.1''',
        doc='''Extension to include CABMI closed loop experiments''',
        author=['Nuria Vendrell Llopis',],
        contact=['nvl2@uab.edu',],
    )
    ns_builder.include_namespace('core')
    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('LabMetaData', namespace='core')
    ns_builder.include_type('NWBContainer', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='core')

    # Calibration metadata group
    Calibration_metadata = NWBGroupSpec(neurodata_type_def='Calibration_metadata',
                                        neurodata_type_inc='LabMetaData',
                                        doc='Metadata result of the calibration and needed for the BMI', quantity='?',
                                        datasets=[NWBDatasetSpec(name='ensemble_indexes',
                                                                 doc='indexes of the neurons used as part of the '
                                                                     'ensemble', dtype='int32',
                                                                 dims=['number of ensemble neurons']),
                                                  NWBDatasetSpec(name='decoder',
                                                                 doc='multiplier to each of the ensemble neurons',
                                                                 dtype='float64', dims=['number of ensemble neurons']),
                                                  NWBDatasetSpec(name='target',
                                                                 doc='Threshold for the cursor, can be one or two '
                                                                     'per dimension of the cursor', dtype='float64',
                                                                 dims=['number of targets']),
                                                  NWBDatasetSpec(name='feedback_target',
                                                                 doc='if there is auditory tone as feedback, value '
                                                                     'in Hz for the auditory tone for each of the'
                                                                     ' targets, can be one or two per dimension '
                                                                     'of the cursor', dtype='float64',
                                                                 dims=['number of audio targets']),
                                                  NWBDatasetSpec(name='ensemble_mean',
                                                                 doc='mean of the activity of each of the ensemble '
                                                                     'neurons during calibration', dtype='float64',
                                                                 dims=['number of ensemble neurons']),
                                                  NWBDatasetSpec(name='ensemble_sd',
                                                                 doc='standard deviation of the activity of each of '
                                                                     'the ensemble neurons during calibration',
                                                                 dtype='float64', dims=['number of ensemble neurons'])],
                                        attributes=[NWBAttributeSpec(name='description', doc='describe the metadata',
                                                                     dtype='text', required=True),
                                                    NWBAttributeSpec(name='category', doc='free category field',
                                                                     dtype='text', required=False),
                                                    NWBAttributeSpec(name='about', doc='about', dtype='text', 
                                                                    required=False),
                                                    NWBAttributeSpec(name='feedback_flag',
                                                                     doc='if there is auditory tone as feedback or not',
                                                                     dtype='bool', required=True)])

    # BMI parameters group
    BMI_parameters = NWBGroupSpec(neurodata_type_def='Parameters_BMI',
                                  neurodata_type_inc='LabMetaData',
                                  doc='parameters required for running calibration and BMI', quantity='?',
                                  datasets=[NWBDatasetSpec(name='back_to_baseline_threshold',
                                                           doc='Required value of the cursor to start a new trial '
                                                               'after going back to baseline', dtype='float64',
                                                           dims=['number of targets']),
                                            NWBDatasetSpec(name='conditions_rule',
                                                           doc='str with the rule to be followed by the conditions'
                                                               ' for it to be considered hitting a target',
                                                           dtype='text', dims=['number of conditions']),
                                            NWBDatasetSpec(name='conditions_target',
                                                           doc='value of each of the conditions to be met by the cursor'
                                                               ' for it to be considered hitting a target',
                                                           dtype='float64', dims=['number of conditions']),
                                            NWBDatasetSpec(name='frames_per_reward_range',
                                                           doc='A range on how many frames should elapse before a '
                                                               'reward is expected.', dtype='int32',
                                                           dims=['lower_value|higher_value'], shape=[2])],
                                  attributes=[NWBAttributeSpec(name='description', doc='describe the BMI_parameters',
                                                               dtype='text', required=True),
                                              NWBAttributeSpec(name='category', doc='free category field', dtype='text',
                                                               required=False),
                                              NWBAttributeSpec(name='about', doc='about', dtype='text',
                                                               required=False),
                                              NWBAttributeSpec(name='back_to_baseline_frames',
                                                               doc='Required number of frames for the cursor to be '
                                                                   'over the back_to_baseline_threshold for it to be'
                                                                   ' considered back to baseline', dtype='int32',
                                                               required=False),
                                              NWBAttributeSpec(name='prefix_window_frames',
                                                               doc='number microscopy frames to ignore at start of bmi '
                                                                   'acquisition', dtype='int32',
                                                               required=False),  # previously prefix_win
                                              NWBAttributeSpec(name='dff_baseline_window_frames',
                                                               doc='Period at the beginning of the BMI without '
                                                                   'calculating cursor to establish the dff '
                                                                   'baseline of the ensemble activity', dtype='int32',
                                                               required=False),  # previously f0_win
                                              NWBAttributeSpec(name='smooth_window_frames',
                                                               doc='number of frames to use for smoothing dff and avoid'
                                                                   'motion artifacts to affect the cursor',
                                                               dtype='int32', required=False),  # previously dff_win
                                              NWBAttributeSpec(name='cursor_zscore_bool',
                                                               doc='if 1, neural activity is zscored before going into '
                                                                   'cursor calculation. if 0, activity is not zscored',
                                                               dtype='bool', required=False),
                                              NWBAttributeSpec(name='relaxation_window_frames',
                                                               doc='number of frames after a hit to stop the BMI',
                                                               dtype='int32', required=False),
                                              NWBAttributeSpec(name='timelimit_frames',
                                                               doc='time limit in frames that the animal has to finish'
                                                                   ' a given trial', dtype='int32',
                                                               required=False),
                                              # CaBMI may not have time limits for trials
                                              NWBAttributeSpec(name='timeout_window_frames',
                                                               doc='if there is a time limit for a trial, the number '
                                                                   'of frames after a miss to stop the BMI as a '
                                                                   'punishment', dtype='int32', required=False)])

    # cursor group
    CaBMI_series = NWBGroupSpec(neurodata_type_def='CaBMISeries', neurodata_type_inc='NWBDataInterface',
                                doc='Data collected while performing a CaBMI experiment', quantity='?',
                                datasets=[NWBDatasetSpec(name='target',
                                                         doc='targets at which the cursor would end up in a *hit*',
                                                         dtype='float64', dims=['number of targets']),
                                          NWBDatasetSpec(name='cursor',
                                                         doc='values of the cursor obtained from decoding neural data',
                                                         dtype='float64', dims=['degrees_freedom, BMI_frames']),
                                          NWBDatasetSpec(name='cursor_audio',
                                                         doc='values of the audio cursor obtained from mapping the '
                                                             'neural cursor (obtained by decodind the neural data of'
                                                             'ensemble neurons) to an auditory tone',
                                                         dtype='int32', dims=['degrees_freedom, BMI_frames']),
                                          NWBDatasetSpec(name='raw_activity',
                                                         doc='Raw activity of the ensemble neurons', dtype='float64',
                                                         dims=['number_ensemble_neurons', 'BMI_frames']),
                                          NWBDatasetSpec(name='baseline_vector',
                                                         doc='Baseline of the fluorescence for each of the ensemble '
                                                             'neurons. Used to reliable calculate the dff of the '
                                                             'ensemble neurons. Updated overtime', dtype='float64',
                                                         dims=['number_ensemble_neurons', 'BMI_frames']),
                                          NWBDatasetSpec(name='self_hits',
                                                         doc='Boolean array with 1 when a hit was achieved due to the'
                                                             'normal (during BMI) activity of ensemble neurons',
                                                         dtype='bool', dims=['BMI_frames']),
                                          NWBDatasetSpec(name='stim_hits',
                                                         doc='Boolean array with 1 when a hit was achieved due to'
                                                             'manipulations to the circuit',
                                                         dtype='bool', dims=['BMI_frames']),
                                          NWBDatasetSpec(name='self_reward',
                                                         doc='Boolean array with 1 when a reward was given after a self'
                                                             'hit was achieved',
                                                         dtype='bool', dims=['BMI_frames']),
                                          NWBDatasetSpec(name='stim_reward',
                                                         doc='Boolean array with 1 when a reward was given after a stim'
                                                             'hit was achieved',
                                                         dtype='bool', dims=['BMI_frames']),
                                          NWBDatasetSpec(name='stim_delivery',
                                                         doc='Boolean array with 1 when a stim was performed',
                                                         dtype='bool', dims=['BMI_frames']),
                                          NWBDatasetSpec(name='trial_start',
                                                         doc='Boolean array with 1 when a new trial started',
                                                         dtype='bool', dims=['BMI_frames']),
                                          NWBDatasetSpec(name='time_vector',
                                                         doc='time it took to complete a frame in ms',
                                                         dtype='float64', dims=['BMI_frames']),
                                          NWBDatasetSpec(name='scheduled_stim',
                                                         doc='Indices of the frames that had been selected before'
                                                             'the experiment starts to have a stim. For random stim'
                                                             'control purposes or holographic pretrains',
                                                         dtype='int32', dims=['number_stims']),
                                          NWBDatasetSpec(name='scheduled_reward',
                                                         doc='Indices of the frames that had been selected before'
                                                             'the experiment starts to have a reward. For random '
                                                             'reward control purposes or other experiments',
                                                         dtype='int32', dims=['number_rewards']),
                                          ],
                                attributes=[NWBAttributeSpec(name='description', doc='describe the CaBMI results',
                                                               dtype='text', required=True),
                                            NWBAttributeSpec(name='about', doc='about doc', dtype='text',
                                                             required=False),
                                            NWBAttributeSpec(name='experiment_type', doc='Type of experiment performed',
                                                             dtype='text', required=False),
                                            NWBAttributeSpec(name='self_hit_counter', doc='counter of the amount of '
                                                                                          'self-hits achieved',
                                                             dtype='int32', required=False),
                                            NWBAttributeSpec(name='stim_hit_counter', doc='counter of the amount of '
                                                                                          'stim-hits achieved',
                                                             dtype='int32', required=False),
                                            NWBAttributeSpec(name='self_reward_counter', doc='counter of the amount of'
                                                                                             ' self-rewards obtained',
                                                             dtype='int32', required=False),
                                            NWBAttributeSpec(name='stim_reward_counter', doc='counter of the amount of'
                                                                                             ' stim-rewards achieved',
                                                             dtype='int32', required=False),
                                            NWBAttributeSpec(name='scheduled_stim_counter',
                                                             doc='counter of the amount of scheduled stims that were '
                                                                 'ultimately given (some scheduled stims may be'
                                                                 'missing if the bmi was busy with something else'
                                                                 'or the animal was not on a trial)',
                                                             dtype='int32', required=False),
                                            NWBAttributeSpec(name='scheduled_reward_counter',
                                                             doc='counter of the amount of scheduled rewards that were '
                                                                 'ultimately given (some scheduled rewards may be'
                                                                 'missing if the bmi was busy with something else'
                                                                 'or the animal was not on a trial)',
                                                             dtype='int32', required=False),
                                            NWBAttributeSpec(name='trial_counter',
                                                             doc='counter of the amount of trials started. This value'
                                                                 'may differ from the amount of hits achieved if the'
                                                                 'last trial was not finished',
                                                             dtype='int32', required=False),
                                            NWBAttributeSpec(name='number_of_hits',
                                                             doc='If the experiments has a timelimit for trials, the'
                                                                 'amount of trials that ended in a hit (achieved a'
                                                                 'target)',
                                                             dtype='int32', required=False),
                                            NWBAttributeSpec(name='number_of_misses',
                                                             doc='If the experiments has a timelimit for trials, the'
                                                                 'amount of trials that ended in a miss (did not '
                                                                 'achieve the target)',
                                                             dtype='int32', required=False),
                                            NWBAttributeSpec(name='last_frame',
                                                             doc='number of the last frame being processed',
                                                             dtype='int32', required=False)])

    ROI_metadata = NWBGroupSpec(neurodata_type_def='ROI_metadata', neurodata_type_inc='NWBDataInterface',
                                doc='Information of the rois used during the experiment',
                                datasets=[NWBDatasetSpec(name='image_mask_roi',
                                                         doc=('ROIs designated using a mask of size [width, height] '
                                                              '(2D recording) or [width, height, depth] (3D recording),'
                                                              ' where for a given pixel a value of 1 indicates '
                                                              ' belonging to the ROI. The depth value may represent '
                                                              'to which plane the roi belonged to'),
                                                         quantity='?',
                                                         dims=None,
                                                         shape=None),
                                          NWBDatasetSpec(name='center_rois',
                                                         doc=('ROIs designated as a list specifying the pixel and radio'
                                                              '([x1, y1, r1], or voxel ([x1, y1, z1, r1]) '
                                                              ' of each ROI, where the items in the list are the '
                                                              ' coordinates of the center of the ROI and the size of '
                                                              ' the Roi given in radio size. The depth value may '
                                                              ' represent to which plane the roi belonged to'),
                                                         quantity='?',
                                                         dims=None,
                                                         shape=None),
                                          NWBDatasetSpec(name='pixel_rois',
                                                         doc=('ROIs designated as a list specifying all the pixels'
                                                              '([x1, y1], or voxel ([x1, y1, z1]) of each ROI, where'
                                                              ' the items in the list are each of the pixels belonging'
                                                              ' to the roi'),
                                                         quantity='?',
                                                         dims=None,
                                                         shape=None)],
                                attributes=[NWBAttributeSpec(name='description', doc='describe the metadata',
                                                             dtype='text', required=True),
                                            NWBAttributeSpec(name='category', doc='free category field', dtype='text',
                                                             required=False),
                                            NWBAttributeSpec(name='about', doc='about', dtype='text',
                                                             required=False)])

    new_data_types = [Calibration_metadata, BMI_parameters, CaBMI_series, ROI_metadata]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
