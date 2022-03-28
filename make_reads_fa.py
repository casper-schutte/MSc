from random import randint
import sys

# This python script successfully takes a fastA file and creates reads according to set parameters
# these reads are written to a fastA (.fa) file with the sequence name correlating numerically to the
# order of the reads.

# filepath = "ref_exp10_3.fa"
# read_file_name = "reads_exp10_3.fa"

filepath = sys.argv[1]
read_file_name = sys.argv[2]


def get_seq(genome):
    """
    Takes a fastA file and returns the full sequence sans the title and newline characters
    input: fastA (.fa) file
    output: string
    """

    a = open(genome)
    b = (a.read()).split(">")
    z = []
    for x in b[1:]:
        z.append(x[x.index("\n") + 1:])
    d = []

    for x in z:
        d.append(x.replace("\n", ""))

    return d


def get_reads(seq_file):
    """
    Creates reads according to the parameters in the argument
    input: The full sequence as a string
    output: list of reads
    """

    read_len = 100
    read_len_2 = 200
    coverage = 20
    # 1x coverage here is defined as the sum of all the reads being equal to the length of the genome
    # 10x coverage indicates the sum of all the reads being 10x the length of the genome.

    # lor = []
    # List of reads
    # number_of_reads = (coverage * (len(seq_file)))/len(lor)
    reads = []
    while len(reads) < (coverage * len(seq_file)) / read_len:
        start_pos = randint(0, len(seq_file) - read_len_2)
        reads.append(seq_file[start_pos:start_pos + read_len])
        reads.append(seq_file[start_pos:start_pos + read_len_2])
    # Double-check the math here to make sure that the desired coverage is achieved
    print(len(reads))
    return reads


def reads_to_file(reads):
    """
    Writes a fastQ file with the list of reads and adds a PHRED score
    input: a list of reads
    output: a fastA file containing the reads and their number
    """

    my_file = open(read_file_name, "w")
    read_num = 1

    for y in reads:
        for x in y:
            my_file.write(">r" + str(read_num) + "\n")
            my_file.write(str(x) + "\n")

            read_num += 1

    my_file.close()

    print(f"done writing reads to file: {read_file_name}")


if __name__ == "__main__":
    h = get_seq(filepath)
    j = []
    for i in h:
        j.append(get_reads(i))
    reads_to_file(j)
