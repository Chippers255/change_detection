# -*- coding: utf-8 -*-

# change_detection.py
# Visual Cognitive Neuroscience Lab
# Brock University
#
# Created by Thomas Nelson <tn90ca@gmail.com>
#
# This script was developed for use by the Visual Cognitive Neuroscience Lab
# at Brock University.


"""This script runs a standard colour change detection task (modeled after Luck & Vogel, 1997, Nature). The script
was written by Thomas Nelson for the Visual Cognitive Neuroscience Lab at Brock University. Feel free to use this
as a starting point for creating your own experiments.

"""


# Import required third party modules
import os
import csv
import math
import random
from psychopy import visual, core, event, gui, monitors, parallel


########################################################################################################################
#                                                  Program Constants                                                   #
########################################################################################################################

EXP_NAME = "change_detection"  # The name of the experiment for save files
USE_EEG  = False  # Set a boolean value to tell the program to send EEG codes or not
VERBOSE  = True  # Set to True to print out a trial timing log for testing

# Set file paths for required directories
EXP_PATH   = os.path.dirname(os.path.realpath(__file__))  # The path to this script
HOME_PATH  = os.path.realpath(os.path.expanduser("~"))  # The path to the home folder
SAVE_PATH  = os.path.join(HOME_PATH, 'Desktop', 'experiment_data', EXP_NAME)  # Path to save experiment results
IMAGE_PATH = os.path.join(EXP_PATH, 'images')  # Path to store any required experiment images

# Note that these RGB values are converted from (0 and 255) to (-1 and 1)
BG_COLOUR     = [0, 0, 0]  # Set a background colour, currently grey
FIX_COLOUR    = [-1, -1, -1]  # Set the fixation colour, currently black
TEXT_COLOUR   = [-1, -1, -1]  # The text colour, currently white
TRIAL_COLOURS = [[-1, -1, -1],  # Black
                 [-1, -1, 1],   # Blue
                 [-1, 1, -1],   # Green
                 [-1, 1, 1],    # Cyan
                 [1, -1, -1],   # Red
                 [1, -1, 1],    # Purple
                 [1, 1, -1],    # Yellow
                 [1, 1, 1]]     # White
                 
COLOUR_NAMES  = {str([-1,-1,-1]) : 'Black',
                 str([-1,-1,1])  : 'Blue',
                 str([-1,1,-1])  : 'Green',
                 str([-1,1,1])   : 'Cyan',
                 str([1,-1,-1])  : 'Red',
                 str([1,-1,1])   : 'Purple',
                 str([1,1,-1])   : 'Yellow',
                 str([1,1,1])    : 'White'}

NUM_TYPE = 3  # Number of different trial types
NUM_REPS = 50  # Number of repetitions for each different trial type

# Note that all sizing is in visual degrees
FIXATION_SIZE   = 0.1  # Size of the fixation at the center of the screen in visual degree
STIM_POS_RADIUS = 4  # Number of visual degrees between the center and stimuli
STIM_SIZE       = 1  # Size of the stimuli in visual degrees, length and width
STIM_THICKNESS  = 1  # The thickness of the outline of the stimuli

TEXT_HEIGHT = 1   # The height in visual degrees of instruction text
TEXT_WRAP   = 50  # The character limit of each line of text before word wrap

# Note that all timing is in seconds
ITI_TIME   = 0.5  # The time in seconds between trials
STIM_TIME  = 0.5  # The time in seconds to display the stimuli
DELAY_TIME = 1.0  # The time in seconds between stimuli and probe
BREAK_TIME = 0.75  # The time in seconds between break end and trial start

INS_MSG   = "You will be presented with coloured squares, try to remember their colours.\n\n"
INS_MSG  += "For each, trial there will follow a second set of squares in the same locations.\n\n"
INS_MSG  += "If there was any change in colour to the second set of squares from the first, press "
INS_MSG  += "the z key,\n\nIf they have not changed colour, press the m key\n\nPress any key when "
INS_MSG  += "you are ready to begin."
BREAK_MSG = "Take a quick break. When you are ready to continue, press any key."
THANK_MSG = "Thank you for your participation. Please go find the experimenter."

# This is a list of the column headers for the output file
HEADER_LIST = ['Subject_Number', 'Trial_Number', 'Number_of_Stim', 'Stim_Colour_1', 'Stim_Colour_2', 'Stim_Colour_3',
               'Stim_Colour_4', 'Stim_Colour_5', 'Stim_Colour_6', 'Probe_Colour_1', 'Probe_Colour_2', 'Probe_Colour_3',
               'Probe_Colour_4', 'Probe_Colour_5', 'Probe_Colour_6', 'Change_Present', 'Subject_Response',
               'Response_Time', 'Response_Error']


########################################################################################################################
#                                                  Class Declaration                                                   #
########################################################################################################################

class Trial(object):
    """The standard trial class represents a single trial in a standard change detection task. This class is used to
    set up and run a trial.

    """

    def __init__(self, trial_num, rep_num):
        """Class constructor function initializes which trial format to follow from parameter input, also calls the
        functions to set the memory trial olour and location.

        trial_num: Integer
            The trial number used to determine the trial format.
        rep_num: Integer
            The rep number of this trial, used to determine colour change.

        """

        self.rep_num     = rep_num
        self.trial_num   = trial_num
        self.num_stimuli = 0

        self.stim_positions = []

        self.change        = False
        self.stim_colours  = []
        self.probe_colours = []
        
        self.signal = 0

        # Determine the load number for this trial based on the trial type number
        if trial_num == 0:
            self.num_stimuli = 2
        elif trial_num == 1:
            self.num_stimuli = 4
        elif trial_num == 2:
            self.num_stimuli = 6
    # end def __init__

    def set_positions(self):
        """This function will determine the location (left or right) for the memory sample and distraction sample. Uses
        even and odd numbers to ensure an even distribution of left and right positioning. Also generates the
        coordinates for the gui and results print out.

        """

        # Generate a list of 12 positions around the center
        for pos in xrange(12):
            angle = math.radians(360 / 12 * pos)
            self.stim_positions.append([math.cos(angle)*STIM_POS_RADIUS, math.sin(angle)*STIM_POS_RADIUS])
        random.shuffle(self.stim_positions)  # Shuffle the list of positions

        # Cut the position list to the correct number of stimuli required
        self.stim_positions = self.stim_positions[:self.num_stimuli]
    # end def set_positions

    def set_colours(self):
        """This function is used to randomly generate memory stimuli colours and memory probe colours based on a colour
        match or not.

        """

        # Shuffle the list of available colours
        random.shuffle(TRIAL_COLOURS)

        # Create the lists of stimuli and probe colours
        for colour in TRIAL_COLOURS:
            self.stim_colours.append(colour)
            self.probe_colours.append(colour)

        # If a change is present replace on of the colours in the probe list with a new colour
        if (self.rep_num % 2) == 0:
            self.change = True
            rand_1 = random.randint(0, self.num_stimuli-1)
            rand_2 = random.randint(self.num_stimuli, 7)
            self.probe_colours[rand_1] = self.probe_colours[rand_2]

        # Cut the colour lists to the correct number of stimuli required
        self.stim_colours  = self.stim_colours[:self.num_stimuli]
        self.probe_colours = self.probe_colours[:self.num_stimuli]
    # end def set_colours
    
    def set_signals():
        self.signal = 100 + (self.trial_num * 10)
        
        if self.change:
            self.signal += 5
    # end def set_signals

# end class Trial


########################################################################################################################
#                                                 Function Declaration                                                 #
########################################################################################################################

def setup_subject():
    """The purpose of this function is to present a dialog box to the experimenter so they can assign a subject number
    to each subject. This number will be used to create an output file and then used a random seed.

    """

    global NUM_REPS

    num_error = gui.Dlg(title="Error!")
    num_error.addText("This is not a valid subject!")

    subj_error = gui.Dlg(title="Error!")
    subj_error.addText("This subject number has already been used!")

    while True:
        subj_info = {'Subject Number': ''}
        subj_dlg  = gui.DlgFromDict(dictionary=subj_info, title=EXP_NAME)

        # If user hits cancel then safely close program
        if not subj_dlg.OK:
            core.quit()

        if subj_info['Subject Number'].isdigit():
            file_name = subj_info['Subject Number'] + '.csv'
            file_path = os.path.normpath(os.path.join(SAVE_PATH, file_name))
            
            # If we are using the test subject number make the experiment shorter
            if int(subj_info['Subject Number']) == 999:
                NUM_REPS = 2
                break

            if not os.path.isfile(file_path):
                break
            else:
                subj_error.show()
        else:
            num_error.show()

    return subj_info['Subject Number'], file_path
# end def setup_subject


def set_psychopy():
    """
    
    """
    
    # Build the monitor with correct sizing for psychopy to calculate visual degrees
    mon = monitors.Monitor('testMonitor')
    mon.setDistance(57)  # Measure first to ensure this is correct
    mon.setWidth(41)     # Measure first to ensure this is correct
    
    # Build the window for psychopy to run the experiment in
    win = visual.Window(fullscr=True, screen=0, allowGUI=False, allowStencil=False, monitor=mon, color=BG_COLOUR,
                        colorSpace='rgb', units='deg')
    
    # Set up an event clock for timing in trials
    event_clock = core.Clock()
    
    # Set up an event catcher to collect keyboard and mouse responses
    mouse    = event.Mouse(win=win)
    key_resp = event.BuilderKeyResponse()                                          )
    
    if USE_EEG:
        parallel.setPortAddress(address=0x378)
        port = parallel.ParallelPort()
    else:
        port = None

    return win, mon, event_clock, key_resp, mouse, port
# End def set_psychopy


def set_trials():
    """
    
    """
    
    # Build all trials before we start experiment
    test_set = []
    
    for rep in xrange(NUM_REPS):
        for trial in xrange(NUM_TYPE):
            set_trial = Trial(trial, rep)  # Initialize the Trial
            set_trial.set_positions()  # Set the stimuli positions for the Trial
            set_trial.set_colours()  # Set the stimuli colours for the Trial
            set_trial.set_signals()  # Set the EEG signals for the Trial
            test_set.append(set_trial)
            
    # Randomize our trial order
    random.shuffle(test_set)
    
    return test_set
# end def set_trials


def display_message(win, fix, txt, msg):
    """A function to display text to the experiment window.

    win: psychopy.visual.Window
        The window to write the message to.

    fix: psychopy.visual.Circle
        The fixation point to be removed from the screen.

    txt: psychopy.visual.TextStim
        The text object to present to the screen.
    
    msg: String
        The contents for the text object.

    """
    
    if USE_EEG:
        win.callOnFlip(parallel.setData, 200)
        
    txt.setText(msg)
    fix.setAutoDraw(False)
    txt.setAutoDraw(True)
    win.flip()
    
    event.waitKeys()
    
    if USE_EEG:
        win.callOnFlip(parallel.setData, 0)
        
    txt.setAutoDraw(False)
    fix.setAutoDraw(True)
    win.flip()
# end def display_message


def display_fixation(win, clk, fix, dur):
    """A function to display a fixation to the screen for a duration of time. This us to be used to either an
    ITI or ISI.

    win: psychopy.visual.Window
        The window to write the message to.

    fix: psychopy.visual.Circle
        The fixation point to be removed from the screen.

    dur: Float
        The duration of time to display the fixation on screen.

    """
    
    event_clock.reset()
    
    while True:
        if clk.getTime() >= dur:
            break
        fix.Draw(True)
        win.flip()
        if clk.getTime() >= dur:
            break
    
    FT = clk.getTime()
    
    if VERBOSE:
        print "FIXATION SCREEN:", FT
# end def display_fixation


########################################################################################################################
#                                                   Experiment Setup                                                   #
########################################################################################################################

# Kill the explorer if we are on a windows machine, if not kill EEG use
if os.name == 'nt':
    os.system("taskkill /im explorer.exe")
else:
    USE_EEG = False

# Collect the subject number and create the subject output file
subj_num, subj_file = setup_subject()

# Create save directory if it does not already exist
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

# Seed random with the subject number so we can recreate the experiment
random.seed(int(subj_num))

# Write output headers to subject save file
with open(subj_file, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(HEADER_LIST)

# Set up psychopy
win, mon, event_clock, key_resp, mouse, port = set_psychopy()

# Set the experiment trials
test_set = set_trials()

# Build all experiment stimuli, *Note this needs to be done before experiment runtime to ensure proper timing
display_text = visual.TextStim(win=win, ori=0, name='text', text="", font='Arial', pos=[0, 0], height=TEXT_HEIGHT,
                               wrapWidth=TEXT_WRAP, colour=TEXT_COLOUR, colourSpace='rgb', opacity=1, depth=-1.0)

fixation = visual.Circle(win, pos=[0, 0], radius=FIXATION_SIZE, lineColour=FIX_COLOUR, fillColour=FIX_COLOUR)

stimuli = []
for target in xrange(6):
    stimuli.append(visual.Rect(win, width=STIM_SIZE, height=STIM_SIZE, fillColourSpace='rgb', lineColourSpace='rgb'))

# Present instructions for the experiment
message(win, fixation, display_text, INS_MSG)

# Open the output file reader for writing
csv_file = open(subj_file, 'a')
writer   = csv.writer(csv_file)

# Set required run time variables
current_trial = 0

########################################################################################################################
#                                                  Experiment Run-time                                                 #
########################################################################################################################

for trial in test_set:
    current_trial += 1

    # Present a break message every 25 trials
    if current_trial % 25 == 0 and current_trial != 0:
        display_message(win, fixation, display_text, BREAK_MSG)

    # Present ITI
    display_fixation(win, event_clock, fixation, ITI)

    # Define stimuli with trial values for presentation
    for target in xrange(trial.num_stimuli):
        stimuli[target].setPos((trial.stim_positions[target][0], trial.stim_positions[target][1]))
        stimuli[target].setFillColour(trial.stim_colours[target])
        stimuli[target].setLineColour(trial.stim_colours[target])
    
    # Present stimuli to the screen
    event_clock.reset()
    while True:
        if event_clock.getTime() >= STIM_TIME:
            break
        for target in xrange(trial.num_stimuli):
            stimuli[target].draw()
        fixation.draw()
        win.flip()
        if event_clock.getTime() >= STIM_TIME:
            break
    ST = event_clock.getTime()
    if VERBOSE:
        print "STIMULI SCREEN:", ST

    # Present memory delay, ISI
    display_fixation(win, event_clock, fixation, DELAY_TIME)

    # Present probes to screen
    for target in xrange(trial.num_stimuli):
        stimuli[target].setFillColour(trial.probe_colours[target])
        stimuli[target].setLineColour(trial.probe_colours[target])
        stimuli[target].setPos((trial.stim_positions[target][0], trial.stim_positions[target][1]))
        stimuli[target].setAutoDraw(True)

    # Wait for key response and record
    win.callOnFlip(event_clock.reset)
    event.clearEvents()
    key_resp.clock.reset()
    win.flip()

    while True:
        # Check for response keys or quit
        if event.getKeys(["z"]):
            response  = True
            resp_time = key_resp.clock.getTime()
            break
        elif event.getKeys(["m"]):
            response  = False
            resp_time = key_resp.clock.getTime()
            break
        elif event.getKeys(["escape"]):
            core.quit() # If escape key is hit then safely close program

    # Output trial results to file
    output = [subj_num, current_trial, trial.num_stimuli]

    for target in xrange(6):
        try:
            output.append(COLOUR_NAMES[str(trial.stim_colours[target])])
        except:
            output.append('NaN')

    for target in xrange(6):
        try:
            output.append(COLOUR_NAMES[str(trial.probe_colours[target])])
        except:
            output.append('NaN')

    output.extend([trial.change, response, resp_time])

    writer.writerow(output)
    csv_file.flush()
# end of experiment

# Close the csv file
csv_file.close()

# Thank subject
display_message(win, fixation, display_text, THANK_MSG)

# Close the experiment
win.close()
core.quit()
