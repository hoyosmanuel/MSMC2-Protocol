.. note::

 Duration of the steps mentioned  in the following steps are for the full dataset, below links foir downloading data now points to reduced datset. So, time duration should be much lesser.  

Data pre-processing steps for PSMC
=====================================================

.. note::

 1) Make sure all of your packages are in your ``$PATH``
 2) Create a folder to work all of this - mine says ``PSMC_Tut``
 3) My working directory path is this - ``/Users/vinaykl/PSMC_Tut``
 4) And all of my packages are in ``/Users/vinaykl/softs``
 5) Remove the ``$`` sign from all of your code, if you copy from here. It denotes the beginning of prompt

A) Download Data for Jungle Owlet
----------------------------------------------

.. note::

  1. The direct FTP server are no longer active - for the ease of it, I have uploaded to GDrive and you 
     people can download from there
  2. These files are slightly larger - try and see if you can have a free space of about 150-200GB for the 
     entire excercise

.. code-block:: console

 READ1 : https://drive.google.com/file/d/1pnoPRcZJL7PHSb1EdGa1E_oGEFUahmuu/view?usp=sharing
 READ2 : https://drive.google.com/file/d/1fKQHmb0AAlWdZuZcKaCjNPq9LIUbFdpO/view?usp=sharing

B) Check the QC of your RAW file
-----------------------------

.. code-block:: console
  
  $ mkdir fastqc_reports  #creating a folder called fastqc_reports to put the reports in one place
  $ ~/softs/FastQC/fastqc SRR12705961_1.fastq.gz SRR12705961_1.fastq.gz ./fastqc_reports # It will take about 15mins to 30mins depending on the system. 

.. note::
 
 1) Please go through the following document to understand what the each parameter represents and how you 
 can interpret your results : https://dnacore.missouri.edu/PDF/FastQC_Manual.pdf

