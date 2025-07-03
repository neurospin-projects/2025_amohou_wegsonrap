#!/bin/env bash

echo "fetch_resources.sh will fetch files of interest for the treatments,"
echo "as well as WDL code (clone github directory)."

# file=""
# output=""

# # Parse options
# while getopts "f:o:" opt; do
#   case $opt in
#     f) file="$OPTARG" ;;
#     o) output="$OPTARG" ;;
#     \?) echo "Usage: $0 -f <file> [-o <output>]"; exit 1 ;;
#   esac
# done

# # Print parsed values
# echo "File: $file"
# echo "Output: $output"


liftover_wdl_install() {

    wget -o $installdir/liftover_plink_beds.wdl https://github.com/dnanexus-rnd/liftover_plink_beds/raw/refs/heads/main/liftover_plink_beds.wdl
    echo -e "\e[32mliftover WDL pipeline fetched.\e[0m"
}

reference_fastagz_install() {

    wget -o $installdir/hg38.fa.gz https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
    gunzip -f hg38.fa.gz
    echo -e "\e[32mreference_fastagz fetched and uncompressed.\e[0m"
}

ucsc_chain_install() {

    wget -o $installdir/b37ToHg38.over.chain https://raw.githubusercontent.com/broadinstitute/gatk/master/scripts/funcotator/data_sources/gnomAD/b37ToHg38.over.chain
    echo -e "\e[32mucsc_chain fetched.\e[0m"
}

bgens_qc_install() {

    wget -o $installdir/bgens_qc.wdl https://github.com/dnanexus/UKB_RAP/raw/refs/heads/main/end_to_end_gwas_phewas/bgens_qc/bgens_qc.wdl
    echo -e "\e[32mbgens_qc WDL pipeline fetched.\e[0m"
}

#### Parsing
installdir=""

# Parse options
while getopts "i:" opt; do
  case $opt in
    i) installdir="$OPTARG" ;;
    \?) echo "Usage: $0 -i <installdir>"; exit 1 ;;
  esac
done
# Check if mandatory arguments are provided
if [[ -z "$installdir"  ]]; then
    echo -e "\e[31mError: -i <installdir> is required.\e[0m"
    echo -e "\e[31mUsage: $0 -i <installdir>.\e[0m"
    echo ""
  exit 1
fi
# Print parsed values
echo "Will install the liftover_plink_beds.wdl in : $installdir"
echo "Will install the hg38.fa.gz in : $installdir"
echo "Will install the b37ToHg38.over.chain in : $installdir"
echo "Will install the bgens_qc.wdl in : $installdir"

#### Installing cmd
liftover_wdl_install $installdir
reference_fastagz_install $installdir
ucsc_chain_install $installdir
bgens_qc_install $installdir