import pandas
import matplotlib as plt

df = pandas.DataFrame(columns=['time', 'input', 'output'])


# def per_sec(in_file):
#     for line in in_file:
#         line = line.split(',')
#         print(line)
# line = line.rstrip('\n')
# line = line.split(',')

# i += 1


with open('data.lvm', encoding='utf-8') as infile:
    i = 0
    while i in range(0, 10000):
        line = next(infile)
        line = line.rstrip('\n')
        line = line.split(',')
        df = df.append({'time': float(line[0]), 'input': float(line[1]), 'output': float(line[2])},
                       ignore_index=True)
        i += 1

print(df)

