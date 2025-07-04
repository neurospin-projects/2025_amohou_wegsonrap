#!/bin/bash
# Script colleting all "dx" commands to be run from a dx-toolkit local shell.

set -euo pipefail 
echo "generate_input_json.sh will create the input.json for dx run,"
echo "using DNAnexus paths (RAP) and resolving them to file-IDs."

#### Définition du fichier de sortie
output_file="./input.json"
echo "Generating $output_file in current directory: $(pwd)"

dx upload hg38.fa --destination /tmp/
dx upload b37ToHg38.over.chain --destination /tmp/

#  Liste des fichiers avec leur clé JSON et chemin DNAnexus 
declare -A single_files=(
  ["stage-common.reference_fastagz"]="/tmp/hg38.fa"
  ["stage-common.ucsc_chain"]="/tmp/b37ToHg38.over.chain"
)

#  Listes de fichiers (ex: plink_beds, bims, fams) 
declare -A plink_paths=(
  ["stage-common.plink_beds"]="
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c1_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c2_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c3_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c4_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c5_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c6_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c7_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c8_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c9_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c10_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c11_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c12_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c13_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c14_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c15_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c16_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c17_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c18_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c19_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c20_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c21_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c22_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cMT_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cX_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cXY_b0_v2.bed\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cY_b0_v2.bed\"
"
  ["stage-common.plink_bims"]="
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c1_b0_v2.bim\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c2_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c3_b0_v2.bim\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c4_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c5_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c6_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c7_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c8_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c9_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c10_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c11_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c12_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c13_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c14_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c15_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c16_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c17_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c18_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c19_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c20_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c21_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c22_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cMT_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cX_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cXY_b0_v2.bim\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cY_b0_v2.bim\"
" 
  ["stage-common.plink_fams"]="
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c1_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c2_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c3_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c4_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c5_b0_v2.fam\"
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c6_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c7_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c8_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c9_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c10_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c11_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c12_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c13_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c14_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c15_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c16_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c17_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c18_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c19_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c20_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c21_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_c22_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cMT_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cX_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cXY_b0_v2.fam\" 
\"/Bulk/Genotype Results/Genotype calls/ukb22418_cY_b0_v2.fam\"
"
)

#### Construction du JSON
echo "{" > "$output_file"

#  Fichiers multiples 
for key in "${!plink_paths[@]}"; do
  echo "  \"$key\": [" >> "$output_file"
  # Utilise un here-string et `while read` pour lire chaque chemin ligne par ligne.
  while IFS= read -r path; do
    # Supprime les guillemets externes s'ils ont été ajoutés pour la déclaration
    path=$(echo "$path" | tr -d '"' | xargs echo -n) # xargs -n pour nettoyer les espaces
    
    # Vérifie si le chemin n'est pas vide (pour éviter les lignes vides de la déclaration)
    if [[ -n "$path" ]]; then
      file_id=$(dx describe "$path" --json | jq -r '.id')
      echo "    {\"\$dnanexus_link\": \"$file_id\"}," >> "$output_file"
    fi
  done <<< "${plink_paths[$key]}"
  sed -i '$ s/,$//' "$output_file"  # retirer la dernière virgule de la liste
  echo "  ]," >> "$output_file"
done

#  Fichiers simples 
for key in "${!single_files[@]}"; do
  dx_path="${single_files[$key]}"
  file_id=$(dx describe "$dx_path" --json | jq -r '.id')
  echo "  \"$key\": {\"\$dnanexus_link\": \"$file_id\"}," >> "$output_file"
done

#  Ajouter la valeur textuelle finale 
echo "  \"stage-common.split_par_build_code\": \"hg38\"" >> "$output_file"
echo "}" >> "$output_file"

echo -e "\e[32m input.json généré avec succès dans $output_file\e[0m"