from random import randint


# This python script successfully takes a fastA file and creates reads according to set parameters
# these reads are written to a fastQ (.fq) file with the sequence name correlating numerically to the
# order of the reads. Quality scores are randomized because the data is simulated for testing.

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
    print(z)
    for x in z:
        d.append(x.replace("\n", ""))

    # full_seq = "".join(d[0:(len(d))])
    print(d)
    # full_seq = full_seq.replace(">", "\n")
    return d


def get_reads(seq_file):
    """
    Creates reads of according to the parameters in the argument
    input: The full sequence as a string
    output: list of reads
    """
    my_reads_f = []
    my_reads_r = []
    read_length = 150
    overlap = 50
    read_pos_f = 0
    read_pos_r = len(seq_file)

    while (read_pos_f + (len(seq_file) - read_pos_r)) < len(seq_file):
        my_reads_f.append(seq_file[read_pos_f:read_pos_f + read_length])
        my_reads_r.append(seq_file[read_pos_r - read_length: read_pos_r])
        read_pos_f += read_length - overlap
        read_pos_r -= read_length - overlap
        # print(read_pos_f + len(seq_file) - read_pos_r)

    # The code above builds read from the sequence, from the front and the end simultaneously.
    print(read_pos_f, read_pos_r, read_pos_r + read_pos_f, len(seq_file))
    print(my_reads_f + my_reads_r[::-1])
    return my_reads_f + my_reads_r[::-1]


"""
    read_pos1 = 0
    my_reads1 = []
    while read_pos1 < len(seq_file):
        my_reads1.append(seq_file[read_pos1:read_pos1 + read_length])
        read_pos1 += read_length - overlap

    print(my_reads1)
"""


def reads_to_file(reads):
    """
    Writes a fastQ file with the list of reads and adds a PHRED score
    input: a list of reads
    output: a fastA file containing the reads and their number
    """
    #   Change the name of the file in the line below to keep track of files
    my_file = open("exp4.fq", "w")
    read_num = 1

    for y in reads:
        for x in y:
            my_file.write("@r" + str(read_num) + "\n")
            my_file.write(str(x) + "\n")
            my_file.write("+" + "\n")

            qual_list = "".join(chr(randint(33, 126)) for y in range(len(x)))

            my_file.write(str(qual_list) + "\n")
            read_num += 1

    my_file.close()

    print("done writing reads to file")


# remember that the actual reads will have associated quality scores


if __name__ == "__main__":
    h = get_seq("lambda_virus.fa")
    j = []
    for i in h:
        j.append(get_reads(i))
    k = reads_to_file(j)
