from random import randint


# This python script successfully takes a fastA file and creates reads according to set parameters
# these reads are written to a fastA (.fa) file with the sequence name correlating numerically to the
# order of the reads

def get_seq(genome):
    """
    Takes a fastA file and returns the full sequence sans the title and newline characters
    input: fastA (.fa) file
    output: string
    """
    a = open(genome)
    b = a.readlines()
    c = b[1:(len(b)) - 1]
    # the 1 excludes the sequence name in the seq file
    d = []
    for x in c:
        d.append(x.strip("\n"))
    full_seq = "".join(d[0:(len(d))])

    return full_seq


def get_reads(seq_file):
    """
    Creates reads of according to the parameters in the argument
    input: The full sequence as a string
    output: list of reads
    """
    my_reads = []
    read_length = 150
    overlap = 50
    read_pos = 0

    # have verified that the data written to file is the same that was from the sequence.
    # now make the reads

    while read_pos < len(seq_file):
        my_reads.append(seq_file[read_pos:read_pos + read_length])
        read_pos += read_length - overlap

    return my_reads


def reads_to_file(reads):
    """
    Writes a fastQ file with the list of reads and adds a PHRED score
    input: a list of reads
    output: a fastA file containing the reads and their number
    """
    my_file = open("test_fastq.fq", "w")
    read_num = 1

    for x in reads:
        my_file.write("@r" + str(read_num) + "\n")
        my_file.write(str(x) + "\n")
        my_file.write("+" + "\n")

        qual_list = "".join(chr(randint(33, 126)) for y in range(len(x)))

        my_file.write(str(qual_list) + "\n")
        read_num += 1


    my_file.close()

    print("done writing reads to file")


# remember that the actual reads will have associated quality scores


# This might be redundant, investigate using biopython to make reads


if __name__ == "__main__":
    h = get_seq("lambda_virus.fa")
    j = get_reads(h)
    k = reads_to_file(j)
