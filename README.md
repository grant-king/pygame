# Simulations
Repository for animation, simulation, and game projects.

## Simulations: Configurable Grid Automatons
Install the required libraries Pygame, Numpy, and cv2 then run the file cga.py, located in simulations/simulations/configurable_grid_automatons repository.

This file provides a template for generating and running 2D cellular automata. Change the ruleset name within the Grid initialization method and configure other settings to alter the default simulation.

Once started, control the simulation with the following keys:
'l': Load states from b&w state_shot file generated in a previous simulation
'i': Load states and cell colors from edges of input image file
'r': Change ruleset
's': Save image of current colors of all cells, regardless of current state
't': Set new timer; choose to set end timer or state shot timer

A state shot is an image of all current cell states; this is as a black and white png to represent which cells are active. It could be loaded later to resume a simulation. State shot timers can be set to collect a state shot every so many steps.

Here are the available rulesets as defined in the Ruleset helper class of ca_models_2.py:
    '2x2',
    'amoeba'
    'assimilation'
    'coagulations'
    'coral'
    'conway'
    'daynight'
    'diamoeba'
    'electrifiedmaze'
    'flakes'
    'flock'
    'fredkin'
    'gnarl'
    'highlife'
    'honeylife'
    'inverselife'
    'ironflock'
    'longlife'
    'life34'
    'lfod'
    'maze'
    'mazectric'
    'move'
    'pedestrianlife'
    'pseudolife'
    'replicator'
    'replicatorlog'
    'seeds'
    'serviettes'
    'stains'
    'walledcities'

