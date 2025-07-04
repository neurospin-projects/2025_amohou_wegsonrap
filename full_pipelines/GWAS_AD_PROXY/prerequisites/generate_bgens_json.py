#!/bin/bash
# Script collecting all "dx" commands to be run from a dx-toolkit local shell.
#Use the command "python file_name.py" in the shell to run the code

import glob
import json
import subprocess
import os
import re


#Collect paths used to find files for the process

output_file_prefix = "gel_impute_data_snps_qc_pass"
plink_options = "--mac 10 --maf 0.0001 --hwe 1e-15 --mind 0.1 --geno 0.1"

path_to_data = '/Bulk/Exome sequences/Population level exome OQFE variants, BGEN format - final release/'
phenotype_folder = '/tmp/'
phenotype_file = 'ad_risk_by_proxy_wes.phe'

inputs = {
    "bgens_qc.extract_files": "Array[File]",
    "bgens_qc.ref_first": "Boolean (optional, default = true)",
    "bgens_qc.keep_file": "File? (optional)",
    "bgens_qc.output_prefix": "String",
    "bgens_qc.plink2_options": "String (optional, default = \"\")",
    "bgens_qc.geno_sample_files": "Array[File]+",
    "bgens_qc.geno_bgen_files": "Array[File]+"
}

#This fonction is used to give a priority number to a key in order to sort a group of keys that have different formats

def extract_number(key):
    # On cherche le nombre après 'c' et avant '_b0'
    match = re.search(r'_c(\d+)_b0', key)
    if match is None:
        # Clé ne correspond pas au format attendu, on la place en fin
        return (2, key)
    c_part = match.group(1)
    if c_part.isdigit():
        # Clés avec un nombre : priorité 0, tri par valeur numérique
        return (0, int(c_part))
    else:
        # Clés avec une lettre ou autre : priorité 1, tri alphabétique
        return (1, c_part)

#This fonction aims to sort the list of file_ids according to their real names on the RAP

def sort(cmd):
    dict = {}
    dico = {}
    for (item) in subprocess.check_output(cmd).splitlines() :
        file_complete_id = item.decode("utf-8") #parce que dans le fichier attendu l'id du projet apparait dans la sortie
        file_id = file_complete_id.split(":")[1]
        file_name = subprocess.check_output(['dx', 'describe', file_id, '--name']).decode('utf-8').split('\n')[0]
        dico[file_id] = file_complete_id #pour faire la correspondance après le tri des file names
        dict[file_name] = file_id
    dict = {k:dict[k] for k in sorted(dict.keys(), key=extract_number)}
    return [f'dx://{dico[file_id]}' for file_id in dict.values()]


#Tri des fichiers bgen
cmd = ['dx', 'find', 'data', '--name', '*.bgen', '--path', path_to_data, '--brief',]
bgens = sort(cmd)

#Tri des fichiers sample
cmd = ['dx', 'find', 'data', '--name', '*.sample', '--path', path_to_data, '--brief',]
samples =sort(cmd)

cmd = ['dx', 'find', 'data', '--name', phenotype_file, '--path', phenotype_folder, '--brief',]
pheno_file = [f'dx://{item.decode("utf-8")}' for item in subprocess.check_output(cmd).splitlines()][0]

# extract_files are not provided, therefore this key can be deleted
del inputs["bgens_qc.extract_files"]
inputs["bgens_qc.ref_first"] = True
inputs["bgens_qc.keep_file"] = pheno_file
inputs["bgens_qc.output_prefix"] = output_file_prefix
inputs["bgens_qc.plink2_options"] = plink_options
inputs["bgens_qc.geno_sample_files"] = samples
inputs["bgens_qc.geno_bgen_files"] = bgens

with open('bgens_qc_input.json', 'w') as f:
    json.dump(inputs, f, indent=2)

