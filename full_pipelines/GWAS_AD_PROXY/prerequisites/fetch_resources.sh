#!/bin/env bash

echo "fetch_resources.sh will fetch files of interert for the treatments,"
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

    wget -o $installdir/liftover_plink_beds.wdl https://github.com/dnanexus-rnd/liftover_plink_beds/blob/main/liftover_plink_beds.wdl
    echo -e "\e[32mliftover WDL pipeline fetched.\e[0m"
}


genome_install() {

    echo -e "\e[32mgenome fetched (ready for dx upload).\e[0m"
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


#### Installing cmd
geno_install
liftover_wdl_install $installdir