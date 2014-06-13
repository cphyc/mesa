mesa
====

Files related to MESA (http://mesa.sourceforge.net/).

viewer.py
=========

A script to interactively explore the profiles of a MESA project.

The script asks for a folder that contains both the history.data, the profiles*.data and the profiles.index files. It creates an interactive history plot. This plot has the basic features given by matplotlib (zoom, ...) and adds functionality.

The first one is the possibility to (right) click the plot. The script will then look for the closest point on the curve, will find the associated model and then the associated profile (through `profiles.index`). The profile found will then be added on another figure plot.

The other one is the possibility to use keyboad shortcuts :
   * `Ctrl+b` will delete the profile plot.
   * `Ctrl+n` will create a new figure or move to the next one on the stack (if any)
   * `Ctrl+p` will move to the previous figure on the stack (if any)


TODO
====

  * improve performances (caching, preloading, efficient indexing)
  * possibility to redefine the axes of a plot (with keystroke for example)
