filepath = "lv_multi_C_test.fa"

my_list = []


def sep_chrom(seq_file):
    a = open(seq_file)
    b = (a.read()).split(">")
    chrom_list = []
    for x in b[1:]:
        chrom_list.append(x[x.index("\n") + 1:])
    return chrom_list


# It works! The FastA file is separated into chromosomes

if __name__ == "__main__":
    separated_chrom = sep_chrom(filepath)
    print(separated_chrom)
