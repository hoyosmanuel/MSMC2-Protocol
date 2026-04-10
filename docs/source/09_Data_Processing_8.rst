MPILEUP
=======

.. note::

   This is an additional key step in the workflow. It is independent from the heterozygosity estimation described in the previous step. Both analyses can be performed in parallel however, running both workflows simultaneously may be computationally/mentally demanding particularly when working with a large number of samples and therefore it is not a recommended standard approach. Again, this implementation is presented for transparency, and users may identify more efficient and streamlined alternatives.

   That said, in this step, a new set of VCF files using ``bcftools mpileup`` will be generated. In contrast to the previous analysis, no neutral mask is applied here. Instead, VCF files are generated separately for each scaffold of interest (the scaffolds assumed to represent autosomes). These scaffold-specific VCF files will be used as input for the `multihetsep` step in MSMC2.

   The output of this step will be organized within a directory named `mask_2`, which will contain subdirectories for each sample.

1) Create directories for the workflow
---------------------------------------

The directory structure is as follows.

.. code-block:: bash

   /lustre/scratch/mhoyosro/project1/MSMC2
   │
   ├── hLar
   │   └── mask_2
   │       ├── sample_893
   │       ├── sample_894
   │       └── sample_930
   │
   ├── mMol
   │   └── mask_2
   │       ├── sample_789
   │       ├── sample_790
   │       └── sample_792
   │
   ├── mMyo
   │   └── mask_2
   │       ├── sample_039
   │       ├── sample_040
   │       ├── sample_041
   │       ├── sample_487
   │       ├── sample_488
   │       └── sample_489
   │
   ├── pDis
   │   └── mask_2
   │       ├── sample_055
   │       ├── sample_067
   │       ├── sample_100
   │       ├── sample_112
   │       └── sample_443
   │
   ├── pKuh
   │   └── mask_2
   │       ├── sample_706
   │       ├── sample_991
   │       └── sample_992
   │
   ├── rFer
   │   └── mask_2
   │       ├── sample_081
   │       ├── sample_361
   │       ├── sample_490
   │       └── sample_794
   │
   └── rAeg
       └── mask_2
           ├── sample_195
           ├── sample_636
           └── sample_819
   



2) Create directories for the workflow
--------------------------------------

A) *Hipposideros larvatus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   nano hLar_bamcaller1.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=mpileup1
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("manual_scaffold_1" "manual_scaffold_2" "manual_scaffold_3" "manual_scaffold_4" "manual_scaffold_5" "manual_scaffold_6" "manual_scaffold_7" "manual_scaffold_8" "manual_scaffold_9" "manual_scaffold_10" "manual_scaffold_11" "manual_scaffold_12" "manual_scaffold_13" "manual_scaffold_15" "manual_scaffold_16")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mHipLar1.2.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 894
   DEPTH894=13.293
   # Depth 893
   DEPTH893=10.544
   # Depth 930
   DEPTH930=13.0935
   
   # BAM894
   BAM894="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23695894.sorted.bam"
   # BAM893
   BAM893="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23695893.sorted.bam"  
   # BAM930
   BAM930="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23683930.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM893 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH893 masks2/sample_893/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_893/out.$region.vcf.gz
   done
   
.. code-block:: bash

   nano hLar_bamcaller2.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=mpileup2
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("manual_scaffold_1" "manual_scaffold_2" "manual_scaffold_3" "manual_scaffold_4" "manual_scaffold_5" "manual_scaffold_6" "manual_scaffold_7" "manual_scaffold_8" "manual_scaffold_9" "manual_scaffold_10" "manual_scaffold_11" "manual_scaffold_12" "manual_scaffold_13" "manual_scaffold_15" "manual_scaffold_16")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mHipLar1.2.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 894
   DEPTH894=13.293
   # Depth 893
   DEPTH893=10.544
   # Depth 930
   DEPTH930=13.0935
   
   # BAM894
   BAM894="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23695894.sorted.bam"
   # BAM893
   BAM893="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23695893.sorted.bam"  
   # BAM930
   BAM930="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23683930.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM894 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH894 masks2/sample_894/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_894/out.$region.vcf.gz
   done
 
.. code-block:: bash

   nano hLar_bamcaller3.sh

.. code-block:: bash
   
   #!/bin/bash
   #SBATCH --job-name=mpileup3
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/hLar
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("manual_scaffold_1" "manual_scaffold_2" "manual_scaffold_3" "manual_scaffold_4" "manual_scaffold_5" "manual_scaffold_6" "manual_scaffold_7" "manual_scaffold_8" "manual_scaffold_9" "manual_scaffold_10" "manual_scaffold_11" "manual_scaffold_12" "manual_scaffold_13" "manual_scaffold_15" "manual_scaffold_16")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mHipLar1.2.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 894
   DEPTH894=13.293
   # Depth 893
   DEPTH893=10.544
   # Depth 930
   DEPTH930=13.0935
   
   # BAM894
   BAM894="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23695894.sorted.bam"
   # BAM893
   BAM893="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23695893.sorted.bam"  
   # BAM930
   BAM930="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23683930.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM930 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH930 masks2/sample_930/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_930/out.$region.vcf.gz
   done
   
