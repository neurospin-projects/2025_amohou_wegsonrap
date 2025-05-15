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
