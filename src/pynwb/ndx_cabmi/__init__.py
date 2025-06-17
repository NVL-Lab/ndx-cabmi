from importlib.resources import files
import os
from pathlib import Path
from pynwb import load_namespaces, get_class

# Get path to the namespace.yaml file with the expected location when installed not in editable mode
__location_of_this_file = Path(files(__name__))
__spec_path = __location_of_this_file / "spec" / "ndx-cabmi.namespace.yaml"

# If that path does not exist, we are likely running in editable mode. Use the local path instead
if not os.path.exists(__spec_path):
    __spec_path = __location_of_this_file.parent.parent.parent / "spec" / "ndx-cabmi.namespace.yaml"

# Load the namespace
load_namespaces(str(__spec_path))

# TODO: Define your classes here to make them accessible at the package level.
# Either have PyNWB generate a class from the spec using `get_class` as shown
# below or write a custom class and register it using the class decorator
# `@register_class("TetrodeSeries", "ndx-cabmi")`
Calibration_metadata = get_class("Calibration_metadata", "ndx-cabmi")
Parameters_BMI = get_class("Parameters_BMI", "ndx-cabmi")
CaBMISeries = get_class("CaBMISeries", "ndx-cabmi")
ROI_metadata = get_class("ROI_metadata", "ndx-cabmi")

# TODO: Add all classes to __all__ to make them accessible at the package level
__all__ = ["Calibration_metadata", "Parameters_BMI", "CaBMISeries", "ROI_metadata"]

# Remove these functions/modules from the package
del load_namespaces, get_class, files, os, __location_of_this_file, __spec_path
