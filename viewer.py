#!python3

# import libraries, ...
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# global variables
current_profile_figure = 2
current_history_figure = 1
profile_figure_list = [2]

def data(f, get_header = True):
    ''' Read the file "f" and interpret it as a profile and return the data
    with the header if get_header == True. '''
    d = pd.read_csv(f, sep=" +", header=5)
    if get_header:
        h= pd.read_csv(f, sep= " +", header=1, nrows = 1)
        return (d,h)
    else:
        return d

def init_figure(num):
    ''' Initialize the figure `num`.'''
    fig = plt.figure(num)
    ax  = fig.add_subplot(111)
    ax.set_xlabel(p_axes[0])
    ax.set_ylabel(p_axes[1])
    ax.legend()
    ax.grid()

def onkeypress(event, key):
    ''' Handle the mouse events sent to the history figure.'''
    global current_profile_figure, profile_figure_list
    key[0] = event.key
    if event.key == "ctrl+b":
        plt.close()
        print("Reset figure 2")
        init_figure(current_profile_figure)
        
    elif event.key == "ctrl+n":
        # if this figure is the last one, add a new one
        if current_profile_figure == profile_figure_list[-1]:
            # add the figure to the list
            profile_figure_list.append(current_profile_figure+1)
            # initialize the figure
            init_figure(current_profile_figure + 1)

        # switch to the next figure
        current_profile_figure += 1
        
        print("Jumping to figure %d" % current_profile_figure)
        
    elif event.key == "ctrl+p":
        # if we are at the first one, jump to the last one
        if current_profile_figure == profile_figure_list[0]:
            current_profile_figure = profile_figure_list[-1] + 1
            
        # switch to the previous figure
        current_profile_figure -= 1
    
        print("Jumping to figure %d" % current_profile_figure)         
        
        
    
def onclick(event, hist, xax, yax, profile_index, p_axes):
    ''' Get an right click, an history file, the x and y axis (for the
    history plot), the profile_index array and the profile axes.
    Add the profile to the current profile plot.'''

    if not event.button == 3:
        return
    
    # try to find the profile that is the closest to that position
    x, y = event.xdata, event.ydata

    # find the data point closest top point clicked
    dist = 0
    index = 0
    # iterate over all lines in the history file to find closest point
    for _x, _y, i in zip(hist.get(xax),
                         hist.get(yax),
                         range(hist.shape[0])):
        _dist = (x-_x)**2 + (y-_y)**2
        if _dist < dist or dist == 0: 
            dist = _dist
            index = i
            
    # get the model number
    model_number = hist.model_number[index]
    print("Loading model %d ..." % model_number)

    # find the closest profile through profile_index
    dist = 0
    ibest = 0
    # first column : model number
    for i in range(profile_index.shape[0]):
        _dist = abs(model_number - profile_index[i,0])
        # if we have a new dist
        if _dist <= dist or dist == 0:
            dist = _dist
            ibest = i
        # else we are going away from the solution, break!
        else:
            break
    profile_number = profile_index[ibest,2]

    # load the profile
    p, h = data(os.path.join(directory, "profile%d.data" % profile_number))

    print("... loaded")

    # get columns to plot
    p_axes = ("mass", "omega")
    
    # plot the profile
    fig2 = plt.figure(current_profile_figure)
    if key[0] == "control":
        print("Clearing figure")
        fig2.clear()
    
    ax2 = fig2.add_subplot(111)

    ax2.plot(p.get(p_axes[0]), p.get(p_axes[1]),
             label="$t= %e, \mathrm{model} = %d$" % (h.star_age, h.model_number))
    ax2.set_xlabel(p_axes[0])
    ax2.set_ylabel(p_axes[1])
    ax2.legend()
    fig2.show()

def ask_for_columns(data, x="", y=""):
    print("".join([ col + ", " for col in data.columns]))

    xform = x
    yform = y
    # xform (resp. yform) are either "" or [somevalue]
    if x != "":
        xform = "[" + x + "]"
    if y != "":
        yform = "[" + y + "]"
    
    xaxis = input("\tx-axis %s? " % xform)
    # if no answer but there is a default answer (in "x")
    if not xaxis and x:
        xaxis = x
        
    while xaxis not in data.columns:
        if xaxis == "?" :
            print("".join([ col + ", " for col in data.columns]))
        xaxis = input("\tx-axis (? for list)%s? " % xform)
        # if no answer but there is a default answer
        if not xaxis and x:
            xaxis = x

    yaxis = input("\ty-axis %s? " % yform)
    # if no answer but there is a default answer
    if not yaxis and y:
        yaxis = y
        
    while yaxis not in data.columns:
        if yaxis == "?":
            print("".join([ col + ", " for col in data.columns]))
        yaxis = input("\ty-axis (? for list)%s? " %yform)
        # if no answer but there is a default answer
        if not yaxis and y:
            yaxis = y        

    return xaxis, yaxis

if __name__ == "__main__":

    ##################################################
    # User input
    ##################################################

    #######################################
    # work directory
    #######################################
    def_dir = "/home/ccc/hyades/pfs/simulations/M=1.3_thermo/C=50/LOGS_RGB"
    directory = os.path.expanduser(input("Please pick a directory [%s]: " % def_dir))
    if not directory:
        directory = def_dir
    while not os.path.isdir(directory):
        print("%s is not a directory." % directory)
        directory = os.path.expanduser(input("Please pick a directory : "))

    # list the directory
    ls = os.listdir(directory)

    #######################################
    # history profile : reading
    #######################################
    hist, h_hist = data(os.path.join(directory, "history.data"))

    #######################################
    # profiles index : reading
    #######################################    
    f = open(os.path.join(directory, "profiles.index"), "r")
    # ommit the first line of the profile index
    f.readline()
    # read the whole index and save it in an array
    profile_index = np.array(
        [ [ int(e) for e in line.split() ] for line in f.readlines() ])
    
    #######################################
    # history profile : axes to plot
    #######################################
    print()
    print("#"*50)
    print("# Axis available for history plot")
    print()
    xaxis, yaxis = ask_for_columns(hist, "star_age", "log_L")

    #######################################
    # profile: axes to plot
    #######################################
    p = data(os.path.join(directory, "profile1.data"), get_header=False)
    print()
    print("#"*50)
    print("# Axis available for profile(s) plot")
    print()
    p_axes = ask_for_columns(p, "mass", "omega")
    

    # create the lambda function so that onclick and onkeypress have
    # access to local vars :D
    key = [None]
    _onclick = lambda event: onclick(event, hist,
                                     xaxis, yaxis, profile_index,
                                     p_axes)
    _onkeypress = lambda event: onkeypress(event, key)

    ##################################################
    # Plots
    ##################################################
    # set interactive mode
    plt.ion()
    
    #######################################
    # profile
    #######################################
    fig2 = plt.figure(current_profile_figure)
    ax2  = fig2.add_subplot(111)
    ax2.set_xlabel(p_axes[0])
    ax2.set_ylabel(p_axes[1])
    ax2.legend()
    ax2.grid()
    
    #######################################
    # history profile
    #######################################
    fig1 = plt.figure(1)

    # add hooks to plot the profiles
    fig1.canvas.mpl_connect('button_press_event', _onclick)
    fig1.canvas.mpl_connect('key_press_event', _onkeypress)
    
    # plot the two selected columns
    ax1 = fig1.add_subplot(111)
    ax1.plot(hist.get(xaxis), hist.get(yaxis))
    ax1.set_xlabel(xaxis)
    ax1.set_ylabel(yaxis)
    ax1.grid()
    fig1.show()
        
