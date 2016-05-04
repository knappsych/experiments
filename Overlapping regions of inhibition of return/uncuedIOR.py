from psychopy import visual, event, core, sound, data, gui
from numpy import *
import random
import os  # handy system and path functions
import sys # to get file system encoding

#This experiment was designed to detect overlapping regions of inhibition
#Two out of five locations are cued with a gap between them
#Should regions of inhibition overlap we should find slower RTs at locations
#between the two cued locations than at the other two uncued locations.
#We should also observer slower response times at the cued locations compared to
#the uncued locations.

# Ensure that relative paths start from the same directory as this script
thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(thisDir)

# Store info about the experiment session
expName = 'IOR_Uncued' 
expInfo = {'participant':''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name = absolute path + name + .csv
filename = thisDir + os.sep + 'data' + os.sep + '%s_%s.csv' %(expName, expInfo['participant'])


#Need to define the window
win = visual.Window(
	fullscr=True, #Make this full screen
	monitor="HomeDellS2470L", #set to the monitor for the experiment
		#Perhaps the above would be good to use with the GUI if we
		#have several monitors used for a single experiment.
	allowGUI=False, #to hide the mouse.
	rgb=[-1,-1,-1], #black background
	units="deg" #Use degrees of visual angle
)

#Find the locations
#How many locations will we have.
nlocs = 5

#First initialize an empty list
locations = [0]*nlocs

#The radius of the bounding circle
radius=5

#The first location in terms of degrees
ldeg=90

#The increment in degrees
deginc=360/nlocs

#Find the x and y coordinates for each of the stimuli
for i in range(0,nlocs):
	rads = deg2rad(ldeg)
	x=cos(rads)*radius
	y=sin(rads)*radius
	locations[i]=(x,y)
	ldeg += deginc

#Create the stimuli
#The fixation cross
fixation = visual.TextStim(
	win,
	text="+",
	pos=(0,0),
	color=[0,0,0],
	height=3
)

#The fixation cue
fixcue = visual.TextStim(
	win,
	text="+",
	pos=(0,0),
	color=[1,1,1],
	height=3
)

#The location placeholders
placeholder = visual.Polygon(
	win,
	edges=4,
	radius=sqrt(2),
	lineColor=[0,0,0],
	lineWidth=4,
	ori=45
)

#The cue
cue = visual.Polygon(
	win,
	edges=4,
	radius=sqrt(2),
	lineColor=[1,1,1],
	lineWidth=4,
	ori=45
)

#The target
target = visual.Polygon(
	win,
	edges=4,
	radius=sqrt(2*pow(.5,2)),
	lineColor=[1,1,1],
	fillColor=[1,1,1],
	ori=45
)

#Feedback
feedback = visual.TextStim(
	win,
	text="default",
	pos=(0,0),
	color=[1,1,1],
	height=1.5
)

#break
breakmsg = visual.TextStim(
	win,
	text="Take a break if you need one.",
	pos=(0,0),
	color=[1,1,1],
	height=1
)

#Continue
continuemsg = visual.TextStim(
	win,
	text="Press any key to continue.",
	pos=(0,-6),
	color=[1,1,1],
	height=1
)

#initialize the sound for errors
sound.init(48000,buffer=128)
buzz = sound.Sound(165,secs=1,sampleRate=44100, bits=8)

for i in range(0,nlocs):
	placeholder.pos = locations[i]
	placeholder.draw()
fixation.draw()

basicDisplay = visual.BufferImageStim(
	win,
	autoLog=False
)

#Clear the buffer
win.clearBuffer()



#Set up the experimental parameters
#two target present for each target absent
targ_pres=["present","present","absent"]
#5 trial types
trial_type=["cue1","cue2","near1","near2","between"]
#3 reps of the trials per block (45 trials per block)
reps_per_block=3
#number of blocks
nblocks=10

#calculating trials per block
trials_per_block=len(targ_pres)*len(trial_type)*reps_per_block;

#calculating trials per experiment
trials_per_exp = trials_per_block*nblocks

#create empty lists to hold the values once we loop through them
tpres=[0]*trials_per_block
ttype=[0]*trials_per_block
idx=[0]*trials_per_block

#create the variables we'll use to save the experimental information
tPres=[0]*trials_per_exp
tType=[0]*trials_per_exp
c1Loc=[0]*trials_per_exp
c2Loc=[0]*trials_per_exp
tLoc=[0]*trials_per_exp
key=[0]*trials_per_exp
RT=[0]*trials_per_exp
error=[0]*trials_per_exp
tNum=[0]*trials_per_exp
block=[0]*trials_per_exp

#set a counter we'll use to fill the lists
i=0

#loop through the trial types to create all the trials types within a block
for rep in range(reps_per_block):
	for pres in range(len(targ_pres)):
		for type in range(len(trial_type)):
			tpres[i]=targ_pres[pres]
			ttype[i]=trial_type[type]
			idx[i]=i
			i += 1

#initialize our RT clock
RTClock = core.Clock()
			
#define the present trial function
def presentTrial(pres,type,tnum):
	tPres[tnum]=pres
	tType[tnum]=type
	tNum[tnum]=tnum+1
	direction=random.choice([-1,1])
	c1Loc[tnum]=random.choice(range(5))
	c2Loc[tnum]=(c1Loc[tnum]+5+direction*2)%5
	if(type=="cue1"):
		tLoc[tnum]=c1Loc[tnum]
	elif(type=="cue2"):
		tLoc[tnum]=c2Loc[tnum]
	elif(type=="near1"):
		tLoc[tnum]=(c1Loc[tnum]+5+direction*4)%5
	elif(type=="near2"):
		tLoc[tnum]=(c1Loc[tnum]+5+direction*3)%5
	else:
		tLoc[tnum]=(c1Loc[tnum]+5+direction)%5
	
	cue.pos=locations[c1Loc[tnum]]
	target.pos=locations[tLoc[tnum]]
	
	#The following is for debugging purposes only
	#The fixation cross
	#debug = visual.TextStim(
	#	win,
	#	text="type = %s, pres = %s" % (type, pres),
	#	pos=(0,1),
	#	color=[0,0,0]
	#)
	
	#The initial display
	for frameN in range(31): #.5 sec
		basicDisplay.draw()
		#debug.draw()
		win.flip()
	
	#The first cue
	for frameN in range(10): #150 ms
		basicDisplay.draw()
		#debug.draw()
		cue.draw()
		win.flip()
	
	#The display again
	for frameN in range(16): #250 ms
		basicDisplay.draw()
		#debug.draw()
		win.flip()
	
	#Get the second cue position
	cue.pos=locations[c2Loc[tnum]]
	
	#The second cue
	for frameN in range(10): #150 ms
		basicDisplay.draw()
		#debug.draw()
		cue.draw()
		win.flip()
		
	#The display again
	for frameN in range(16): #250 ms
		basicDisplay.draw()
		#debug.draw()
		win.flip()
	
	#Cue the fixation
	for frameN in range(10): #150 ms
		basicDisplay.draw()
		#debug.draw()
		fixcue.draw()
		win.flip()
	
	#The display again
	for frameN in range(16): #250 ms
		basicDisplay.draw()
		#debug.draw()
		win.flip()
	
	#The target
	basicDisplay.draw()
	if (pres=="present"):
		target.draw()
	win.flip()
	RTClock.reset()
	keyPress=event.waitKeys(maxWait=.6,timeStamped=RTClock)
	
	#Get the key and the response time if there was a key press.
	if(keyPress!=None):
		key[tnum]=keyPress[0][0]
		RT[tnum]=keyPress[0][1]*1000
		if (key[tnum]=="escape"):
			core.quit()
	
	#Set the feedback
	if((pres=="absent") & (key[tnum]!=0)):
		feedback.setText("There was no target!")
		error[tnum]="FA"
	elif((pres=="present") & (key[tnum]==0)):
		feedback.setText("You missed the target!")
		error[tnum]="Miss"
	elif((pres=="present") & (key[tnum]!="space")):
		feedback.setText("Wrong Key!")
		error[tnum]="WrongKey"
	else:
		feedback.setText("Nice Job!")
		error[tnum]="None"
	
	#Present feedback and error tone if an error was made
	feedback.draw()
	win.flip()
	if(error[tnum]!="None"):#Present error tone
		buzz.play()
	core.wait(1)
	win.flip()

def presentInstructions():
	instructions = visual.TextStim(win,
		text=("In this experiment you'll be asked to press the "
			  "spacebar as soon as you see a target box.\n\n"
			  "The target won't appear on every trial, so don't "
			  "press the spacebar unless you see the target"),
		pos=(0,0),
		color=[1,1,1],
		height=1
		)
	instructions.draw()
	continuemsg.draw()
	win.flip()
	event.waitKeys()
	
	text=("Every trial will begin with the following display. "
		  "Notice the fixation cross in the center of the "
		  "screen. Stay focused on the cross so you have "
		  "the best chance of seeing everything.")
	instructions.setText(text)
	instructions.setPos((0,10.5))
	basicDisplay.draw()
	instructions.draw()
	continuemsg.draw()
	win.flip()
	event.waitKeys()
	
	text=("Before the target appears two of the five locations will "
		  "briefly brighten. You should ignore this as it doesn't "
		  "predict where the target will appear.")
	instructions.setText(text)
	basicDisplay.draw()
	cue.setPos(locations[1])
	instructions.draw()
	cue.draw()
	text="Here's an example:"
	instructions.setText(text)
	instructions.setPos((-10.5,1.7))
	instructions.draw()
	continuemsg.draw()
	win.flip()
	event.waitKeys()
	
	text=("Here's an example of the target box. Press the "
		  "spacebar as soon as you see it.")
	instructions.setText(text)
	instructions.setPos((0,10.5))
	basicDisplay.draw()
	instructions.draw()
	target.setPos(locations[0])
	target.draw()
	continuemsg.draw()
	win.flip()
	event.waitKeys()
	
	text=("Remember, don't press the spacebar until you "
		  "see the target box.\n\nAlso, make sure to "
		  "stay focused on the fixation to have the best "
		  "chance of quickly detecting the target, "
		  "regardless of where it appears.\n\nPlease be "
		  "as quick and accurate as possible.")
	instructions.setText(text)
	instructions.setPos((0,2.5))
	instructions.draw()
	continuemsg.draw()
	win.flip()
	event.waitKeys()

presentInstructions()

#Loop through the trials
trialnum=0
for blockn in range(nblocks):
	random.shuffle(idx)
	breakmsg.setText("Take a break if you need one.\n\n You have %d blocks to go" %
		(nblocks-blockn))
	breakmsg.draw()
	continuemsg.draw()
	win.flip()
	event.waitKeys()
	
	for i in range(len(idx)):
		presentTrial(tpres[idx[i]],ttype[idx[i]],trialnum)
		block[trialnum]=blockn+1
		trialnum+=1

#Thank the participant for participating.
feedback.setText("Thank you for participating!")
feedback.draw()
win.flip()

f=False
#Write the data to our file
if(os.path.isfile(filename)):
	f = open(filename,'a')
else:
	f = open(filename,'w')
	#Write the headers first
	f.write("exp,sub,date,block,trial,tpres,ttype,c1loc,c2loc,tloc,key,rt,error\n")
		
#Loopthrough the trials
for i in range(trialnum):
	#f.write("%s,%d,%s,%d,%d,%s,%s,%d,%d,%d,%s,%d,%s\n" % 
	f.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % 
		(expName,
		expInfo['participant'],
		expInfo['date'],
		block[i],
		tNum[i],
		tPres[i],
		tType[i],
		c1Loc[i],
		c2Loc[i],
		tLoc[i],
		key[i],
		RT[i],
		error[i]
		)
	)
f.close()
	
feedback.draw()
continuemsg.draw()
win.flip()
event.waitKeys()
core.quit()

#presentTrial("present","cue1",0)
#presentTrial("present","cue2",1)
#presentTrial("present","near1",2)
#presentTrial("present","near2",3)
#presentTrial("present","between",4)
#presentTrial("absent","cue1",5)
