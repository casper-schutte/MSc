import numpy as np
# from Class_test import Block
from class_SAM import SAM

file = SAM()
filepath = 'b21_x_k12.filtered.sam'
output_file_name = "real_data_test_2.txt"
number = file.ReadSAMFile(filepath)

# This file is used to test the new algorithm for calculating continuous blocks
# This algorithm will be incorporated into "find_borders.py" after testing. The method used in "find_borders.py" was
# found to be lacking in flexibility.

my_array = []
read_nums = []
my_chroms = []
my_as = []
my_list = []
my_score = []


def find_consecutive_blocks():
    for i in range(number):
        my_array.append(int(file.GetField(i, "POS")))
        read_nums.append(file.GetField(i, "QNAME"))
        my_chroms.append((file.GetField(i, "RNAME")))
        # my_as.append(file.GetOPTValue(i, "AS"))
        my_score.append(file.GetField(i, "MAPQ"))
    diffs = np.diff(my_array)
    iterable = []
    pos = 0
    last_pos = 0
    while pos + 1 < len(my_array):
        if diffs[pos] > 15 or diffs[pos] < -15 or diffs[pos] == 1:
            # These numbers are set according to how the reads are simultaneously created from the end
            # and the start of the file. Sometimes an intermediate read is created which overlaps the middle
            # and this can cause the program to question the continuity of the reads. The allowance of
            # overlap solves this.
            # The last OR statement lets us catch insertions at the start of a sequence, because changing from
            # position 0 (didn't map anywhere) to position 1 (start of sequence) does not trigger the previous
            # arguements.
            iterable.append([[get_fields(last_pos), get_fields(pos)]])
            last_pos = pos + 1
        pos += 1
    iterable.append([[get_fields(last_pos), get_fields(pos)]])

    # print(iterable)

    flat_list = [y for z in iterable for y in z]

    print(flat_list)
    pos_in_list = 0
    current_read = None
    for reads in flat_list:
        print(reads[0], reads[1])
        # for read in border:
        pos_in_list += 1
        if reads[0][3] == "1" or reads[0][3] == "0":
            reads[0][0] = "*"
            reads[0][1] = "*"
            reads[0][3] = "*"
        if reads[1][3] == "1" or reads[1][3] == "0":
            reads[1][0] = "*"
            reads[1][1] = "*"
            reads[1][3] = "*"
        if reads[1][3] == "*" and reads[0][3] == "*":
            flat_list[(pos_in_list - 1)]

        elif reads[0][2] == reads[1][2]:
            flat_list.remove(flat_list[pos_in_list - 1])

    print(pos_in_list)

    # there is a way to return the order as well, using the pos and arranging them consecutively.
    # In some cases, extra information can be obtained from the way the borders are returned. See the explanation in
    # "experiment_5.txt" for details and examples on this.

    return flat_list


def get_fields(i):
    # return [my_array[i], read_nums[i], my_chroms[i], my_as[i]]
    # return [my_array[i], my_chroms[i], read_nums[i], my_score[i]]

    return [my_array[i], "*", read_nums[i], my_score[i]]
    # This cleans up returns when dealing with a unichromosomal organism


def get_borders(blocks):
    mapped_badly = []
    for border in blocks:
        for read in border:
            if read == "*":
                pass
            elif read[3] == "*":
                pass
            elif 42 > int(read[3]) > 20:
                # The score thresholds need to either be calibrated to the results or simply set by the user
                # With long duplications, we get long blocks that are not continuous positionally but score very
                # low (MAPQ = 1). This makes the returned "borders" and badly mapped reads very messy and confusing.
                # A MAPQ of 20 indicates that the aligner calculates a 0.99 probability of the read mapping to that
                # position
                mapped_badly.append(read)
    print(f"Reads containing borders: {mapped_badly}")
    return mapped_badly


def write_results_to_file(blocks, borders):
    my_file = open(output_file_name, "w")
    my_file.write("Continuous blocks:" + "\n")
    my_file.write("Position on chromosome, Chromosome, Read number, MAPQ score" + "\n")
    for x in blocks:
        my_file.write(str(x) + "\n")

    my_file.write("\n")
    my_file.write("Borders:" + "\n")
    for y in borders:
        my_file.write("\n")
        my_file.write(str(y) + "\n")


if __name__ == "__main__":
    a = find_consecutive_blocks()
    b = get_borders(a)
    write_results_to_file(a, b)
