import pandas
import matplotlib.pyplot as plt
import numpy as np

# plt.style.use('style/elegant.mplstyle')

df = pandas.DataFrame(columns=['time', 'output'])

with open('data_350_450.lvm', encoding='utf-8') as infile:
    i = 3500000
    while i in range(3500000, 4500000):
        line = next(infile)
        line = line.rstrip('\n')
        line = line.split(',')
        df = df.append({'time': i, 'output': float(line[1])}, ignore_index=True)
        print("time: ", i)
        i += 1

t = df['time']
x = df['output']

fig, ax = plt.subplots()
ax.plot(t, x)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Signal amplitude');

plt.show()

# f_s = 10000
#
# from scipy import fftpack
#
# X = fftpack.fft(x)
# freqs = fftpack.fftfreq(len(x)) * f_s
#
# fig, ax = plt.subplots()
#
# ax.stem(freqs, np.abs(X))
# ax.set_xlabel('Frequency in Hertz [Hz]')
# ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
#
# plt.show()
