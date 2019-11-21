import pandas
import matplotlib.pyplot as plt
import numpy as np

# plt.style.use('style/elegant.mplstyle')

# df = pandas.DataFrame(columns=['time', 'output'])
df = []
with open('data.lvm', encoding='utf-8') as infile:
    i = 0
    while i in range(0, 10000):
        line = next(infile)
        line = line.rstrip('\n')
        line = line.split(',')
        df.append((i, float(line[1])))
        # df = df.append({'time': i, 'output': float(line[1])}, ignore_index=True)
        print("time: ", i)

        i += 1
#
# t = df['time']
# x = df['output']
# print(df)

t = [i[0] for i in df]
x = [j[1] for j in df]

fig, ax = plt.subplots()
ax.plot(t, x)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Signal amplitude');

plt.show()


f_s = 10000

from scipy import fftpack

X = fftpack.fft(x)

# freqs = fftpack.fftfreq(len(x)) * f_s
#
# fig, ax = plt.subplots()
#
# ax.stem(freqs, np.abs(X), use_line_collection=True)
# ax.set_xlabel('Frequency in Hertz [Hz]')
# ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
#
# plt.show()
