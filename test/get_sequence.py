# Find a way to make reads into a dict? or an array
# Need to take out first line (done, verified that both lists are equally long)
# Find out how long reads should be. Do I append them so I can change read length?
# Randomize quality scores for fastq files and reads? Maybe those genome sims could help
# MAKE A BIG PICTURE FLOW DIAGRAM


def get_seq(genome):
    a = open(genome)
    b = a.readlines()
    c = b[1:(len(b)) - 1]
    # the 1 excludes the sequence name in the seq file

    d = []

    for x in c:
        d.append(x.strip("\n"))

    full_seq = "".join(d[0:(len(d))])

    return(full_seq)




get_seq("lambda_virus.fa")
