# import numpy as np

from class_SAM import SAM

file = SAM()
filepath = 'exp7_6.sorted.sam'
number = file.ReadSAMFile(filepath)

"""
It is VITAL that the variable "read_len" is set to be the same as in the script used to create the reads
"""
read_len = 100


def get_border_reads():
    # This function creates a list with various fields for the reads. The reads which do not map properly (indicated
    # by the CIGAR string) are returned.
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

    borders = []
    for read in enumerate(rocigar):
        if read[1] == f"{read_len}M":
            pass
        else:
            borders.append([chrom[read[0]], pos[read[0]], read_name[read[0]], mapq[read[0]], read[1]])

    # print(borders)
    return borders


def get_borders(borders):
    # This function takes the reads which are suspected to contain rearrangement breakpoints and extracts the CIGAR
    # strings. Then, the reads are returned BUT with ADJUSTED positions. These positions refer to the last (or first)
    # mapping read, depending on whether it matched initially or started matching somewhere along its length.
    bps = []
    # bps = breakpoints
    for border in borders:
        cigar_str = border[4]
        temp_list = []
        for character in cigar_str:
            if character == "M":
                bps.append(temp_list)
                break
            elif character.isalpha() and character != "M":
                temp_list = ["-"]
            elif character.isdigit():
                if not temp_list:
                    temp_list.append(character)
                else:
                    temp_list.append("".join(character))

    # print(bps)
    # print(len(bps))
    matching = []
    for numbers in bps:
        matching.append("".join(numbers[0:]))

    print(matching)
    print(len(matching))

    breakpoints = []
    for m in enumerate(matching):
        if m[1].count("-") == 0:
            breakpoints.append([
                borders[m[0]][0], borders[m[0]][1] + int(m[1]), borders[m[0]][2], borders[m[0]][3], borders[m[0]][4],
                "+"
            ])

        else:
            breakpoints.append([
                borders[m[0]][0], borders[m[0]][1], borders[m[0]][2], borders[m[0]][3],
                borders[m[0]][4], "-"
            ])

    print(breakpoints)
    return breakpoints


def refine_breakpoints(bp):
    pos = []

    mapqs = []
    for read in bp:
        mapqs.append(read[3])
        pos.append(read[1])

    conf_borders = []
    nonconf_borders = []

    for read in bp:
        # write a function that takes the mapq score into account, and extends the reads by the inverse of the MAPQ
        # Multiplied by some constant (optimize). In this way, we can statistically back up the position of the
        # breakpoint with multiple reads that map to the same area.
        if read[3] > 40:
            # print(read)
            conf_borders.append(read)
        else:
            nonconf_borders.append(read)

    print(conf_borders)
    border_areas = []
    allowance = 50
    # Think about letting allowance change to be inversely proportional to the MAPQ score.
    counter = 0
    # counter to keep track of where we are in the list
    for border in conf_borders:
        # This loop groups the most confident borders by whether they are within a certain distance from one another.
        if not border_areas:
            border_areas.append([border])
            print(border_areas)
        elif border[1] - allowance <= border_areas[counter][0][1] <= border[1] + allowance \
                and border[0] == border_areas[counter][0][0]:
            border_areas[counter].append(border)
            print(border_areas)
        else:
            border_areas.append([border])
            counter += 1
            print(border_areas)

    print(border_areas)
    print(len(bp))
    done = []
    for border in nonconf_borders:
        if border not in done:
            for cb in border_areas:
                print(f"cb: {cb}")
                if border[1] - allowance <= cb[0][1] <= border[1] + allowance:
                    border_areas[border_areas.index(cb)].append(border)
                    done.append(border)

    for border in nonconf_borders:
        if border not in done:
            border_areas.append([border])

    print(border_areas)
    print(len(border_areas[0]) + len(border_areas[1]))

    return border_areas

    #


def write_to_file(breakpoints):
    my_file = open(file_name, "w")
    my_file.write(f"chromosome \t position \t read name \t MAPQ \t CIGAR string \n")
    for area in breakpoints:
        for bp in area:
            my_file.write(f"{bp[0]} \t \t {bp[1]} \t \t {bp[2]} \t \t {bp[3]} \t {bp[4]} \n")
        my_file.write("\n")


if __name__ == "__main__":
    read_info = get_border_reads()
    find_breakpoints = get_borders(read_info)
    file_name = "exp7_6.txt"  # Desired name for output file
    # write_to_file(find_breakpoints)
    refined_breakpoints = refine_breakpoints(find_breakpoints)
    write_to_file(refined_breakpoints)
