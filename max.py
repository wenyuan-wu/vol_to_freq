max = 0
with open('data.lvm', encoding='utf-8') as infile:
    for line in infile:
        line = line.rstrip('\n')
        line = line.split(',')
        num = float(line[1])

        if num >= max:
            max = num
            print(max)
print(max)