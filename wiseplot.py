##################################################
# Vanessa Moss 08/11/2015
# Paper credit: Wright et al (2010)
# Image credit: Chao-Wei Tsai
##################################################

import os
import sys
from math import *
from numpy import *
import matplotlib.pyplot as plt
from matplotlib import rc
#rc('text', usetex=True)
#rc('font',**{'family':'STIXGeneral', 'size':18})
rc('font',**{'family':'serif','serif':['serif'],'size':20})
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage,AnnotationBbox
from matplotlib.cbook import get_sample_data
from astropy.io import ascii

##################################################

# Convert from WISE colours to plot position
# DO NOT CHANGE!
def wise2pix(x,y):

    # Convert x coordinate
    # Formula: x - xmin/(xmax-xmin)
    xnorm = (x - -1) / float(7 - -1)

    # Convert y coordinate
    # Formula: y - ymin/(ymax-ymin)
    ynorm = (y - -0.5) / float(4 - -0.5)

    return xnorm,ynorm

##################################################

# Define column headings
# SET THESE BEFORE RUNNING THE CODE IF THEY ARE DIFFERENT TO DEFAULTS
# Defaults: ['W1','W2','W3'] and ['W1err','W2err','W3err']
wise1,wise2,wise3 = ['w1mpro','w2mpro','w3mpro']
werr1,werr2,werr3 = ['w1sigmpro','w2sigmpro','w3sigmpro']

# Options
ploterr = True # Toggle for plotting errors
print('Plotting of errors is set to... %s' % ploterr)

# For labelling figure output
if ploterr == True:
    perr = 'err_'
else:
    perr = ''

# Read file
try: 
    filename = sys.argv[1]
    print('Reading from file... %s' % filename)
except:
    print('No filename specified! Using example...')
    filename = 'example.txt'
fname = '.'.join(filename.split('.')[0:-1])

# Read data
d = ascii.read(filename)
print()
print('Number of sources:',len(d))
print()

# Check for user-defined column headings:
try:
    print('Data:',wise1,wise2,wise3)
    if ploterr == True:
        print('Errors:',werr1,werr2,werr3)
    print('... specified column headings detected!')

except:
    print('You have not defined column headings, so I will assume the defaults...')
    wise1,wise2,wise3 = ['W1','W2','W3']
    print('Data:',wise1,wise2,wise3)
    if ploterr == True:
        werr1,werr2,werr3 = ['W1err','W2err','W3err']    
        print('Errors:',werr1,werr2,werr3)

# Create columns
try:
    w1 = d[wise1]
    w2 = d[wise2]
    w3 = d[wise3]
except:
    print('Fatal error: could not find specified column headings... quitting!')
    sys.exit()

# Errors
if ploterr == True:
    w1e = d[werr1]
    w2e = d[werr2]
    w3e = d[werr3]

##################################################

# WISE background plot (Wright et al 2010)
## DO NOT CHANGE!
print
print('Setting up plot...')
ratio = 1.11#1.065
xdim = 8
ydim = xdim*ratio
plt.figure(figsize=(xdim,ydim))
ax = plt.gca()

# Redo x-labels
xticks = arange(-1,8,1)
xact = linspace(0,1,9)
xlabs = [str(x) for x in xticks]
xlab = [xlabs[1],xlabs[3],xlabs[5],xlabs[7]]
xtix = [xact[1],xact[3],xact[5],xact[7]]
ax.set_xticks(xtix)
ax.set_xticklabels(xlab)

# Redo y-labels
yticks = arange(-0.5,4.5,0.5)
yact = linspace(0,1,10)
ylabs = [str(int(y)) for y in yticks]
ylab = [ylabs[1],ylabs[3],ylabs[5],ylabs[7],ylabs[9]]
ytix = [yact[1],yact[3],yact[5],yact[7],yact[9]]
ax.set_yticks(ytix)
ax.set_yticklabels(ylab)

# Set the axis limits
plt.xlim(0,1)
plt.ylim(0,1)

# Incorporate the background image
sfig = 'wright2010data.png'
arr_lena = plt.imread(sfig)
imagebox = OffsetImage(arr_lena, zoom=0.27)
ab = AnnotationBbox(imagebox, [0.5,0.5],
                    xybox=(0., 0.),
                    xycoords='data',
                    boxcoords="offset points",
                    frameon=False)
ax.add_artist(ab)

##################################################

# Plot
print('Plotting data...')
(x,y) = wise2pix(w2-w3,w1-w2)

# Scatter plot
# Change plotting parameters of data here if needed
plt.scatter(x,y,facecolor='r',marker='o',s=10,zorder=101,alpha=1.0,linewidth=0.5)

# Error plot
if ploterr == True:
    w12e = sqrt(w1e**2+w2e**2)
    w23e = sqrt(w3e**2+w2e**2)
    (xe,ye) = wise2pix((w2-w3)+w23e,(w1-w2)+w12e)
    xe1 = xe-x
    ye1 = ye-y
    plt.errorbar(x,y,xerr=xe1,yerr=ye1,fmt='None',zorder=100,ecolor='k')

# Labels
plt.xlabel('[ 4.6 ] - [ 12 ] in mag')
plt.ylabel('[ 3.4 ] - [ 4.6 ] in mag')

# Text credit 
# DO NOT REMOVE!
plt.text(0.995,1.01,'Image credit: Chao-Wei Tsai; from Wright et al. 2010',fontsize=8,horizontalalignment='right')

##################################################

# NOTE: DISPLAYED FIGURE IS SCALED WRONG
# SAVED PDF IS SCALED CORRECTLY!
print('Saving figure...')
plt.savefig('%s_%sallwise.pdf' % (fname,perr),dpi=200,bbox_inches='tight')
print()
print('... done!')

