import numpy as np

from class_SAM import SAM

file = SAM()
filepath = 'chrom_test.sam'
number = file.ReadSAMFile(filepath)

my_array = [1, 2, 4, 5, 6, 7, 9, 10]
read_nums = ["r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9", "r10"]

diffs = np.diff(my_array)


def find_consecutive_blocks():
    iterable = []
    borders = []
    pos = 0

    while pos + 1 < len(my_array):
        if diffs[pos] > 1:
            iterable.append([abc(pos), abc(pos + 1)])
        pos += 1
    print(iterable)


def abc(i):
    return [my_array[i], read_nums[i]]


if __name__ == "__main__":
    find_consecutive_blocks()
