import numpy as np

from class_SAM import SAM

file = SAM()
filepath = 'exp7_1.sam'
number = file.ReadSAMFile(filepath)


def get_borders():
    pos = []
    mapq = []
    chrom = []
    read_name = []
    cigar = []
    rocigar = []
    for i in range(number):
        pos.append(int(file.GetField(i, "POS")))
        mapq.append(int(file.GetField(i, "MAPQ")))
        chrom.append(file.GetField(i, "RNAME"))
        read_name.append(file.GetField(i, "QNAME"))
        cigar.append(file.GetCIGARvalues(i))
        rocigar.append(file.GetField(i, "CIGAR"))

    diffs = np.array(mapq)
    bad_maps = []
    for read in enumerate(diffs):
        if read[1] < 44:
            bad_maps.append([read[0], read[1]])

    temp_list = []
    current_pos = 0
    border_areas = []
    done_reads = []
    for read in bad_maps:
        if read not in done_reads:
            if not temp_list:
                temp_list.append(read)
                done_reads.append(read)
                current_pos += 1

            elif read == bad_maps[-1]:
                pass

            elif read[0] + 1 == bad_maps[current_pos + 1][0]:
                temp_list.append(read)
                done_reads.append(read)
                current_pos += 1

            else:
                temp_list.append(read)
                done_reads.append(read)
                border_areas.append(temp_list)
                current_pos += 1
                temp_list = []

    print(border_areas)
    print(done_reads)
    print(bad_maps)


if __name__ == "__main__":
    read_info = get_borders()
