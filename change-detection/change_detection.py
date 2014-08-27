# -*- coding: utf-8 -*-

# change_detection.py
# Visual Cognitive Neuroscience Lab
# Brock University
#
# Created by Thomas Nelson <tn90ca@gmail.com>
# Since 2013-10-24
#
# This library was developed for use by the Visual Cognitive
# Neuroscience Lab at Brock University.

from psychopy import visual, core, data, event, logging, sound, gui, misc, monitors
from psychopy.constants import *
from vcnlib import *
import os
import vcnlib
import random
import math
import Image
import ctypes

########## Begin Program Constants ##########
EXP_NAME           = "change_detection"
MONITOR_NAME       = "vcnLab"
NUM_REPS           = 50  # Number of reps for each trial type, there are 5 trial types
NUM_TARGET_POS     = 12  # Number of postention positions that items can be placed into
TARGET_POS_RADIUS  = 4  # The distance between the fixation point to the the memory probes
TARGET_SIZE        = 1   # The size of the target shape, this value is for both the length and width
FIXATION_SIZE      = 0.1 # The radius of the fixation dot in degrees
SAMPLE_LENGTH      = 0.5 # The length in seconds to display memory sample
ITI_LENGTH         = 1.0 # Delay between emory sample and memory probe
PROBE_LINE_WIDTH   = 2   # The thickness of the outline that inidicates the probed location
ISI                = 0.5 # The duration of time separating trials
TEXT_HEIGHT        = 1   # Height of the instructions text
TEXT_WRAPPING      = 50  # Wrapping width of the instructions text
########## End Program Constants ##########

########## Begin Display Text ##########
insMsg   = "You will be presented with coloured squares, try to remember their colours.\n\nFor each, trial there will follow a second set of squares in the same locations.\n\nIf there was any change in colour to the second set of squares from the first, press the z key,\n\nIf they have not changed colour, press the m key\n\nPress any key when you are ready to begin.";
errMsg   = "This subject number has already been used, please select another!";
breakMsg = "Take a quick break. When you are ready to continue, press any key.";
thankMsg = "Thank you for your participation. Please go find the experimenter.";
########## End Display Text ##########

########## Begin Global Variables ##########
user       = ''
outputFile = ''
hit        = 0
miss       = 0
fa         = 0
cr         = 0
########## End Global Variables ##########

# This function will get the subject number and set up a file for the subjects 
# results. The subject number '999' is used as a test case for development and
# other purposes.
def setSubject():
  global user, outputFile, NUM_REPS

  E1 = gui.Dlg(title="Error!")
  E1.addText(errMsg)

  while True:
    S1Info = {'subjNum':''}
    S1     = gui.DlgFromDict(dictionary=S1Info, title=EXP_NAME)
    if S1.OK == False:
      core.quit()

    if S1Info['subjNum'].isdigit():
      fileName = 'C:\\Users\\vcnlab\\Desktop\\data\\change_detection\\' + EXP_NAME + '_' + S1Info['subjNum'] + '.csv'

      if int(S1Info['subjNum']) == 999: 
        break

      if not os.path.isfile(fileName): 
        break
      else:
        E1.show()
  
  user = Subject(EXP_NAME, S1Info['subjNum'])

  if int(user.getSubject()) == 999:
    NUM_REPS = 6

  outputFile = open(fileName, 'w')
# End def setSubject()

# The setColumns function is used to prepare the users results file by 
# creating the column headers.
def setColumns():
  global outputFile

  outStr = "user,trial,setSize,changePresent,response,responseTime"
  outputFile.write(outStr + "\n")
# End def setColumns()


random.seed() #initialize random number generator

setSubject()
setColumns()

# Setup the Psychopy variables (screen, stimuli, sounds, ect)
win        = visual.Window(fullscr=True, screen=0, allowGUI=False, allowStencil=False, monitor=MONITOR_NAME, color=[0,0,0], colorSpace='rgb', units='deg')
mon        = monitors.Monitor(MONITOR_NAME)
trialClock = core.Clock()
eventClock = core.Clock()
keyResp    = event.BuilderKeyResponse()  # create an object of type KeyResponse
mouse      = event.Mouse(win=win)
errorTone  = sound.SoundPygame(500,0.05)
fixation   = visual.Circle(win, pos=(0,0), radius=(FIXATION_SIZE), lineColor='black', fillColor='black')

testSet = []
for rep in range(0, NUM_REPS):
  for trial in range(3):
    setTrial = ChangeDetectionTrial(trial)
    setTrial.setPositions(TARGET_POS_RADIUS,NUM_TARGET_POS)
    setTrial.setColors(rep)
    testSet.append(setTrial)
random.shuffle(testSet)
random.shuffle(testSet)

#present instructions for the current block 
fixation.setAutoDraw(False)
instructions = visual.TextStim(win=win, ori=0, name='text', text="", font=u'Arial', pos=[0, 0], height=TEXT_HEIGHT, wrapWidth=TEXT_WRAPPING, color=u'black', colorSpace=u'rgb', opacity=1, depth=-1.0)
instructions.setText(insMsg)
instructions.setAutoDraw(True); win.flip(); event.waitKeys(); instructions.setAutoDraw(False); win.flip()
fixation.setAutoDraw(True)

currentTrial = 0

for trial in testSet: 
  currentTrial += 1

  if currentTrial % 25 == 0 and currentTrial != 0: #take a break every so often
    instructions = visual.TextStim(win=win, ori=0, name='text',
      text=breakMsg,
      font=u'Arial', pos=[0, 0], height=TEXT_HEIGHT, wrapWidth=TEXT_WRAPPING, color=u'black', colorSpace=u'rgb', opacity=1, depth=-1.0)
    fixation.setAutoDraw(False)
    instructions.setAutoDraw(True); win.flip(); event.waitKeys();instructions.setAutoDraw(False); win.flip()
    fixation.setAutoDraw(True)
    eventClock.reset()
    while eventClock.getTime < 0.75: 
      pass
      
  #setup a list target stimuli that can be drawn to screen (later)
  targetStim = []
  for target in range(trial.numTargets):
    targetStim.append(visual.Rect(win, width=TARGET_SIZE, height=TARGET_SIZE, fillColor=[-1,-1,-1], fillColorSpace='rgb', lineColor=[-1,-1,-1], lineColorSpace='rgb'))
  probeRect = visual.Rect(win, width=TARGET_SIZE, height=TARGET_SIZE, fillColor=[0,0,0], fillColorSpace='rgb', lineColor=[-1,-1,-1], lineColorSpace='rgb', lineWidth=PROBE_LINE_WIDTH) #used on trials where the probed item is a square

  mouse.setVisible(0)
  #probe = probeRect

  #present ISI, just fixation
  fixation.setAutoDraw(True)
  win.flip()
  eventClock.reset()
  while eventClock.getTime() < ISI: 
    pass
  
  #present memory sample
  for target in range(trial.numTargets):
    targetStim[target].setFillColor(trial.trialColors[target])
    targetStim[target].setLineColor(trial.trialColors[target])
    targetStim[target].setPos((trial.targetPositions[target][0], trial.targetPositions[target][1]))
    targetStim[target].setAutoDraw(True)
  win.flip()
  eventClock.reset()
  while eventClock.getTime() < SAMPLE_LENGTH: 
    pass

  #present memory delay    
  for target in range(trial.numTargets):
      targetStim[target].setAutoDraw(False)
  win.flip()
  eventClock.reset()
  while eventClock.getTime() < ITI_LENGTH: 
    pass

  #present memory sample
  for target in range(trial.numTargets):
    targetStim[target].setFillColor(trial.probeColor[target])
    targetStim[target].setLineColor(trial.probeColor[target])
    targetStim[target].setPos((trial.targetPositions[target][0], trial.targetPositions[target][1]))
    targetStim[target].setAutoDraw(True)
  win.flip()
  
  #get clicks and wait for response.
  eventClock.reset()
  keyResp.status = NOT_STARTED

  while True:
      t = eventClock.getTime()

      #initialize key checker
      if keyResp.status == NOT_STARTED:
        keyResp.tStart = t
        keyResp.status = STARTED
        keyResp.clock.reset()
        event.clearEvents()

      # check for quit (the [Esc] key)
      if event.getKeys(["z"]):
        response = 'y'
        keyResp.rt = keyResp.clock.getTime()
        if trial.change:
          hit += 1
        else:
          fa += 1
        break
      elif event.getKeys(["m"]):
        response = 'n'
        keyResp.rt = keyResp.clock.getTime()
        if trial.change:
          miss += 1
        else:
          cr += 1
        break
      elif event.getKeys(["escape"]):
        core.quit()

  #output trial results to file
  outStr =  str(user.getSubject()) + ','
  outStr += str(currentTrial) + ','
  outStr += str(trial.numTargets) + ','
  outStr += str(trial.change) + ','
  outStr += str(response) + ','
  outStr += str(keyResp.rt)

  outputFile.write(outStr + '\n')
  
  #clear display    
  for target in range(0, trial.numTargets):
    targetStim[target].setAutoDraw(False)

fixation.setAutoDraw(False)
outputFile.write("Hit: " + str(hit) + ", Miss: " + str(miss) + ", False Alarm: " + str(fa) + ", Correct Rejection: " + str(cr) + ", Trials: " + str(currentTrial) + "\n")
outputFile.close()

#Thank subject
instructions = visual.TextStim(win=win, ori=0, name='text', text=thankMsg, font=u'Arial', pos=[0, 0], height=TEXT_HEIGHT, wrapWidth=TEXT_WRAPPING, color=u'black', colorSpace=u'rgb', opacity=1, depth=-1.0)
instructions.setAutoDraw(True); win.flip(); event.waitKeys(); instructions.setAutoDraw(False); win.flip()

win.close()
core.quit()