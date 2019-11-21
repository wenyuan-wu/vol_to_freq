import sys


infile = sys.argv[1]
skip = int(sys.argv[2])

outfile = "outputdata.txt"

in_file = open(infile, 'r', encoding='utf-8')
out_file = open(outfile, 'w+', encoding='utf-8')
counter = 0
while True:
    skip_counter = 0
    while 0 <= skip_counter <= skip:
        next(in_file)
        skip_counter += 1
    
    
    line = next(in_file)
    line = line.split(',')
    new_line = [counter, float(line[1])]
    print("Current entries: {} {}".format(counter, new_line[1]))
    
    out_file.write("{} {}\n".format(new_line[0], new_line[1]))
    counter += 0.0001

in_file.close()
out_file.close()
