# import sys

sAB = "sAB.txt"
sBA = "sBA.txt"
mAB = "mAB.txt"
mBA = "mBA.txt"
genome_a = []
genome_b = []


def extract_borders(file_name):
    with open(file_name, "r") as f:
        borders = []
        sab_lines = f.read()
        border_groups = sab_lines.split(">")
        border_groups = border_groups[1:]
        border_groups = [x.split("\n") for x in border_groups]
        for i in border_groups:
            temp_list = []
            for j in i:
                if j != "":
                    temp_list.append(j.split("\t"))
            borders.append(temp_list)
        return borders


def get_connected_borders(file_name):
    with open(file_name, "r") as f:
        connected_borders = []
        temp_list = f.readlines()
        for i in temp_list:
            i = i.replace("\n", "")
            # Pick up here:
            j = [int(i[0]), list(i[1])]
            connected_borders.append(i.split("\t"))
    return connected_borders




if __name__ == "__main__":
    ab = extract_borders(sAB)
    print(ab)
    print(get_connected_borders(mAB))
