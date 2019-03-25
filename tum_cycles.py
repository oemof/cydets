import pandas as pd
import matplotlib.pyplot as plt

# data (comes from matlab since octaves' findpeaks does no work properly!)
df = pd.read_csv('results_A5_2026_TES.csv', index_col=0)
print(df)
df['duration'] = df['t3'] - df['t1']
df['amplitude'] = df['amplitude'] * 211.11  # scale back to nominal capacity

# plot scatter
ax = df.plot(kind='scatter', x='duration', y='amplitude', grid=True)
ax.set_axisbelow(True)
ax.set_xlabel('Period length (h)')
ax.set_ylabel('Amplitude (MWh)')
plt.savefig('scatterplot.pdf', format='pdf', dpi=600)
plt.close()

# plot histogram for amplitude
ax = df['amplitude'].plot(kind='hist', bins=30, grid=True)
ax.set_axisbelow(True)
ax.set_title('30 bins, n=' + str(len(df)))
ax.set_xlabel('Amplitude (MWh)')
ax.set_ylabel('Frequency')
plt.savefig('histogram_amplitude.pdf', format='pdf', dpi=600)
plt.close()

# plot histogram for duration
ax = df['duration'].plot(kind='hist', bins=30, grid=True)
ax.set_axisbelow(True)
ax.set_title('30 bins, n=' + str(len(df)))
ax.set_xlabel('Duration (h)')
ax.set_ylabel('Frequency')
plt.savefig('histogram_duration.pdf', format='pdf', dpi=600)
plt.close()
