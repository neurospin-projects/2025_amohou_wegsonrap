# Import packages 
import dxpy
import subprocess

import glob
import os
import pandas as pd
#from distutils.version import LooseVersion
from looseversion import LooseVersion


# Get project ID
project_id = dxpy.find_one_project()["id"]

# Automatically discover dispensed dataset ID and load the dataset 
dispensed_dataset_id = dxpy.find_one_data_object(typename='Dataset', name='app*.dataset', folder='/', name_mode='glob', project=project_id)['id']

dataset = (':').join([project_id, dispensed_dataset_id])

cmd = ["dx", "extract_dataset", dataset, "-ddd", "--delimiter", ","]
subprocess.check_call(cmd)



path = os.getcwd()
data_dict_csv = glob.glob(os.path.join(path, "*.data_dictionary.csv"))[0]
data_dict_df = pd.read_csv(data_dict_csv)
data_dict_df.head()


path = os.getcwd()
data_dict_csv = glob.glob(os.path.join(path, "*.data_dictionary.csv"))[0]
data_dict_df = pd.read_csv(data_dict_csv)
data_dict_df.head()



def field_names_for_ids(field_id):
    field_names = ["eid"]
    for _id in field_id:
        select_field_names = list(data_dict_df[data_dict_df.name.str.match(r'^p{}(_i\d+)?(_a\d+)?$'.format(_id))].name.values)
        field_names += select_field_names
    field_names = sorted([field for field in field_names], key=lambda n: LooseVersion(n))

    field_names = [f"participant.{f}" for f in field_names]
    return ",".join(field_names)

field_ids = ['31', '21022', '22001', '22006', '22009', '22019', '22021', '22027',
             '41270', '20107', '2946', '1807',
             '20110', '3526', '1845']
field_names = field_names_for_ids(field_ids)

cmd = ["dx", "extract_dataset", dataset, "--fields", field_names, "--delimiter", ",", "--output", "extracted_data.sql", "--sql"]
subprocess.check_call(cmd)

import pyspark

sc = pyspark.SparkContext()
spark = pyspark.sql.SparkSession(sc)

with open("extracted_data.sql", "r") as file:
    retrieve_sql=""
    for line in file:
        retrieve_sql += line.strip()

temp_df = spark.sql(retrieve_sql.strip(";"))
pdf = temp_df.toPandas()

print(pdf.head())


print(">> Fin traitement jeudi")
import re
pdf = pdf.rename(columns=lambda x: re.sub('participant.','',x))


codings_csv = glob.glob(os.path.join(path, "*.codings.csv"))[0]
codings_df = pd.read_csv(codings_csv)
codings_df.head()

# Collapse ICD-10 codes for Alzheimer's disease (G30* and F00*)
ad_icd_codes = list(
    codings_df[(codings_df["coding_name"] == "data_coding_19") & ((codings_df["parent_code"] == "G30") | (codings_df["parent_code"] == "F00"))]["code"])
ad_icd_codes

print(">> Block 1")
import ast
import numpy as np

# Replace NaN with string None for p41270

# Note: eval will return Nonetype for string "None"
pdf["p41270"] = pdf["p41270"].replace(np.nan, "None")


# Get each participant's hospital inpatient records in ICD10 Diagnoses
def icd10_codes(row):
    icd10_codes = row['p41270'] or []
    return list( set(icd10_codes) )

pdf['icd10_codes'] = pdf.apply(icd10_codes, axis=1)

# If the participant has any of the ICD-10 codes for AD, record the risk to "2" 
def has_ad_icd10(row): 
    return 0 if set(row['icd10_codes']).isdisjoint(ad_icd_codes) else 2 
pdf['has_ad_icd10'] = pdf.apply(has_ad_icd10, axis=1) 

pdf['illnesses_of_father'] = pdf.filter(regex=('p20107*')).apply(
    lambda x: list(set(eval(x.any() or "[]"))),  
    axis=1)

pdf['illnesses_of_mother'] = pdf.filter(regex=('p20110*')).apply(
    lambda x: list(set(eval(x.any() or "[]"))), 
    axis=1)



print(">> Block 2 ICD")


# Get the max age between age at death and recorded age

pdf['father_age'] = pdf.filter(regex=(r'(p1807_*|p2946_*)')).max(axis=1)
pdf['mother_age'] = pdf.filter(regex=(r'(p3526_*|p1845_*)')).max(axis=1)

# If the parent has diagnosed with AD (code 10), record it as 1; 
# else assign parent's AD risk with their risk, which is their age (proportional to diff of age of 100) with minimum risk at 0.32 

def parents_ad_risk(row): 
    import numpy as np 

    father_ad_risk = 1 if 10 in row['illnesses_of_father'] else np.maximum(0.32, (100 - row['father_age'])/100)
    mother_ad_risk = 1 if 10 in row['illnesses_of_mother'] else np.maximum(0.32, (100 - row['mother_age'])/100)
    return father_ad_risk + mother_ad_risk 

pdf['parents_ad_risk'] = pdf.apply(parents_ad_risk, axis=1) 
pdf['ad_risk_by_proxy'] = pdf[['has_ad_icd10','parents_ad_risk']].max(axis=1) 
pdf[['ad_risk_by_proxy','parents_ad_risk','has_ad_icd10']].head() 


print(">> Block 3 SCan Parents")


pdf_qced = pdf[
           (pdf['p31'] == pdf['p22001']) & # Filter in sex and genetic sex are the same
           (pdf['p22006']==1) &            # in_white_british_ancestry_subset
           (pdf['p22019'].isnull()) &      # Not Sex chromosome aneuploidy
           (pdf['p22021']!=10) &           # Not Ten or more third-degree relatives identified (not 'excess_relatives')
           (pdf['p22027'].isnull()) &      # Not het_missing_outliers
           ((pdf['father_age'].notnull()) & (pdf['father_age']>0)) &  # There is father's age
           ((pdf['mother_age'].notnull()) & (pdf['mother_age']>0)) &  # There is mother's age
           (pdf['illnesses_of_father'].apply(lambda x:(-11 not in x and -13 not in x))) &  # Filter out "do not know" or "prefer not to answer" father illness
           (pdf['illnesses_of_mother'].apply(lambda x:(-11 not in x and -13 not in x)))    # Filter out "do not know" or "prefer not to answer" mother illness
]


print(">> Block 3 Fin traitements")
