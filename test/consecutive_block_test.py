import numpy as np

from class_SAM import SAM

file = SAM()
filepath = 'chrom_test.sam'
number = file.ReadSAMFile(filepath)

my_array = []
read_nums = []
my_chroms = []


def find_consecutive_blocks():
    for i in range(number):
        my_array.append(int(file.GetField(i, "POS")))
        read_nums.append(file.GetField(i, "QNAME"))
        my_chroms.append((file.GetField(i, "RNAME")))
    diffs = np.diff(my_array)
    iterable = []
    borders = []
    pos = 0
    print(diffs)
    while pos + 1 < len(my_array):
        if diffs[pos] > 100 or diffs[pos] < 0:
            iterable.append([abc(pos), abc(pos + 1)])
        pos += 1
    print(iterable)

    flat_list = [y for z in iterable for y in z]
    print(flat_list)


def abc(i):
    return [my_array[i], read_nums[i], my_chroms[i]]


if __name__ == "__main__":
    find_consecutive_blocks()
