# MSc
Designing a statistically rigorous Burrows-Wheeler mapping algorithm to find rearrangement breakpoints

# Usage:
At this time, the use of this algorithm requires that the bioinformatics tool, Bowtie2, be installed. Using this script,
one can take two genomes of very closely related species and calculate where the borders of rearrangements are. 



The script "make_reads.py" is used to construct reads from genomes in the FastA format. 
Bowtie2 is then used to align reads from one genome to the other (by indexing the other genome and performing an 
alignment)

Example:

Used make_reads.py to construct reads from one of the genomes (reads.fa)

/$ Bowtie2-build path/to/index.fa index_name

/$ Bowtie2 --local -f -x index_name -U path/to/reads.fa -S alignment_name.sam 

Then find_borders.py (which is dependent on the class_SAM.py module) can be used to view the continuous 
blocks and the borders between them, with information (position on chromosome, chromosome name, 
read name, mapping score). 

This algorithm is not complete, but is being updated, it may not work as intended in its current form.