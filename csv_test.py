import pandas
import matplotlib.pyplot as plt
import numpy as np

df = pandas.read_csv('goodluck.csv', header=None, sep=";")
print(df)
# N = 10000
# T = 0.0001
# x = df[0]
# y = df[1]
# yf = scipy.fftpack.fft(y)
# xf = x

# fig, ax = plt.subplots()
# ax.plot(xf, 2.0/N * np.abs(yf[:N]))
# plt.show()

# f = 10  # Frequency, in cycles per second, or Hertz
f_s = 10000  # Sampling rate, or number of measurements per second

t = df[0]

x = df[1]

fig, ax = plt.subplots()
ax.plot(t, x)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Signal amplitude');

plt.show()

from scipy import fftpack

X = fftpack.fft(x)
print(X)


freqs = fftpack.fftfreq(len(x)) * f_s

fig, ax = plt.subplots()

ax.stem(freqs, np.abs(X))
ax.set_xlabel('Frequency in Hertz [Hz]')
ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
# ax.set_xlim(-f_s / 2, f_s / 2)
# ax.set_ylim(-5, 110)

plt.show()
