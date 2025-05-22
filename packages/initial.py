import dxpy
import subprocess
import glob
import os
import pandas as pd
import numpy as np
import re

# Get the current project ID
project_id = dxpy.find_one_project()["id"]
dataset = f"{project_id}:{dispensed_dataset_id}"

print('Step 2: Access and Extract the Dataset')
# Discover the dispensed dataset ID
dispensed_dataset_id = dxpy.find_one_data_object(typename='Dataset', name='app*.dataset', folder='/', name_mode='glob', project=projec_id)['id']


# Extract the dataset
cmd = ["dx", "extract_dataset", dataset, "-ddd", "--delimiter", ","]
subprocess.check_call(cmd)

print('Step 3: Load the Data Dictionary')
# Locate the data dictionary CSV file
path = os.getcwd()
data_dict_csv = glob.glob(os.path.join(path, "*.data_dictionary.csv"))[0]
data_dict_df = pd.read_csv(data_dict_csv)

print('Step 4: Define Function to Retrieve Field Names')
from distutils.version import LooseVersion

def field_names_for_ids(field_ids):
    field_names = ["eid"]
    for _id in field_ids:
        select_field_names = list(data_dict_df[data_dict_df.name.str.match(rf'^p{_id}(_i\d+)?(_a\d+)?$')].name.values)
        field_names += select_field_names
    field_names = sorted([field for field in field_names], key=LooseVersion)
    field_names = [f"participant.{f}" for f in field_names]
    return ",".join(field_names)

# Specify the field IDs of interest
field_ids = ['31', '21022', '22001', '22006', '22009', '22019', '22021', '22027',
             '41270', '20107', '2946', '1807',
             '20110', '3526', '1845']
field_names = field_names_for_ids(field_ids)
