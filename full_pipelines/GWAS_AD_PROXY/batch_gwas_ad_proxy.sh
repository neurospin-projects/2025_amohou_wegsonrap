#!/bin/bash
# Script colleting all "dx run" commands to be run from a dx-toolkit local shell.

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