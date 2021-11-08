
# Here I will test a class method for further manipulating the borders

class Block:
    def __init__(self, pos, chrom, read_name, score):
        self.pos = pos
        self.chrom = chrom
        self.read_name = read_name
        self.score = score


a = Block(1, 'Chr2', 'r1', '44')
b = Block(1501, 'Chr2', 'r16', '25')


print(a.pos)

print(b.chrom)
