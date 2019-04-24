import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import scipy.io
from math import pi
import os, sys

workdir, _ = os.path.split(os.path.abspath(__file__))
outputdir = os.path.abspath(sys.argv[1])
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

colors = ['C0', 'C1', 'C2', 'C3']
linetypes = ['-', '--', '-.', ':']
outputtypes = ['pdf', 'svg', 'png']

torquecomponents = {'matfile' : '165ad54_pmdpspcm_24-Jan-2019_13-32-16__convertedTimeseries.mat',
             'title' : 'Torque Components of Single CMG',
             'svgname' : 'cmg-torque-components-plot'}
datasets = [torquecomponents]

titles = [r'CMG Torque Component Magnitude [Nm]',
          r'Gimbal Torque Components Magnitude [Nm]',
          r'System Motion [deg]',
         ]
varnames = [['tau_cmg_norm', 'tau_reaction_norm'],
            ['tau_gimbal_norm', 'tau_reaction_gimbal_norm'],
            ['theta2', 'delta'],
           ]
labels = [[r'CMG Output (Gyro x Gimbalrate)', r'Reaction Torque (Gyro x Baserate)'],
          ['Rotation Torque (Gimbalassembly Inertia)', 'Reaction Torque (Gimbal x Baserate)'],
          [r'Plattform Angle $\theta_2$', r'Gimbal Angle $\delta$'],
         ]
ylims = [[],
         [0, 0.1],
         [-100, 100],
        ]
xlims = [0, 15]

for ds in datasets:
    fig, axs = plt.subplots(len(titles), 1, sharex=True)
    fig.subplots_adjust(hspace=0.6)

    mat = scipy.io.loadmat(ds['matfile'])
    time = mat['time']
    for radval in ['theta1', 'theta2', 'delta']:
        mat[radval] *= 180 / pi
    for tauval in ['tau_cmg',
                   'tau_reaction',
                   'tau_reaction_gimbal',
                   'tau_gimbal']:
        mat[tauval+'_norm'] = np.linalg.norm(mat[tauval][:,0,:], axis=0)
    for i, ax in enumerate(['x', 'y', 'z']):
        mat['tau_base_'+ax] = mat['tau_base_i'][i, 0, :].T
    mat['tau_motor_1'] = mat['tau_motor'][:,0,:].T
    mat['delta_neg'] = mat['delta'] * -1
    mat['tau_W'] /= 2


    for i, ax in enumerate(axs):
        for j, varname in enumerate(varnames[i]):
            ax.plot(time, mat[varname],
                    linetypes[j],
                    color=colors[j],
                    label=labels[i][j],
                    linewidth='0.85')

        if len(ylims[i]) == 2:
            ax.set_ylim(ylims[i])
        ax.set_xlim(xlims)
        ax.set_title(titles[i], loc='left')
        ax.legend(loc=1, framealpha=1)
        ax.grid(axis='y')

    #sns.despine(trim=True, offset={'left':2,'right':2,'top':2,'bottom':2})
    sns.despine(trim=True, offset=2)
    for ax in axs[0:-1]:
        ax.get_xaxis().set_visible(False)
        ax.spines['bottom'].set_visible(False)
    plt.xlabel('Time [s]')
    suptitle = fig.suptitle(ds['title'], y=1.02)
    plt.tight_layout()

    for ftype in outputtypes:
        plt.savefig('%s/%s.%s' % (outputdir, ds['svgname'], ftype),
                    bbox_extra_artists=(suptitle,), bbox_inches="tight")
