.. note::

 MSMC methods assume homogeneous recombination and diploid Mendelian inheritance (Mather et al., 2019). Therefore, excluding sex chromosomes (or sex-linked loci located on autosomes) from the main analysis is advisable. Here, we removed these regions prior to analysis. Alternative and potentially more robust approaches may exist; however, the following describes the procedure used in this study.



Detect sex chromosomes
======================

1. Create a directory with the sexual markers
----------------------------------------------

.. code-block:: bash

 mkdir /lustre/scratch/mhoyosro/project1/SEX_MARKERS

 #Activate Blast
 . /home/mhoyosro/conda/etc/profile.d/conda.sh
 conda activate blast

 #Create the DataBases

 cd /lustre/scratch/mhoyosro/project1/SEX_MARKERS
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mHipLar1.2.pri.fa -dbtype nucl -out hLar_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mMolMol1.2.pri.fa -dbtype nucl -out mMol_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa -dbtype nucl -out mMyo_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mPhyDis1.3.pri.fa -dbtype nucl -out pDis_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mPipKuh1.2.pri.fa -dbtype nucl -out pKuh_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mRhiFer1.5.pri.fa -dbtype nucl -out rFer_DB
 makeblastdb -in /lustre/scratch/mhoyosro/project1/GENOMES/mRouAeg1.4.pri.fa -dbtype nucl -out rAeg_DB

#Look for the KDM5C first 
blastn -query KDM5C_gene.fa -db hLar_DB -out hLar_res_KDM5C.txt -outfmt 6
blastn -query KDM5C_gene.fa -db mMol_DB -out mMol_res_KDM5C.txt -outfmt 6
blastn -query KDM5C_gene.fa -db mMyo_DB -out mMyo_res_KDM5C.txt -outfmt 6
blastn -query KDM5C_gene.fa -db pDis_DB -out pDis_res_KDM5C.txt -outfmt 6
blastn -query KDM5C_gene.fa -db pKuh_DB -out pKuh_res_KDM5C.txt -outfmt 6
blastn -query KDM5C_gene.fa -db rFer_DB -out rFer_res_KDM5C.txt -outfmt 6
blastn -query KDM5C_gene.fa -db rAeg_DB -out rAeg_res_KDM5C.txt -outfmt 6

#Look for the ZFX 
blastn -query ZFX_gene.fa -db hLar_DB -out hLar_res_ZFX.txt -outfmt 6
blastn -query ZFX_gene.fa -db mMol_DB -out mMol_res_ZFX.txt -outfmt 6
blastn -query ZFX_gene.fa -db mMyo_DB -out mMyo_res_ZFX.txt -outfmt 6
blastn -query ZFX_gene.fa -db pDis_DB -out pDis_res_ZFX.txt -outfmt 6
blastn -query ZFX_gene.fa -db pKuh_DB -out pKuh_res_ZFX.txt -outfmt 6
blastn -query ZFX_gene.fa -db rFer_DB -out rFer_res_ZFX.txt -outfmt 6
blastn -query ZFX_gene.fa -db rAeg_DB -out rAeg_res_ZFX.txt -outfmt 6

#Look for the SRY
blastn -query SRY_gene.fa -db hLar_DB -out hLar_res_SRY.txt -outfmt 6
blastn -query SRY_gene.fa -db mMol_DB -out mMol_res_SRY.txt -outfmt 6
blastn -query SRY_gene.fa -db mMyo_DB -out mMyo_res_SRY.txt -outfmt 6
blastn -query SRY_gene.fa -db pDis_DB -out pDis_res_SRY.txt -outfmt 6
blastn -query SRY_gene.fa -db pKuh_DB -out pKuh_res_SRY.txt -outfmt 6
blastn -query SRY_gene.fa -db rFer_DB -out rFer_res_SRY.txt -outfmt 6
blastn -query SRY_gene.fa -db rAeg_DB -out rAeg_res_SRY.txt -outfmt 6


#Look for the X 
blastn -query pKuhRNA-binding_motif_protein_X_Chrm.fa -db pKuh_DB -out pKuh_res_X_prot.txt -outfmt 6


nano blstr2.sh

#!/bin/bash
#SBATCH --job-name=blstr2
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=1
cd /lustre/scratch/mhoyosro/project1/SEX_MARKERS

. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate blast


blastn -query pKuh_randomX.fa -db pKuh_DB -out pKuh_random1_X_prot.txt -outfmt 6


nano mapX.sh
#!/bin/bash
#SBATCH --job-name=mapping
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

cd /lustre/scratch/mhoyosro/project1/SEX_MARKERS
ROOT=/lustre/scratch/mhoyosro/project1/GENOMES

bwa aln -t 64 $ROOT/mPipKuh1.2.pri.fa pKuh_random1_X_prot.fa > pKuh_random1_X_prot.sai && 
BWA_THREAD=64 bwa samse $ROOT/mPipKuh1.2.pri.fa pKuh_random1_X_prot.sai pKuh_random1_X_prot.fa  > pKuh_random1_X_prot.sam









cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
#2n = 32 => 14 Autosomas + X Y
#Chromosome X = manual_scaffold_14 

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
#2n = 48 => 22 Autosomas + X Y
#Chromosome X = scaffold_m16_p_2 & scaffold_m16_p_1

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
#2n = 44 => 20 Autosomas + X Y
#Chromosome X = scaffold_m19_p_4

cd /lustre/scratch/mhoyosro/project1/MSMC2/pDis
#2n = 32 => 14 Autosomas + X Y
#Chromosome X = scaffold_m19_p_9 (Usando el alineamiento del cromosoma X)

cd /lustre/scratch/mhoyosro/project1/MSMC2/pKuh
#2n = 44 => 20 Autosomas + X Y
#Chromosome X = ???  Voy a decir que es el 16 de acuerdo a ZFX

cd /lustre/scratch/mhoyosro/project1/MSMC2/rFer
#2n = 58 => 27 Autosomas + X Y
#Chromosome X = scaffold_m29_p_1 (confirmado con el alineamiento del cromosoma X)

cd /lustre/scratch/mhoyosro/project1/MSMC2/rAeg
#2n = 36 => 16 Autosomas + X Y
#Chromosome X = scaffold_m13_p_9 (confirmado con el alineamiento del cromosoma X)

