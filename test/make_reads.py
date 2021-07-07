
# Find a way to make reads into a dict? or an array
# Need to take out first line (done, verified that both lists are equally long)
# Find out how long reads should be. Do I append them so I can change read length?
# Randomize quality scores for fastq files and reads? Maybe those genome sims could help
# MAKE A BIG PICTURE FLOW DIAGRAM

def test1(genome):
    a = open(genome)
    b = a.readlines()
    c = b[1:(len(b))-1]
    # the 1 excludes the sequence name in the seq file
   # print(c)
    d = []

    for x in c:
        d.append(x.strip("\n"))
    print(d)
    full_seq = "".join(d[0:(len(d))])
    print(full_seq)

# Now full_seq can be chopped up into reads in a new file
# remember that the actual reads will have associated quality scores


test1("lambda_virus.fa")
