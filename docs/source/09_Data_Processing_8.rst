MPILEUP
=======

.. note::

   This is an additional key step in the workflow. It is independent from the heterozygosity estimation described in the previous step. Both analyses can be performed in parallel however, running both workflows simultaneously may be computationally/mentally demanding particularly when working with a large number of samples and therefore it is not a recommended standard approach. Again, this implementation is presented for transparency, and users may identify more efficient and streamlined alternatives.

   That said, in this step, a new set of VCF files using ``bcftools mpileup`` will be generated. In contrast to the previous analysis, no neutral mask is applied here. Instead, VCF files are generated separately for each scaffold of interest (the scaffolds assumed to represent autosomes). These scaffold-specific VCF files will be used as input for the `multihetsep` step in MSMC2.

   The output of this step will be organized within a directory named `mask_2`, which will contain subdirectories for each sample.

1) Create directories for the workflow
--------------------------------------
