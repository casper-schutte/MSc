from class_SAM import SAM
import numpy as np

file = SAM()
filepath = 'chrom_test.sam'
number = file.ReadSAMFile(filepath)


def check_qual():
    """
    This function takes a .sam file as input, in the variable (filepath)
    Based on the mapping quality (MAPQ field in SAM file) the reads that mapped
    badly can be returned. This threshold can be changed. Currently it looks for
    reads with a lower mapping quality than the maximum MAPQ, which seems to work
    for the artificial genome used to test it.
    This threshold will be changed as appropriate after testing on real data
    """

    qual_list = []
    for i in range(number):
        qual_list.append([file.GetField(i, 'QNAME'), int(file.GetField(i, 'MAPQ')), int(file.GetField(i, 'POS')),
                          file.GetField(i, 'RNAME')])

    bad_mapq = []

    for j in qual_list:

        if j[1] < max(qual_list[k][1] for k in range(number)):
            bad_mapq.append(j)
    # Iterates through the qual_list and appends reads that had a mapping quality
    # below a certain threshold.

    print("these reads mapped badly:", bad_mapq)
    return bad_mapq


def find_consecutive_blocks():
    """
    This function returns the read number and position of the first and last read in
    a consecutive block. These should correlate with synteny blocks
    """
    iterable = []
    for i in range(number):
        iterable.append(int(file.GetField(i, 'POS')))

    my_seq = np.split(iterable, np.array(np.where(np.abs(np.diff(iterable)) > 100)[0]) + 1)
    # This line returns reads in blocks that differ by no more than the read length minus
    # the overlap. In other words, the blocks that are returned can be thought of as
    # synteny blocks.
    # Change the "100" to "read length - overlap." This will distinguish consecutive
    # reads from nonconsecutive ones.
    blocks = []
    for s in my_seq:
        if len(s) > 1:
            # excludes single reads that don't map anywhere
            blocks.append((s[0], s[-1]))
    print("consecutive blocks: ", blocks)
    return blocks


def find_border(quals, con_blocks):
    my_blocks = [y for z in con_blocks for y in z]
    print(my_blocks)
    # Flattens the list of borders
    my_borders = []
    print(quals)
    print(con_blocks)
    for j in quals:
        for k in my_blocks:
            if k == j[2]:
                # This line needs to change, how to connect the correct blocks and bad maps?
                my_borders.append((k, j[0], j[3]))
                # my_borders.append((k, j[0]))

                # This last line adds the edge of a consecutive block (k), the read name/number (j[0])
                # and the chromosome/sequence name j[3].

    print(f"The borders are: {my_borders}")
    return my_borders


if __name__ == "__main__":
    a = check_qual()
    b = find_consecutive_blocks()
    c = find_border(a, b)
