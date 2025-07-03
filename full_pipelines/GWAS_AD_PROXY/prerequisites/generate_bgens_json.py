import glob
import json
import subprocess
import os

def _get_admin_info():
    """ Automatically discover project_id
    """
    dx_project_context_id  = os.environ.get("DX_PROJECT_CONTEXT_ID")
    print(f'DX_PROJECT_CONTEXT_ID is: [{dx_project_context_id}]')
    
    return dx_project_context_id

@dxpy.entry_point('main')
def main():
    
    # Get admin information (collate group-id)
    project_id = _get_admin_info()

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

    cmd = ['dx', 'find', 'data', '--name', '*.bgen', '--path', path_to_data, '--brief',]
    bgens =[f'dx://{item.decode("utf-8")}' for item in subprocess.check_output(cmd).splitlines()]

    cmd = ['dx', 'find', 'data', '--name', '*.sample', '--path', path_to_data, '--brief',]
    samples = [f'dx://{item.decode("utf-8")}' for item in subprocess.check_output(cmd).splitlines()]

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

    local_outfname='bgens_qc_input.json'
    with open(local_outfname, 'w') as f:
        json.dump(inputs, f)

    # output management and upload outputfile
    remote_outDXFile = dxpy.upload_local_file(local_outfname, project=project_id, folder='/tmp')
    output = {}
    output["outputfile"] = dxpy.dxlink(remote_outDXFile)

    return output

dxpy.run()