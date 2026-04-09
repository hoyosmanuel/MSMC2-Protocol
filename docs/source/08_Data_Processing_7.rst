Calculate heterozygosity
========================

1) Calculate Heterozigosity using a ``bcftools mpileup``
----------------------------------------------------------

.. note::

   At this stage, the dataset includes intergenic regions previously intersected with the mappability mask (Directory mask_1), which were used as putatively neutral regions. The karyotypes of the study species are known, and sex-linked scaffolds were identified in a previous step (X markers). Because MSMC assumes approximately homogeneous recombination and diploid Mendelian inheritance, scaffolds corresponding to the X chromosome were excluded from the main analysis. The scaffold number does not necessarily correspond 1:1 with chromosome number in genome assemblies produce with PCBIO, as assemblies may remain fragmented. Therefore, the following scaffold selection was guided by both karyotype information and prior identification of sex-linked regions.






Rhoads A, Au KF. PacBio Sequencing and Its Applications. Genomics Proteomics Bioinformatics. 2015 Oct;13(5):278-89. doi: 10.1016/j.gpb.2015.08.002. Epub 2015 Nov 2. PMID: 26542840; PMCID: PMC4678779.
