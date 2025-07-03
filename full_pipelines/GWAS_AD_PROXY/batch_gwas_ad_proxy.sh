#!/bin/bash
# Script collecting all "dx run" commands to be run from a dx-toolkit local shell.

# Step1
#######
# prolog to select field and obtain a file for table exporter
    ret=$($ROOT_INSTALL/prerequisites/build-ns-app-prolog.sh)
    appret=$(echo $ret | grep -o 'applet-[a-zA-Z0-9]\+' | grep -v 'applet-id')
dx run --priority high $appret -ioutprefix=selected_fields -y --watch

# Table exporter
dx run table-exporter \
    -idataset_or_cohort_or_dashboard=app64984_20250411144839.dataset \
    -ifield_names_file_txt=/tmp/selected_fields.csv \
    -ientity=participant \
    -icoding_option=RAW \
    -ioutput=raw_extract \
    --destination tmp/ --priority high -y --watch

# Munge the raw_extract.csv file to run Alz Dis by proxy algo. Modified from the notebook
# to accomodate the software envir available on "dx app" vs "dx sparkjupyter"
    ret=$($ROOT_INSTALL/prerequisites/build-ns-app-getadproxy.sh)
    appret=$(echo $ret | grep -o 'applet-[a-zA-Z0-9]\+' | grep -v 'applet-id')
dx run --priority high $appret -itabexport_with_icd=/tmp/raw_extract.csv -y --watch

# Step2 
#######

#To perform the liftover on bed, bim, fam files from Genotype calls folder. The input.json file is generated via the sh file generate_input_json that can be find in the folder /prerequisites/

    ret=$(java -jar ~/bin/dxCompiler.jar compile $ROOT_INSTALL/prerequisites/liftover_plink_beds.wdl --project project-Gxv2Xz0J01k1gpZV8FgPF6pq --destination /tmp/)
    appret=$(echo $ret | grep -o 'workflow-[a-zA-Z0-9]\+' | grep -v 'workflow-id')

dx run --priority high $appret -f $ROOT_INSTALL/prerequisites/input.json --brief -y --watch --destination /tmp/ 

# Step3 
#######

#To perform the quality control step on both array genotype data and WES data
# For array genotype data
dx run app-swiss-army-knife  \
    -iin="/tmp/ukb_c1-22_hg38_merged.bim" \
    -iin="/tmp/ukb_c1-22_hg38_merged.bed" \
    -iin="/tmp/ukb_c1-22_hg38_merged.fam" \
    -icmd="plink2 --bfile ukb_c1-22_hg38_merged --out final_array_snps_CRCh38_qc_pass --mac 100 --maf 0.01 --hwe 1e-15 --mind 0.1 --geno 0.1 --write-snplist --write-samples --no-id-header --threads $(nproc)" \
    --destination /tmp/ --priority high -y --watch


# For WES data
java -jar ~/bin/dxCompiler.jar compile $ROOT_INSTALL/prerequisites/bgens_qc.wdl -project project-Gxv2Xz0J01k1gpZV8FgPF6pq -inputs $ROOT_INSTALL/prerequisites/bgens_qc_input.json -archive -folder '/tmp/'
dx run /tmp/bgens_qc -f $ROOT_INSTALL/prerequisites/bgens_qc_input.json --destination /tmp/

# Step4 
#######