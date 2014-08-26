# -*- coding: utf-8 -*-

# standard_trial.py
# Visual Cognitive Neuroscience Lab
# Brock University
#
# Created by Thomas Nelson on 2013-10-24
#
# This library was developed for use by the Visual Cognitive
# Neuroscience Lab at Brock University.

class Standard_Trial(object):

   # Class constructor function initializes which trial format to follow from
   # parameter input, also calls the functions to set the memory trial colour
   # and location.
   #
   # @param self  This is is a default python argument
   # @param trial The trial number used to determine the trial format
   # @param rep   The rep number used to determine probe location
  def __init__(self, trialNum):
    self.trialNum    = trialNum
    self.numTargets  = 0

    if trial == 0:
      self.numTargets = 2
    elif trial == 1:
      self.numTargets = 4
    elif trial == 2:
      self.numTargets = 6

   # This function will determine the location (left or right) for the memory
   # sample and distraction sample. Uses even and odd numbers to ensure an even
   # distribution of left and right positioning. Also generates the coordinates
   # for the gui and results print out.
   #
   # @param self   This is is a default python argument
   # @param rep    The rep number used to given an even distribution of locations
   # @param radius The distance of the probe from the fixation point
  def setPositions(self, radius, num):
    random.seed() #initialize random number generator
    self.targetPositions = []

    for pos in range(0, num):
      angle = math.radians(360 / num * pos)
      self.targetPositions.append([math.cos(angle)*radius, math.sin(angle)*radius])

    random.shuffle(self.targetPositions)
    self.targetPositions = self.targetPositions[:self.numTargets]

   # This function is used to randomly generate memory sample colours and 
   # memory distraction colours based on a colour match or not.
   #
   # @param self This is is a default python argument
   # @param rep  The rep number used to given an even distribution colours
  def setColors(self, rep):
    random.seed() #initialize random number generator
    self.trialColors = [[-1,-1,-1],[-1,-1,1],[-1,1,-1],[-1,1,1],[1,-1,-1],[1,-1,1],[1,1,-1],[1,1,1]]
    self.probeColor  = []
    self.change = False
    random.shuffle(self.trialColors)
    for color in self.trialColors:
      self.probeColor.append(color)

    if (rep % 2) == 0:
      self.change = True
      self.probeColor[random.randint(0,self.numTargets-1)] = self.probeColor[random.randint(self.numTargets,7)]

    self.trialColors = self.trialColors[:self.numTargets]
    self.probeColor  = self.probeColor[:self.numTargets]