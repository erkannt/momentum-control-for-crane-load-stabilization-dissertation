import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import scipy.io
from math import pi
import os, sys

workdir, _ = os.path.split(os.path.abspath(__file__))
output = os.path.abspath(sys.argv[1])
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

fastgyros = {'matfile' : 'Gimbal-Limit-5000rpm--f4a4f2c_17-Dec-2018_12-01-43__convertedTimeseries',
             'title' : 'SPCMG Singularity Avoidance w. 5000 rpm Gyros'}

datasets = [fastgyros]

titles = [r'Pendulum Angle $\theta$ [deg]',
          r'CMG Torque $\tau$ [Nm]',
          r'Gimbal Velocity $\dot\delta$ [rad/s]',
          r'Gimbal Position $\delta$ [deg]',
         ]
varnames = [['theta1', 'theta2'],
            ['tau_W', 'tau'],
            ['ddelta_W', 'ddelta_Wprime', 'ddelta'],
            ['delta', 'delta_neg'],
           ]
labels = [[r'$\theta_1$', r'$\theta_2$'],
          ['Target', 'Achieved'],
          ['Initial Target', 'Set Target', 'Achieved'],
          [r'$\delta_1$', r'$\delta_2$'],
         ]
colors = ['C0', 'C1', 'C2']
linetypes = ['-', '--', '-.']
ylims = [[-20, 20], [-3, 3], [-10, 10], [-100, 100]]

for ds in datasets:
    fig, axs = plt.subplots(4, 1, sharex=True)
    fig.subplots_adjust(hspace=0.6)

    mat = scipy.io.loadmat(ds['matfile'])
    time = mat['time']
    for radval in ['theta1', 'theta2', 'delta']:
        mat[radval] *= 180 / pi
    mat['delta_neg'] = mat['delta'] * -1

    for i, ax in enumerate(axs):
        for j, varname in enumerate(varnames[i]):
            ax.plot(time, mat[varname],
                    linetypes[len(varnames[i])-j-1],
                    color=colors[len(varnames[i])-j-1],
                    label=labels[i][j],
                    linewidth='0.85')

        if len(ylims[i]) == 2:
            ax.set_ylim(ylims[i])
        ax.set_xlim([0, 15])
        ax.set_title(titles[i], loc='left')
        ax.legend(loc=1, framealpha=1)
        ax.grid(axis='y')

    #sns.despine(trim=True, offset={'left':2,'right':2,'top':2,'bottom':2})
    sns.despine(trim=True, offset=5)
    for ax in axs[0:-1]:
        ax.get_xaxis().set_visible(False)
        ax.spines['bottom'].set_visible(False)
    plt.xlabel('Time [s]')
    fig.suptitle(ds['title'])

    plt.savefig(output)