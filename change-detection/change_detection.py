# -*- coding: utf-8 -*-

# change_detection.py
# Visual Cognitive Neuroscience Lab
# Brock University
#
# Created by Thomas Nelson <tn90ca@gmail.com>
# Created on 2013-10-24
# Modified by Thomas Nelson on 2015-01-27
#
# This script was developed for use by the Visual Cognitive
# Neuroscience Lab at Brock University.

"""This script runs a standard color change detection task (modeled after Luck
& Vogel, 1997, Nature). The script was written by Thomas Nelson for the Visual
Cognitive Neuroscience Lab at Brock University. Feel free to use this as a
starting point for creating your own change detection experiments.

"""

from psychopy import visual, core, data, event, logging, sound, gui, misc, monitors
from psychopy.constants import *
from os.path import expanduser
import os
import csv
import math
import time
import random

###################################################################################################
######################################## Program Constants ########################################
###################################################################################################
EXP_NAME     = "change_detection" # The name of the experiment for save files
MONITOR_NAME = "vcnlab"           # The name of the monitor set in PsychoPy
HOME_PATH    = expanduser("~")
SAVE_PATH    = os.path.normpath(os.path.join(HOME_PATH,'Desktop','data',EXP_NAME))

BG_COLOR     = [0, 0, 0]    # Set a background color, currently grey
FIX_COLOR    = [-1, -1, -1] # Set the fixation color, currently black
TEXT_COLOR   = [1, 1, 1]    # The text color, currently white
TRIAL_COLORS = [[-1,-1,-1], # Black
                [-1,-1,1],  # Blue
                [-1,1,-1],  # Green
                [-1,1,1],   # Cyan
                [1,-1,-1],  # Red
                [1,-1,1],   # Purple
                [1,1,-1],   # Yellow
                [1,1,1]     # White
               ]
COLOR_NAMES  = {str([-1,-1,-1]):'Black',
                str([-1,-1,1]):'Blue',
                str([-1,1,-1]):'Green',
                str([-1,1,1]):'Cyan',
                str([1,-1,-1]):'Red',
                str([1,-1,1]):'Purple',
                str([1,1,-1]):'Yellow',
                str([1,1,1]):'White'
               }

NUM_REPS = 50 # Number of reps for each trial type
NUM_TYPE = 3  # Number of trial types, should be set to 3

NUM_STIM_POS    = 12 # The number of positions for stimuli to be placed
STIM_POS_RADIUS = 4  # Number of visual degrees between the center and stimuli
STIM_SIZE       = 1  # Size of the stimuli in visual degrees, length and width
STIM_THICKNESS  = 1  # The thickness of the outline of the stimuli

FIXATION_SIZE = 0.1 # Size of the fixation at the center of the screen

TEXT_HEIGHT = 1  # The height in visual degrees of instruction text
TEXT_WRAP   = 50 # The character limit of each line of text before word wrap

ITI        = 0.5  # The time in seconds between trials
STIM_TIME  = 0.5  # The time in seconds to display the stimuli
DELAY_TIME = 1.0  # The time in seconds between stimuli and probe
BREAK_TIME = 0.75 # The time in seconds between break end and trial start

INS_MSG   = "You will be presented with coloured squares, try to remember their colours.\n\n"
INS_MSG  += "For each, trial there will follow a second set of squares in the same locations.\n\n"
INS_MSG  += "If there was any change in colour to the second set of squares from the first, press "
INS_MSG  += "the z key,\n\nIf they have not changed colour, press the m key\n\nPress any key when "
INS_MSG  += "you are ready to begin."
BREAK_MSG = "Take a quick break. When you are ready to continue, press any key."
THANK_MSG = "Thank you for your participation. Please go find the experimenter."

HEADER_LIST = ['Subject_Number', 'Trial_Number', 'Number_of_Stim', 'Stim_Color_1',
               'Stim_Color_2', 'Stim_Color_3', 'Stim_Color_4', 'Stim_Color_5', 'Stim_Color_6',
               'Probe_Color_1', 'Probe_Color_2', 'Probe_Color_3', 'Probe_Color_4',
               'Probe_Color_5', 'Probe_Color_6', 'Change_Present', 'Subject_Response',
               'Response_Time', 'Response_Error'
              ]


###################################################################################################
######################################## Class Declaration ########################################
###################################################################################################
class Trial(object):
    """The standard trial class represents a single trial in a standard change
    detection task. This class is used to set up and run a trial.
    
    """
    
    def __init__(self, trial_num, rep_num):
        """Class constructor function initializes which trial format to follow
        from parameter input, also calls the functions to set the memory trial
        colour and location.
        
        :param trial_num: The trial number used to determine the trial format.
        :param rep_num:   The rep number of this trial, used to determine color
                           change.
        
        """
        
        self.trial_num   = trial_num
        self.rep_num     = rep_num
        self.num_stimuli = 0

        if trial_num == 0:
            self.num_stimuli = 2
        elif trial_num == 1:
            self.num_stimuli = 4
        elif trial_num == 2:
            self.num_stimuli = 6
    # end def __init__

    def set_positions(self, positions):
        """This function will determine the location (left or right) for the
        memory sample and distraction sample. Uses even and odd numbers to
        ensure an even distribution of left and right positioning. Also
        generates the coordinates for the gui and results print out.
        
        :param positions: The list of possible positions for the stimuli
    
        """
    
        random.seed()  # Initialize random number generator

        self.stim_positions = []

        for pos in positions:
            self.stim_positions.append(pos)
            
        random.shuffle(self.stim_positions)
        self.stim_positions = self.stim_positions[:self.num_stimuli]
    # end def set_positions

    def set_colors(self):
        """This function is used to randomly generate memory stimuli colours and
        memory probe colours based on a colour match or not.

        """

        random.seed()  # Initialize random number generator

        self.stim_colors  = []
        self.probe_colors = []
        self.change       = False

        random.shuffle(TRIAL_COLORS)

        for color in TRIAL_COLORS:
            self.stim_colors.append(color)
            self.probe_colors.append(color)
        
        if (self.rep_num % 2) == 0:
            self.change = True
            rand_1 = random.randint(0,self.num_stimuli-1)
            rand_2 = random.randint(self.num_stimuli,7)
            self.probe_colors[rand_1] = self.probe_colors[rand_2]

        self.stim_colors  = self.stim_colors[:self.num_stimuli]
        self.probe_colors = self.probe_colors[:self.num_stimuli]
    # end def set_colors

# end class Standard_Trial


###################################################################################################
####################################### Function Declaration ######################################
###################################################################################################
def setup_subject():
    global NUM_REPS
    
    subj_error = gui.Dlg(title="Error!")
    subj_error.addText("This subject number has already been used, please select another!")

    while True:
        subj_info = {'Subject Number':''}
        subj_dlg  = gui.DlgFromDict(dictionary=subj_info, title=EXP_NAME)
    
        if subj_dlg.OK == False:
            core.quit(0)  # If used hits cancel then safely close program
    
        if subj_info['Subject Number'].isdigit():
            subj_file  = os.path.join(SAVE_PATH,(EXP_NAME + '_' + subj_info['Subject Number'] + '.csv'))
    
            if int(subj_info['Subject Number']) == 999:
                break
    
            if not os.path.isfile(fileName):
                break
            else:
                subj_error.show()
    
    user_dict = {'subj_num' : subj_info['Subject Number'], 'subj_file' : subj_file}
    
    if int(subj_info['Subject Number']) == 999:
        NUM_REPS = 6
        
    return user_dict
# end def setup_subject


###################################################################################################
######################################## Experiment Setup #########################################
###################################################################################################
# Seed random with time so each experiment is different
random.seed()

# Create Save directory if it does not already exist
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

# Setup subject with number and save file
subject   = setup_subject()
subj_file = subject['subj_file']
subj_num  = subject['subj_num']

# Write output headers to subject save file
with open(subj_file, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(HEADER_LIST)

# Setup all required PsychoPY variables
win         = visual.Window(fullscr=True, screen=0, allowGUI=False, allowStencil=False,
                            monitor=MONITOR_NAME, color=BG_COLOR, colorSpace='rgb', units='deg'
                           )
mon         = monitors.Monitor(MONITOR_NAME)
event_clock = core.Clock()
key_resp    = event.BuilderKeyResponse()

# Setup all stimuli positiona
positions = []
for pos in xrange(NUM_STIM_POS):
    angle = math.radians(360 / NUM_STIM_POS * pos)
    positions.append([math.cos(angle)*STIM_POS_RADIUS, math.sin(angle)*STIM_POS_RADIUS])

# Build all trials before we start experiment
test_set = []

for rep in xrange(NUM_REPS):
    for trial in xrange(NUM_TYPE):
        set_trial = Trial(trial, rep)
        set_trial.set_positions(positions)
        set_trial.set_colors()
        test_set.append(set_trial)

random.shuffle(test_set) # Randomize our trial order

# Build all experiment stimuli
instructions = visual.TextStim(win=win, ori=0, name='text', text="", font='Arial', pos=[0, 0],
                               height=TEXT_HEIGHT, wrapWidth=TEXT_WRAP, color=TEXT_COLOR,
                               colorSpace='rgb', opacity=1, depth=-1.0
                              )
fixation = visual.Circle(win, pos=[0, 0], radius=FIXATION_SIZE, lineColor=FIX_COLOR,
                         fillColor=FIX_COLOR
                        )
stimuli = []
for target in xrange(6):
    stimuli.append(visual.Rect(win, width=STIM_SIZE, height=STIM_SIZE, fillColorSpace='rgb',
                               lineColorSpace='rgb'
                              ))

# Present instructions for the experiment
fixation.setAutoDraw(False)
instructions.setText(INS_MSG)
instructions.setAutoDraw(True)
win.flip()
event.waitKeys()
instructions.setAutoDraw(False)
fixation.setAutoDraw(True)
win.flip()

# Open the output file reader for writing
csv_file = open(subj_file, 'a')
writer   = csv.writer(csv_file)


###################################################################################################
####################################### Experiment Runtime ########################################
###################################################################################################
current_trial = 0

for trial in test_set:
    current_trial += 1

    # Present a break message every 25 trials
    if current_trial % 25 == 0 and current_trial != 0:
        fixation.setAutoDraw(False)
        instructions.setText(BREAK_MSG)
        instructions.setAutoDraw(True)
        win.flip()
        event.waitKeys()
        instructions.setAutoDraw(False)
        fixation.setAutoDraw(True)
        win.flip()
        event_clock.reset()
        while event_clock.getTime < BREAK_TIME:
            pass

    # Present ITI, just fixation
    event_clock.reset()
    while event_clock.getTime() < ITI:
        pass
    
    # Present stimuli to screen
    for target in xrange(trial.num_stimuli):
        stimuli[target].setPos((trial.stim_positions[target][0], trial.stim_positions[target][1]))
        stimuli[target].setFillColor(trial.stim_colors[target])
        stimuli[target].setLineColor(trial.stim_colors[target])
        stimuli[target].setAutoDraw(True)
    win.flip()
    event_clock.reset()
    while event_clock.getTime() < STIM_TIME:
        pass

    # Present memory delay
    for target in xrange(trial.num_stimuli):
        stimuli[target].setAutoDraw(False)
    win.flip()
    event_clock.reset()
    while event_clock.getTime() < DELAY_TIME:
        pass

    # Present probes to screen
    for target in xrange(trial.num_stimuli):
        stimuli[target].setFillColor(trial.probe_colors[target])
        stimuli[target].setLineColor(trial.probe_colors[target])
        stimuli[target].setPos((trial.stim_positions[target][0], trial.stim_positions[target][1]))
        stimuli[target].setAutoDraw(True)
    win.flip()
    
    # Wait for key response and record
    event_clock.reset()
    start           = event_clock.getTime()
    key_resp.status = NOT_STARTED

    while True:

        # Initialize response key checker
        if key_resp.status == NOT_STARTED:
            key_resp.tStart = start
            key_resp.status = STARTED
            key_resp.clock.reset()
            event.clearEvents()

        # Check for response keys or quit
        if event.getKeys(["z"]):
            response = True
            key_resp.rt = key_resp.clock.getTime()
            break
        elif event.getKeys(["m"]):
            response = False
            key_resp.rt = key_resp.clock.getTime()
            break
        elif event.getKeys(["escape"]):
            core.quit(0) # If escape key is hit then safely close program

    # Output trial results to file
    output = []
    output.append(subj_num)
    output.append(current_trial)
    output.append(trial.num_stimuli)
    
    for target in xrange(trial.num_stimuli):
        output.append(COLOR_NAMES[str(trial.stim_colors[target])])
    
    if trial.num_stimuli < 6:
        output.append('NaN')
        output.append('NaN')
        
    if trial.num_stimuli < 4:
        output.append('NaN')
        output.append('NaN')
    
    for target in xrange(trial.num_stimuli):
        output.append(COLOR_NAMES[str(trial.probe_colors[target])])
    
    if trial.num_stimuli < 6:
        output.append('NaN')
        output.append('NaN')
        
    if trial.num_stimuli < 4:
        output.append('NaN')
        output.append('NaN')
        
    output.append(trial.change)
    output.append(response)
    output.append(key_resp.rt)
    
        
    writer.writerow(output)
    csv_file.flush()
    
    # Clear display at end of trial
    for target in xrange(trial.num_stimuli):
        stimuli[target].setAutoDraw(False)
    win.flip()
# end of experiment

# Close the csv file
csv_file.close()

# Thank subject
fixation.setAutoDraw(False)
instructions.setText(THANK_MSG)
instructions.setAutoDraw(True)
win.flip()
event.waitKeys()

# Close the experiment
win.close()
core.quit()
