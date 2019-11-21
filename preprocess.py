in_file = open('data.lvm', 'r', encoding='utf-8')
out_file = open('data_test.lvm', 'w+', encoding='utf-8')
counter = 0
while 0 <= counter <= 734:
    line = next(in_file)
    line = line.split(',')
    new_line = [counter, float(line[1])]
    print(counter)
    print(new_line)
    out_file.write("{} {}\n".format(new_line[0], new_line[1]))
    counter += 0.0001

in_file.close()
out_file.close()
