#Générer les inputs dans un fichier json pour lancer l'app regenie

import json

# Chemins des fichiers génomiques principaux
bed = "/tmp/ukb_c1-22_hg38_merged.bed"
bim = "/tmp/ukb_c1-22_hg38_merged.bim"
fam = "/tmp/ukb_c1-22_hg38_merged.fam"

# Fonction pour générer les chemins triés
def sorted_paths(prefix, ext, n=22):
    return [f"{prefix}_c{chrom}_b0_v1.{ext}" for chrom in range(1, n + 1)]

# Générer les listes triées
bgen_paths = sorted_paths("/Bulk/Exome sequences/Population level exome OQFE variants, BGEN format - final release/ukb23159", "bgen")
bgi_paths = sorted_paths("/Bulk/Exome sequences/Population level exome OQFE variants, BGEN format - final release/ukb23159", "bgen.bgi")
sample_paths = sorted_paths("/Bulk/Exome sequences/Population level exome OQFE variants, BGEN format - final release/ukb23159", "sample")

# Autres fichiers d'entrée
pheno_txt = "/tmp/ad_by_proxy_GWAS_500K/ad_risk_by_proxy_wes.phe"
step1_snps = "/tmp/final_array_snps_CRCh38_qc_pass.snplist"
step2_snps = "/tmp/gel_impute_data_snps_qc_pass.snplist"
covar_txt = pheno_txt

# Construction du dictionnaire d'inputs
inputs = {
    "wgr_genotype_bed": bed,
    "wgr_genotype_bim": bim,
    "wgr_genotype_fam": fam,
    "genotype_bgens": bgen_paths,
    "genotype_bgis": bgi_paths,
    "genotype_samples": sample_paths,
    "pheno_txt": pheno_txt,
    "step1_extract_txts": step1_snps,
    "step2_extract_txts": step2_snps,
    "step1_ref_first": True,
    "covar_txt": covar_txt,
    "quant_traits": False,
    "step1_block_size": 1000,
    "step2_block_size": 200,
    "pheno_names": "ad_by_proxy",
    "use_firth_approx": True,
    "min_mac": 3,
    "covar_names": "age,sex,pc1,pc2,pc3,pc4,pc5,pc6,pc7,pc8,pc9,pc10"
}

# Sauvegarde dans un fichier
with open("regenie_input.json", "w") as f:
    json.dump(inputs, f, indent=2)