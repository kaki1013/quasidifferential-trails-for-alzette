def get_freq(filename):
    d = dict()
    with open(filename, "r") as f:
        arr = [line for line in f.readlines() if 'Weight' in line]

        for line in arr:
            l, r = line.index(':'), line.index('[')

            weight, sign = int(line[l+1:r].strip()), int(line[r+1:r+3].strip())
            tmp = (weight, sign)

            if tmp in d:
                d[tmp] += 1
            else:
                d[tmp] = 1

    return d


weight = 39
num = 7
for idx in range(num):
    filename = f"{weight}/diff_{idx}_weight_{weight}.txt"
    # filename = f"diff_{idx}_weight_{weight}.txt"
    d = get_freq(filename)

    d = sorted(list(d.items()), key=lambda x: (x[0][0], -x[0][1]))
    # d = sorted(list(get_freq(filename)), key=lambda x: (x[0], -x[1]))
    d = list(map(lambda x:((x[0][0]+6, x[0][1]), x[1]), d))
    print(idx, d)

