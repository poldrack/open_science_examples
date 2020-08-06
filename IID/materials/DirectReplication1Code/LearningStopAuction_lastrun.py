#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.82.01), Tue Jun 23 10:46:22 2015
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'LearningTask'  # from the Builder filename that created this script
expInfo = {u'session': u'', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data' + os.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.WARNING)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color='black', colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "StimSetup"
StimSetupClock = core.Clock()
#***************************

from copy import deepcopy
import random

colors = ['yellow', 'white', 'orange', 'magenta', 'green', 'gray', 'cyan', 'blue']
shapes = ['triangle', 'square', 'line', 'invertedtriangle', 'hexagon', 'diamond', 'cross', 'circle']
rewards = [0.50, 1.00, 2.00, 4.00] * 2
conditions = ['go', 'go', 'go', 'go', 'stop', 'stop', 'stop', 'stop']
trialDetailsList = []
learningTrialList = []
learningPracTrialList = []
auctionTrialList = []
rewardList = []
rewardCount = 1
numStim = 8
numLearningTrials = 400
numLearningRepetitions = 50
numLearningPracTrial = 10
stopTaskTrials = 288
numStopPracTrial = 10
stopTrialsPerStopStim = 27
goTrialsPerStopStim = 9
goTrialsPerGoStim = 36
stopTrialList = []
stopPracTrialList = []
auctionTrials = 80
auctionTrialsPerStim = 10
auctionAmounts = 5
eachAuctionAmountCount = 2
auctionAmountsList = [[34, 68, 102, 136, 170, 204], [39, 78, 117, 156, 195, 234], [44, 88, 132, 176, 220, 264], [49, 98, 147, 196, 245, 294], [54, 108, 162, 216, 270, 324]]

shuffle(colors)
shuffle(shapes)

for i, color in enumerate(colors): # cycle through each color and keep track of an index number
    trialDetails = {} # a dictionary of key-value pairs
    trialDetails['fileName'] = shapes[i] + color + '.gif'
    trialDetails['reward'] = rewards[i]
    trialDetails['condition'] = conditions[i]
    trialDetailsList.append(trialDetails)

shuffle(trialDetailsList) # do this now to ensure that order of presentation of rewards and conditions is also shuffled

for k in range(0, numLearningRepetitions):
    for n in range (0, numStim): 
        learningTrialList.append(deepcopy(trialDetailsList[n]))

shuffle(learningTrialList)

thisExp.addData("learningTrialList", learningTrialList)

for o in range(0, numLearningPracTrial):
    p = random.randrange(0, numStim)
    learningPracTrialList.append(deepcopy(trialDetailsList[p]))

shuffle(learningPracTrialList)

thisExp.addData("learningPracTrialList", learningPracTrialList)

for q in range(0, numStim):
    if trialDetailsList[q]['condition'] == 'go':
        trialDetailsList[q]['stopOrGo'] =  'go'
        for i in range(0, goTrialsPerGoStim):
            stopTrialList.append(deepcopy(trialDetailsList[q]))
    elif trialDetailsList[q]['condition'] == 'stop': 
        for j in range(0, goTrialsPerStopStim):
            trialDetailsList[q]['stopOrGo'] = 'go'
            stopTrialList.append(deepcopy(trialDetailsList[q]))
        for r in range(0, stopTrialsPerStopStim):
            trialDetailsList[q]['stopOrGo'] = 'stop'
            stopTrialList.append(deepcopy(trialDetailsList[q]))

shuffle(stopTrialList)

thisExp.addData("stopTrialList", stopTrialList)

for s in range(0, numStopPracTrial):
    s = random.randrange(0, numStim)
    stopPracTrialList.append(deepcopy(trialDetailsList[s]))
    
shuffle(stopPracTrialList)

thisExp.addData("stopPracTrialList", stopPracTrialList)

for l in range(0, auctionAmounts):
    for t in range(0, numStim):
        for u in range(0, eachAuctionAmountCount):
            shuffle(auctionAmountsList[l])
            trialDetailsList[t]['auctionAmount'] = auctionAmountsList[l]
            auctionTrialList.append(deepcopy(trialDetailsList[t]))

shuffle(auctionTrialList)

thisExp.addData("auctionTrialList", auctionTrialList)

#***************************

# Initialize components for Routine "instrPractice"
instrPracticeClock = core.Clock()
instruct1 = visual.TextStim(win=win, ori=0, name='instruct1',
    text='A shape stimulus will appear on every trial. \n\nIf it appears in the upper right quadrant, PRESS W\n\nIf it appears in the lower right quadrant, PRESS S\n\nIf it appears in the lower left quadrant, PRESS A\n\nIf it appears in the upper left quadrant, PRESS Q\n\nResponding as fast and as accurately as possible will lead to higher rewards. The computer will randomly pick five of the trials at the end of the experiment and pay out the amount associated with those trials.\n\nPress the 9 key when you are ready to proceed. ',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "NewPracStim"
NewPracStimClock = core.Clock()


# Initialize components for Routine "startTrialPrac"
startTrialPracClock = core.Clock()


# Initialize components for Routine "trial"
trialClock = core.Clock()
learningFix = visual.TextStim(win=win, ori=0, name='learningFix',
    text='+',    font='Arial',
    pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
learningStim = visual.ImageStim(win=win, name='learningStim',units='pix', 
    image='sin', mask=None,
    ori=0, pos=[0,0], size=[151, 151],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "feedback"
feedbackClock = core.Clock()
#***************************

#message variable just needs some value at start
message=0

#***************************
feedback_2 = visual.TextStim(win=win, ori=0, name='feedback_2',
    text='default text',    font='Arial',
    pos=[0, 0], height=.2, wrapWidth=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    depth=-1.0)
image = visual.ImageStim(win=win, name='image',units='pix', 
    image='sin', mask=None,
    ori=0, pos=[0,0], size=[151, 151],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "Blank"
BlankClock = core.Clock()
text_2 = visual.TextStim(win=win, ori=0, name='text_2',
    text=None,    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "endTrial"
endTrialClock = core.Clock()


# Initialize components for Routine "instrStopPrac"
instrStopPracClock = core.Clock()
instrStopText = visual.TextStim(win=win, ori=0, name='instrStopText',
    text='A shape stimulus will appear on the left or right side of the screen\n\nIf it appears on the left, press Z\n\nIf it appears on the right, press M\n\nIf you hear a tone, do not press anything on that trial\n\nResponding quickly to the location of the shape and withholding your response when you hear a tone are equally important. \n\nPress the 9 key when you are ready to proceed. ',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)


# Initialize components for Routine "newPracStopStim"
newPracStopStimClock = core.Clock()


# Initialize components for Routine "StopTrial"
StopTrialClock = core.Clock()
stopSignal = sound.Sound('900', secs=-1)
stopSignal.setVolume(None)
fixStop = visual.TextStim(win=win, ori=0, name='fixStop',
    text='|',    font='Arial',
    pos=[0, 0], height=4, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
goStim = visual.ImageStim(win=win, name='goStim',units='pix', 
    image='sin', mask=None,
    ori=0, pos=[0,0], size=[151, 151],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "blankStop"
blankStopClock = core.Clock()
text_4 = visual.TextStim(win=win, ori=0, name='text_4',
    text=None,    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "pracStopCleanUp"
pracStopCleanUpClock = core.Clock()


# Initialize components for Routine "endOfStopBlockFeedback"
endOfStopBlockFeedbackClock = core.Clock()

text_5 = visual.TextStim(win=win, ori=0, name='text_5',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Initialize components for Routine "instrPractice"
instrPracticeClock = core.Clock()
instruct1 = visual.TextStim(win=win, ori=0, name='instruct1',
    text='A shape stimulus will appear on every trial. \n\nIf it appears in the upper right quadrant, PRESS W\n\nIf it appears in the lower right quadrant, PRESS S\n\nIf it appears in the lower left quadrant, PRESS A\n\nIf it appears in the upper left quadrant, PRESS Q\n\nResponding as fast and as accurately as possible will lead to higher rewards. The computer will randomly pick five of the trials at the end of the experiment and pay out the amount associated with those trials.\n\nPress the 9 key when you are ready to proceed. ',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "NewStim"
NewStimClock = core.Clock()


# Initialize components for Routine "startTrial"
startTrialClock = core.Clock()


# Initialize components for Routine "trial"
trialClock = core.Clock()
learningFix = visual.TextStim(win=win, ori=0, name='learningFix',
    text='+',    font='Arial',
    pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
learningStim = visual.ImageStim(win=win, name='learningStim',units='pix', 
    image='sin', mask=None,
    ori=0, pos=[0,0], size=[151, 151],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "feedback"
feedbackClock = core.Clock()
#***************************

#message variable just needs some value at start
message=0

#***************************
feedback_2 = visual.TextStim(win=win, ori=0, name='feedback_2',
    text='default text',    font='Arial',
    pos=[0, 0], height=.2, wrapWidth=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    depth=-1.0)
image = visual.ImageStim(win=win, name='image',units='pix', 
    image='sin', mask=None,
    ori=0, pos=[0,0], size=[151, 151],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "Blank"
BlankClock = core.Clock()
text_2 = visual.TextStim(win=win, ori=0, name='text_2',
    text=None,    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "endTrialMain"
endTrialMainClock = core.Clock()


# Initialize components for Routine "learningRest"
learningRestClock = core.Clock()
text = visual.TextStim(win=win, ori=0, name='text',
    text='Please Take a Moment to Rest\n\n(press the 9 key to continue)',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "instrStopPrac"
instrStopPracClock = core.Clock()
instrStopText = visual.TextStim(win=win, ori=0, name='instrStopText',
    text='A shape stimulus will appear on the left or right side of the screen\n\nIf it appears on the left, press Z\n\nIf it appears on the right, press M\n\nIf you hear a tone, do not press anything on that trial\n\nResponding quickly to the location of the shape and withholding your response when you hear a tone are equally important. \n\nPress the 9 key when you are ready to proceed. ',    font='Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)


# Initialize components for Routine "stopBlockSetup"
stopBlockSetupClock = core.Clock()


# Initialize components for Routine "newStopStim"
newStopStimClock = core.Clock()


# Initialize components for Routine "StopTrial"
StopTrialClock = core.Clock()
stopSignal = sound.Sound('900', secs=-1)
stopSignal.setVolume(None)
fixStop = visual.TextStim(win=win, ori=0, name='fixStop',
    text='|',    font='Arial',
    pos=[0, 0], height=4, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
goStim = visual.ImageStim(win=win, name='goStim',units='pix', 
    image='sin', mask=None,
    ori=0, pos=[0,0], size=[151, 151],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "blankStop"
blankStopClock = core.Clock()
text_4 = visual.TextStim(win=win, ori=0, name='text_4',
    text=None,    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "SSDChange"
SSDChangeClock = core.Clock()


# Initialize components for Routine "endOfStopBlockFeedback"
endOfStopBlockFeedbackClock = core.Clock()

text_5 = visual.TextStim(win=win, ori=0, name='text_5',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Initialize components for Routine "instrAuction"
instrAuctionClock = core.Clock()
text_7 = visual.TextStim(win=win, ori=0, name='text_7',
    text=u'Please go get the Experimenter so that you can read the written instructions for final phase of the study. \n\nThe payoff from this final phase will be paid out at the end of the experiment. \n\nPress the 9 key after you have gotten the experimenter and read the instructions. ',    font=u'Arial',
    pos=[0, 0], height=0.07, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "newAuctionStim"
newAuctionStimClock = core.Clock()


# Initialize components for Routine "auctionTrial"
auctionTrialClock = core.Clock()
Fix = visual.TextStim(win=win, ori=0, name='Fix',
    text='+',    font='Arial',
    pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
R = visual.TextStim(win=win, ori=0, name='R',
    text='R',    font='Arial',
    units='norm', pos=[-.75, -.7], height=.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
auctionStim = visual.ImageStim(win=win, name='auctionStim',units='pix', 
    image='sin', mask=None,
    ori=0, pos=[0, 0], size=[151, 151],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
T = visual.TextStim(win=win, ori=0, name='T',
    text='T',    font='Arial',
    units='norm', pos=[-.45, -.7], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0)
Y = visual.TextStim(win=win, ori=0, name='Y',
    text='Y',    font='Arial',
    units='norm', pos=[-.15, -.7], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-4.0)
U = visual.TextStim(win=win, ori=0, name='U',
    text='U',    font='Arial',
    units='norm', pos=[.15, -.7], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-5.0)
I = visual.TextStim(win=win, ori=0, name='I',
    text='I',    font='Arial',
    units='norm', pos=[.45, -.7], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-6.0)
O = visual.TextStim(win=win, ori=0, name='O',
    text='O',    font='Arial',
    units='norm', pos=[.75, -.7], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-7.0)
RAmount = visual.TextStim(win=win, ori=0, name='RAmount',
    text='default text',    font='Arial',
    units='norm', pos=[-.75, -.4], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-8.0)
TAmount = visual.TextStim(win=win, ori=0, name='TAmount',
    text='default text',    font='Arial',
    units='norm', pos=[-.45, -.4], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-9.0)
YAmount = visual.TextStim(win=win, ori=0, name='YAmount',
    text='default text',    font='Arial',
    units='norm', pos=[-.15, -.4], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-10.0)
UAmount = visual.TextStim(win=win, ori=0, name='UAmount',
    text='default text',    font='Arial',
    units='norm', pos=[.15, -.4], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-11.0)
IAmount = visual.TextStim(win=win, ori=0, name='IAmount',
    text='default text',    font='Arial',
    units='norm', pos=[.45, -.4], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-12.0)
OAmount = visual.TextStim(win=win, ori=0, name='OAmount',
    text='default text',    font='Arial',
    units='norm', pos=[.75, -.4], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-13.0)


# Initialize components for Routine "auctionITI"
auctionITIClock = core.Clock()
text_3 = visual.TextStim(win=win, ori=0, name='text_3',
    text=None,    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)


# Initialize components for Routine "auctionBreak"
auctionBreakClock = core.Clock()
text_9 = visual.TextStim(win=win, ori=0, name='text_9',
    text='Please Take a Break\n\n(press the 9 key to continue)',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "rewardCalc"
rewardCalcClock = core.Clock()

text_11 = visual.TextStim(win=win, ori=0, name='text_11',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "StimSetup"-------
t = 0
StimSetupClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat

# keep track of which components have finished
StimSetupComponents = []
for thisComponent in StimSetupComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "StimSetup"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = StimSetupClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in StimSetupComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "StimSetup"-------
for thisComponent in StimSetupComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "StimSetup" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "instrPractice"-------
t = 0
instrPracticeClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
ok1 = event.BuilderKeyResponse()  # create an object of type KeyResponse
ok1.status = NOT_STARTED
# keep track of which components have finished
instrPracticeComponents = []
instrPracticeComponents.append(instruct1)
instrPracticeComponents.append(ok1)
for thisComponent in instrPracticeComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instrPractice"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instrPracticeClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instruct1* updates
    if t >= 0.0 and instruct1.status == NOT_STARTED:
        # keep track of start time/frame for later
        instruct1.tStart = t  # underestimates by a little under one frame
        instruct1.frameNStart = frameN  # exact frame index
        instruct1.setAutoDraw(True)
    
    # *ok1* updates
    if t >= 0.0 and ok1.status == NOT_STARTED:
        # keep track of start time/frame for later
        ok1.tStart = t  # underestimates by a little under one frame
        ok1.frameNStart = frameN  # exact frame index
        ok1.status = STARTED
        # keyboard checking is just starting
        ok1.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if ok1.status == STARTED:
        theseKeys = event.getKeys(keyList=['9'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            if ok1.keys == []:  # then this was the first keypress
                ok1.keys = theseKeys[0]  # just the first key pressed
                ok1.rt = ok1.clock.getTime()
                # a response ends the routine
                continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrPracticeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "instrPractice"-------
for thisComponent in instrPracticeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if ok1.keys in ['', [], None]:  # No response was made
   ok1.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('ok1.keys',ok1.keys)
if ok1.keys != None:  # we had a response
    thisExp.addData('ok1.rt', ok1.rt)
thisExp.nextEntry()
# the Routine "instrPractice" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
pracTrials = data.TrialHandler(nReps=1, method='fullRandom', 
    extraInfo=expInfo, originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
    trialList=data.importConditions('TrialtypesLearningPrac.xlsx'),
    seed=None, name='pracTrials')
thisExp.addLoop(pracTrials)  # add the loop to the experiment
thisPracTrial = pracTrials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisPracTrial.rgb)
if thisPracTrial != None:
    for paramName in thisPracTrial.keys():
        exec(paramName + '= thisPracTrial.' + paramName)

for thisPracTrial in pracTrials:
    currentLoop = pracTrials
    # abbreviate parameter names if possible (e.g. rgb = thisPracTrial.rgb)
    if thisPracTrial != None:
        for paramName in thisPracTrial.keys():
            exec(paramName + '= thisPracTrial.' + paramName)
    
    #------Prepare to start Routine "NewPracStim"-------
    t = 0
    NewPracStimClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    #***************************
    
    SameStimPresentationCount = 0
    
    currentLearningPracTrial = learningPracTrialList.pop(0)
    currentStimulus = currentLearningPracTrial['fileName']
    currentReward = currentLearningPracTrial['reward']
    currentStimType = currentLearningPracTrial['condition']
    
    #***************************
    # keep track of which components have finished
    NewPracStimComponents = []
    for thisComponent in NewPracStimComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "NewPracStim"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = NewPracStimClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in NewPracStimComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "NewPracStim"-------
    for thisComponent in NewPracStimComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "NewPracStim" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    ReDoLoopPrac = data.TrialHandler(nReps=5, method='sequential', 
        extraInfo=expInfo, originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
        trialList=[None],
        seed=None, name='ReDoLoopPrac')
    thisExp.addLoop(ReDoLoopPrac)  # add the loop to the experiment
    thisReDoLoopPrac = ReDoLoopPrac.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisReDoLoopPrac.rgb)
    if thisReDoLoopPrac != None:
        for paramName in thisReDoLoopPrac.keys():
            exec(paramName + '= thisReDoLoopPrac.' + paramName)
    
    for thisReDoLoopPrac in ReDoLoopPrac:
        currentLoop = ReDoLoopPrac
        # abbreviate parameter names if possible (e.g. rgb = thisReDoLoopPrac.rgb)
        if thisReDoLoopPrac != None:
            for paramName in thisReDoLoopPrac.keys():
                exec(paramName + '= thisReDoLoopPrac.' + paramName)
        
        #------Prepare to start Routine "startTrialPrac"-------
        t = 0
        startTrialPracClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        SameStimPresentationCount = SameStimPresentationCount + 1
        # keep track of which components have finished
        startTrialPracComponents = []
        for thisComponent in startTrialPracComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "startTrialPrac"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = startTrialPracClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in startTrialPracComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "startTrialPrac"-------
        for thisComponent in startTrialPracComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # the Routine "startTrialPrac" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        #------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock 
        frameN = -1
        routineTimer.add(1.500000)
        # update component parameters for each repeat
        resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        resp.status = NOT_STARTED
        learningStim.setPos([xPos, yPos])
        learningStim.setImage(currentStimulus)
        # keep track of which components have finished
        trialComponents = []
        trialComponents.append(resp)
        trialComponents.append(learningFix)
        trialComponents.append(learningStim)
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "trial"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *resp* updates
            if t >= .5 and resp.status == NOT_STARTED:
                # keep track of start time/frame for later
                resp.tStart = t  # underestimates by a little under one frame
                resp.frameNStart = frameN  # exact frame index
                resp.status = STARTED
                # keyboard checking is just starting
                resp.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if resp.status == STARTED and t >= (.5 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
                resp.status = STOPPED
            if resp.status == STARTED:
                theseKeys = event.getKeys(keyList=['q', 'w', 's', 'a'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if resp.keys == []:  # then this was the first keypress
                        resp.keys = theseKeys[0]  # just the first key pressed
                        resp.rt = resp.clock.getTime()
                        # was this 'correct'?
                        if (resp.keys == str(corrAns)) or (resp.keys == corrAns):
                            resp.corr = 1
                        else:
                            resp.corr = 0
            
            # *learningFix* updates
            if t >= 0.0 and learningFix.status == NOT_STARTED:
                # keep track of start time/frame for later
                learningFix.tStart = t  # underestimates by a little under one frame
                learningFix.frameNStart = frameN  # exact frame index
                learningFix.setAutoDraw(True)
            if learningFix.status == STARTED and t >= (0.0 + (1.5-win.monitorFramePeriod*0.75)): #most of one frame period left
                learningFix.setAutoDraw(False)
            
            # *learningStim* updates
            if t >= .5 and learningStim.status == NOT_STARTED:
                # keep track of start time/frame for later
                learningStim.tStart = t  # underestimates by a little under one frame
                learningStim.frameNStart = frameN  # exact frame index
                learningStim.setAutoDraw(True)
            if learningStim.status == STARTED and t >= (.5 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                learningStim.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if resp.keys in ['', [], None]:  # No response was made
           resp.keys=None
           # was no response the correct answer?!
           if str(corrAns).lower() == 'none': resp.corr = 1  # correct non-response
           else: resp.corr = 0  # failed to respond (incorrectly)
        # store data for ReDoLoopPrac (TrialHandler)
        ReDoLoopPrac.addData('resp.keys',resp.keys)
        ReDoLoopPrac.addData('resp.corr', resp.corr)
        if resp.keys != None:  # we had a response
            ReDoLoopPrac.addData('resp.rt', resp.rt)
        
        #------Prepare to start Routine "feedback"-------
        t = 0
        feedbackClock.reset()  # clock 
        frameN = -1
        routineTimer.add(1.000000)
        # update component parameters for each repeat
        #***************************
        
        import random
        
        displayReward = random.randrange(1, 6)
        
        if resp.corr:#stored on last run routine
            if displayReward == 1:
                computedReward = 0 # On 20% of all trials I want to give a 0 reward
            else: 
                computedReward = round(currentReward + (random.randrange(-25, 26)*.01), 2)
            message = "You won $ %.2f" %computedReward
        elif resp.keys is None: 
            message ="Too Slow"
            computedReward = 0 
        else:
            message="Wrong"
            computedReward = 0
        
        #***************************
        feedback_2.setText(message)
        image.setPos([xPos, yPos])
        image.setImage(currentStimulus)
        feedbackResp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        feedbackResp.status = NOT_STARTED
        # keep track of which components have finished
        feedbackComponents = []
        feedbackComponents.append(feedback_2)
        feedbackComponents.append(image)
        feedbackComponents.append(feedbackResp)
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "feedback"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = feedbackClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # *feedback_2* updates
            if t >= 0.0 and feedback_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                feedback_2.tStart = t  # underestimates by a little under one frame
                feedback_2.frameNStart = frameN  # exact frame index
                feedback_2.setAutoDraw(True)
            if feedback_2.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                feedback_2.setAutoDraw(False)
            
            # *image* updates
            if t >= 0.0 and image.status == NOT_STARTED:
                # keep track of start time/frame for later
                image.tStart = t  # underestimates by a little under one frame
                image.frameNStart = frameN  # exact frame index
                image.setAutoDraw(True)
            if image.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                image.setAutoDraw(False)
            
            # *feedbackResp* updates
            if t >= 0.0 and feedbackResp.status == NOT_STARTED:
                # keep track of start time/frame for later
                feedbackResp.tStart = t  # underestimates by a little under one frame
                feedbackResp.frameNStart = frameN  # exact frame index
                feedbackResp.status = STARTED
                # keyboard checking is just starting
                feedbackResp.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if feedbackResp.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                feedbackResp.status = STOPPED
            if feedbackResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['q', 'w', 's', 'a'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if feedbackResp.keys == []:  # then this was the first keypress
                        feedbackResp.keys = theseKeys[0]  # just the first key pressed
                        feedbackResp.rt = feedbackResp.clock.getTime()
                        # was this 'correct'?
                        if (feedbackResp.keys == str(corrAns)) or (feedbackResp.keys == corrAns):
                            feedbackResp.corr = 1
                        else:
                            feedbackResp.corr = 0
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "feedback"-------
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # check responses
        if feedbackResp.keys in ['', [], None]:  # No response was made
           feedbackResp.keys=None
           # was no response the correct answer?!
           if str(corrAns).lower() == 'none': feedbackResp.corr = 1  # correct non-response
           else: feedbackResp.corr = 0  # failed to respond (incorrectly)
        # store data for ReDoLoopPrac (TrialHandler)
        ReDoLoopPrac.addData('feedbackResp.keys',feedbackResp.keys)
        ReDoLoopPrac.addData('feedbackResp.corr', feedbackResp.corr)
        if feedbackResp.keys != None:  # we had a response
            ReDoLoopPrac.addData('feedbackResp.rt', feedbackResp.rt)
        
        #------Prepare to start Routine "Blank"-------
        t = 0
        BlankClock.reset()  # clock 
        frameN = -1
        routineTimer.add(0.500000)
        # update component parameters for each repeat
        # keep track of which components have finished
        BlankComponents = []
        BlankComponents.append(text_2)
        for thisComponent in BlankComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "Blank"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = BlankClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text_2* updates
            if t >= 0 and text_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                text_2.tStart = t  # underestimates by a little under one frame
                text_2.frameNStart = frameN  # exact frame index
                text_2.setAutoDraw(True)
            if text_2.status == STARTED and t >= (0 + (.5-win.monitorFramePeriod*0.75)): #most of one frame period left
                text_2.setAutoDraw(False)
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in BlankComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "Blank"-------
        for thisComponent in BlankComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        #------Prepare to start Routine "endTrial"-------
        t = 0
        endTrialClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        
        # keep track of which components have finished
        endTrialComponents = []
        for thisComponent in endTrialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "endTrial"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = endTrialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in endTrialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "endTrial"-------
        for thisComponent in endTrialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        #***************************
        
        if resp.corr:
            ReDoLoopPrac.finished = True
        
        pracTrials.addData("currentReward", currentReward)
        pracTrials.addData("currentStimulus", currentStimulus) 
        pracTrials.addData("currentStimType", currentStimType)
        
        if SameStimPresentationCount == 1:
            pracTrials.addData("firstPracComputedRewardOutput", computedReward)
            pracTrials.addData("firstPracLearningStimOnset", learningStim.tStart)
            pracTrials.addData("firstPracLearningFixOnset", learningFix.tStart)
            pracTrials.addData("firstPracPresentationRT", resp.rt)
            pracTrials.addData("firstPracPresentationAcc", resp.corr)
            pracTrials.addData("firstPracPresentationResp", resp.keys)
            pracTrials.addData("firstPracEndTrialTimeStamp", core.getTime())
        elif SameStimPresentationCount == 2: 
            pracTrials.addData("secondPracComputedRewardOutput", computedReward)
            pracTrials.addData("secondPracLearningStimOnset", learningStim.tStart)
            pracTrials.addData("secondPracLearningFixOnset", learningFix.tStart)
            pracTrials.addData("secondPracPresentationRT", resp.rt)
            pracTrials.addData("secondPracPresentationAcc", resp.corr)
            pracTrials.addData("secondPracPresentationResp", resp.keys)
            pracTrials.addData("secondPracEndTrialTimeStamp", core.getTime())
        elif SameStimPresentationCount == 3: 
            pracTrials.addData("thirdPracComputedRewardOutput", computedReward)
            pracTrials.addData("thirdPracLearningStimOnset", learningStim.tStart)
            pracTrials.addData("thirdPracLearningFixOnset", learningFix.tStart)
            pracTrials.addData("thirdPracPresentationRT", resp.rt)
            pracTrials.addData("thirdPracPresentationAcc", resp.corr)
            pracTrials.addData("thirdPracPresentationResp", resp.keys)
            pracTrials.addData("thirdPracEndTrialTimeStamp", core.getTime())
        elif SameStimPresentationCount == 4: 
            pracTrials.addData("fourthPracComputedRewardOutput", computedReward)
            pracTrials.addData("fourthPracLearningStimOnset", learningStim.tStart)
            pracTrials.addData("fourthPracLearningFixOnset", learningFix.tStart)
            pracTrials.addData("fourthPracPresentationRT", resp.rt)
            pracTrials.addData("fourthPracPresentationAcc", resp.corr)
            pracTrials.addData("fourthPracPresentationResp", resp.keys)
            pracTrials.addData("fourthPracEndTrialTimeStamp", core.getTime())
        elif SameStimPresentationCount == 5: 
            pracTrials.addData("fifthPracComputedRewardOutput", computedReward)
            pracTrials.addData("fifthPracLearningStimOnset", learningStim.tStart)
            pracTrials.addData("fifthPracLearningFixOnset", learningFix.tStart)
            pracTrials.addData("fifthPracPresentationRT", resp.rt)
            pracTrials.addData("fifthPracPresentationAcc", resp.corr)
            pracTrials.addData("fifthPracPresentationResp", resp.keys)
            pracTrials.addData("fifthPracEndTrialTimeStamp", core.getTime())
        
        #***************************
        # the Routine "endTrial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
    # completed 5 repeats of 'ReDoLoopPrac'
    
    thisExp.nextEntry()
    
# completed 1 repeats of 'pracTrials'

# get names of stimulus parameters
if pracTrials.trialList in ([], [None], None):  params = []
else:  params = pracTrials.trialList[0].keys()
# save data for this loop
pracTrials.saveAsExcel(filename + '.xlsx', sheetName='pracTrials',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

#------Prepare to start Routine "instrStopPrac"-------
t = 0
instrStopPracClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp_2.status = NOT_STARTED
#***************************

InitSSD = .25
SSDLeft = InitSSD
SSDRight = InitSSD
goCumRT = 0
goRTCount = 0
omissionCount = 0
commissionCount = 0
stopTrialCount = 0
stopSuccessCount = 0
goTrialCount = 0

#***************************
# keep track of which components have finished
instrStopPracComponents = []
instrStopPracComponents.append(instrStopText)
instrStopPracComponents.append(key_resp_2)
for thisComponent in instrStopPracComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instrStopPrac"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instrStopPracClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrStopText* updates
    if t >= 0.0 and instrStopText.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrStopText.tStart = t  # underestimates by a little under one frame
        instrStopText.frameNStart = frameN  # exact frame index
        instrStopText.setAutoDraw(True)
    
    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_2.tStart = t  # underestimates by a little under one frame
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['9'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrStopPracComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "instrStopPrac"-------
for thisComponent in instrStopPracComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "instrStopPrac" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
pracStopTrials = data.TrialHandler(nReps=5, method='fullRandom', 
    extraInfo=expInfo, originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
    trialList=data.importConditions('trialtypeStop.xlsx'),
    seed=None, name='pracStopTrials')
thisExp.addLoop(pracStopTrials)  # add the loop to the experiment
thisPracStopTrial = pracStopTrials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisPracStopTrial.rgb)
if thisPracStopTrial != None:
    for paramName in thisPracStopTrial.keys():
        exec(paramName + '= thisPracStopTrial.' + paramName)

for thisPracStopTrial in pracStopTrials:
    currentLoop = pracStopTrials
    # abbreviate parameter names if possible (e.g. rgb = thisPracStopTrial.rgb)
    if thisPracStopTrial != None:
        for paramName in thisPracStopTrial.keys():
            exec(paramName + '= thisPracStopTrial.' + paramName)
    
    #------Prepare to start Routine "newPracStopStim"-------
    t = 0
    newPracStopStimClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    #***************************
    pracStopTrials.addData("StartTrialTimeStamp", core.getTime())
    
    currentStopPracTrial = stopPracTrialList.pop(0)
    currentGoStim = currentStopPracTrial['fileName']
    currentStopOrGo = currentStopPracTrial['stopOrGo']
    currentStimType = currentStopPracTrial['condition']
    currentStopStimValue = currentStopPracTrial['reward']
    
    if currentStopOrGo == 'stop':
        SSD = .25
        stopSignal.setVolume(.2)
    elif currentStopOrGo == 'go': 
        SSD = -1 #This makes it so the auditory tone does not occur. There's probably a more elegant way to do this. Suggestions?
        stopSignal.setVolume(0)
    #
    pracStopTrials.addData("trialType", currentStopOrGo)
    pracStopTrials.addData("goStim", currentGoStim)
    pracStopTrials.addData("stimType", currentStimType)
    pracStopTrials.addData("stopStimValue", currentStopStimValue)
    SSDInput = SSD + .5 # +.5 because that's the duration of the fixation cross before the go stim appears
    
    #***************************
    # keep track of which components have finished
    newPracStopStimComponents = []
    for thisComponent in newPracStopStimComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "newPracStopStim"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = newPracStopStimClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in newPracStopStimComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "newPracStopStim"-------
    for thisComponent in newPracStopStimComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "newPracStopStim" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    #------Prepare to start Routine "StopTrial"-------
    t = 0
    StopTrialClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    goStim.setPos([xPosGoStim, yPosGoStim])
    goStim.setImage(currentGoStim)
    goResp = event.BuilderKeyResponse()  # create an object of type KeyResponse
    goResp.status = NOT_STARTED
    # keep track of which components have finished
    StopTrialComponents = []
    StopTrialComponents.append(stopSignal)
    StopTrialComponents.append(fixStop)
    StopTrialComponents.append(goStim)
    StopTrialComponents.append(goResp)
    for thisComponent in StopTrialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "StopTrial"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = StopTrialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # start/stop stopSignal
        if t >= SSDInput and stopSignal.status == NOT_STARTED:
            # keep track of start time/frame for later
            stopSignal.tStart = t  # underestimates by a little under one frame
            stopSignal.frameNStart = frameN  # exact frame index
            stopSignal.play()  # start the sound (it finishes automatically)
        if stopSignal.status == STARTED and t >= (SSDInput + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
            stopSignal.stop()  # stop the sound (if longer than duration)
        
        # *fixStop* updates
        if t >= 0.0 and fixStop.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixStop.tStart = t  # underestimates by a little under one frame
            fixStop.frameNStart = frameN  # exact frame index
            fixStop.setAutoDraw(True)
        if fixStop.status == STARTED and t >= (0.0 + (1.5-win.monitorFramePeriod*0.75)): #most of one frame period left
            fixStop.setAutoDraw(False)
        
        # *goStim* updates
        if t >= .5 and goStim.status == NOT_STARTED:
            # keep track of start time/frame for later
            goStim.tStart = t  # underestimates by a little under one frame
            goStim.frameNStart = frameN  # exact frame index
            goStim.setAutoDraw(True)
        if goStim.status == STARTED and t >= (.5 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
            goStim.setAutoDraw(False)
        
        # *goResp* updates
        if t >= .5 and goResp.status == NOT_STARTED:
            # keep track of start time/frame for later
            goResp.tStart = t  # underestimates by a little under one frame
            goResp.frameNStart = frameN  # exact frame index
            goResp.status = STARTED
            # keyboard checking is just starting
            goResp.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if goResp.status == STARTED and t >= (.5 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
            goResp.status = STOPPED
        if goResp.status == STARTED:
            theseKeys = event.getKeys(keyList=['z', 'm'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if goResp.keys == []:  # then this was the first keypress
                    goResp.keys = theseKeys[0]  # just the first key pressed
                    goResp.rt = goResp.clock.getTime()
                    # was this 'correct'?
                    if (goResp.keys == str(corrGoResp)) or (goResp.keys == corrGoResp):
                        goResp.corr = 1
                    else:
                        goResp.corr = 0
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in StopTrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "StopTrial"-------
    for thisComponent in StopTrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    stopSignal.stop() #ensure sound has stopped at end of routine
    # check responses
    if goResp.keys in ['', [], None]:  # No response was made
       goResp.keys=None
       # was no response the correct answer?!
       if str(corrGoResp).lower() == 'none': goResp.corr = 1  # correct non-response
       else: goResp.corr = 0  # failed to respond (incorrectly)
    # store data for pracStopTrials (TrialHandler)
    pracStopTrials.addData('goResp.keys',goResp.keys)
    pracStopTrials.addData('goResp.corr', goResp.corr)
    if goResp.keys != None:  # we had a response
        pracStopTrials.addData('goResp.rt', goResp.rt)
    # the Routine "StopTrial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    #------Prepare to start Routine "blankStop"-------
    t = 0
    blankStopClock.reset()  # clock 
    frameN = -1
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    key_resp_9 = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_resp_9.status = NOT_STARTED
    # keep track of which components have finished
    blankStopComponents = []
    blankStopComponents.append(text_4)
    blankStopComponents.append(key_resp_9)
    for thisComponent in blankStopComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "blankStop"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = blankStopClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_4* updates
        if t >= 0.0 and text_4.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_4.tStart = t  # underestimates by a little under one frame
            text_4.frameNStart = frameN  # exact frame index
            text_4.setAutoDraw(True)
        if text_4.status == STARTED and t >= (0.0 + (1.5-win.monitorFramePeriod*0.75)): #most of one frame period left
            text_4.setAutoDraw(False)
        
        # *key_resp_9* updates
        if t >= 0.0 and key_resp_9.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_9.tStart = t  # underestimates by a little under one frame
            key_resp_9.frameNStart = frameN  # exact frame index
            key_resp_9.status = STARTED
            # keyboard checking is just starting
            key_resp_9.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if key_resp_9.status == STARTED and t >= (0.0 + (1.5-win.monitorFramePeriod*0.75)): #most of one frame period left
            key_resp_9.status = STOPPED
        if key_resp_9.status == STARTED:
            theseKeys = event.getKeys(keyList=['z', 'm'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if key_resp_9.keys == []:  # then this was the first keypress
                    key_resp_9.keys = theseKeys[0]  # just the first key pressed
                    key_resp_9.rt = key_resp_9.clock.getTime()
                    # was this 'correct'?
                    if (key_resp_9.keys == str(corrGoResp)) or (key_resp_9.keys == corrGoResp):
                        key_resp_9.corr = 1
                    else:
                        key_resp_9.corr = 0
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in blankStopComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "blankStop"-------
    for thisComponent in blankStopComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_9.keys in ['', [], None]:  # No response was made
       key_resp_9.keys=None
       # was no response the correct answer?!
       if str(corrGoResp).lower() == 'none': key_resp_9.corr = 1  # correct non-response
       else: key_resp_9.corr = 0  # failed to respond (incorrectly)
    # store data for pracStopTrials (TrialHandler)
    pracStopTrials.addData('key_resp_9.keys',key_resp_9.keys)
    pracStopTrials.addData('key_resp_9.corr', key_resp_9.corr)
    if key_resp_9.keys != None:  # we had a response
        pracStopTrials.addData('key_resp_9.rt', key_resp_9.rt)
    
    #------Prepare to start Routine "pracStopCleanUp"-------
    t = 0
    pracStopCleanUpClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    #***************************
    
    if currentStopPracTrial['stopOrGo'] == 'go':
        goTrialCount = goTrialCount + 1
    
    if goResp.corr and currentStopPracTrial['stopOrGo'] == 'go':
        goCumRT = goCumRT + goResp.rt
        goRTCount = goRTCount + 1
    
    if currentStopPracTrial['stopOrGo'] == 'stop':
        stopTrialCount = stopTrialCount + 1
    
    if currentStopPracTrial['stopOrGo'] == 'stop' and goResp.keys is None and key_resp_9.keys is None:
        stopSuccessCount = stopSuccessCount + 1
    
    if currentStopPracTrial['stopOrGo'] == 'go':
        if goResp.keys is None:
            omissionCount = omissionCount + 1
        elif goResp.corr == 0:
            commissionCount = commissionCount + 1
    
    #Outputting a bunch of variables
    pracStopTrials.addData("fixStopOnset", fixStop.tStart)
    pracStopTrials.addData("goStimOnset", goStim.tStart)
    if SSD  != -1:
        pracStopTrials.addData("stopSignalOnset", stopSignal.tStart)
    
    #***************************
    # keep track of which components have finished
    pracStopCleanUpComponents = []
    for thisComponent in pracStopCleanUpComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "pracStopCleanUp"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = pracStopCleanUpClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in pracStopCleanUpComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "pracStopCleanUp"-------
    for thisComponent in pracStopCleanUpComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    pracStopTrials.addData("EndTrialTimeStamp", core.getTime())
    # the Routine "pracStopCleanUp" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 5 repeats of 'pracStopTrials'

# get names of stimulus parameters
if pracStopTrials.trialList in ([], [None], None):  params = []
else:  params = pracStopTrials.trialList[0].keys()
# save data for this loop
pracStopTrials.saveAsExcel(filename + '.xlsx', sheetName='pracStopTrials',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

#------Prepare to start Routine "endOfStopBlockFeedback"-------
t = 0
endOfStopBlockFeedbackClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
#***************************

if goRTCount > 0:
    goRTFeedback = goCumRT/goRTCount
    goRTFeedback = round(goRTFeedback, 2)
else:
    goRTFeedback = 'Null'

if goTrialCount > 0:
    commissionRate = (commissionCount/goTrialCount)*100
    commissionRate = round(commissionRate, 2)
    omissionRate = (omissionCount/goTrialCount)*100
    omissionRate = round(omissionRate, 2)
else: 
    commissionRate = 'Null'
    omissionRate = 'Null'

if stopTrialCount > 0: 
    probabilityOfStop = stopSuccessCount/stopTrialCount
    probabilityOfStop = round(probabilityOfStop, 2)
else:
    probabilityOfStop = 'Null'

SSDFeedback = (SSDLeft+SSDRight)/2
SSDFeedback = round(SSDFeedback, 2)

stopMessage = " RT = " + str(goRTFeedback) + "\n Omission % = " + str(omissionRate) + "\n Commission % = " + str(commissionRate) + "\n\n\n\n " + str(probabilityOfStop) + "\n " + str(SSDFeedback) + "\n\n (Press the 9 key to continue)"

#***************************
text_5.setText(stopMessage)
key_resp_3 = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp_3.status = NOT_STARTED
# keep track of which components have finished
endOfStopBlockFeedbackComponents = []
endOfStopBlockFeedbackComponents.append(text_5)
endOfStopBlockFeedbackComponents.append(key_resp_3)
for thisComponent in endOfStopBlockFeedbackComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "endOfStopBlockFeedback"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = endOfStopBlockFeedbackClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # *text_5* updates
    if t >= 0.0 and text_5.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_5.tStart = t  # underestimates by a little under one frame
        text_5.frameNStart = frameN  # exact frame index
        text_5.setAutoDraw(True)
    
    # *key_resp_3* updates
    if t >= 0.0 and key_resp_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_3.tStart = t  # underestimates by a little under one frame
        key_resp_3.frameNStart = frameN  # exact frame index
        key_resp_3.status = STARTED
        # keyboard checking is just starting
        key_resp_3.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if key_resp_3.status == STARTED:
        theseKeys = event.getKeys(keyList=['9'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_3.keys = theseKeys[-1]  # just the last key pressed
            key_resp_3.rt = key_resp_3.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endOfStopBlockFeedbackComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "endOfStopBlockFeedback"-------
for thisComponent in endOfStopBlockFeedbackComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if key_resp_3.keys in ['', [], None]:  # No response was made
   key_resp_3.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('key_resp_3.keys',key_resp_3.keys)
if key_resp_3.keys != None:  # we had a response
    thisExp.addData('key_resp_3.rt', key_resp_3.rt)
thisExp.nextEntry()
# the Routine "endOfStopBlockFeedback" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "instrPractice"-------
t = 0
instrPracticeClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
ok1 = event.BuilderKeyResponse()  # create an object of type KeyResponse
ok1.status = NOT_STARTED
# keep track of which components have finished
instrPracticeComponents = []
instrPracticeComponents.append(instruct1)
instrPracticeComponents.append(ok1)
for thisComponent in instrPracticeComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instrPractice"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instrPracticeClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instruct1* updates
    if t >= 0.0 and instruct1.status == NOT_STARTED:
        # keep track of start time/frame for later
        instruct1.tStart = t  # underestimates by a little under one frame
        instruct1.frameNStart = frameN  # exact frame index
        instruct1.setAutoDraw(True)
    
    # *ok1* updates
    if t >= 0.0 and ok1.status == NOT_STARTED:
        # keep track of start time/frame for later
        ok1.tStart = t  # underestimates by a little under one frame
        ok1.frameNStart = frameN  # exact frame index
        ok1.status = STARTED
        # keyboard checking is just starting
        ok1.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if ok1.status == STARTED:
        theseKeys = event.getKeys(keyList=['9'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            if ok1.keys == []:  # then this was the first keypress
                ok1.keys = theseKeys[0]  # just the first key pressed
                ok1.rt = ok1.clock.getTime()
                # a response ends the routine
                continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrPracticeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "instrPractice"-------
for thisComponent in instrPracticeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if ok1.keys in ['', [], None]:  # No response was made
   ok1.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('ok1.keys',ok1.keys)
if ok1.keys != None:  # we had a response
    thisExp.addData('ok1.rt', ok1.rt)
thisExp.nextEntry()
# the Routine "instrPractice" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
Blocks = data.TrialHandler(nReps=4, method='sequential', 
    extraInfo=expInfo, originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
    trialList=[None],
    seed=None, name='Blocks')
thisExp.addLoop(Blocks)  # add the loop to the experiment
thisBlock = Blocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisBlock.rgb)
if thisBlock != None:
    for paramName in thisBlock.keys():
        exec(paramName + '= thisBlock.' + paramName)

for thisBlock in Blocks:
    currentLoop = Blocks
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock.keys():
            exec(paramName + '= thisBlock.' + paramName)
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=25.0, method='fullRandom', 
        extraInfo=expInfo, originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
        trialList=data.importConditions('TrialtypesLearning.xlsx'),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)
        
        #------Prepare to start Routine "NewStim"-------
        t = 0
        NewStimClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        #***************************
        
        SameStimPresentationCount = 0
        
        currentLearningTrial = learningTrialList.pop(0)
        currentStimulus = currentLearningTrial['fileName']
        currentReward = currentLearningTrial['reward']
        currentStimType = currentLearningTrial['condition']
        
        #***************************
        # keep track of which components have finished
        NewStimComponents = []
        for thisComponent in NewStimComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "NewStim"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = NewStimClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in NewStimComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "NewStim"-------
        for thisComponent in NewStimComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # the Routine "NewStim" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        ReDoLoopMain = data.TrialHandler(nReps=5, method='sequential', 
            extraInfo=expInfo, originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
            trialList=[None],
            seed=None, name='ReDoLoopMain')
        thisExp.addLoop(ReDoLoopMain)  # add the loop to the experiment
        thisReDoLoopMain = ReDoLoopMain.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb=thisReDoLoopMain.rgb)
        if thisReDoLoopMain != None:
            for paramName in thisReDoLoopMain.keys():
                exec(paramName + '= thisReDoLoopMain.' + paramName)
        
        for thisReDoLoopMain in ReDoLoopMain:
            currentLoop = ReDoLoopMain
            # abbreviate parameter names if possible (e.g. rgb = thisReDoLoopMain.rgb)
            if thisReDoLoopMain != None:
                for paramName in thisReDoLoopMain.keys():
                    exec(paramName + '= thisReDoLoopMain.' + paramName)
            
            #------Prepare to start Routine "startTrial"-------
            t = 0
            startTrialClock.reset()  # clock 
            frameN = -1
            # update component parameters for each repeat
            SameStimPresentationCount = SameStimPresentationCount + 1
            # keep track of which components have finished
            startTrialComponents = []
            for thisComponent in startTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            #-------Start Routine "startTrial"-------
            continueRoutine = True
            while continueRoutine:
                # get current time
                t = startTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in startTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            #-------Ending Routine "startTrial"-------
            for thisComponent in startTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            
            # the Routine "startTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            #------Prepare to start Routine "trial"-------
            t = 0
            trialClock.reset()  # clock 
            frameN = -1
            routineTimer.add(1.500000)
            # update component parameters for each repeat
            resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
            resp.status = NOT_STARTED
            learningStim.setPos([xPos, yPos])
            learningStim.setImage(currentStimulus)
            # keep track of which components have finished
            trialComponents = []
            trialComponents.append(resp)
            trialComponents.append(learningFix)
            trialComponents.append(learningStim)
            for thisComponent in trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            #-------Start Routine "trial"-------
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *resp* updates
                if t >= .5 and resp.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    resp.tStart = t  # underestimates by a little under one frame
                    resp.frameNStart = frameN  # exact frame index
                    resp.status = STARTED
                    # keyboard checking is just starting
                    resp.clock.reset()  # now t=0
                    event.clearEvents(eventType='keyboard')
                if resp.status == STARTED and t >= (.5 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
                    resp.status = STOPPED
                if resp.status == STARTED:
                    theseKeys = event.getKeys(keyList=['q', 'w', 's', 'a'])
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if resp.keys == []:  # then this was the first keypress
                            resp.keys = theseKeys[0]  # just the first key pressed
                            resp.rt = resp.clock.getTime()
                            # was this 'correct'?
                            if (resp.keys == str(corrAns)) or (resp.keys == corrAns):
                                resp.corr = 1
                            else:
                                resp.corr = 0
                
                # *learningFix* updates
                if t >= 0.0 and learningFix.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    learningFix.tStart = t  # underestimates by a little under one frame
                    learningFix.frameNStart = frameN  # exact frame index
                    learningFix.setAutoDraw(True)
                if learningFix.status == STARTED and t >= (0.0 + (1.5-win.monitorFramePeriod*0.75)): #most of one frame period left
                    learningFix.setAutoDraw(False)
                
                # *learningStim* updates
                if t >= .5 and learningStim.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    learningStim.tStart = t  # underestimates by a little under one frame
                    learningStim.frameNStart = frameN  # exact frame index
                    learningStim.setAutoDraw(True)
                if learningStim.status == STARTED and t >= (.5 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                    learningStim.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            #-------Ending Routine "trial"-------
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # check responses
            if resp.keys in ['', [], None]:  # No response was made
               resp.keys=None
               # was no response the correct answer?!
               if str(corrAns).lower() == 'none': resp.corr = 1  # correct non-response
               else: resp.corr = 0  # failed to respond (incorrectly)
            # store data for ReDoLoopMain (TrialHandler)
            ReDoLoopMain.addData('resp.keys',resp.keys)
            ReDoLoopMain.addData('resp.corr', resp.corr)
            if resp.keys != None:  # we had a response
                ReDoLoopMain.addData('resp.rt', resp.rt)
            
            #------Prepare to start Routine "feedback"-------
            t = 0
            feedbackClock.reset()  # clock 
            frameN = -1
            routineTimer.add(1.000000)
            # update component parameters for each repeat
            #***************************
            
            import random
            
            displayReward = random.randrange(1, 6)
            
            if resp.corr:#stored on last run routine
                if displayReward == 1:
                    computedReward = 0 # On 20% of all trials I want to give a 0 reward
                else: 
                    computedReward = round(currentReward + (random.randrange(-25, 26)*.01), 2)
                message = "You won $ %.2f" %computedReward
            elif resp.keys is None: 
                message ="Too Slow"
                computedReward = 0 
            else:
                message="Wrong"
                computedReward = 0
            
            #***************************
            feedback_2.setText(message)
            image.setPos([xPos, yPos])
            image.setImage(currentStimulus)
            feedbackResp = event.BuilderKeyResponse()  # create an object of type KeyResponse
            feedbackResp.status = NOT_STARTED
            # keep track of which components have finished
            feedbackComponents = []
            feedbackComponents.append(feedback_2)
            feedbackComponents.append(image)
            feedbackComponents.append(feedbackResp)
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            #-------Start Routine "feedback"-------
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = feedbackClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                
                # *feedback_2* updates
                if t >= 0.0 and feedback_2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    feedback_2.tStart = t  # underestimates by a little under one frame
                    feedback_2.frameNStart = frameN  # exact frame index
                    feedback_2.setAutoDraw(True)
                if feedback_2.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                    feedback_2.setAutoDraw(False)
                
                # *image* updates
                if t >= 0.0 and image.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    image.tStart = t  # underestimates by a little under one frame
                    image.frameNStart = frameN  # exact frame index
                    image.setAutoDraw(True)
                if image.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                    image.setAutoDraw(False)
                
                # *feedbackResp* updates
                if t >= 0.0 and feedbackResp.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    feedbackResp.tStart = t  # underestimates by a little under one frame
                    feedbackResp.frameNStart = frameN  # exact frame index
                    feedbackResp.status = STARTED
                    # keyboard checking is just starting
                    feedbackResp.clock.reset()  # now t=0
                    event.clearEvents(eventType='keyboard')
                if feedbackResp.status == STARTED and t >= (0.0 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                    feedbackResp.status = STOPPED
                if feedbackResp.status == STARTED:
                    theseKeys = event.getKeys(keyList=['q', 'w', 's', 'a'])
                    
                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if feedbackResp.keys == []:  # then this was the first keypress
                            feedbackResp.keys = theseKeys[0]  # just the first key pressed
                            feedbackResp.rt = feedbackResp.clock.getTime()
                            # was this 'correct'?
                            if (feedbackResp.keys == str(corrAns)) or (feedbackResp.keys == corrAns):
                                feedbackResp.corr = 1
                            else:
                                feedbackResp.corr = 0
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in feedbackComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            #-------Ending Routine "feedback"-------
            for thisComponent in feedbackComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            
            # check responses
            if feedbackResp.keys in ['', [], None]:  # No response was made
               feedbackResp.keys=None
               # was no response the correct answer?!
               if str(corrAns).lower() == 'none': feedbackResp.corr = 1  # correct non-response
               else: feedbackResp.corr = 0  # failed to respond (incorrectly)
            # store data for ReDoLoopMain (TrialHandler)
            ReDoLoopMain.addData('feedbackResp.keys',feedbackResp.keys)
            ReDoLoopMain.addData('feedbackResp.corr', feedbackResp.corr)
            if feedbackResp.keys != None:  # we had a response
                ReDoLoopMain.addData('feedbackResp.rt', feedbackResp.rt)
            
            #------Prepare to start Routine "Blank"-------
            t = 0
            BlankClock.reset()  # clock 
            frameN = -1
            routineTimer.add(0.500000)
            # update component parameters for each repeat
            # keep track of which components have finished
            BlankComponents = []
            BlankComponents.append(text_2)
            for thisComponent in BlankComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            #-------Start Routine "Blank"-------
            continueRoutine = True
            while continueRoutine and routineTimer.getTime() > 0:
                # get current time
                t = BlankClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *text_2* updates
                if t >= 0 and text_2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    text_2.tStart = t  # underestimates by a little under one frame
                    text_2.frameNStart = frameN  # exact frame index
                    text_2.setAutoDraw(True)
                if text_2.status == STARTED and t >= (0 + (.5-win.monitorFramePeriod*0.75)): #most of one frame period left
                    text_2.setAutoDraw(False)
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in BlankComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            #-------Ending Routine "Blank"-------
            for thisComponent in BlankComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            
            #------Prepare to start Routine "endTrialMain"-------
            t = 0
            endTrialMainClock.reset()  # clock 
            frameN = -1
            # update component parameters for each repeat
            
            # keep track of which components have finished
            endTrialMainComponents = []
            for thisComponent in endTrialMainComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            
            #-------Start Routine "endTrialMain"-------
            continueRoutine = True
            while continueRoutine:
                # get current time
                t = endTrialMainClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in endTrialMainComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            #-------Ending Routine "endTrialMain"-------
            for thisComponent in endTrialMainComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            #***************************
            
            if resp.corr:
                ReDoLoopMain.finished = True
                rewardList.append(deepcopy(computedReward))
            
            trials.addData("currentReward", currentReward)
            trials.addData("currentStimulus", currentStimulus) 
            trials.addData("currentStimType", currentStimType)
            
            if SameStimPresentationCount == 1:
                trials.addData("firstComputedRewardOutput", computedReward)
                trials.addData("firstLearningStimOnset", learningStim.tStart)
                trials.addData("firstLearningFixOnset", learningFix.tStart)
                trials.addData("firstPresentationRT", resp.rt)
                trials.addData("firstPresentationAcc", resp.corr)
                trials.addData("firstPresentationResp", resp.keys)
                trials.addData("firstEndTrialTimeStamp", core.getTime())
            elif SameStimPresentationCount == 2: 
                trials.addData("secondComputedRewardOutput", computedReward)
                trials.addData("secondLearningStimOnset", learningStim.tStart)
                trials.addData("secondLearningFixOnset", learningFix.tStart)
                trials.addData("secondPresentationRT", resp.rt)
                trials.addData("secondPresentationAcc", resp.corr)
                trials.addData("secondPresentationResp", resp.keys)
                trials.addData("secondEndTrialTimeStamp", core.getTime())
            elif SameStimPresentationCount == 3: 
                trials.addData("thirdComputedRewardOutput", computedReward)
                trials.addData("thirdLearningStimOnset", learningStim.tStart)
                trials.addData("thirdLearningFixOnset", learningFix.tStart)
                trials.addData("thirdPresentationRT", resp.rt)
                trials.addData("thirdPresentationAcc", resp.corr)
                trials.addData("thirdPresentationResp", resp.keys)
                trials.addData("thirdEndTrialTimeStamp", core.getTime())
            elif SameStimPresentationCount == 4: 
                trials.addData("fourthComputedRewardOutput", computedReward)
                trials.addData("fourthLearningStimOnset", learningStim.tStart)
                trials.addData("fourthLearningFixOnset", learningFix.tStart)
                trials.addData("fourthPresentationRT", resp.rt)
                trials.addData("fourthPresentationAcc", resp.corr)
                trials.addData("fourthPresentationResp", resp.keys)
                trials.addData("fourthEndTrialTimeStamp", core.getTime())
            elif SameStimPresentationCount == 5: 
                trials.addData("fifthComputedRewardOutput", computedReward)
                trials.addData("fifthLearningStimOnset", learningStim.tStart)
                trials.addData("fifthLearningFixOnset", learningFix.tStart)
                trials.addData("fifthPresentationRT", resp.rt)
                trials.addData("fifthPresentationAcc", resp.corr)
                trials.addData("fifthPresentationResp", resp.keys)
                trials.addData("fifthEndTrialTimeStamp", core.getTime())
            
            #***************************
            # the Routine "endTrialMain" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
        # completed 5 repeats of 'ReDoLoopMain'
        
        thisExp.nextEntry()
        
    # completed 25.0 repeats of 'trials'
    
    # get names of stimulus parameters
    if trials.trialList in ([], [None], None):  params = []
    else:  params = trials.trialList[0].keys()
    # save data for this loop
    trials.saveAsExcel(filename + '.xlsx', sheetName='trials',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    
    #------Prepare to start Routine "learningRest"-------
    t = 0
    learningRestClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    key_resp_7 = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_resp_7.status = NOT_STARTED
    # keep track of which components have finished
    learningRestComponents = []
    learningRestComponents.append(text)
    learningRestComponents.append(key_resp_7)
    for thisComponent in learningRestComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "learningRest"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = learningRestClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        if t >= 0.0 and text.status == NOT_STARTED:
            # keep track of start time/frame for later
            text.tStart = t  # underestimates by a little under one frame
            text.frameNStart = frameN  # exact frame index
            text.setAutoDraw(True)
        
        # *key_resp_7* updates
        if t >= 0.0 and key_resp_7.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_7.tStart = t  # underestimates by a little under one frame
            key_resp_7.frameNStart = frameN  # exact frame index
            key_resp_7.status = STARTED
            # keyboard checking is just starting
            key_resp_7.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if key_resp_7.status == STARTED:
            theseKeys = event.getKeys(keyList=['9'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if key_resp_7.keys == []:  # then this was the first keypress
                    key_resp_7.keys = theseKeys[0]  # just the first key pressed
                    key_resp_7.rt = key_resp_7.clock.getTime()
                    # a response ends the routine
                    continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in learningRestComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "learningRest"-------
    for thisComponent in learningRestComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_7.keys in ['', [], None]:  # No response was made
       key_resp_7.keys=None
    # store data for Blocks (TrialHandler)
    Blocks.addData('key_resp_7.keys',key_resp_7.keys)
    if key_resp_7.keys != None:  # we had a response
        Blocks.addData('key_resp_7.rt', key_resp_7.rt)
    # the Routine "learningRest" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 4 repeats of 'Blocks'

# get names of stimulus parameters
if Blocks.trialList in ([], [None], None):  params = []
else:  params = Blocks.trialList[0].keys()
# save data for this loop
Blocks.saveAsExcel(filename + '.xlsx', sheetName='Blocks',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

#------Prepare to start Routine "instrStopPrac"-------
t = 0
instrStopPracClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp_2.status = NOT_STARTED
#***************************

InitSSD = .25
SSDLeft = InitSSD
SSDRight = InitSSD
goCumRT = 0
goRTCount = 0
omissionCount = 0
commissionCount = 0
stopTrialCount = 0
stopSuccessCount = 0
goTrialCount = 0

#***************************
# keep track of which components have finished
instrStopPracComponents = []
instrStopPracComponents.append(instrStopText)
instrStopPracComponents.append(key_resp_2)
for thisComponent in instrStopPracComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instrStopPrac"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instrStopPracClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrStopText* updates
    if t >= 0.0 and instrStopText.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrStopText.tStart = t  # underestimates by a little under one frame
        instrStopText.frameNStart = frameN  # exact frame index
        instrStopText.setAutoDraw(True)
    
    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_2.tStart = t  # underestimates by a little under one frame
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['9'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrStopPracComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "instrStopPrac"-------
for thisComponent in instrStopPracComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "instrStopPrac" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
StopBlocks = data.TrialHandler(nReps=8, method='sequential', 
    extraInfo=expInfo, originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
    trialList=[None],
    seed=None, name='StopBlocks')
thisExp.addLoop(StopBlocks)  # add the loop to the experiment
thisStopBlock = StopBlocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisStopBlock.rgb)
if thisStopBlock != None:
    for paramName in thisStopBlock.keys():
        exec(paramName + '= thisStopBlock.' + paramName)

for thisStopBlock in StopBlocks:
    currentLoop = StopBlocks
    # abbreviate parameter names if possible (e.g. rgb = thisStopBlock.rgb)
    if thisStopBlock != None:
        for paramName in thisStopBlock.keys():
            exec(paramName + '= thisStopBlock.' + paramName)
    
    #------Prepare to start Routine "stopBlockSetup"-------
    t = 0
    stopBlockSetupClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    #***************************
    
    goCumRT = 0
    goRTCount = 0
    omissionCount = 0
    commissionCount = 0
    stopTrialCount = 0
    stopSuccessCount = 0
    goTrialCount = 0
    
    #***************************
    # keep track of which components have finished
    stopBlockSetupComponents = []
    for thisComponent in stopBlockSetupComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "stopBlockSetup"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = stopBlockSetupClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in stopBlockSetupComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "stopBlockSetup"-------
    for thisComponent in stopBlockSetupComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "stopBlockSetup" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    StopTrials = data.TrialHandler(nReps=18, method='fullRandom', 
        extraInfo=expInfo, originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
        trialList=data.importConditions('trialtypeStop.xlsx'),
        seed=None, name='StopTrials')
    thisExp.addLoop(StopTrials)  # add the loop to the experiment
    thisStopTrial = StopTrials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisStopTrial.rgb)
    if thisStopTrial != None:
        for paramName in thisStopTrial.keys():
            exec(paramName + '= thisStopTrial.' + paramName)
    
    for thisStopTrial in StopTrials:
        currentLoop = StopTrials
        # abbreviate parameter names if possible (e.g. rgb = thisStopTrial.rgb)
        if thisStopTrial != None:
            for paramName in thisStopTrial.keys():
                exec(paramName + '= thisStopTrial.' + paramName)
        
        #------Prepare to start Routine "newStopStim"-------
        t = 0
        newStopStimClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        #***************************
        
        StopTrials.addData("StartTrialTimeStamp", core.getTime())
        
        currentStopTrial = stopTrialList.pop(0)
        currentGoStim = currentStopTrial['fileName']
        currentStopOrGo = currentStopTrial['stopOrGo']
        currentStimType = currentStopTrial['condition']
        currentStopStimValue = currentStopTrial['reward']
        
        #Separate SSD tracking algorithms for left and right responses
        if currentStopOrGo == 'stop':
            stopSignal.setVolume(.2)
            if xPosGoStim == -200:
                SSD = deepcopy(SSDLeft)
            else:
                SSD = deepcopy(SSDRight)
        elif currentStopOrGo == 'go':
            SSD = -1
            stopSignal.setVolume(0)
        
        StopTrials.addData("beginningSSD", SSD)
        StopTrials.addData("trialType", currentStopOrGo)
        StopTrials.addData("goStim", currentGoStim)
        StopTrials.addData("stimType", currentStimType)
        StopTrials.addData("stopStimValue", currentStopStimValue)
        SSDInput = SSD + .5
        
        #***************************
        # keep track of which components have finished
        newStopStimComponents = []
        for thisComponent in newStopStimComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "newStopStim"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = newStopStimClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in newStopStimComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "newStopStim"-------
        for thisComponent in newStopStimComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # the Routine "newStopStim" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        #------Prepare to start Routine "StopTrial"-------
        t = 0
        StopTrialClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        goStim.setPos([xPosGoStim, yPosGoStim])
        goStim.setImage(currentGoStim)
        goResp = event.BuilderKeyResponse()  # create an object of type KeyResponse
        goResp.status = NOT_STARTED
        # keep track of which components have finished
        StopTrialComponents = []
        StopTrialComponents.append(stopSignal)
        StopTrialComponents.append(fixStop)
        StopTrialComponents.append(goStim)
        StopTrialComponents.append(goResp)
        for thisComponent in StopTrialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "StopTrial"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = StopTrialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # start/stop stopSignal
            if t >= SSDInput and stopSignal.status == NOT_STARTED:
                # keep track of start time/frame for later
                stopSignal.tStart = t  # underestimates by a little under one frame
                stopSignal.frameNStart = frameN  # exact frame index
                stopSignal.play()  # start the sound (it finishes automatically)
            if stopSignal.status == STARTED and t >= (SSDInput + (.2-win.monitorFramePeriod*0.75)): #most of one frame period left
                stopSignal.stop()  # stop the sound (if longer than duration)
            
            # *fixStop* updates
            if t >= 0.0 and fixStop.status == NOT_STARTED:
                # keep track of start time/frame for later
                fixStop.tStart = t  # underestimates by a little under one frame
                fixStop.frameNStart = frameN  # exact frame index
                fixStop.setAutoDraw(True)
            if fixStop.status == STARTED and t >= (0.0 + (1.5-win.monitorFramePeriod*0.75)): #most of one frame period left
                fixStop.setAutoDraw(False)
            
            # *goStim* updates
            if t >= .5 and goStim.status == NOT_STARTED:
                # keep track of start time/frame for later
                goStim.tStart = t  # underestimates by a little under one frame
                goStim.frameNStart = frameN  # exact frame index
                goStim.setAutoDraw(True)
            if goStim.status == STARTED and t >= (.5 + (1.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                goStim.setAutoDraw(False)
            
            # *goResp* updates
            if t >= .5 and goResp.status == NOT_STARTED:
                # keep track of start time/frame for later
                goResp.tStart = t  # underestimates by a little under one frame
                goResp.frameNStart = frameN  # exact frame index
                goResp.status = STARTED
                # keyboard checking is just starting
                goResp.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if goResp.status == STARTED and t >= (.5 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
                goResp.status = STOPPED
            if goResp.status == STARTED:
                theseKeys = event.getKeys(keyList=['z', 'm'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if goResp.keys == []:  # then this was the first keypress
                        goResp.keys = theseKeys[0]  # just the first key pressed
                        goResp.rt = goResp.clock.getTime()
                        # was this 'correct'?
                        if (goResp.keys == str(corrGoResp)) or (goResp.keys == corrGoResp):
                            goResp.corr = 1
                        else:
                            goResp.corr = 0
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in StopTrialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "StopTrial"-------
        for thisComponent in StopTrialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        stopSignal.stop() #ensure sound has stopped at end of routine
        # check responses
        if goResp.keys in ['', [], None]:  # No response was made
           goResp.keys=None
           # was no response the correct answer?!
           if str(corrGoResp).lower() == 'none': goResp.corr = 1  # correct non-response
           else: goResp.corr = 0  # failed to respond (incorrectly)
        # store data for StopTrials (TrialHandler)
        StopTrials.addData('goResp.keys',goResp.keys)
        StopTrials.addData('goResp.corr', goResp.corr)
        if goResp.keys != None:  # we had a response
            StopTrials.addData('goResp.rt', goResp.rt)
        # the Routine "StopTrial" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        #------Prepare to start Routine "blankStop"-------
        t = 0
        blankStopClock.reset()  # clock 
        frameN = -1
        routineTimer.add(1.500000)
        # update component parameters for each repeat
        key_resp_9 = event.BuilderKeyResponse()  # create an object of type KeyResponse
        key_resp_9.status = NOT_STARTED
        # keep track of which components have finished
        blankStopComponents = []
        blankStopComponents.append(text_4)
        blankStopComponents.append(key_resp_9)
        for thisComponent in blankStopComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "blankStop"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = blankStopClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text_4* updates
            if t >= 0.0 and text_4.status == NOT_STARTED:
                # keep track of start time/frame for later
                text_4.tStart = t  # underestimates by a little under one frame
                text_4.frameNStart = frameN  # exact frame index
                text_4.setAutoDraw(True)
            if text_4.status == STARTED and t >= (0.0 + (1.5-win.monitorFramePeriod*0.75)): #most of one frame period left
                text_4.setAutoDraw(False)
            
            # *key_resp_9* updates
            if t >= 0.0 and key_resp_9.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_9.tStart = t  # underestimates by a little under one frame
                key_resp_9.frameNStart = frameN  # exact frame index
                key_resp_9.status = STARTED
                # keyboard checking is just starting
                key_resp_9.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if key_resp_9.status == STARTED and t >= (0.0 + (1.5-win.monitorFramePeriod*0.75)): #most of one frame period left
                key_resp_9.status = STOPPED
            if key_resp_9.status == STARTED:
                theseKeys = event.getKeys(keyList=['z', 'm'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if key_resp_9.keys == []:  # then this was the first keypress
                        key_resp_9.keys = theseKeys[0]  # just the first key pressed
                        key_resp_9.rt = key_resp_9.clock.getTime()
                        # was this 'correct'?
                        if (key_resp_9.keys == str(corrGoResp)) or (key_resp_9.keys == corrGoResp):
                            key_resp_9.corr = 1
                        else:
                            key_resp_9.corr = 0
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in blankStopComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "blankStop"-------
        for thisComponent in blankStopComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_9.keys in ['', [], None]:  # No response was made
           key_resp_9.keys=None
           # was no response the correct answer?!
           if str(corrGoResp).lower() == 'none': key_resp_9.corr = 1  # correct non-response
           else: key_resp_9.corr = 0  # failed to respond (incorrectly)
        # store data for StopTrials (TrialHandler)
        StopTrials.addData('key_resp_9.keys',key_resp_9.keys)
        StopTrials.addData('key_resp_9.corr', key_resp_9.corr)
        if key_resp_9.keys != None:  # we had a response
            StopTrials.addData('key_resp_9.rt', key_resp_9.rt)
        
        #------Prepare to start Routine "SSDChange"-------
        t = 0
        SSDChangeClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        #***************************
        
        #Adjusting SSD within a range of 0-750ms
        if currentStopTrial['stopOrGo'] == 'stop':
            if goResp.keys is None:
                if SSD <= .75:
                    if xPosGoStim == -200:
                        SSDLeft = deepcopy(SSDLeft)  + .05
                        SSD = SSDLeft
                    if xPosGoStim == 200:
                        SSDRight = deepcopy(SSDRight) + .05
                        SSD = SSDRight
            else:
                if SSD > .001:
                    if xPosGoStim == -200:
                        SSDLeft = deepcopy(SSDLeft) - .05
                        SSD = SSDLeft
                    if xPosGoStim == 200:
                        SSDRight = deepcopy(SSDRight) - .05
                        SSD = SSDRight
        
        if currentStopTrial['stopOrGo'] == 'go':
            goTrialCount = goTrialCount + 1
        
        if goResp.corr and currentStopTrial['stopOrGo'] == 'go':
            goCumRT = goCumRT + goResp.rt
            goRTCount = goRTCount + 1
        
        if currentStopTrial['stopOrGo'] == 'stop':
            stopTrialCount = stopTrialCount + 1
        
        if currentStopTrial['stopOrGo'] == 'stop' and goResp.keys is None and key_resp_9.keys is None:
            stopSuccessCount = stopSuccessCount + 1
        
        if currentStopTrial['stopOrGo'] == 'go':
            if goResp.keys is None:
                omissionCount = omissionCount + 1
            elif goResp.corr == 0:
                commissionCount = commissionCount + 1
        
        StopTrials.addData("fixStopOnset", fixStop.tStart)
        StopTrials.addData("goStimOnset", goStim.tStart)
        if SSD  != -1:
            StopTrials.addData("stopSignalOnset", stopSignal.tStart)
        
        #***************************
        # keep track of which components have finished
        SSDChangeComponents = []
        for thisComponent in SSDChangeComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "SSDChange"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = SSDChangeClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in SSDChangeComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "SSDChange"-------
        for thisComponent in SSDChangeComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        #***************************
        
        StopTrials.addData("EndingSSD", SSD)
        StopTrials.addData("EndTrialTimeStamp", core.getTime())
        
        #***************************
        # the Routine "SSDChange" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 18 repeats of 'StopTrials'
    
    # get names of stimulus parameters
    if StopTrials.trialList in ([], [None], None):  params = []
    else:  params = StopTrials.trialList[0].keys()
    # save data for this loop
    StopTrials.saveAsExcel(filename + '.xlsx', sheetName='StopTrials',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    
    #------Prepare to start Routine "endOfStopBlockFeedback"-------
    t = 0
    endOfStopBlockFeedbackClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    #***************************
    
    if goRTCount > 0:
        goRTFeedback = goCumRT/goRTCount
        goRTFeedback = round(goRTFeedback, 2)
    else:
        goRTFeedback = 'Null'
    
    if goTrialCount > 0:
        commissionRate = (commissionCount/goTrialCount)*100
        commissionRate = round(commissionRate, 2)
        omissionRate = (omissionCount/goTrialCount)*100
        omissionRate = round(omissionRate, 2)
    else: 
        commissionRate = 'Null'
        omissionRate = 'Null'
    
    if stopTrialCount > 0: 
        probabilityOfStop = stopSuccessCount/stopTrialCount
        probabilityOfStop = round(probabilityOfStop, 2)
    else:
        probabilityOfStop = 'Null'
    
    SSDFeedback = (SSDLeft+SSDRight)/2
    SSDFeedback = round(SSDFeedback, 2)
    
    stopMessage = " RT = " + str(goRTFeedback) + "\n Omission % = " + str(omissionRate) + "\n Commission % = " + str(commissionRate) + "\n\n\n\n " + str(probabilityOfStop) + "\n " + str(SSDFeedback) + "\n\n (Press the 9 key to continue)"
    
    #***************************
    text_5.setText(stopMessage)
    key_resp_3 = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_resp_3.status = NOT_STARTED
    # keep track of which components have finished
    endOfStopBlockFeedbackComponents = []
    endOfStopBlockFeedbackComponents.append(text_5)
    endOfStopBlockFeedbackComponents.append(key_resp_3)
    for thisComponent in endOfStopBlockFeedbackComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "endOfStopBlockFeedback"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = endOfStopBlockFeedbackClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *text_5* updates
        if t >= 0.0 and text_5.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_5.tStart = t  # underestimates by a little under one frame
            text_5.frameNStart = frameN  # exact frame index
            text_5.setAutoDraw(True)
        
        # *key_resp_3* updates
        if t >= 0.0 and key_resp_3.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_3.tStart = t  # underestimates by a little under one frame
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            key_resp_3.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if key_resp_3.status == STARTED:
            theseKeys = event.getKeys(keyList=['9'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_resp_3.keys = theseKeys[-1]  # just the last key pressed
                key_resp_3.rt = key_resp_3.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in endOfStopBlockFeedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "endOfStopBlockFeedback"-------
    for thisComponent in endOfStopBlockFeedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # check responses
    if key_resp_3.keys in ['', [], None]:  # No response was made
       key_resp_3.keys=None
    # store data for StopBlocks (TrialHandler)
    StopBlocks.addData('key_resp_3.keys',key_resp_3.keys)
    if key_resp_3.keys != None:  # we had a response
        StopBlocks.addData('key_resp_3.rt', key_resp_3.rt)
    # the Routine "endOfStopBlockFeedback" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 8 repeats of 'StopBlocks'


#------Prepare to start Routine "instrAuction"-------
t = 0
instrAuctionClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
key_resp_4 = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp_4.status = NOT_STARTED
# keep track of which components have finished
instrAuctionComponents = []
instrAuctionComponents.append(text_7)
instrAuctionComponents.append(key_resp_4)
for thisComponent in instrAuctionComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instrAuction"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instrAuctionClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_7* updates
    if t >= 0.0 and text_7.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_7.tStart = t  # underestimates by a little under one frame
        text_7.frameNStart = frameN  # exact frame index
        text_7.setAutoDraw(True)
    
    # *key_resp_4* updates
    if t >= 0.0 and key_resp_4.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_4.tStart = t  # underestimates by a little under one frame
        key_resp_4.frameNStart = frameN  # exact frame index
        key_resp_4.status = STARTED
        # keyboard checking is just starting
        key_resp_4.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if key_resp_4.status == STARTED:
        theseKeys = event.getKeys(keyList=['9'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_4.keys = theseKeys[-1]  # just the last key pressed
            key_resp_4.rt = key_resp_4.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrAuctionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "instrAuction"-------
for thisComponent in instrAuctionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_4.keys in ['', [], None]:  # No response was made
   key_resp_4.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('key_resp_4.keys',key_resp_4.keys)
if key_resp_4.keys != None:  # we had a response
    thisExp.addData('key_resp_4.rt', key_resp_4.rt)
thisExp.nextEntry()
# the Routine "instrAuction" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
auctionBlocks = data.TrialHandler(nReps=4, method='random', 
    extraInfo=expInfo, originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
    trialList=[None],
    seed=None, name='auctionBlocks')
thisExp.addLoop(auctionBlocks)  # add the loop to the experiment
thisAuctionBlock = auctionBlocks.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisAuctionBlock.rgb)
if thisAuctionBlock != None:
    for paramName in thisAuctionBlock.keys():
        exec(paramName + '= thisAuctionBlock.' + paramName)

for thisAuctionBlock in auctionBlocks:
    currentLoop = auctionBlocks
    # abbreviate parameter names if possible (e.g. rgb = thisAuctionBlock.rgb)
    if thisAuctionBlock != None:
        for paramName in thisAuctionBlock.keys():
            exec(paramName + '= thisAuctionBlock.' + paramName)
    
    # set up handler to look after randomisation of conditions etc
    auctionTrials = data.TrialHandler(nReps=20, method='sequential', 
        extraInfo=expInfo, originPath='/Users/poldracklab/Documents/Bissett/trainedInhibition/LearningStopAuction.psyexp',
        trialList=[None],
        seed=None, name='auctionTrials')
    thisExp.addLoop(auctionTrials)  # add the loop to the experiment
    thisAuctionTrial = auctionTrials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisAuctionTrial.rgb)
    if thisAuctionTrial != None:
        for paramName in thisAuctionTrial.keys():
            exec(paramName + '= thisAuctionTrial.' + paramName)
    
    for thisAuctionTrial in auctionTrials:
        currentLoop = auctionTrials
        # abbreviate parameter names if possible (e.g. rgb = thisAuctionTrial.rgb)
        if thisAuctionTrial != None:
            for paramName in thisAuctionTrial.keys():
                exec(paramName + '= thisAuctionTrial.' + paramName)
        
        #------Prepare to start Routine "newAuctionStim"-------
        t = 0
        newAuctionStimClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        #***************************
        
        auctionTrials.addData("StartTrialTimeStamp", core.getTime())
        
        currentAuctionTrial = auctionTrialList.pop(0)
        currentAuctionStim = currentAuctionTrial['fileName']
        currentAuctionAmount = currentAuctionTrial['auctionAmount']
        currentAuctionStimValue = currentAuctionTrial['reward']
        currentAuctionCondition = currentAuctionTrial['condition']
        
        #***************************
        # keep track of which components have finished
        newAuctionStimComponents = []
        for thisComponent in newAuctionStimComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "newAuctionStim"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = newAuctionStimClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in newAuctionStimComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "newAuctionStim"-------
        for thisComponent in newAuctionStimComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        
        # the Routine "newAuctionStim" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        #------Prepare to start Routine "auctionTrial"-------
        t = 0
        auctionTrialClock.reset()  # clock 
        frameN = -1
        routineTimer.add(6.000000)
        # update component parameters for each repeat
        auctionStim.setImage(currentAuctionStim)
        RAmount.setText(currentAuctionAmount[0])
        TAmount.setText(currentAuctionAmount[1])
        YAmount.setText(currentAuctionAmount[2])
        UAmount.setText(currentAuctionAmount[3])
        IAmount.setText(currentAuctionAmount[4])
        OAmount.setText(currentAuctionAmount[5])
        auctionResponse = event.BuilderKeyResponse()  # create an object of type KeyResponse
        auctionResponse.status = NOT_STARTED
        startTime = trialClock.getTime()
        
        
        # keep track of which components have finished
        auctionTrialComponents = []
        auctionTrialComponents.append(Fix)
        auctionTrialComponents.append(R)
        auctionTrialComponents.append(auctionStim)
        auctionTrialComponents.append(T)
        auctionTrialComponents.append(Y)
        auctionTrialComponents.append(U)
        auctionTrialComponents.append(I)
        auctionTrialComponents.append(O)
        auctionTrialComponents.append(RAmount)
        auctionTrialComponents.append(TAmount)
        auctionTrialComponents.append(YAmount)
        auctionTrialComponents.append(UAmount)
        auctionTrialComponents.append(IAmount)
        auctionTrialComponents.append(OAmount)
        auctionTrialComponents.append(auctionResponse)
        for thisComponent in auctionTrialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "auctionTrial"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = auctionTrialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fix* updates
            if t >= 0.0 and Fix.status == NOT_STARTED:
                # keep track of start time/frame for later
                Fix.tStart = t  # underestimates by a little under one frame
                Fix.frameNStart = frameN  # exact frame index
                Fix.setAutoDraw(True)
            if Fix.status == STARTED and t >= (0.0 + (.5-win.monitorFramePeriod*0.75)): #most of one frame period left
                Fix.setAutoDraw(False)
            
            # *R* updates
            if t >= 1.0 and R.status == NOT_STARTED:
                # keep track of start time/frame for later
                R.tStart = t  # underestimates by a little under one frame
                R.frameNStart = frameN  # exact frame index
                R.setAutoDraw(True)
            if R.status == STARTED and t >= (1.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
                R.setAutoDraw(False)
            
            # *auctionStim* updates
            if t >= .5 and auctionStim.status == NOT_STARTED:
                # keep track of start time/frame for later
                auctionStim.tStart = t  # underestimates by a little under one frame
                auctionStim.frameNStart = frameN  # exact frame index
                auctionStim.setAutoDraw(True)
            if auctionStim.status == STARTED and t >= (.5 + (5.5-win.monitorFramePeriod*0.75)): #most of one frame period left
                auctionStim.setAutoDraw(False)
            
            # *T* updates
            if t >= 1.0 and T.status == NOT_STARTED:
                # keep track of start time/frame for later
                T.tStart = t  # underestimates by a little under one frame
                T.frameNStart = frameN  # exact frame index
                T.setAutoDraw(True)
            if T.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                T.setAutoDraw(False)
            
            # *Y* updates
            if t >= 1.0 and Y.status == NOT_STARTED:
                # keep track of start time/frame for later
                Y.tStart = t  # underestimates by a little under one frame
                Y.frameNStart = frameN  # exact frame index
                Y.setAutoDraw(True)
            if Y.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                Y.setAutoDraw(False)
            
            # *U* updates
            if t >= 1.0 and U.status == NOT_STARTED:
                # keep track of start time/frame for later
                U.tStart = t  # underestimates by a little under one frame
                U.frameNStart = frameN  # exact frame index
                U.setAutoDraw(True)
            if U.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                U.setAutoDraw(False)
            
            # *I* updates
            if t >= 1.0 and I.status == NOT_STARTED:
                # keep track of start time/frame for later
                I.tStart = t  # underestimates by a little under one frame
                I.frameNStart = frameN  # exact frame index
                I.setAutoDraw(True)
            if I.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                I.setAutoDraw(False)
            
            # *O* updates
            if t >= 1.0 and O.status == NOT_STARTED:
                # keep track of start time/frame for later
                O.tStart = t  # underestimates by a little under one frame
                O.frameNStart = frameN  # exact frame index
                O.setAutoDraw(True)
            if O.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                O.setAutoDraw(False)
            
            # *RAmount* updates
            if t >= 1.0 and RAmount.status == NOT_STARTED:
                # keep track of start time/frame for later
                RAmount.tStart = t  # underestimates by a little under one frame
                RAmount.frameNStart = frameN  # exact frame index
                RAmount.setAutoDraw(True)
            if RAmount.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                RAmount.setAutoDraw(False)
            
            # *TAmount* updates
            if t >= 1.0 and TAmount.status == NOT_STARTED:
                # keep track of start time/frame for later
                TAmount.tStart = t  # underestimates by a little under one frame
                TAmount.frameNStart = frameN  # exact frame index
                TAmount.setAutoDraw(True)
            if TAmount.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                TAmount.setAutoDraw(False)
            
            # *YAmount* updates
            if t >= 1.0 and YAmount.status == NOT_STARTED:
                # keep track of start time/frame for later
                YAmount.tStart = t  # underestimates by a little under one frame
                YAmount.frameNStart = frameN  # exact frame index
                YAmount.setAutoDraw(True)
            if YAmount.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                YAmount.setAutoDraw(False)
            
            # *UAmount* updates
            if t >= 1.0 and UAmount.status == NOT_STARTED:
                # keep track of start time/frame for later
                UAmount.tStart = t  # underestimates by a little under one frame
                UAmount.frameNStart = frameN  # exact frame index
                UAmount.setAutoDraw(True)
            if UAmount.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                UAmount.setAutoDraw(False)
            
            # *IAmount* updates
            if t >= 1.0 and IAmount.status == NOT_STARTED:
                # keep track of start time/frame for later
                IAmount.tStart = t  # underestimates by a little under one frame
                IAmount.frameNStart = frameN  # exact frame index
                IAmount.setAutoDraw(True)
            if IAmount.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                IAmount.setAutoDraw(False)
            
            # *OAmount* updates
            if t >= 1.0 and OAmount.status == NOT_STARTED:
                # keep track of start time/frame for later
                OAmount.tStart = t  # underestimates by a little under one frame
                OAmount.frameNStart = frameN  # exact frame index
                OAmount.setAutoDraw(True)
            if OAmount.status == STARTED and t >= (1.0 + (5.0-win.monitorFramePeriod*0.75)): #most of one frame period left
                OAmount.setAutoDraw(False)
            
            # *auctionResponse* updates
            if t >= 1.0 and auctionResponse.status == NOT_STARTED:
                # keep track of start time/frame for later
                auctionResponse.tStart = t  # underestimates by a little under one frame
                auctionResponse.frameNStart = frameN  # exact frame index
                auctionResponse.status = STARTED
                # keyboard checking is just starting
                auctionResponse.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if auctionResponse.status == STARTED and t >= (1.0 + (5-win.monitorFramePeriod*0.75)): #most of one frame period left
                auctionResponse.status = STOPPED
            if auctionResponse.status == STARTED:
                theseKeys = event.getKeys(keyList=['r', 't', 'y', 'u', 'i', 'o'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    if auctionResponse.keys == []:  # then this was the first keypress
                        auctionResponse.keys = theseKeys[0]  # just the first key pressed
                        auctionResponse.rt = auctionResponse.clock.getTime()
                        # a response ends the routine
                        continueRoutine = False
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in auctionTrialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "auctionTrial"-------
        for thisComponent in auctionTrialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if auctionResponse.keys in ['', [], None]:  # No response was made
           auctionResponse.keys=None
        # store data for auctionTrials (TrialHandler)
        auctionTrials.addData('auctionResponse.keys',auctionResponse.keys)
        if auctionResponse.keys != None:  # we had a response
            auctionTrials.addData('auctionResponse.rt', auctionResponse.rt)
        endTime = trialClock.getTime()
        auctionStimDuration = endTime - startTime
        ITIDur = 6 - auctionStimDuration
        
        auctionTrials.addData("auctionStimDuration", auctionStimDuration)
        
        
        
        #------Prepare to start Routine "auctionITI"-------
        t = 0
        auctionITIClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        if auctionResponse.keys == 'r':
            chosenAuctionAmount = currentAuctionAmount[0]
        elif auctionResponse.keys == 't':
            chosenAuctionAmount = currentAuctionAmount[1]
        elif auctionResponse.keys == 'y':
            chosenAuctionAmount = currentAuctionAmount[2]
        elif auctionResponse.keys == 'u':
            chosenAuctionAmount = currentAuctionAmount[3]
        elif auctionResponse.keys == 'i':
            chosenAuctionAmount = currentAuctionAmount[4]
        elif auctionResponse.keys == 'o':
            chosenAuctionAmount = currentAuctionAmount[5]
        else: 
            chosenAuctionAmount = 0
        # keep track of which components have finished
        auctionITIComponents = []
        auctionITIComponents.append(text_3)
        for thisComponent in auctionITIComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "auctionITI"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = auctionITIClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text_3* updates
            if t >= 0.0 and text_3.status == NOT_STARTED:
                # keep track of start time/frame for later
                text_3.tStart = t  # underestimates by a little under one frame
                text_3.frameNStart = frameN  # exact frame index
                text_3.setAutoDraw(True)
            if text_3.status == STARTED and t >= (0.0 + (ITIDur-win.monitorFramePeriod*0.75)): #most of one frame period left
                text_3.setAutoDraw(False)
            
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in auctionITIComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "auctionITI"-------
        for thisComponent in auctionITIComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        auctionTrials.addData("EndTrialTimeStamp", core.getTime())
        auctionTrials.addData("auctionStim", currentAuctionStim)
        auctionTrials.addData("auctionAmounts", currentAuctionAmount)
        auctionTrials.addData("auctionStimValue", currentAuctionStimValue)
        auctionTrials.addData("auctionCondition", currentAuctionCondition)
        auctionTrials.addData("chosenAuctionAmount", chosenAuctionAmount)
        # the Routine "auctionITI" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 20 repeats of 'auctionTrials'
    
    # get names of stimulus parameters
    if auctionTrials.trialList in ([], [None], None):  params = []
    else:  params = auctionTrials.trialList[0].keys()
    # save data for this loop
    auctionTrials.saveAsExcel(filename + '.xlsx', sheetName='auctionTrials',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    
    #------Prepare to start Routine "auctionBreak"-------
    t = 0
    auctionBreakClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    key_resp_5 = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_resp_5.status = NOT_STARTED
    # keep track of which components have finished
    auctionBreakComponents = []
    auctionBreakComponents.append(text_9)
    auctionBreakComponents.append(key_resp_5)
    for thisComponent in auctionBreakComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "auctionBreak"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = auctionBreakClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_9* updates
        if t >= 0.0 and text_9.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_9.tStart = t  # underestimates by a little under one frame
            text_9.frameNStart = frameN  # exact frame index
            text_9.setAutoDraw(True)
        
        # *key_resp_5* updates
        if t >= 0.0 and key_resp_5.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_5.tStart = t  # underestimates by a little under one frame
            key_resp_5.frameNStart = frameN  # exact frame index
            key_resp_5.status = STARTED
            # keyboard checking is just starting
            key_resp_5.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if key_resp_5.status == STARTED:
            theseKeys = event.getKeys(keyList=['9'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                if key_resp_5.keys == []:  # then this was the first keypress
                    key_resp_5.keys = theseKeys[0]  # just the first key pressed
                    key_resp_5.rt = key_resp_5.clock.getTime()
                    # a response ends the routine
                    continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in auctionBreakComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "auctionBreak"-------
    for thisComponent in auctionBreakComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # check responses
    if key_resp_5.keys in ['', [], None]:  # No response was made
       key_resp_5.keys=None
    # store data for auctionBlocks (TrialHandler)
    auctionBlocks.addData('key_resp_5.keys',key_resp_5.keys)
    if key_resp_5.keys != None:  # we had a response
        auctionBlocks.addData('key_resp_5.rt', key_resp_5.rt)
    # the Routine "auctionBreak" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
# completed 4 repeats of 'auctionBlocks'


#------Prepare to start Routine "rewardCalc"-------
t = 0
rewardCalcClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
#***************************

shuffle(rewardList)

thisExp.addData("shuffledRewardList", rewardList)

chosenReward1 = rewardList.pop(0)
chosenReward2 = rewardList.pop(1)
chosenReward3 = rewardList.pop(2)
chosenReward4 = rewardList.pop(3)
chosenReward5 = rewardList.pop(4)

totalReward = 12 + chosenReward1 + chosenReward2 + chosenReward3 + chosenReward4 + chosenReward5

displayedReward = "In total, you earned $ %.2f" %totalReward

thisExp.addData("chosenReward1", chosenReward1)
thisExp.addData("chosenReward2", chosenReward2)
thisExp.addData("chosenReward3", chosenReward3)
thisExp.addData("chosenReward4", chosenReward4)
thisExp.addData("chosenReward5", chosenReward5)

#***************************


text_11.setText(displayedReward)
key_resp_6 = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp_6.status = NOT_STARTED
# keep track of which components have finished
rewardCalcComponents = []
rewardCalcComponents.append(text_11)
rewardCalcComponents.append(key_resp_6)
for thisComponent in rewardCalcComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "rewardCalc"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = rewardCalcClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # *text_11* updates
    if t >= 0.0 and text_11.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_11.tStart = t  # underestimates by a little under one frame
        text_11.frameNStart = frameN  # exact frame index
        text_11.setAutoDraw(True)
    
    # *key_resp_6* updates
    if t >= 0.0 and key_resp_6.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_6.tStart = t  # underestimates by a little under one frame
        key_resp_6.frameNStart = frameN  # exact frame index
        key_resp_6.status = STARTED
        # keyboard checking is just starting
        key_resp_6.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if key_resp_6.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_6.keys = theseKeys[-1]  # just the last key pressed
            key_resp_6.rt = key_resp_6.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in rewardCalcComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "rewardCalc"-------
for thisComponent in rewardCalcComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if key_resp_6.keys in ['', [], None]:  # No response was made
   key_resp_6.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('key_resp_6.keys',key_resp_6.keys)
if key_resp_6.keys != None:  # we had a response
    thisExp.addData('key_resp_6.rt', key_resp_6.rt)
thisExp.nextEntry()
# the Routine "rewardCalc" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()






















win.close()
core.quit()
