import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import scipy.io
from math import pi
import os

workdir, _ = os.path.split(os.path.abspath(__file__))
os.chdir(workdir)

plt.rc('text', usetex=True)
rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    # helvetica font
    r'\usepackage{sansmath}',   # math-font matching  helvetica
    r'\sansmath'                # actually tell tex to use it!
    r'\usepackage{siunitx}',    # micro symbols
    r'\sisetup{detect-all}',    # force siunitx to use the fonts
]  
sns.set()
sns.set_style("ticks")
sns.set_context("paper")

matfile = 'DP-full-theta-dump--f4a4f2c_17-Dec-2018_12-26-04__convertedTimeseries.mat'

titles = [r'Position [deg]',
          r'Velocity [rad/s]',
          r'Acceleration [rad/s$^2$]']
varnames = ['theta',
          'dtheta',
          'ddtheta']

fig, axs = plt.subplots(3, 1, sharex=True)
fig.subplots_adjust(hspace=0.3)

mat = scipy.io.loadmat(matfile)

for i, ax in enumerate(axs):
    time = mat['time']
    data = []
    theta1 = mat[varnames[i] + '1']
    theta2 = mat[varnames[i] + '2']
    if i == 0:
        theta1, theta2 = theta1 * 180 / pi, theta2 * 180 / pi
    ax.plot(time, theta1, '--', linewidth='0.85', color='C1', label=r'$m_1$')
    ax.plot(time, theta2, linewidth='0.85', color='C0', label=r'$m_2$')

    ax.set_title(titles[i], loc='left', pad=0)
    ax.grid(axis='y')

sns.despine(trim=True)
axs[0].legend(loc=1, framealpha=1)
for ax in axs[0:2]:
    ax.get_xaxis().set_visible(False)
    ax.spines['bottom'].set_visible(False)
plt.xlabel('Time [s]')

plt.savefig("../../figures/dp-oscillations.svg")
plt.savefig("../../figures/dp-oscillations.pdf")
plt.savefig("../../figures/dp-oscillations.png")