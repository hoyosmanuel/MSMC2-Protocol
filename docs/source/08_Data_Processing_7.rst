Calculate heterozygosity
========================

1) Calculate Heterozigosity using a ``bcftools mpileup``
----------------------------------------------------------

.. note::

  | So, let's recapitulate a bit to have a map of what we have so far:
  | · Directory Mask_1 contains the intergenic fraccion which is neutral
  | · Conocemos el caritipo de las especies sobre las que estamos haciendo esto
  | · Los genomas de referencias han sido obtenidos con tecnología PACBIO por lo que los scaffolds vienen representado cada uno de los cromosomas
  | · Conocemos cuales de esos scaffolds/cromosomas era cromosomas X o hacian parte de un cromosoma x
  | · El objetivo de este analisis es usar autosomas, con aproximadamente homogeneous recombination and Mendelian inheritance así que hay que eliminé los cromosomas X (que los identifiqué previamente). 
  | · La vaina es que no podemos asumir que un scaffold es cromosoma, porque los cromosomas se pueden romper durante la procesamiento PACBIO (Rhoads & Au, 2015)



  | · Ahora, los murcielagos de este trabajo obviament son diploides (2n) pero los scaffolds/cromosomas del genoma de referencia son un consenso de los dos asi que en mi estudio desde el punto de vista práctico el cariotipo es (n) 
  | · Las especies entonces están así:
  | *Hipposideros larvatus* n = 14 - X
  | *Molossus molossus* n = 22 - X
  | *Myotis myotis* n = 20 - X
  | *Phyllostomus discolor* n = 14 - X
  | *Pipistrellus kuhlii* n = 14 - X
  | *Rhinolophus ferrumequinum* n = 14 - X
  | *Rousettus aegyptiacus n = 14 - X


2n = 32 => 14 pairs of Autosomes + X Y
Chromosome X = manual_scaffold_14
B) Molossus molossus
2n = 48 => 22 pairs of Autosomes + X Y
Chromosome X = scaffold_m16_p_2 & scaffold_m16_p_1

C) Myotis myotis
2n = 44 => 20 pairs of Autosomes + X Y
Chromosome X = scaffold_m19_p_4
D) Phyllostomus discolor
2n = 32 => 14 pairs of Autosomes + X Y
Chromosome X = scaffold_m19_p_9
E) Pipistrellus kuhlii
2n = 44 => 20 pairs of Autosomes + X Y
Chromosome X = 16 (Scaffold 16 was tentatively assigned based on ZFX)
F) Rhinolophus ferrumequinum
2n = 58 => 27 pairs of Autosomes + X Y
Chromosome X = scaffold_m29_p_1
G) Rousettus aegyptiacus
2n = 36 => 16 pairs of Autosomes + X Y
Chromosome X = scaffold_m13_p_9









Rhoads A, Au KF. PacBio Sequencing and Its Applications. Genomics Proteomics Bioinformatics. 2015 Oct;13(5):278-89. doi: 10.1016/j.gpb.2015.08.002. Epub 2015 Nov 2. PMID: 26542840; PMCID: PMC4678779.
