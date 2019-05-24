import os, sys
import scipy.io
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

""" Use passed args as savepath, otherwise only show plots """
workdir, _ = os.path.split(os.path.abspath(__file__))
if len(sys.argv) == 1:
    output = False
else:
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

target = {'matfile' : 'GiMRate6-target-200Hz__convertedTimeseries.mat',
          'title' : 'Target'}
real = {'matfile' : 'GiMRate6-Real-200Hz__convertedTimeseries.mat',
          'title' : 'Real'}
sim = {'matfile' : 'GiMRate6-200Hz__convertedTimeseries.mat',
          'title' : 'Simulated'}


datasets = [real, sim, target]

colors = ['C0', 'C1', 'C2']
linetypes = ['-', '--', '-.']

for ds, col, lt in zip(datasets, colors, linetypes):
    mat = scipy.io.loadmat(ds['matfile'])
    plt.plot(mat['time'], mat['data'],
             lt, color=col,
             label=ds['title'],
             )

#sns.despine(trim=True, offset={'left':2,'right':2,'top':2,'bottom':2})
sns.despine(trim=True, offset=5)
plt.xlabel('Time [s]')

plt.show()

#plt.savefig(output)