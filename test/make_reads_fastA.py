# This python script successfully takes a fastA file and creates reads according to set parameters
# these reads are written to a fastA (.fa) file with the sequence name correlating numerically to the
# order of the reads

def get_seq(genome):
    """
    Takes a fastA file and returns the full sequence sans the title and newline characters
    input: fastA (.fa) file
    output: fastA (.fa) file
    """
    a = open(genome)
    b = a.readlines()
    c = b[1:(len(b)) - 1]
    # the 1 excludes the sequence name in the seq file
    d = []
    for x in c:
        d.append(x.strip("\n"))
    full_seq = "".join(d[0:(len(d))])

    return (full_seq)



def get_reads(seq_file):

    """
    Creates reads of according to the parameters in the argument
    input: The full sequence as a string
    output: reads in string format INSIDE a list called "my_reads"
    """
    my_reads = []
    read_length = 150
    overlap = 50
    read_pos = 0

    # have verified that the data written to file is the same that was from the sequence.
    # now make the reads

    while read_pos < len(seq_file):
        my_reads.append(seq_file[read_pos:read_pos+read_length])
        read_pos += read_length - overlap

    for x in my_reads:
        print(len(x))
    return(my_reads)



def reads_to_file(reads):
    """
    Writes a fastA file with from the list of reads
    input: a list of reads
    output: a fastA file containing the reads and their number
    """
    my_file = open("test_reads.fa", "w")
    read_num = 1
    for x in reads:
        my_file.write(">" + str(read_num)+"\n")
        my_file.write(str(x) + "\n")
        read_num += 1
    my_file.close()

    print("done writing reads to file")

# remember that the actual reads will have associated quality scores


# This might be redundant, investigate using biopython to make reads


if __name__ == "__main__":
    h = get_seq("lambda_virus.fa")
    j = get_reads(h)
    k = reads_to_file(j)


