# -*- coding: utf-8 -*-

# standard_trial.py
# Visual Cognitive Neuroscience Lab
# Brock University
#
# Created by Thomas Nelson <tn90ca@gmail.com>
# Since 2013-10-24
#
# This library was developed for use by the Visual Cognitive
# Neuroscience Lab at Brock University.

import random
import math

class Standard_Trial(object):
    """The standard trial class represents a single trial in a standard change
    detection task. This class is used to set up and run a trial.
    
    """
    
    def __init__(self, trialNum=0, repNum=0):
        """Class constructor function initializes which trial format to follow
        from parameter input, also calls the functions to set the memory trial
        colour and location.
        
        :param trialNum: The trial number used to determine the trial format.
        :type trialNum: integer
        :param repNum: The rep number of this trial, used to determine color
            change.
        :type repNum: integer
        
        """
        
        self.trialNum   = trialNum
        self.repNum     = repNum
        self.numTargets = 0

        if trial == 0:
            self.numTargets = 2
        elif trial == 1:
            self.numTargets = 4
        elif trial == 2:
            self.numTargets = 6
    # end def __init__

    def setPositions(self, positionRadius=5, numPositions=12):
        """This function will determine the location (left or right) for the
        memory sample and distraction sample. Uses even and odd numbers to
        ensure an even distribution of left and right positioning. Also
        generates the coordinates for the gui and results print out.
        
        :param positionRadius: The distance from the squares to the fixation
            point.
        :type positionRadius: integer
        :param numPositions: The number of positions around the fixations
            for the squares to appear.
        :type numPositions: integer
    
        """
    
        random.seed() #initialize random number generator

        self.targetPositions = []

        for pos in range(0, numPositions):
            angle = math.radians(360 / numPositions * pos)
            self.targetPositions.append([math.cos(angle)*positionRadius,
                                         math.sin(angle)*positionRadius])

        random.shuffle(self.targetPositions)
        self.targetPositions = self.targetPositions[:self.numTargets]
    # end def setPositions

    def setColors(self):
        """This function is used to randomly generate memory sample colours and
        memory distraction colours based on a colour match or not.

        """

        random.seed() #initialize random number generator

        self.trialColors = [[-1,-1,-1],[-1,-1,1],[-1,1,-1],[-1,1,1],[1,-1,-1],
                            [1,-1,1],[1,1,-1],[1,1,1]]
        self.probeColor  = []
        self.change      = False

        random.shuffle(self.trialColors)

        for color in self.trialColors:
          self.probeColor.append(color)

        if (repNum % 2) == 0:
          self.change = True
          self.probeColor[random.randint(0,self.numTargets-1)] = self.probeColor[random.randint(self.numTargets,7)]

        self.trialColors = self.trialColors[:self.numTargets]
        self.probeColor  = self.probeColor[:self.numTargets]
    # end def setColors

# end class Standard_Trial