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

    worst_maps = []
    for score in enumerate(mapq):
        if int(score[1]) < 10:
            # worst_maps.append([score, rocigar[int(score[0])]])
            worst_maps.append([score[0], score[1]])

    print(worst_maps)

    breakpoint_areas = []
    r_list = []
    f_list = []
    for mapq_score in worst_maps:

        r_temp_list = []
        f_temp_list = []
        r_counter = 1
        f_counter = 0

        while mapq[mapq_score[0] - r_counter + 2] < max(mapq):
            # backwards
            current_read = mapq_score[0] - r_counter
            r_temp_list.append([mapq[current_read], rocigar[current_read], pos[current_read]])
            r_counter += 1

        r_list.append(r_temp_list[:: - 1])
        f_list.append([mapq[mapq_score[0]], rocigar[mapq_score[0]], pos[mapq_score[0]]])

        while mapq[mapq_score[0] + f_counter - 1] < max(mapq):
            # forwards
            current_read = mapq_score[0] + f_counter
            f_temp_list.append([mapq[current_read], rocigar[current_read], pos[current_read]])
            f_counter += 1


        f_list[0].append(f_temp_list)
        print(r_temp_list)

    # print(r_list[::-1])
    #print(f_list)

    borders = []
    #for area in f_list:
    #    print(area)



# Consider just iterating through the list and


if __name__ == "__main__":
    read_info = get_borders()
