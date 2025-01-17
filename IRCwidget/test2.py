from scipy.signal import butter, sosfreqz
import numpy as np
import matplotlib.pyplot  as plt

SAMPLE_RATE = 44100
CUT_OFF_F = 20000

nyq=SAMPLE_RATE/2
norm_cut_f = CUT_OFF_F/nyq
sos = butter(10, norm_cut_f, output='sos')
w, h = sosfreqz(sos, worN = 2000)
f = w*(SAMPLE_RATE/(np.pi*2))
plt.plot(f, abs(h))
plt.show()
