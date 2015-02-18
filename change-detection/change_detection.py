# -*- coding: utf-8 -*-

# change_detection.py
# Visual Cognitive Neuroscience Lab
# Brock University
#
# Created by Thomas Nelson <tn90ca@gmail.com>
# Created..........................2013-10-24
# Modified.........................2015-01-30
#
# This script was developed for use by the Visual Cognitive
# Neuroscience Lab at Brock University.


"""This script runs a standard colour change detection task (modeled after Luck & Vogel, 1997,
Nature). The script was written by Thomas Nelson for the Visual Cognitive Neuroscience Lab at Brock
University. Feel free to use this as a starting point for creating your own change detection
experiments.

"""


from psychopy import visual, core, data, event, gui, misc, monitors
from psychopy.constants import *
import os
import csv
import math
import random


###################################################################################################
######################################## Program Constants ########################################
###################################################################################################
EXP_NAME     = "change_detection" # The name of the experiment for save files
MONITOR_NAME = "vcnlab"           # The name of the monitor set in PsychoPy
HOME_PATH    = os.path.expanduser("~")
SAVE_PATH    = os.path.normpath(os.path.join(HOME_PATH, 'Desktop', 'data', EXP_NAME))

BG_COLOUR     = [0, 0, 0]    # Set a background colour, currently grey
FIX_COLOUR    = [-1, -1, -1] # Set the fixation colour, currently black
TEXT_COLOUR   = [1, 1, 1]    # The text colour, currently white
TRIAL_COLOURS = [[-1,-1,-1], # Black
                [-1,-1,1],   # Blue
                [-1,1,-1],   # Green
                [-1,1,1],    # Cyan
                [1,-1,-1],   # Red
                [1,-1,1],    # Purple
                [1,1,-1],    # Yellow
                [1,1,1]      # White
               ]
COLOUR_NAMES  = {str([-1,-1,-1]) : 'Black',
                 str([-1,-1,1])  : 'Blue',
                 str([-1,1,-1])  : 'Green',
                 str([-1,1,1])   : 'Cyan',
                 str([1,-1,-1])  : 'Red',
                 str([1,-1,1])   : 'Purple',
                 str([1,1,-1])   : 'Yellow',
                 str([1,1,1])    : 'White'
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

HEADER_LIST = ['Subject_Number', 'Trial_Number', 'Number_of_Stim', 'Stim_Colour_1',
               'Stim_Colour_2', 'Stim_Colour_3', 'Stim_Colour_4', 'Stim_Colour_5', 'Stim_Colour_6',
               'Probe_Colour_1', 'Probe_Colour_2', 'Probe_Colour_3', 'Probe_Colour_4',
               'Probe_Colour_5', 'Probe_Colour_6', 'Change_Present', 'Subject_Response',
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
        :param rep_num:   The rep number of this trial, used to determine colour
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

    def set_colours(self):
        """This function is used to randomly generate memory stimuli colours and
        memory probe colours based on a colour match or not.

        """

        random.seed()  # Initialize random number generator

        self.stim_colours  = []
        self.probe_colours = []
        self.change       = False

        random.shuffle(TRIAL_COLOURS)

        for colour in TRIAL_COLOURS:
            self.stim_colours.append(colour)
            self.probe_colours.append(colour)
        
        if (self.rep_num % 2) == 0:
            self.change = True
            rand_1 = random.randint(0,self.num_stimuli-1)
            rand_2 = random.randint(self.num_stimuli,7)
            self.probe_colours[rand_1] = self.probe_colours[rand_2]

        self.stim_colours  = self.stim_colours[:self.num_stimuli]
        self.probe_colours = self.probe_colours[:self.num_stimuli]
    # end def set_colours

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
    
            if not os.path.isfile(subj_file):
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
try:
    win = visual.Window(fullscr=True, screen=0, allowGUI=False, allowStencil=False,
                        monitor=MONITOR_NAME, color=BACKGROUND_COLOUR, colorSpace='rgb', units='deg')
    mon = monitors.Monitor(MONITOR_NAME)
except:
    obj_error = gui.Dlg(title="Error!")
    obj_error.addText("You need to go into the monitor settings of psychopy and set up a monitor and name it.")
    obj_error.show
    core.quit(0)  # If used hits cancel then safely close program
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
        set_trial.set_colours()
        test_set.append(set_trial)

random.shuffle(test_set) # Randomize our trial order

# Build all experiment stimuli
instructions = visual.TextStim(win=win, ori=0, name='text', text="", font='Arial', pos=[0, 0],
                               height=TEXT_HEIGHT, wrapWidth=TEXT_WRAP, colour=TEXT_COLOUR,
                               colourSpace='rgb', opacity=1, depth=-1.0
                              )
fixation = visual.Circle(win, pos=[0, 0], radius=FIXATION_SIZE, lineColour=FIX_COLOUR,
                         fillColour=FIX_COLOUR
                        )
stimuli = []
for target in xrange(6):
    stimuli.append(visual.Rect(win, width=STIM_SIZE, height=STIM_SIZE, fillColourSpace='rgb',
                               lineColourSpace='rgb'
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

# Set required run time variables
current_trial = 0

###################################################################################################
####################################### Experiment Runtime ########################################
###################################################################################################
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
        stimuli[target].setFillColour(trial.stim_colours[target])
        stimuli[target].setLineColour(trial.stim_colours[target])
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
        stimuli[target].setFillColour(trial.probe_colours[target])
        stimuli[target].setLineColour(trial.probe_colours[target])
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
        output.append(COLOUR_NAMES[str(trial.stim_colours[target])])
    
    if trial.num_stimuli < 6:
        output.append('NaN')
        output.append('NaN')
        
    if trial.num_stimuli < 4:
        output.append('NaN')
        output.append('NaN')
    
    for target in xrange(trial.num_stimuli):
        output.append(COLOUR_NAMES[str(trial.probe_colours[target])])
    
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
