import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import scipy.io
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
rcParams['figure.figsize'] = 9,5
sns.set()
sns.set_style("ticks")
sns.set_context("paper")

matfiles= ['free--a970957_04-Dec-2018_13-16-25.mat',
           'P--a970957_04-Dec-2018_13-20-40.mat',
           'PD--a970957_04-Dec-2018_13-21-27.mat',
           'PDalpha--a970957_04-Dec-2018_13-22-17.mat']
titles = ['No Controller',
          'P-Controller',
          'PD-Controller',
          r'PD$\alpha$-Controller']

fig, axs = plt.subplots(4, 1, sharex=True)
fig.subplots_adjust(hspace=0.3)

for i, file in enumerate(matfiles):
    mat = scipy.io.loadmat(file)

    time = mat['theta']['time'][0][0]
    theta1 = mat['theta']['signals'][0][0][0][0][0]
    theta2 = mat['theta']['signals'][0][0][0][1][0]
    axs[i].plot(time, theta1, '--', linewidth='0.85', color='C1', label=r'$\theta_1$')
    axs[i].plot(time, theta2, linewidth='0.85', color='C0', label=r'$\theta_2$')

    axs[i].set_title(titles[i], loc='left', pad=0)
    axs[i].set_ylim([-40,40])
    axs[i].grid(axis='y')

sns.despine(trim=True)
axs[0].legend(framealpha=1)
for ax in axs[0:3]:
    ax.get_xaxis().set_visible(False)
    ax.spines['bottom'].set_visible(False)
plt.xlabel('Time [s]')

plt.savefig("../../figures/controller-comparison-plot.svg")
plt.savefig("../../figures/controller-comparison-plot.pdf")
plt.savefig("../../figures/controller-comparison-plot.png")