A = [1, 3, 6 ,4 ,1 ,2, -1, 5, 10, -10, 8]



def solution(N):
    remain = N % 3
    repeats = N // 3

    print(remain)
    print(repeats)
    seq = ["+", "-", "-"]
    str1 = "+--" * repeats
    print(seq[remain-1], str1)
    while remain > 0:
        str1.join(seq[remain-1])
        print(str1)
        remain -= 1

    print(str1.join(seq[0]))


if __name__ == "__main__":

    my_list =(enumerate("+--", 70))
    print(my_list)