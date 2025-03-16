# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec

# TODO: import other spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-cabmi""",
        version="""0.1.0""",
        doc="""Extension to include CABMI closed loop experiments""",
        author=[
            "Nuria Vendrell Llopis",
        ],
        contact=[
            "nvl2@uab.edu",
        ],
    )
    ns_builder.include_namespace("core")
    ns_builder.include_type('TimeSeries', namespace='core')
    
    # TODO: if your extension builds on another extension, include the namespace
    # of the other extension below
    # ns_builder.include_namespace("ndx-other-extension")

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/stable/tutorials/general/extensions.html
    # for more information
    Calibration_metadata = NWBGroupSpec(neurodata_type_def='Calibration_metadata',
                                        neurodata_type_inc='NWBDataInterface',
                                        doc='Metadata result of the calibration and needed for the BMI')
    Calibration_metadata.add_attribute(name='description', doc='describe the metadata', dtype='text', required=True)
    Calibration_metadata.add_attribute(name='category', doc='free category field', dtype='text', required=False)
    Calibration_metadata.add_attribute(name='help', doc='help', dtype='text', value='stores whatev data')
    Calibration_metadata.add_attribute(name='Ensemble_indeces',
                                       doc='indeces of the neurons used as part of the ensemble', dtype='int32',
                                       dims=['number of ensemble neurons'], required=True)
    Calibration_metadata.add_attribute(name='Decoder',
                                       doc='multiplier to each of the ensemble neurons', dtype='float64',
                                       dims=['number of ensemble neurons'], required=True)
    Calibration_metadata.add_attribute(name='Target',
                                       doc='Threshold for the cursor, can be one or two per dimension of the cursor',
                                       dtype='float64', dims=['number of targets'], required=True)
    Calibration_metadata.add_attribute(name='Ensemble_mean',
                                       doc='mean of the activity of each of the ensemble neurons during calibration',
                                       dtype='float64', dims=['number of ensemble neurons'], required=False)
    Calibration_metadata.add_attribute(name='Ensemble_sd',
                                       doc='standard deviation of the activity of each of the ensemble neurons'
                                           ' during calibration', dtype='float64', dims=['number of ensemble neurons'],
                                       required=False)

    BMI_parameters = NWBGroupSpec(neurodata_type_def='Parameters needed to run the BMI',
                                  neurodata_type_inc='NWBDataInterface',
                                  doc='parameters required for running calibration and BMI')
    BMI_parameters.add_attribute(name='Back_to_baseline_threshold', doc='Required value of the cursor to start a '
                                                                        'new trial after going back to baseline',
                                 dtype='float64', dims=['number of targets'], required=True)
    BMI_parameters.add_attribute(name='Back_to_baseline_frames', doc='Required number of frames for the cursor to be'
                                                                     'over the back_to_baseline_threshold for it to'
                                                                     'be considered back to baseline',                                                          'going back to baseline',
                                 dtype='int32', required=True)
    BMI_parameters.add_attribute(name='number_conditions_target', doc='number of conditions to be met by the cursor '
                                                                  'to be considered as hitting a target',
                                 dtype='int32', required=True)
    BMI_parameters.add_dataset(name='conditions_target', doc='value of each of the conditions to be met by the cursor'
                                                             ' for it to be considered hitting a target',
                               dtype='float64', dims=['number of conditions'], required=True)
    BMI_parameters.add_dataset(name='seconds_per_reward_range', doc=' a range on how many frames should elapse before'
                                                                    ' a reward is expected.',
                               dtype='int32', dims=['lower value, higher value'], shape=[None, 2], required=True)


    point_node = NWBGroupSpec(neurodata_type_def='PointNode',
                              neurodata_type_inc='Node',
                              doc='A node that represents a single 2D point in space (e.g. reward well, novel object'
                                  ' location)',
                              quantity='*',
                              datasets=[NWBDatasetSpec(doc='x/y coordinate of this 2D point',
                                                       name='coords',
                                                       dtype='float',
                                                       dims=['num_coords', 'x_vals|y_vals'],
                                                       shape=[1, 2])],
                              attributes=[
                                  NWBAttributeSpec(name='help', doc='help doc', dtype='text', value='Apparatus Point')])

    cursor_series = NWBGroupSpec(
        neurodata_type_def="CursorSeries",
        neurodata_type_inc="TimeSeries",
        doc="An extension of TimeSeries to include BMI cursor data and metadata.",
        attributes=[NWBAttributeSpec(name="Target", doc="Target result of calibration.", dtype="float64",
                                     required=True)],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [cursor_series]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
