
# Here I will test a class method for further manipulating the borders

class ContBlock:
    def __init__(self, pos, chrom, read_name, score):
        self.pos = pos
        self.chrom = chrom
        self.read_name = read_name
        self.score = score


a = ContBlock(1, 'gi|9626243|ref|NC_001416.1|', 'r1', '44')

print(a.pos)
