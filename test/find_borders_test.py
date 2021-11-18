import numpy as np

from class_SAM import SAM

file = SAM()
filepath = 'exp7_2.sorted.sam'
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
        if read[1] == "100M":
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

    # print(matching)
    # print(len(matching))

    breakpoints = []
    for m in enumerate(matching):
        if m[1].count("-") == 0:
            breakpoints.append([
                borders[m[0]][0], borders[m[0]][1] + int(m[1]), borders[m[0]][2], borders[m[0]][3], borders[m[0]][4]
            ])

        else:
            breakpoints.append([
                borders[m[0]][0], borders[m[0]][1] + read_len + int(m[1]), borders[m[0]][2], borders[m[0]][3],
                borders[m[0]][4]
            ])

    print(breakpoints)
    return breakpoints


def write_to_file(breakpoints):
    my_file = open(file_name, "w")
    my_file.write(f"chromosome \t position \t read name \t MAPQ \t CIGAR string \n")
    for bp in breakpoints:
        my_file.write(f"{bp[0]} \t \t {bp[1]} \t \t {bp[2]} \t \t {bp[3]} \t {bp[4]} \n")


if __name__ == "__main__":
    read_info = get_border_reads()
    find_breakpoints = get_borders(read_info)
    file_name = "exp7_2.txt"  # Desired name for output file
    write_to_file(find_breakpoints)
