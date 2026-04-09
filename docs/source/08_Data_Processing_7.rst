Calculate heterozygosity
========================

1) Calculate Heterozigosity using a ``bcftools mpileup``
----------------------------------------------------------

.. note::

  | So, let's recapitulate a bit to have a map of what we have so far:
  | · Directory Mask_1 contains the intergenic fraccion which is neutral
  | · Conocemos el caritipo de las especies sobre las que estamos haciendo esto
  | · Los genomas de referencias han sido obtenidos con tecnología PACBIO por lo que los scaffolds vienen representado cada uno de los cromosomas
  | · Conocemos cuales de esos scaffolds/cromosomas son cromosomas X
  | · El objetivo de este analisis es usar Autosomas, con aproximadamente homogeneous recombination and Mendelian inheritance así que hay que eliminé los cromosomas X (que los identifiqué previamente). 
  | · Ahora, los murcielagos de este trabajo obviament son diploides (2n) pero los scaffolds/cromosomas del genoma de referencia son un consenso de los dos asi que en mi estudio desde el punto de vista práctico el cariotipo es (n) 





