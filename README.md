# MSc
Designing a statistically rigorous Burrows-Wheeler mapping algorithm to find rearrangement breakpoints

# Usage:
At this time, the use of this algorithm requires that the bioinformatics tools Bowtie2 and SamTools to be installed.
The bash script calls all the necessary scripts and tools to run the algorithm. This algorithm is still in development. 

In the current version, the algorithm first creates reads from the 2 selected genomes (A and B). This is done by a 
Python script where one can adjust the coverage and read lengths. Bowtie2 is then called to index the genomes and 
map reads from genome A onto reference genome B and vice versa. This mapping process is completed twice, once 
with Bowtie2's single-reporting mode and once in multi-report mode. This allows us to get an accurate measure of 
the mapping quality as well as information about which breakpoints are in physical proximity. The outputs are saved as 
SAM files. SamTools is then called to sort the SAM files. Finally, another Python script is called to look for reads 
that do not map over their full length, but have a mapping quality above a certain threshold. These reads are used as places 
to start looking for borders. The Python script outputs a text file containing the reads that support the breakpoints. 
