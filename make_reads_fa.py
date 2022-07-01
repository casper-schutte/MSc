from random import randint
import sys

# This python script successfully takes a fastA file and creates reads according to set parameters
# these reads are written to a fastA (.fa) file with the sequence name correlating numerically to the
# order of the reads.

# filepath = "ref_exp11.fa"
# read_file_name = "reads_exp11.fa"

filepath = sys.argv[1]
read_file_name = sys.argv[2]


def get_seq(genome):
    """
    Takes a fastA file and returns the full sequence sans the title and newline characters
    input: fastA (.fa) file
    output: string
    """

    with open(genome, "r") as a:
        b = (a.read()).split(">")
        z = []
        for x in b[1:]:
            z.append(x[x.index("\n") + 1:])
        d = []

        for x in z:
            d.append(x.replace("\n", ""))
    # print(len(d))
    # This method returns a list of the sequences in the fastA file, where each chromosome is an element. This is
    # important because if this wasn't done, reads would be created that span 2 chromosomes
    return d


def get_reads(seq_file, new_pos):
    """
    Creates reads according to the parameters in the argument
    input: The full sequence as a string
    output: list of reads
    """
    read_len = 200
    # read_len_2 = 200
    # coverage = 20
    # 1x coverage here is defined as the sum of all the reads being equal to the length of the genome
    # 10x coverage indicates the sum of all the reads being 10x the length of the genome.
    # number_of_reads = (coverage * (len(seq_file)))/len(lor)
    reads = []
    # while len(reads) < (coverage * len(seq_file)) / read_len:
    read_pos = 0
    overlap = 190
    # Need to do some math to recalculate the coverage that is being achieved. There is probably a way to do this with
    # a simple formula.
    while read_pos < len(seq_file):
        reads.append(seq_file[read_pos:read_pos + read_len])
        read_pos += read_len - overlap
        # Now, we might be able to tell how long certain rearrangements are... might be.
        # reads.append(seq_file[start_pos:start_pos + read_len_2])
    # Double-check the math here to make sure that the desired coverage is achieved
    # print(len(reads))
    return reads


def reads_to_file(reads):
    """
    Writes a fastA file with the list of reads
    input: a list of reads
    output: a fastA file containing the reads and their number
    """

    my_file = open(read_file_name, "w")
    reads = sorted(reads)
    read_num = 1
    for y in reads:
        for x in y:
            # print(x)
            my_file.write(">r" + str(read_num) + "\n")
            my_file.write(str(x) + "\n")
            read_num += 1

    my_file.close()

    print(f"done writing reads to file: {read_file_name}")


if __name__ == "__main__":
    h = get_seq(filepath)
    j = []
    new_pos = 0
    for i in h:
        j.append(get_reads(i, new_pos))
        new_pos += len(i)
        # r = get_reads(i, new_pos)
        # print(len(i))
        # This method still needs to be updated. The starting positions in get_reads() are reset upon each iteration.
        # I need to adjust each new starting position. This method might work! Again, why am I making them randomly?
    # print(j)
    reads_to_file(j)
