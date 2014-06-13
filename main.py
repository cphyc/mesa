#!python3

# import libraries, ...
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def data(f, get_header = True):
    ''' Read the file "f" and interpret it as a profile and return the data
    with the header if get_header == True. '''
    d = pd.read_csv(f, sep=" +", header=5)
    if get_header:
        h= pd.read_csv(f, sep= " +", header=1, nrows = 1)
        return (d,h)
    else:
        return d

def onkeypress(event, key):
    key[0] = event.key
    if event.key == "ctrl+b":
        plt.close(2)
        print("Reset figure 2")
        fig2 = plt.figure(2)
        ax2  = fig2.add_subplot(111)
        ax2.set_xlabel(p_axes[0])
        ax2.set_ylabel(p_axes[1])
        ax2.legend()
        ax2.grid()
        
    
def onclick(event, hist, key, xax, yax, profile_index, p_axes):
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
    fig2 = plt.figure(2)
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
    if x != "":
        xform = "[" + x + "]"
    if y != "":
        yform = "[" + y + "]"
        
    xaxis = input("\tx-axis %s? " % xform)
    # if no answer but there is a default answer
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
    directory = os.path.expanduser(input("Please pick a directory [/home/ccc/hyades/pfs/simulations/M=1.3_thermo/C=50/LOGS_RGB]: "))
    if not directory:
        directory = "/home/ccc/hyades/pfs/simulations/M=1.3_thermo/C=50/LOGS_RGB"
    while not os.path.isdir(directory):
        print("%s is not a directory." % directory)
        directory = os.path.expanduser(input("Please pick a directory : "))

    # list the directory
    ls = os.listdir(directory)
    assert("history.data" in ls)

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
    print("# Axis available for history plot")
    print()
    p_axes = ask_for_columns(p, "mass", "omega")
    

    # create the lambda function so that onclick and onkeypress have
    # access to local vars :D
    key = [None]
    _onclick = lambda event: onclick(event, hist, key,
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
    fig2 = plt.figure(2)
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
        