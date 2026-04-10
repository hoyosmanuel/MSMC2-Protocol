MPILEUP
=======

.. note::

   This is an additional key step in the workflow. It is independent from the heterozygosity estimation described in the previous step. Both analyses can be performed in parallel however, running both workflows simultaneously may be computationally/mentally demanding particularly when working with a large number of samples and therefore it is not a recommended standard approach. Again, this implementation is presented for transparency, and users may identify more efficient and streamlined alternatives.

   That said, in this step, a new set of VCF files using ``bcftools mpileup`` will be generated. In contrast to the previous analysis, no neutral mask is applied here. Instead, VCF files are generated separately for each scaffold of interest (the scaffolds assumed to represent autosomes). These scaffold-specific VCF files will be used as input for the `multihetsep` step in MSMC2.

   The output of this step will be organized within a directory named `mask_2`, which will contain subdirectories for each sample.

1) Create directories for the workflow
--------------------------------------

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
   
   
