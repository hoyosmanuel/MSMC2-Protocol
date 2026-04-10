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
   
   # Depth 893
   DEPTH893=10.544
   
   # BAM893
   BAM893="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23695893.sorted.bam"  
   
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
   
   # BAM894
   BAM894="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23695894.sorted.bam"
   
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

   # Depth 930
   DEPTH930=13.0935

   # BAM930
   BAM930="/lustre/scratch/mhoyosro/project1/MSMC2/hLar/SRR23683930.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM930 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH930 masks2/sample_930/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_930/out.$region.vcf.gz
   done


B) *Molossus molossus*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   nano mMol_bamcaller1.sh

.. code-block:: bash
   
   #!/bin/bash
   #SBATCH --job-name=mpileup4
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m16_p_3" "scaffold_m16_p_4" "scaffold_m16_p_5" "scaffold_m16_p_6" "scaffold_m16_p_7" "scaffold_m16_p_8" "scaffold_m16_p_9" "scaffold_m16_p_10" "scaffold_m16_p_11" "scaffold_m16_p_12" "scaffold_m16_p_13" "scaffold_m16_p_14" "scaffold_m16_p_15" "scaffold_m16_p_16" "scaffold_m16_p_17" "scaffold_m16_p_18" "scaffold_m16_p_19" "scaffold_m16_p_20" "scaffold_m16_p_21" "scaffold_m16_p_22" "scaffold_m16_p_23" "scaffold_m16_p_24" )
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMolMol1.2.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMol/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 789
   DEPTH789=22.418
   
   # BAM789
   BAM789="/lustre/scratch/mhoyosro/project1/MSMC2/mMol/SRR11747789.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM789 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH789 masks2/sample_789/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_789/out.$region.vcf.gz
   done
   
.. code-block:: bash

   nano mMol_bamcaller2.sh

.. code-block:: bash
   
   #!/bin/bash
   #SBATCH --job-name=mpileup5
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m16_p_3" "scaffold_m16_p_4" "scaffold_m16_p_5" "scaffold_m16_p_6" "scaffold_m16_p_7" "scaffold_m16_p_8" "scaffold_m16_p_9" "scaffold_m16_p_10" "scaffold_m16_p_11" "scaffold_m16_p_12" "scaffold_m16_p_13" "scaffold_m16_p_14" "scaffold_m16_p_15" "scaffold_m16_p_16" "scaffold_m16_p_17" "scaffold_m16_p_18" "scaffold_m16_p_19" "scaffold_m16_p_20" "scaffold_m16_p_21" "scaffold_m16_p_22" "scaffold_m16_p_23" "scaffold_m16_p_24" )
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMolMol1.2.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMol/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"

   # Depth 790
   DEPTH790=24.9835

   # BAM790
   BAM790="/lustre/scratch/mhoyosro/project1/MSMC2/mMol/SRR11747790.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM790 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH790 masks2/sample_790/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_790/out.$region.vcf.gz
   done
    
.. code-block:: bash

   nano mMol_bamcaller3.sh

.. code-block:: bash
   
   #!/bin/bash
   #SBATCH --job-name=mpileup6
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMol
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m16_p_3" "scaffold_m16_p_4" "scaffold_m16_p_5" "scaffold_m16_p_6" "scaffold_m16_p_7" "scaffold_m16_p_8" "scaffold_m16_p_9" "scaffold_m16_p_10" "scaffold_m16_p_11" "scaffold_m16_p_12" "scaffold_m16_p_13" "scaffold_m16_p_14" "scaffold_m16_p_15" "scaffold_m16_p_16" "scaffold_m16_p_17" "scaffold_m16_p_18" "scaffold_m16_p_19" "scaffold_m16_p_20" "scaffold_m16_p_21" "scaffold_m16_p_22" "scaffold_m16_p_23" "scaffold_m16_p_24" )
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMolMol1.2.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMol/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"

   # Depth 792
   DEPTH792=41.6384

   # BAM792
   BAM792="/lustre/scratch/mhoyosro/project1/MSMC2/mMol/SRR11747792.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM792 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH792 masks2/sample_792/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_792/out.$region.vcf.gz
   done

C) *Myotis myotis*
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   nano mMyo_bamcaller1.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=mpileup7
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 039
   DEPTH039=4.62979
   
   # BAM039
   BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM039 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH039 masks2/sample_039/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_039/out.$region.vcf.gz
   done

.. code-block:: bash

   nano mMyo_bamcaller2.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=mpileup8
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 039
   DEPTH039=4.62979
   # Depth 040
   DEPTH040=28.6231
   # Depth 041
   DEPTH041=32.4736
   # Depth 487
   DEPTH487=14.5317
   # Depth 488
   DEPTH488=18.5191
   # Depth 489
   DEPTH489=46.3561
   
   # BAM039
   BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
   # BAM040
   BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
   # BAM041
   BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
   # BAM487
   BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
   # BAM488
   BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
   # BAM489
   BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM040 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH040 masks2/sample_040/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_040/out.$region.vcf.gz
   done

.. code-block:: bash

   nano mMyo_bamcaller3.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=mpileup9
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 039
   DEPTH039=4.62979
   # Depth 040
   DEPTH040=28.6231
   # Depth 041
   DEPTH041=32.4736
   # Depth 487
   DEPTH487=14.5317
   # Depth 488
   DEPTH488=18.5191
   # Depth 489
   DEPTH489=46.3561
   
   # BAM039
   BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
   # BAM040
   BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
   # BAM041
   BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
   # BAM487
   BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
   # BAM488
   BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
   # BAM489
   BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM041 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH041 masks2/sample_041/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_041/out.$region.vcf.gz
   done

.. code-block:: bash

   nano mMyo_bamcaller4.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=mpilup10
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 039
   DEPTH039=4.62979
   # Depth 040
   DEPTH040=28.6231
   # Depth 041
   DEPTH041=32.4736
   # Depth 487
   DEPTH487=14.5317
   # Depth 488
   DEPTH488=18.5191
   # Depth 489
   DEPTH489=46.3561
   
   # BAM039
   BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
   # BAM040
   BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
   # BAM041
   BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
   # BAM487
   BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
   # BAM488
   BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
   # BAM489
   BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM487 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH487 masks2/sample_487/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_487/out.$region.vcf.gz
   done

.. code-block:: bash

   nano mMyo_bamcaller5.sh

.. code-block:: bash
   
   #!/bin/bash
   #SBATCH --job-name=mpilup11
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 039
   DEPTH039=4.62979
   # Depth 040
   DEPTH040=28.6231
   # Depth 041
   DEPTH041=32.4736
   # Depth 487
   DEPTH487=14.5317
   # Depth 488
   DEPTH488=18.5191
   # Depth 489
   DEPTH489=46.3561
   
   # BAM039
   BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
   # BAM040
   BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
   # BAM041
   BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
   # BAM487
   BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
   # BAM488
   BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
   # BAM489
   BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  
      
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM488 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH488 masks2/sample_488/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_488/out.$region.vcf.gz
   done

.. code-block:: bash

   nano mMyo_bamcaller6.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=mpilup12
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 039
   DEPTH039=4.62979
   # Depth 040
   DEPTH040=28.6231
   # Depth 041
   DEPTH041=32.4736
   # Depth 487
   DEPTH487=14.5317
   # Depth 488
   DEPTH488=18.5191
   # Depth 489
   DEPTH489=46.3561
   
   # BAM039
   BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
   # BAM040
   BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
   # BAM041
   BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
   # BAM487
   BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
   # BAM488
   BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
   # BAM489
   BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM489 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH489 masks2/sample_489/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_489/out.$region.vcf.gz
   done

=======
REPEART
=======

.. code-block:: bash

   nano mMyo_bamcaller7.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=mpileup7
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 039
   DEPTH039=4.62979
   # Depth 040
   DEPTH040=28.6231
   # Depth 041
   DEPTH041=32.4736
   # Depth 487
   DEPTH487=14.5317
   # Depth 488
   DEPTH488=18.5191
   # Depth 489
   DEPTH489=46.3561
   
   # BAM039
   BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
   # BAM040
   BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
   # BAM041
   BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
   # BAM487
   BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
   # BAM488
   BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
   # BAM489
   BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM039 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH039 masks2/sample_039/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_039/out.$region.vcf.gz
   done
 
.. code-block:: bash

   nano mMyo_bamcaller8.sh

.. code-block:: bash

   #!/bin/bash
   #SBATCH --job-name=mpileup8
   #SBATCH --output=%x.%j.out
   #SBATCH --error=%x.%j.err
   #SBATCH --partition=nocona
   #SBATCH --nodes=1
   #SBATCH --ntasks=64
   
   cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo
   
   . /home/mhoyosro/conda/etc/profile.d/conda.sh
   conda activate alineador
   
   # List of values of the argument -r
   regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")
   
   # Route to the reference file
   reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"
   
   # Bamcaller
   TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"
   
   # Options for samtools mpileup
   options="-B -q 20 -Q 20 -C 50"
   
   # Depth 039
   DEPTH039=4.62979
   # Depth 040
   DEPTH040=28.6231
   # Depth 041
   DEPTH041=32.4736
   # Depth 487
   DEPTH487=14.5317
   # Depth 488
   DEPTH488=18.5191
   # Depth 489
   DEPTH489=46.3561
   
   # BAM039
   BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
   # BAM040
   BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
   # BAM041
   BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
   # BAM487
   BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
   # BAM488
   BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
   # BAM489
   BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  
   
   for region in "${regions[@]}"; do
   OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM040 | \
   OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
   OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
   python $TOOL $DEPTH040 masks2/sample_040/$region.mask.bed.gz                  | \
   gzip -c  >  output_sample_040/out.$region.vcf.gz
   done


nano bamcaller9.sh

#!/bin/bash
#SBATCH --job-name=mpileup9
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo

. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate alineador

# List of values of the argument -r
regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")

# Route to the reference file
reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"

# Bamcaller
TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"


# Options for samtools mpileup
options="-B -q 20 -Q 20 -C 50"

# Depth 039
DEPTH039=4.62979
# Depth 040
DEPTH040=28.6231
# Depth 041
DEPTH041=32.4736
# Depth 487
DEPTH487=14.5317
# Depth 488
DEPTH488=18.5191
# Depth 489
DEPTH489=46.3561



# BAM039
BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
# BAM040
BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
# BAM041
BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
# BAM487
BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
# BAM488
BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
# BAM489
BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  



for region in "${regions[@]}"; do
OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM041 | \
OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
python $TOOL $DEPTH041 masks2/sample_041/$region.mask.bed.gz                  | \
gzip -c  >  output_sample_041/out.$region.vcf.gz
done




nano bamcaller10.sh

#!/bin/bash
#SBATCH --job-name=mpilup10
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo

. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate alineador

# List of values of the argument -r
regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")

# Route to the reference file
reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"

# Bamcaller
TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"


# Options for samtools mpileup
options="-B -q 20 -Q 20 -C 50"

# Depth 039
DEPTH039=4.62979
# Depth 040
DEPTH040=28.6231
# Depth 041
DEPTH041=32.4736
# Depth 487
DEPTH487=14.5317
# Depth 488
DEPTH488=18.5191
# Depth 489
DEPTH489=46.3561



# BAM039
BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
# BAM040
BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
# BAM041
BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
# BAM487
BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
# BAM488
BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
# BAM489
BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  



for region in "${regions[@]}"; do
OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM487 | \
OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
python $TOOL $DEPTH487 masks2/sample_487/$region.mask.bed.gz                  | \
gzip -c  >  output_sample_487/out.$region.vcf.gz
done




nano bamcaller11.sh

#!/bin/bash
#SBATCH --job-name=mpilup11
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo

. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate alineador

# List of values of the argument -r
regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")

# Route to the reference file
reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"

# Bamcaller
TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"


# Options for samtools mpileup
options="-B -q 20 -Q 20 -C 50"

# Depth 039
DEPTH039=4.62979
# Depth 040
DEPTH040=28.6231
# Depth 041
DEPTH041=32.4736
# Depth 487
DEPTH487=14.5317
# Depth 488
DEPTH488=18.5191
# Depth 489
DEPTH489=46.3561



# BAM039
BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
# BAM040
BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
# BAM041
BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
# BAM487
BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
# BAM488
BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
# BAM489
BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  



for region in "${regions[@]}"; do
OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM488 | \
OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
python $TOOL $DEPTH488 masks2/sample_488/$region.mask.bed.gz                  | \
gzip -c  >  output_sample_488/out.$region.vcf.gz
done






nano bamcaller12.sh

#!/bin/bash
#SBATCH --job-name=mpilup12
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err
#SBATCH --partition=nocona
#SBATCH --nodes=1
#SBATCH --ntasks=64

cd /lustre/scratch/mhoyosro/project1/MSMC2/mMyo

. /home/mhoyosro/conda/etc/profile.d/conda.sh
conda activate alineador

# List of values of the argument -r
regions=("scaffold_m19_p_1" "scaffold_m19_p_2" "scaffold_m19_p_3" "scaffold_m19_p_5" "scaffold_m19_p_6" "scaffold_m19_p_7" "scaffold_m19_p_8" "scaffold_m19_p_9" "scaffold_m19_p_10" "scaffold_m19_p_11" "scaffold_m19_p_12" "scaffold_m19_p_13" "scaffold_m19_p_14" "scaffold_m19_p_15" "scaffold_m19_p_16" "scaffold_m19_p_17" "scaffold_m19_p_18" "scaffold_m19_p_19" "scaffold_m19_p_20" "scaffold_m19_p_21")

# Route to the reference file
reference="/lustre/scratch/mhoyosro/project1/GENOMES/mMyoMyo1.6.pri.fa"

# Bamcaller
TOOL="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/msmc-tools-master/bamCaller.py"


# Options for samtools mpileup
options="-B -q 20 -Q 20 -C 50"

# Depth 039
DEPTH039=4.62979
# Depth 040
DEPTH040=28.6231
# Depth 041
DEPTH041=32.4736
# Depth 487
DEPTH487=14.5317
# Depth 488
DEPTH488=18.5191
# Depth 489
DEPTH489=46.3561



# BAM039
BAM039="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650039.sorted.bam"
# BAM040
BAM040="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650040.sorted.bam"  
# BAM041
BAM041="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR11650041.sorted.bam"  
# BAM487
BAM487="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216487.sorted.bam"
# BAM488
BAM488="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216488.sorted.bam"  
# BAM489
BAM489="/lustre/scratch/mhoyosro/project1/MSMC2/mMyo/SRR27216489.sorted.bam"  



for region in "${regions[@]}"; do
OMP_NUM_THREADS=64 bcftools mpileup $options -r $region -f $reference $BAM489 | \
OMP_NUM_THREADS=64 bcftools call -c -V indels                                 | \
OMP_NUM_THREADS=64 bcftools view -i 'INFO/DP>10'                              | \
python $TOOL $DEPTH489 masks2/sample_489/$region.mask.bed.gz                  | \
gzip -c  >  output_sample_489/out.$region.vcf.gz
done
