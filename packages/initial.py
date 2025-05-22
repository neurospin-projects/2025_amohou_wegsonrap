import dxpy
import subprocess
import glob
import os
import pandas as pd
import numpy as np
import re

print('Step 2: Access and Extract the Dataset')
# Get the current project ID
project_id = dxpy.find_one_project()["id"]

# Discover the dispensed dataset ID
dispensed_dataset_id = dxpy.find_one_data_object(typename='Dataset', name='app*.dataset', folder='/', name_mode='glob', project=project_id)['id']
dataset = f"{project_id}:{dispensed_dataset_id}"

# Extract the dataset
cmd = ["dx", "extract_dataset", dataset, "-ddd", "--delimiter", ","]
subprocess.check_call(cmd)

print('Step 3: Load the Data Dictionary')
# Locate the data dictionary CSV file
path = os.getcwd()
data_dict_csv = glob.glob(os.path.join(path, "*.data_dictionary.csv"))[0]
data_dict_df = pd.read_csv(data_dict_csv)

print('Step 4: Define Function to Retrieve Field Names')
from looseversion import LooseVersion

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


print('Step 5: Extract the Relevant Data Fields')
# Extract the specified fields
cmd = ["dx", "extract_dataset", dataset, "--fields", field_names, "--delimiter", ",", "--output", "extracted_data.sql", "--sql"]
subprocess.check_call(cmd)

STOP

cmd = ["dx", "extract_dataset", dataset, "--fields", field_names, "--delimiter", ",", "--output", "extracted_data.csv"]
subprocess.check_call(cmd)

# Load the extracted data into a DataFrame
pdf = pd.read_csv("extracted_data.csv")

# Remove the 'participant.' prefix from column names
pdf.columns = pdf.columns.str.replace('participant.', '', regex=False)

print('Step 6: Identify Alzheimers Disease ICD-10 Codes')
# Load the codings CSV
codings_csv = glob.glob(os.path.join(path, "*.codings.csv"))[0]
codings_df = pd.read_csv(codings_csv)

# Identify ICD-10 codes for Alzheimer's Disease (G30* and F00*)
ad_icd_codes = codings_df[
    (codings_df["coding_name"] == "data_coding_19") &
    (codings_df["parent_code"].isin(["G30", "F00"]))
]["code"].tolist()


print('Step 7: Derive the AD-by-Proxy Phenotype')
# Replace NaN with empty lists for ICD-10 codes
pdf["p41270"] = pdf["p41270"].apply(lambda x: [] if pd.isna(x) else eval(x))

# Determine if participant has AD-related ICD-10 codes
pdf['has_ad_icd10'] = pdf["p41270"].apply(lambda codes: 2 if set(codes).intersection(ad_icd_codes) else 0)

# Process parental illnesses
pdf['illnesses_of_father'] = pdf.filter(regex='p20107').apply(lambda x: list(set().union(*[eval(i) if pd.notna(i) else [] for i in x])), axis=1)
pdf['illnesses_of_mother'] = pdf.filter(regex='p20110').apply(lambda x: list(set().union(*[eval(i) if pd.notna(i) else [] for i in x])), axis=1)

# Determine parental ages
pdf['father_age'] = pdf[['p1807', 'p2946']].max(axis=1)
pdf['mother_age'] = pdf[['p3526', 'p1845']].max(axis=1)

# Calculate parental AD risk
def calculate_parental_ad_risk(row):
    father_risk = 1 if 10 in row['illnesses_of_father'] else max(0.32, (100 - row['father_age']) / 100)
    mother_risk = 1 if 10 in row['illnesses_of_mother'] else max(0.32, (100 - row['mother_age']) / 100)
    return father_risk + mother_risk

pdf['parents_ad_risk'] = pdf.apply(calculate_parental_ad_risk, axis=1)

# Determine overall AD risk by proxy
pdf['ad_risk_by_proxy'] = pdf[['has_ad_icd10', 'parents_ad_risk']].max(axis=1)

# Define case/control status based on AD risk
pdf['ad_by_proxy'] = np.where(pdf['ad_risk_by_proxy'] >= 1, 1, 0)
