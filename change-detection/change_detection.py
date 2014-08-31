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

"""This script runs a standard color change detection task (modeled after Luck & Vogel, 1997, Nature). The script was written by Thomas Nelson for the Visual Cognitive Neuroscience Lab at Brock University. Feel free to use this as a starting point for creating your own change detection experiments.

"""

from psychopy import visual, core, data, event, logging, sound, gui, misc, monitors
from psychopy.constants import *
from vcnlib import Subject, Standard_Trial
import os
import vcnlib
import random
import math
import Image
import ctypes

########## Begin Program Constants ##########
EXP_NAME          = "change_detection"
MONITOR_NAME      = "vcnLab"
NUM_REPS          = 50  # Number of reps for each trial type, there are 5 trial types
NUM_TARGET_POS    = 12  # Number of postention positions that items can be placed into
TARGET_POS_RADIUS = 4  # The distance between the fixation point to the the memory probes
TARGET_SIZE       = 1   # The size of the target shape, this value is for both the length and width
FIXATION_SIZE     = 0.1 # The radius of the fixation dot in degrees
SAMPLE_LENGTH     = 0.5 # The length in seconds to display memory sample
ITI_LENGTH        = 0.5 # Delay between emory sample and memory probe
PROBE_LINE_WIDTH  = 2   # The thickness of the outline that inidicates the probed location
DELAY_LENGTH      = 1.0 # The duration of time separating trials
TEXT_HEIGHT       = 1   # Height of the instructions text
TEXT_WRAPPING     = 50  # Wrapping width of the instructions text
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

random.seed() # Initialize random number generator

########## Begin Subject Setup ##########
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
########## End Subject Setup ##########

########## Start Column Setup ##########
outStr = "user,trial,setSize,changePresent,response,responseTime"
outputFile.write(outStr + "\n")
########## End Column Setup ##########

########## Start PsychoPy Setup ##########
win        = visual.Window(fullscr=True, screen=0, allowGUI=False, allowStencil=False, monitor=MONITOR_NAME, color=[0,0,0], colorSpace='rgb', units='deg')
mon        = monitors.Monitor(MONITOR_NAME)
trialClock = core.Clock()
eventClock = core.Clock()
keyResp    = event.BuilderKeyResponse()  # create an object of type KeyResponse
mouse      = event.Mouse(win=win)
errorTone  = sound.SoundPygame(500,0.05)
fixation   = visual.Circle(win, pos=(0,0), radius=(FIXATION_SIZE), lineColor='black', fillColor='black')
########## End PsychoPy Setup ##########

########## Build Trial Set ##########
testSet = []
for rep in range(0, NUM_REPS):
    for trial in range(3):
        setTrial = Standard_Trial(trial,rep)
        setTrial.setPositions(TARGET_POS_RADIUS,NUM_TARGET_POS)
        setTrial.setColors()
        testSet.append(setTrial)
random.shuffle(testSet)
########## Build Trial Set ##########

# Present instructions for the experiment
fixation.setAutoDraw(False)
instructions = visual.TextStim(win=win, ori=0, name='text', text="", font=u'Arial', pos=[0, 0], height=TEXT_HEIGHT, wrapWidth=TEXT_WRAPPING, color=u'black', colorSpace=u'rgb', opacity=1, depth=-1.0)
instructions.setText(insMsg)
instructions.setAutoDraw(True); win.flip(); event.waitKeys(); instructions.setAutoDraw(False); win.flip()
fixation.setAutoDraw(True)

# Begin the experiment
currentTrial = 0
for trial in testSet: 
    currentTrial += 1

    # Present a break message every 25 trials; any key to skip
    if currentTrial % 25 == 0 and currentTrial != 0:
        instructions = visual.TextStim(win=win, ori=0, name='text', text=breakMsg, font=u'Arial', pos=[0, 0], height=TEXT_HEIGHT, wrapWidth=TEXT_WRAPPING, color=u'black', colorSpace=u'rgb', opacity=1, depth=-1.0)
        fixation.setAutoDraw(False)
        instructions.setAutoDraw(True)
        win.flip()
        event.waitKeys()
        instructions.setAutoDraw(False)
        win.flip()

        fixation.setAutoDraw(True)
        eventClock.reset()
        while eventClock.getTime < 0.75: 
            pass
        
    # Setup target stimuli for late use
    targetStim = []
    for target in range(trial.numTargets):
        targetStim.append(visual.Rect(win, width=TARGET_SIZE, height=TARGET_SIZE, fillColor=trial.trialColors[target], pos=trial.targetPositions[target], fillColorSpace='rgb', lineColor=trial.trialColors[target], lineColorSpace='rgb'))

    mouse.setVisible(0)

    # Present ITI, just fixation
    fixation.setAutoDraw(True)
    win.flip()
    eventClock.reset()
    while eventClock.getTime() < ITI_LENGTH: 
        pass
    
    # Present memory sample
    for target in range(trial.numTargets):
        targetStim[target].setAutoDraw(True)
    win.flip()
    eventClock.reset()
    while eventClock.getTime() < SAMPLE_LENGTH: 
        pass

    # Present memory delay    
    for target in range(trial.numTargets):
        targetStim[target].setAutoDraw(False)
    win.flip()
    eventClock.reset()
    while eventClock.getTime() < DELAY_LENGTH: 
        pass

    # Present memory test sample
    for target in range(trial.numTargets):
        targetStim[target].setFillColor(trial.probeColor[target])
        targetStim[target].setLineColor(trial.probeColor[target])
        targetStim[target].setPos((trial.targetPositions[target][0], trial.targetPositions[target][1]))
        targetStim[target].setAutoDraw(True)
    win.flip()
    
    # Wait for key response and record
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

        # Check for response keys or quit
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

    # Output trial results to file
    outStr =  str(user.getSubject()) + ','
    outStr += str(currentTrial) + ','
    outStr += str(trial.numTargets) + ','
    outStr += str(trial.change) + ','
    outStr += str(response) + ','
    outStr += str(keyResp.rt)

    outputFile.write(outStr + '\n')
    
    # Clear display at end of trial 
    for target in range(0, trial.numTargets):
        targetStim[target].setAutoDraw(False)
        fixation.setAutoDraw(False)

# end of experiment

outputFile.write("Hit: " + str(hit) + ", Miss: " + str(miss) + ", False Alarm: " + str(fa) + ", Correct Rejection: " + str(cr) + ", Trials: " + str(currentTrial) + "\n")
outputFile.close()

# Thank subject
instructions = visual.TextStim(win=win, ori=0, name='text', text=thankMsg, font=u'Arial', pos=[0, 0], height=TEXT_HEIGHT, wrapWidth=TEXT_WRAPPING, color=u'black', colorSpace=u'rgb', opacity=1, depth=-1.0)
instructions.setAutoDraw(True); win.flip(); event.waitKeys(); instructions.setAutoDraw(False); win.flip()

win.close()
core.quit()