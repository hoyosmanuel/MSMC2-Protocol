Calculate heterozygosity
========================

1) Generate VCF files for heterozygosity estimation using a ``bcftools mpileup``
---------------------------------------------------------------------------------

.. note::

   At this stage, the dataset includes intergenic regions previously intersected with the mappability mask (mask_1), which were used as putatively neutral regions. The karyotypes of the study species are known, and sex-linked scaffolds were identified in a previous step (X markers). Because MSMC assumes approximately homogeneous recombination and diploid Mendelian inheritance, scaffolds corresponding to the X chromosome were excluded from the main analysis. The scaffold number does not necessarily correspond 1:1 with chromosome number in genome assemblies produce with PACBIO, as assemblies may remain fragmented. Therefore, the following scaffold selection was guided by both karyotype information and prior identification of sex-linked regions.

.. note::

   For clarity, the following code is presented "step by step". However, it is more efficient to run it as an array job; it is broken down here so you can better understand the underlying logic, since using an array may make it harder to follow what is happening. This step is critical and requires careful attention. The `bcftools mpileup` command converts BAM alignments into VCF format.

   The analysis is restricted to:
   - The putative autosomal scaffolds (`-r`)
   - The neutral callable regions in mask_1 (`-R`)
   - Estas options="-B -q 20 -Q 20 -C 50" se refieren a calidad así de una vez vamos a estar purgando posisiciones de mala calidad

.. code-block:: bash

   nano VCF2.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=VCF2
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64

   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador 

   BAM894="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23695894.sorted.bam"
   BAM893="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23695893.sorted.bam"
   BAM930="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23683930.sorted.bam"

   BAM789="/lustre/scratch/mhoyosro/project1/MSMC2/mMol/SRR11747789.sorted.bam"
   BAM790="/lustre/scratch/mhoyosro/project1/MSMC2/mMol/SRR11747790.sorted.bam"
   BAM792="/lustre/scratch/mhoyosro/project1/MSMC2/mMol/SRR11747792.sorted.bam"

   BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
   BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"
   BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"
   BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
   BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"
   BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"

   BAM443="/lustre/scratch/mhoyosro/project1/MSMC2/pDis/SRR11788443.sorted.bam"
   BAM055="/lustre/scratch/mhoyosro/project1/MSMC2/pDis/SRR25743055.sorted.bam"
   BAM067="/lustre/scratch/mhoyosro/project1/MSMC2/pDis/SRR25743067.sorted.bam"
   BAM100="/lustre/scratch/mhoyosro/project1/MSMC2/pDis/SRR25743100.sorted.bam"
   BAM112="/lustre/scratch/mhoyosro/project1/MSMC2/pDis/SRR25743112.sorted.bam"

   BAM706="/lustre/scratch/mhoyosro/project1/MSMC2/pKuh/SRR11744706.sorted.bam"
   BAM991="/lustre/scratch/mhoyosro/project1/MSMC2/pKuh/SRR11744991.sorted.bam"
   BAM992="/lustre/scratch/mhoyosro/project1/MSMC2/pKuh/SRR11744992.sorted.bam"

   BAM490="/lustre/scratch/mhoyosro/project1/MSMC2/rFer/SRR11776490.sorted.bam"
   BAM081="/lustre/scratch/mhoyosro/project1/MSMC2/rFer/SRR11777081.sorted.bam"
   BAM794="/lustre/scratch/mhoyosro/project1/MSMC2/rFer/SRR30056794.sorted.bam"
   BAM361="/lustre/scratch/mhoyosro/project1/MSMC2/rFer/SRR924361.sorted.bam"

   BAM195="/lustre/scratch/mhoyosro/project1/MSMC2/rAeg/SRR11773195.sorted.bam"
   BAM636="/lustre/scratch/mhoyosro/project1/MSMC2/rAeg/SRR11773636.sorted.bam"
   BAM819="/lustre/scratch/mhoyosro/project1/MSMC2/rAeg/SRR7637819.sorted.bam"

   ref_1="/lustre/scratch/mhoyosro/project1/GENOMES/mHipLar1.2.pri.fa"
   ref_2="/lustre/scratch/mhoyosro/project1/GENOMES/mMolMol1.2.pri.fa"
   ref_3="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"
   ref_4="/lustre/scratch/mhoyosro/project1/GENOMES/mPhyDis1.3.pri.fa"
   ref_5="/lustre/scratch/mhoyosro/project1/GENOMES/mPipKuh1.2.pri.fa"
   ref_6="/lustre/scratch/mhoyosro/project1/GENOMES/mRhiFer1.5.pri.fa"
   ref_7="/lustre/scratch/mhoyosro/project1/GENOMES/mRouAeg1.4.pri.fa"

   maks_1="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/combined_neutral.bed"
   maks_2="/lustre/scratch/mhoyosro/project1/MSMC2/mMol/combined_neutral.bed"
   maks_3="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/combined_neutral.bed"
   maks_4="/lustre/scratch/mhoyosro/project1/MSMC2/pDis/combined_neutral.bed"
   maks_5="/lustre/scratch/mhoyosro/project1/MSMC2/pKuh/combined_neutral.bed"
   maks_6="/lustre/scratch/mhoyosro/project1/MSMC2/rFer/combined_neutral.bed"
   maks_7="/lustre/scratch/mhoyosro/project1/MSMC2/rAeg/combined_neutral.bed"

   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"

   # List of values of the argument -r
   regions1=("manual_scaffold_1" "manual_scaffold_2" "manual_scaffold_3" "manual_scaffold_4" "manual_scaffold_5" "manual_scaffold_6" "manual_scaffold_7" "manual_scaffold_8" "manual_scaffold_9" "manual_scaffold_10" "manual_scaffold_11" "manual_scaffold_12" "manual_scaffold_13" "manual_scaffold_15" "manual_scaffold_16")

   regions2=("scaffold_m16_p_3" "scaffold_m16_p_4" "scaffold_m16_p_5" "scaffold_m16_p_6" "scaffold_m16_p_7" "scaffold_m16_p_8" "scaffold_m16_p_9" "scaffold_m16_p_10" "scaffold_m16_p_11" "scaffold_m16_p_12" "scaffold_m16_p_13" "scaffold_m16_p_14" "scaffold_m16_p_15" "scaffold_m16_p_16" "scaffold_m16_p_17" "scaffold_m16_p_18" "scaffold_m16_p_19" "scaffold_m16_p_20" "scaffold_m16_p_21" "scaffold_m16_p_22" "scaffold_m16_p_23" "scaffold_m16_p_24")

   regions3=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")

   regions4=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_4" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15")

   regions5=("scaffold_m20_p_1" "scaffold_m20_p_2" "scaffold_m20_p_3" "scaffold_m20_p_4" "scaffold_m20_p_5" "scaffold_m20_p_6" "scaffold_m20_p_7" "scaffold_m20_p_8" "scaffold_m20_p_9" "scaffold_m20_p_10" "scaffold_m20_p_11" "scaffold_m20_p_12" "scaffold_m20_p_13" "scaffold_m20_p_14" "scaffold_m20_p_15" "scaffold_m20_p_17" "scaffold_m20_p_18" "scaffold_m20_p_19" "scaffold_m20_p_20" "scaffold_m20_p_21")

   regions6=("scaffold_m13_p_1" "scaffold_m13_p_2" "scaffold_m13_p_3" "scaffold_m13_p_4" "scaffold_m13_p_5" "scaffold_m13_p_6" "scaffold_m13_p_7" "scaffold_m13_p_8" "scaffold_m13_p_10" "scaffold_m13_p_11" "scaffold_m13_p_12" "scaffold_m13_p_13" "scaffold_m13_p_14" "scaffold_m13_p_15" "scaffold_m13_p_16" "scaffold_m13_p_17")

   regions7=("scaffold_m29_p_1" "scaffold_m29_p_2" "scaffold_m29_p_3" "scaffold_m29_p_4" "scaffold_m29_p_5" "scaffold_m29_p_6" "scaffold_m29_p_7" "scaffold_m29_p_8" "scaffold_m29_p_9" "scaffold_m29_p_10" "scaffold_m29_p_11" "scaffold_m29_p_12" "scaffold_m29_p_13" "scaffold_m29_p_14" "scaffold_m29_p_15" "scaffold_m29_p_16" "scaffold_m29_p_17" "scaffold_m29_p_18" "scaffold_m29_p_19" "scaffold_m29_p_20" "scaffold_m29_p_21" "scaffold_m29_p_22" "scaffold_m29_p_23" "scaffold_m29_p_24" "scaffold_m29_p_25" "scaffold_m29_p_26" "scaffold_m29_p_27" "scaffold_m29_p_28")

   cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions1 -f $ref_1 -R $maks_1 $BAM894 -O v -o  894_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions1 -f $ref_1 -R $maks_1 $BAM893 -O v -o  893_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions1 -f $ref_1 -R $maks_1 $BAM930 -O v -o  930_pileup_masked.vcf

   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions2 -f $ref_2 -R $maks_2 $BAM789 -O v -o  789_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions2 -f $ref_2 -R $maks_2 $BAM790 -O v -o  790_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions2 -f $ref_2 -R $maks_2 $BAM792 -O v -o  792_pileup_masked.vcf

   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions3 -f $ref_3 -R $maks_3 $BAM039 -O v -o  039_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions3 -f $ref_3 -R $maks_3 $BAM040 -O v -o  040_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions3 -f $ref_3 -R $maks_3 $BAM041 -O v -o  041_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions3 -f $ref_3 -R $maks_3 $BAM487 -O v -o  487_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions3 -f $ref_3 -R $maks_3 $BAM488 -O v -o  488_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions3 -f $ref_3 -R $maks_3 $BAM489 -O v -o  489_pileup_masked.vcf

   cd /lustre/scratch/mhoyosro/project1/MSMC2/pDis
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions4 -f $ref_4 -R $maks_4 $BAM443 -O v -o  443_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions4 -f $ref_4 -R $maks_4 $BAM055 -O v -o  055_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions4 -f $ref_4 -R $maks_4 $BAM067 -O v -o  067_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions4 -f $ref_4 -R $maks_4 $BAM100 -O v -o  100_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions4 -f $ref_4 -R $maks_4 $BAM112 -O v -o  112_pileup_masked.vcf

   cd /lustre/scratch/mhoyosro/project1/MSMC2/pKuh
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions5 -f $ref_5 -R $maks_5 $BAM706 -O v -o  706_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions5 -f $ref_5 -R $maks_5 $BAM991 -O v -o  991_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions5 -f $ref_5 -R $maks_5 $BAM992 -O v -o  992_pileup_masked.vcf

   cd /lustre/scratch/mhoyosro/project1/MSMC2/rFer
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions6 -f $ref_6 -R $maks_6 $BAM490 -O v -o  490_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions6 -f $ref_6 -R $maks_6 $BAM081 -O v -o  081_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions6 -f $ref_6 -R $maks_6 $BAM794 -O v -o  794_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions6 -f $ref_6 -R $maks_6 $BAM361 -O v -o  361_pileup_masked.vcf

   cd /lustre/scratch/mhoyosro/project1/MSMC2/rAeg
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions7 -f $ref_7 -R $maks_7 $BAM195 -O v -o  195_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions7 -f $ref_7 -R $maks_7 $BAM636 -O v -o  636_pileup_masked.vcf
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $regions7 -f $ref_7 -R $maks_7 $BAM819 -O v -o  819_pileup_masked.vcf



2) Calculate Heterozygosity of the positive samples
----------------------------------------------------------

.. note::

   In the previous implementation, scaffold restriction using the `-r` argument was not correctly applied, leading to the inclusion of unintended scaffolds in the output VCF. To resolve this, an additional filtering step is introduced to restrict the analysis to the predefined set of autosomal scaffolds by applying the command `grep`.

A) *Hipposideros larvatus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

**for 894_pileup_masked.vcf:**

.. code-block:: bash

   # The first command counts sites with an alternative allele different from `<*>`
   # The second command counts all evaluated sites in the retained autosomal scaffolds. 
   grep -E '^manual_scaffold_(1[0-3]|15|16|[1-9])\b' 894_pileup_H.vcf \
     | awk -F'\t' '$5 != "<*>"' \
     | wc -l
   grep -E '^manual_scaffold_(1[0-3]|15|16|[1-9])\b' 894_pileup_masked.vcf \
     | wc -l

| *RESULT:*
| Number of variable sites: 4,486,890  
| Total evaluated sites: 847,505,239
| *Estimated heterozygosity:*
| H = 4,486,890 / 847,505,239 = **0.00529423275**

**for 893_pileup_masked.vcf:**

.. code-block:: bash

   grep -E '^manual_scaffold_(1[0-3]|15|16|[1-9])\b' 893_pileup_masked.vcf \
     | awk -F'\t' '$5 != "<*>"' \
     | wc -l
   grep -E '^manual_scaffold_(1[0-3]|15|16|[1-9])\b' 893_pileup_masked.vcf \
     | wc -l

| *RESULT:*
| Number of variable sites: 4,009,791 
| Total evaluated sites: 846,087,679
| *Estimated heterozygosity:*
| H = 4,009,791 / 846,087,679 = **0.0047392145**

**for 930_pileup_masked.vcf:**

.. code-block:: bash

   grep -E '^manual_scaffold_(1[0-3]|15|16|[1-9])\b' 930_pileup_masked.vcf \
     | awk -F'\t' '$5 != "<*>"' \
     | wc -l

   grep -E '^manual_scaffold_(1[0-3]|15|16|[1-9])\b' 930_pileup_masked.vcf \
     | wc -l

| *RESULT:*
| Number of variable sites: 1,182,931
| Total evaluated sites: 846,087,679
| *Estimated heterozygosity:*
| H = 4,009,791 / 846,087,679 = **0.0047392145**

B) *Molossus molossus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

**for 789_pileup_masked.vcf:**

.. code-block:: bash

   grep -E '^scaffold_m16_p_([3-9]|1[0-9]|2[0-4])\b' 789_pileup_masked.vcf \
     | awk -F'\t' '$5 != "<*>"' \
     | wc -l
   
   grep -E '^scaffold_m16_p_([3-9]|1[0-9]|2[0-4])\b' 789_pileup_masked.vcf \
     | wc -l

| *RESULT:*
| Number of variable sites: 8,719,790
| Total evaluated sites: 667,039,993
| *Estimated heterozygosity:*
| H = 8,719,790 / 667,039,993 = **0.01307236461**

**for 790_pileup_masked.vcf:**

.. code-block:: bash

   grep -E '^scaffold_m16_p_([3-9]|1[0-9]|2[0-4])\b' 790_pileup_masked.vcf \
     | awk -F'\t' '$5 != "<*>"' \
     | wc -l
   
   grep -E '^scaffold_m16_p_([3-9]|1[0-9]|2[0-4])\b' 790_pileup_masked.vcf \
     | wc -l

| *RESULT:*
| Number of variable sites: 18,232,438
| Total evaluated sites: 736,604,893
| *Estimated heterozygosity:*
| H = 18,232,438 / 736,604,893 = **0.02475199143**

**for 792_pileup_masked.vcf:**

.. code-block:: bash

   grep -E '^scaffold_m16_p_([3-9]|1[0-9]|2[0-4])\b' 792_pileup_masked.vcf \
     | awk -F'\t' '$5 != "<*>"' \
     | wc -l
   
   grep -E '^scaffold_m16_p_([3-9]|1[0-9]|2[0-4])\b' 792_pileup_masked.vcf \
     | wc -l

| *RESULT:*
| Number of variable sites: 00,000,000
| Total evaluated sites: 000,000,000
| *Estimated heterozygosity:*
| H = 00,000,000 / 000,000,000 = **0.000000000**

C) *Myotis myotis*
~~~~~~~~~~~~~~~~~~~~~~~~~~

**for 487_pileup_masked.vcf:**

.. code-block:: bash
   
   grep -E '^scaffold_m19_p_(1[0-9]|2[0-1]|[1-3]|[5-9])\b' 487_pileup_masked.vcf \
     | awk -F'\t' '$5 != "<*>"' \
     | wc -l
   
   grep -E '^scaffold_m19_p_(1[0-9]|2[0-1]|[1-3]|[5-9])\b' 487_pileup_masked.vcf \
     | wc -l

| *RESULT:*
| Number of variable sites: 5,668,299
| Total evaluated sites: 679,334,581
| *Estimated heterozygosity:*
| H = 5,668,299 / 679,334,581 = **0.0083438988**

**for 488_pileup_masked.vcf:**

.. code-block:: bash
   
   grep -E '^scaffold_m19_p_(1[0-9]|2[0-1]|[1-3]|[5-9])\b' 488_pileup_masked.vcf \
     | awk -F'\t' '$5 != "<*>"' \
     | wc -l
   
   grep -E '^scaffold_m19_p_(1[0-9]|2[0-1]|[1-3]|[5-9])\b' 488_pileup_masked.vcf \
     | wc -l

| *RESULT:*
| Number of variable sites: 7,867,343
| Total evaluated sites: 680,229,630
| *Estimated heterozygosity:*
| H = 7,867,343 / 680,229,630 = **0.01156571641**

**for 489_pileup_masked.vcf:**

.. code-block:: bash
   
   grep -E '^scaffold_m19_p_(1[0-9]|2[0-1]|[1-3]|[5-9])\b' 489_pileup_masked.vcf \
     | awk -F'\t' '$5 != "<*>"' \
     | wc -l
   
   grep -E '^scaffold_m19_p_(1[0-9]|2[0-1]|[1-3]|[5-9])\b' 489_pileup_masked.vcf \
     | wc -l

| *RESULT:*
| Number of variable sites: 9,041,822
| Total evaluated sites: 681,186,892
| *Estimated heterozygosity:*
| H = 9,041,822 / 681,186,892 = **0.01327362887**



D) *Phyllostomus discolor*
~~~~~~~~~~~~~~~~~~~~~~~~~~

E) *Pipistrellus kuhlii*
~~~~~~~~~~~~~~~~~~~~~~~~~~

F) *Rhinolophus ferrumequinum*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

G) *Rousettus aegyptiacus*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Rhoads A, Au KF. PacBio Sequencing and Its Applications. Genomics Proteomics Bioinformatics. 2015 Oct;13(5):278-89. doi: 10.1016/j.gpb.2015.08.002. Epub 2015 Nov 2. PMID: 26542840; PMCID: PMC4678779.

https://en.wikipedia.org/wiki/Variant_Call_Format
