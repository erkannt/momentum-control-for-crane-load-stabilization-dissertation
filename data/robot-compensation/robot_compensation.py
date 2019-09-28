import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import scipy.io
from math import pi
import os, sys

""" Use passed args as savepath, otherwise only show plots """
workdir, _ = os.path.split(os.path.abspath(__file__))
if len(sys.argv) == 1:
    output = False
else:
    output = os.path.abspath(sys.argv[1])
os.chdir(workdir)


def output_figure(output):
    sns.despine(trim=True, offset=2)
    plt.tight_layout()
    if output:
        plt.savefig(output)
    else:
        plt.show()


def fmt_axcol(axs):
    for ax in axs:
        ax.grid(axis="y")
        ax.set_ylabel("X Pos [m]")
    for ax in axs[0:-1]:
        ax.get_xaxis().set_visible(False)
        ax.spines["bottom"].set_visible(False)
    axs[-1].set_xlabel("Time [s]")
    axs[0].legend(loc=1, framealpha=1)
    # fig.subplots_adjust(hspace=0.6)


plt.rc('text', usetex=True)
rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    # helvetica font
    r'\usepackage{sansmath}',   # math-font matching  helvetica
    r'\sansmath'                # actually tell tex to use it!
    r'\usepackage{siunitx}',    # micro symbols
    r'\sisetup{detect-all}',    # force siunitx to use the fonts
]
rcParams['figure.figsize'] = 9,4
sns.set()
sns.set_style("ticks")
sns.set_context("paper")

no_comp_data = scipy.io.loadmat('no_comp__convertedTimeseries.mat')
with_comp_data = scipy.io.loadmat('with_comp__convertedTimeseries.mat')

titles = [r'Without Compensation',
          r'With CMGs informed by robot model']

fig, axs = plt.subplots(2, 1, sharex=True)

for i, (ax, data, title) in enumerate(zip(axs, [no_comp_data, with_comp_data], titles)):
    time = data['time']
    x_target = data['tool_pos_fixed_robot_X']
    x_sim = data['tool_pos_pendulum_robot_X']
    ax.plot(time, x_target, '--', linewidth='0.85', color='C1', label=r'Fixed Robot')
    ax.plot(time, x_sim, linewidth='0.85', color='C0', label=r'Attached to Pendulum')
    ax.set_title(title, loc='left', pad=0)

fmt_axcol(axs)
output_figure(output)
