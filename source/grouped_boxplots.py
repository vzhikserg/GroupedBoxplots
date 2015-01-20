"""
Script for visualisation of grouped boxplots
"""

import csv
import matplotlib.pyplot as plt
from collections import defaultdict
from pylab import plot, show, xlim, xlabel, ylabel,\
                ylim, legend, boxplot, setp

### BEGIN PARAMETERS ###
# sources of information to display
fileNames = ["../samples/grouped_boxplots_1.csv", "../samples/grouped_boxplots_2.csv"]

# parameters for the y axis
miny = 0
maxy = 100

# the set of strings to appear in the legend
legendDesc = ["First measurement", "Second measurement"]

# the set of colors to draw lines
colors = ['blue','red','green','cyan','magenta','yellow','black']

# do you need markers at all?
needMarker = True
# all possible markers http://matplotlib.org/api/markers_api.html
markers = [ 'o', 'v', 's', '4', '+', ',', '.']
# the marker size
msize = 4.15

# name of the x axis
xname = "Candy"
# name of the y axis
yname = "Some values"

### END PARAMETERS ###

def loadData(fileNames):
    """ 
    loads necessary data from csv file(s)
    """    
    data = []        
    for fileName in fileNames:
        with open(fileName, "rt") as csvfile:    
            dataserie = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
            # a dictionary whose value defaults to a list.
            grouped_data = defaultdict(list)
            # loop to fill the dictionary
            for i, row in enumerate(dataserie):
                # skip the header line and any empty rows
                # we take advantage of the first row being indexed at 0
                # i=0 which evaluates as false, as does an empty row
                if not i or not row:
                    continue
                # unpack the columns into local variables
                group, value = row            
                # group fitness values by popsize
                grouped_data[str(group)].append(float(value))
            # add dictionary to data
            data.append(grouped_data)
    return data

def setBoxColors(bp, num): 
    """
    sets the colors of the box plots pairs
    """
    m=0
    for i in range(0, num):
        setp(bp['boxes'][i], color=colors[i])    
        setp(bp['caps'][2*i], color=colors[i])
        setp(bp['caps'][2*i+1], color=colors[i])
        setp(bp['whiskers'][2*i], color=colors[i])
        setp(bp['whiskers'][2*i+1], color=colors[i])
        setp(bp['fliers'][2*i], color=colors[i])
        setp(bp['fliers'][2*i+1], color=colors[i])
        if needMarker:
            setp(bp['medians'][i], color=colors[i], \
                 marker=markers[m], markersize=msize)
        else:
            setp(bp['medians'][i], color=colors[i])
        m=m+1

def createBoxplot(data, legendDesc=[], fileName='', xname='', yname=''):
    """
    creates the boxplots
    """
    keys = sorted(data[0].keys())
    centerKeyPositions = []
    i=2
    for key in keys:
        toVisualize = []
        boxPositions = []
        for dataSet in data:
            toVisualize.append(dataSet.get(key))
            boxPositions.append(i)
            i=i+1            
        bp = boxplot(toVisualize, positions = boxPositions, widths = 0.7)
        centerKeyPositions.append(float(sum(boxPositions))/len(boxPositions))
        setBoxColors(bp,len(data))
        i=i+2
    ax = plt.gca()    
    ax.set_xticklabels(keys)
    ax.set_xticks(centerKeyPositions)
    xlim(0,i)
    ylim(miny,maxy) 
    if (xname!=''):
        xlabel(xname)
    if (yname!=''):
        ylabel(yname)
    
    # display legend
    if len(legendDesc)!=0:
        # draw temporary lines and use them to create a legend
        invisibleLines = []
        for i in range(0, len(data)):
            if needMarker:            
                hL, = plot([1,1],color=colors[i], linestyle='-', \
                       marker=markers[i], markersize=msize)
                invisibleLines.append(hL)
            else:
                hL, = plot([1,1],color=colors[i], linestyle='-')
                invisibleLines.append(hL)
        # first we draw legend        
        legend(invisibleLines,legendDesc, loc='upper center', \
               ncol=len(data) ,fontsize=12)
        # then we make the temporary lines invisible
        for l in invisibleLines:
            l.set_visible(False) 
    

extractedData = loadData(fileNames)
createBoxplot(extractedData, legendDesc, xname=xname, yname=yname)
show()
# uncomment the next line if you want to save the figure ('pdf', 'png', ...)
#savefig("somefilename.pdf",  format='pdf')
