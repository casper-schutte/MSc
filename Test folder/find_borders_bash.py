from class_SAM import SAM

from itertools import groupby

import sys

file = SAM()
#filepath = 'ma_2.sam.sorted.sam'
filepath = sys.argv[1]
outname = sys.argv[2]
number = file.ReadSAMFile(filepath)

"""
It is VITAL that the variable "read_len" is set to be the same as in the script used to create the reads
"""
read_len = 100
read_len_2 = 200


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
    # Now the reads that had CIGAR strings that did not show full matches are appended to the "borders" list, along
    # with its associated information.
    for read in enumerate(rocigar):
        if read[1] == f"{read_len}M" or read[1] == f"{read_len_2}M":
            pass
        else:
            borders.append([chrom[read[0]], pos[read[0]], read_name[read[0]], mapq[read[0]], read[1]])

    return borders


def get_borders(borders):
    # This function takes the reads which are suspected to contain rearrangement breakpoints and extracts the CIGAR
    # strings. Then, the reads are returned BUT with ADJUSTED positions. These positions refer to the last (or first)
    # mapping read, depending on whether it matched initially or started matching somewhere along its length.

    bps = []
    for border in borders:
        cigar_str = border[4]
        temp_list = []
        for character in cigar_str:
            if character == "M":
                bps.append(temp_list)
                break
                # Honestly a pretty a cool piece of original code.
            elif character.isalpha() and character != "M":
                temp_list = ["-"]
            elif character.isdigit():
                if not temp_list:
                    temp_list.append(character)
                else:
                    temp_list.append("".join(character))

    matching = []
    for numbers in bps:
        matching.append("".join(numbers[0:]))

    breakpoints = []
    for m in enumerate(matching):
        if m[1].count("-") == 0:
            breakpoints.append([
                borders[m[0]][0], borders[m[0]][1] + int(m[1]), borders[m[0]][2], borders[m[0]][3], borders[m[0]][4],
                "+"
            ])
            # The "+ int(m[1])" shifts the position to the breakpoint instead of where the read starts.
            # For the reads that do match at the start (below), the position already refers to where the potential
            # breakpoints.
        else:
            breakpoints.append([
                borders[m[0]][0], borders[m[0]][1], borders[m[0]][2], borders[m[0]][3],
                borders[m[0]][4], "-"
            ])
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
            conf_borders.append(read)
        else:
            nonconf_borders.append(read)

    border_areas = []
    allowance = 10
    # Think about letting allowance change to be inversely proportional to the MAPQ score.
    counter = 0
    # counter to keep track of where we are in the list
    for border in conf_borders:
        # This loop groups the most confident borders by whether they are within a certain distance from one another.
        if not border_areas:
            border_areas.append([border])
        elif border[1] - allowance <= border_areas[counter][0][1] <= border[1] + allowance \
                and border[0] == border_areas[counter][0][0]:
            border_areas[counter].append(border)
        else:
            border_areas.append([border])
            counter += 1

    done = []
    for border in nonconf_borders:
        if border not in done:
            for cb in border_areas:
                # print(f"cb: {cb}")
                if border[1] - allowance <= cb[0][1] <= border[1] + allowance and border[0] == cb[0][0]:
                    border_areas[border_areas.index(cb)].append(border)
                    done.append(border)

    for border in nonconf_borders:
        if border not in done:
            border_areas.append([border])

    # print(border_areas)
    print(len(border_areas[0]) + len(border_areas[1]))

    return border_areas


def write_to_file(breakpoints, duplicated_reads):
    # This function writes the potential borders to a file (name specified at bottom of the script).
    # If there are duplicated reads (if Bowtie2 is in k-reporting mode), they will be appended to the end of the
    # output file, along with their occurrence.

    my_file = open(file_name, "w")
    if duplicated_reads is None:
        pass
    else:
        my_file.write(f"connected borders: \n")
        for dup in duplicated_reads:
            my_file.write(f"{dup}  \n")
            my_file.write("\n")
            
    #my_file.write(f"chromosome \t position \t read name \t MAPQ \t CIGAR string \n")
    my_file.write(f"\n")
    for area in breakpoints:
        my_file.write(f"{str(len(area))} ")
        #my_file.write("\n")
        my_file.write(f"{area[0]}")
        #for bp in area:
            #my_file.write(f"{bp[0]} \t \t {bp[1]} \t \t {bp[2]} \t \t {bp[3]} \t {bp[4]} \n")

        my_file.write("\n")
    
    my_file.close()


def find_duplicate_reads(breakpoints):
    for border in breakpoints:
        print(border)
    flat_borders = [border for x in breakpoints for border in x]
    read_names = [x[2] for x in flat_borders]
    duplicates = []
    print(read_names)
    for name in enumerate(read_names):
        if read_names.count(name[1]) > 1:
            duplicates.append(flat_borders[name[0]])
    duplicates.sort(key=lambda x: x[2])
    print(f"duplicates: {duplicates}")
    # This sorcery checks for reads mapping to more than one place
    grouped_borders = [list(x) for y, x in groupby(duplicates, lambda x: x[2])]
    print(grouped_borders)

    connected_borders = []
    for border in grouped_borders:
        connected_borders.append([border[0][0], border[0][1],
                                  border[1][0], border[1][1]])

    print(connected_borders)
    my_set = [tuple(x) for x in connected_borders]
    my_set = set(my_set)
    print(my_set)
    my_list = []
    for connection in my_set:
        my_list.append([connected_borders.count(list(connection)),
                        connection])

    print(my_list)
    if not grouped_borders:
        return None
    else:
        return my_list


if __name__ == "__main__":
    read_info = get_border_reads()
    find_breakpoints = get_borders(read_info)
    file_name = outname  # Desired name for output file
    refined_breakpoints = refine_breakpoints(find_breakpoints)
    dup_reads = find_duplicate_reads(refined_breakpoints)
    write_to_file(refined_breakpoints, dup_reads)

# Change the way the files are opened such that you use "with" instead of the current method.
