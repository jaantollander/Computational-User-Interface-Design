# =============================================================================
# 7 Consumed Endurance
# ---------------------
# adjust three sliders to control joint angles, get real-time limb modelling
# "anthropometrics table" button: show such a table from GitHub link
# "male/female" toggle: change associated anthropometrics based on gender
# graphical illustration in the left shows human upper limb,
# and counterpart in the right shows limb modelling for consumed endurance
# =============================================================================
import tkinter as tk
from tkinter import ttk
import math as ma
import webbrowser

# overall layout
root = tk.Tk()
root.title("Consumed Endurance GUI")
root.resizable(width=False, height=False)
visualizationUi = ttk.Labelframe(root,text="Visualization")
modellingUi = ttk.Labelframe(root,text="Modelling")
visualizationUi.grid(row=0,column=0,padx=10,pady=20)
modellingUi.grid(row=0,column=1,padx=10,pady=20)

# anthropometrics parameters for arm visualization
ratioAll = 0.0025 # scale of real human / scale in the code
ratioCoMUpperArm = 0.452
ratioCoMForearm = 0.424
ratioCoMHand = 0.397
lengthUpperArm = 132
lengthForearm = 108
lengthHand = 76
massUpperArm = 2.1
massForearm = 1.2
massHand = 0.4
massxg = (massUpperArm+massForearm+massHand)*10
maxTorque = 22.94
angleUpperArm = 0
angleForearm = 0
angleHand = 0
xShoulder = 30.0
yShoulder = 237.0
xElbow = xShoulder + lengthUpperArm*ma.cos(angleUpperArm*ma.pi/180)
yElbow = yShoulder - lengthUpperArm*ma.sin(angleUpperArm*ma.pi/180)
xWrist = xElbow + lengthForearm*ma.cos(angleForearm*ma.pi/180)
yWrist = yElbow - lengthForearm*ma.sin(angleForearm*ma.pi/180)
xFingerTip = xWrist + lengthHand*ma.cos(angleHand*ma.pi/180)
yFingerTip = yWrist - lengthHand*ma.sin(angleHand*ma.pi/180)
xAPoint = xShoulder*(1 - ratioCoMUpperArm) + xElbow*ratioCoMUpperArm
yAPoint = yShoulder*(1 - ratioCoMUpperArm) + yElbow*ratioCoMUpperArm
xBPoint = xElbow*(1 - ratioCoMForearm) + xWrist*ratioCoMForearm
yBPoint = yElbow*(1 - ratioCoMForearm) + yWrist*ratioCoMForearm
xCPoint = xWrist*(1 - ratioCoMHand) + xFingerTip*ratioCoMHand
yCPoint = yWrist*(1 - ratioCoMHand) + yFingerTip*ratioCoMHand
xDPoint = xBPoint*(1 - (massHand/(massForearm+massHand))) + xCPoint*(massHand/(massForearm+massHand))
yDPoint = yBPoint*(1 - (massHand/(massForearm+massHand))) + yCPoint*(massHand/(massForearm+massHand))
xCoMPoint = xAPoint*(1 - ((massForearm+massHand)/(massUpperArm+massForearm+massHand))) + xDPoint*((massForearm+massHand)/(massUpperArm+massForearm+massHand))
yCoMPoint = yAPoint*(1 - ((massForearm+massHand)/(massUpperArm+massForearm+massHand))) + yDPoint*((massForearm+massHand)/(massUpperArm+massForearm+massHand))
rLength = 0.0
T_shoulder = 0.0
strength = 0.0
endurance = 0.0

# consumed endurance modelling
def modelConsumedEndurance():
    def modelRLength():
        global rLength
        rLength = ma.sqrt(ma.pow((xCoMPoint-xShoulder),2) + ma.pow((yCoMPoint-yShoulder),2))
        rLength = rLength*ratioAll
    def modelTShoulder():
        global T_shoulder
        T_shoulder = rLength*massxg*((xCoMPoint-xShoulder)*ratioAll/rLength)
    def modelStrength():
        global strength
        strength = 100*T_shoulder/maxTorque
    def modelEndurance():
        global endurance
        endurance = 1236.5/(ma.pow(strength - 15, 0.618)) - 72.5
    modelRLength()
    modelTShoulder()
    modelStrength()
    modelEndurance()

# update limb drawing in both graphical illustrations
def updateLimb():
    global xAPoint
    xAPoint=xShoulder*(1-ratioCoMUpperArm)+xElbow*ratioCoMUpperArm
    global yAPoint
    yAPoint=yShoulder*(1-ratioCoMUpperArm)+yElbow*ratioCoMUpperArm
    global xBPoint
    xBPoint=xElbow*(1-ratioCoMForearm)+xWrist*ratioCoMForearm
    global yBPoint
    yBPoint=yElbow*(1-ratioCoMForearm)+yWrist*ratioCoMForearm
    global xCPoint
    xCPoint=xWrist*(1-ratioCoMHand)+xFingerTip*ratioCoMHand
    global yCPoint
    yCPoint=yWrist*(1-ratioCoMHand)+yFingerTip*ratioCoMHand
    global xDPoint
    xDPoint=xBPoint*(1-(massHand/(massForearm+massHand)))+xCPoint*(massHand/(massForearm+massHand))
    global yDPoint
    yDPoint=yBPoint*(1-(massHand/(massForearm+massHand)))+yCPoint*(massHand/(massForearm+massHand))
    global xCoMPoint
    xCoMPoint=xAPoint*(1-((massForearm+massHand)/(massUpperArm+massForearm+massHand)))+xDPoint*((massForearm+massHand)/(massUpperArm+massForearm+massHand))
    global yCoMPoint
    yCoMPoint=yAPoint*(1-((massForearm+massHand)/(massUpperArm+massForearm+massHand)))+yDPoint*((massForearm+massHand)/(massUpperArm+massForearm+massHand))
    canvasVis.coords(jointElbowVis,xElbow-20,yElbow+20,xElbow+20,yElbow-20)
    canvasVis.coords(jointWristVis,xWrist-8,yWrist+8,xWrist+8,yWrist-8)
    canvasVis.coords(jointFingerTipVis,xFingerTip-3,yFingerTip+3,xFingerTip+3,yFingerTip-3)
    canvasVis.coords(limbUpperArm,xShoulder+27*ma.sin(angleUpperArm),yShoulder+27*ma.cos(angleUpperArm),xElbow+20*ma.sin(angleUpperArm),yElbow+20*ma.cos(angleUpperArm),xElbow-20*ma.sin(angleUpperArm),yElbow-20*ma.cos(angleUpperArm),xShoulder-27*ma.sin(angleUpperArm),yShoulder-27*ma.cos(angleUpperArm))
    canvasVis.coords(limbForearm,xElbow+20*ma.sin(angleForearm),yElbow+20*ma.cos(angleForearm),xWrist+8*ma.sin(angleForearm),yWrist+8*ma.cos(angleForearm),xWrist-8*ma.sin(angleForearm),yWrist-8*ma.cos(angleForearm),xElbow-20*ma.sin(angleForearm),yElbow-20*ma.cos(angleForearm))
    canvasVis.coords(limbHand,xWrist-8*ma.sin(angleHand),yWrist-8*ma.cos(angleHand),xWrist+35*(ma.cos(angleHand))-15*ma.sin(angleHand),yWrist-35*ma.sin(angleHand)-15*ma.cos(angleHand),xFingerTip-3*ma.sin(angleHand),yFingerTip-3*ma.cos(angleHand),xFingerTip+3*ma.sin(angleHand),yFingerTip+3*ma.cos(angleHand),xFingerTip-35*ma.cos(angleHand)-3*ma.sin(angleHand),yFingerTip+35*ma.sin(angleHand)-3*ma.cos(angleHand),xWrist+20*ma.cos(angleHand)+8*ma.sin(angleHand),yWrist+8*ma.cos(angleHand)-20*ma.sin(angleHand),xWrist+8*ma.sin(angleHand),yWrist+8*ma.cos(angleHand))
    canvasMod.coords(armMod,xShoulder,yShoulder,xElbow,yElbow,xWrist,yWrist,xFingerTip,yFingerTip)
    canvasMod.coords(jointElbowMod,xElbow-5,yElbow+5,xElbow+5,yElbow-5)
    canvasMod.coords(jointWristMod,xWrist-5,yWrist+5,xWrist+5,yWrist-5)
    canvasMod.coords(jointFingerTipMod,xFingerTip-5,yFingerTip+5,xFingerTip+5,yFingerTip-5)
    canvasMod.coords(pointAMod,xAPoint-2,yAPoint+2,xAPoint+2,yAPoint-2)
    canvasMod.coords(pointBMod,xBPoint-2,yBPoint+2,xBPoint+2,yBPoint-2)
    canvasMod.coords(pointCMod,xCPoint-2,yCPoint+2,xCPoint+2,yCPoint-2)
    canvasMod.coords(pointDMod,xDPoint-2,yDPoint+2,xDPoint+2,yDPoint-2)
    canvasMod.coords(pointCoMMod,xCoMPoint-3,yCoMPoint+3,xCoMPoint+3,yCoMPoint-3)
    canvasMod.coords(labelElbowMod,xElbow,yElbow-10)
    canvasMod.coords(labelWristMod,xWrist,yWrist-10)
    canvasMod.coords(labelFingerTipMod,xFingerTip,yFingerTip-10)
    canvasMod.coords(labelAPoint,xAPoint,yAPoint+10)
    canvasMod.coords(labelBPoint,xBPoint,yBPoint+10)
    canvasMod.coords(labelCPoint,xCPoint,yCPoint+10)
    canvasMod.coords(labelDPoint,xDPoint,yDPoint+10)
    canvasMod.coords(labelCoMPoint,xCoMPoint,yCoMPoint+10)
    canvasMod.coords(lineBC,xBPoint,yBPoint,xCPoint,yCPoint)
    canvasMod.coords(lineAD,xAPoint,yAPoint,xDPoint,yDPoint)
    canvasMod.coords(lineMg,xCoMPoint,yCoMPoint,xCoMPoint,yCoMPoint+30)

# sliders controlling associated limb segment angles
def onAngleUpperArmChanged(val):
    # update positions of shoulder, elbow, wrist and fingertip respectively
    global angleUpperArm
    angleUpperArm=float(val)*ma.pi/180
    global xElbow
    xElbow=xShoulder+lengthUpperArm*ma.cos(angleUpperArm)
    global yElbow
    yElbow=yShoulder-lengthUpperArm*ma.sin(angleUpperArm)
    global xWrist
    xWrist=xElbow+lengthForearm*ma.cos(angleForearm)
    global yWrist
    yWrist=yElbow-lengthForearm*ma.sin(angleForearm)
    global xFingerTip
    xFingerTip=xWrist+lengthHand*ma.cos(angleHand)
    global yFingerTip
    yFingerTip=yWrist-lengthHand*ma.sin(angleHand)
    # update limb drawing
    updateLimb()
    # update consumed endurance modelling
    modelConsumedEndurance()
    VariableT_shoulder.set(float("{0:.2f}".format(T_shoulder))) # only display 2 decimal digits
    VariableStrength.set(float("{0:.2f}".format(strength)))
    VariableEndurance.set(float("{0:.2f}".format(endurance)))

def onAngleForearmChanged(val):
    global angleForearm
    angleForearm=float(val)*ma.pi/180
    global xWrist
    xWrist=xElbow+lengthForearm*ma.cos(angleForearm)
    global yWrist
    yWrist=yElbow-lengthForearm*ma.sin(angleForearm)
    global xFingerTip
    xFingerTip=xWrist+lengthHand*ma.cos(angleHand)
    global yFingerTip
    yFingerTip=yWrist-lengthHand*ma.sin(angleHand)
    # update limb drawing
    updateLimb()
    # update consumed endurance modelling
    modelConsumedEndurance()
    VariableT_shoulder.set(float("{0:.2f}".format(T_shoulder))) # only display 2 decimal digits
    VariableStrength.set(float("{0:.2f}".format(strength)))
    VariableEndurance.set(float("{0:.2f}".format(endurance)))

def onAngleHandChanged(val):
    global angleHand
    angleHand=float(val)*ma.pi/180
    global xFingerTip
    xFingerTip=xWrist+lengthHand*ma.cos(angleHand)
    global yFingerTip
    yFingerTip=yWrist-lengthHand*ma.sin(angleHand)
    # update limb drawing
    updateLimb()
    # update consumed endurance modelling
    modelConsumedEndurance()
    VariableT_shoulder.set(float("{0:.2f}".format(T_shoulder))) # only display 2 decimal digits
    VariableStrength.set(float("{0:.2f}".format(strength)))
    VariableEndurance.set(float("{0:.2f}".format(endurance)))

def onGenderChanged(*args):
    global lengthUpperArm
    global lengthForearm
    global lengthHand
    global massUpperArm
    global massForearm
    global massHand
    global massxg
    global maxTorque
    if gender.get()=="male":
        lengthUpperArm=132
        lengthForearm=108
        lengthHand=76
        massUpperArm=2.1
        massForearm=1.2
        massHand=0.4
        massxg=(2.1+1.2+0.4)*10
        maxTorque=22.94
    if gender.get()=="female":
        lengthUpperArm=124
        lengthForearm=94
        lengthHand=73
        massUpperArm=1.7
        massForearm=1.0
        massHand=0.4
        massxg=(1.7+1.0+0.4)*10
        maxTorque=18.57
    sliderUpperArm.set(sliderUpperArm.get()-5)
    sliderUpperArm.set(sliderUpperArm.get()+5)

def onResetClicked(event):
    sliderUpperArm.set(0)
    sliderForearm.set(0)
    sliderHand.set(0)

def onTableClicked(event):
    webbrowser.open_new(r"https://github.com/avaniyu/Aalto_EngineeringForHumans/blob/master/7_CE/Anthropometrics_Table.jpg")

#visualization (Vis) UI
canvasVis=tk.Canvas(visualizationUi,bg="white",borderwidth=2,relief=tk.GROOVE,width=400,height=400)
jointShoulderVis=canvasVis.create_oval(xShoulder-27,yShoulder+27,xShoulder+27,yShoulder-27,fill='#ffdbac',outline='#ffdbac')
jointElbowVis=canvasVis.create_oval(xElbow-20,yElbow+20,xElbow+20,yElbow-2,fill='#ffdbac',outline='#ffdbac')
jointWristVis=canvasVis.create_oval(xWrist-8,yWrist+8,xWrist+8,yWrist-8,fill='#ffdbac',outline='#ffdbac')
jointFingerTipVis=canvasVis.create_oval(xFingerTip-3,yFingerTip+3,xFingerTip+3,yFingerTip-3,fill='#ffdbac',outline='#ffdbac')
limbUpperArm=canvasVis.create_polygon([xShoulder,yShoulder+27,xElbow,yElbow+20,xElbow,yElbow-20,xShoulder,yShoulder-27],fill='#ffdbac')#this HEX is skin colour
limbForearm=canvasVis.create_polygon([xElbow,yElbow+20,xWrist,yWrist+8,xWrist,yWrist-8,xElbow,yElbow-20],fill='#ffdbac',outline='#ffdbac')
limbHand=canvasVis.create_polygon([xWrist,yWrist-8,xWrist+35,yWrist-15,xFingerTip,yFingerTip-3,xFingerTip,yFingerTip+3,xFingerTip-35,yFingerTip-3,xWrist+20,yWrist+8,xWrist,yWrist+8],fill='#ffdbac',outline='#ffdbac')
sliderUpperArm=tk.Scale(visualizationUi,from_=30,to=-70,resolution=5,command=onAngleUpperArmChanged,tickinterval=30)
sliderForearm=tk.Scale(visualizationUi,from_=80,to=0,resolution=5,command=onAngleForearmChanged,tickinterval=30)
sliderHand=tk.Scale(visualizationUi,from_=60,to=-80,resolution=5,command=onAngleHandChanged,tickinterval=30)
labelAngleUpperArm=tk.Label(visualizationUi,text="Upper Arm Angle")
labelAngleForearm=tk.Label(visualizationUi,text="Forearm Angle")
labelAngleHand=tk.Label(visualizationUi,text="Hand Angle")
buttonTable=tk.Button(visualizationUi,text="Anthropometrics Table")
gender=tk.StringVar()
gender.set("male")
buttonGender=tk.OptionMenu(visualizationUi,gender,"male","female")
buttonReset=tk.Button(visualizationUi,text="Reset",bg='#6fccdd',width=10)
canvasVis.grid(row=0,column=0,rowspan=6,columnspan=2,padx=10,pady=10)
labelAngleUpperArm.grid(row=0,column=2,padx=10)
sliderUpperArm.grid(row=1,column=2,sticky=tk.E,padx=10)
labelAngleForearm.grid(row=2,column=2,padx=10)
sliderForearm.grid(row=3,column=2,sticky=tk.E,padx=10)
labelAngleHand.grid(row=4,column=2,padx=10)
sliderHand.grid(row=5,column=2,sticky=tk.E,padx=10)
buttonTable.grid(row=6,column=0,padx=10,pady=10,sticky=tk.E)
buttonGender.grid(row=6,column=1,padx=10,pady=10,sticky=tk.EW)
buttonReset.grid(row=6,column=2,padx=10,pady=10)
buttonReset.bind('<Button-1>',onResetClicked)
buttonTable.bind('<Button-1>',onTableClicked)
gender.trace("w",onGenderChanged)

#modelling (Mod) UI
canvasMod=tk.Canvas(modellingUi,borderwidth=2,relief=tk.GROOVE,width=400,height=400)
armMod=canvasMod.create_line(xShoulder,yShoulder,xElbow,yElbow,xWrist,yWrist,xFingerTip,yFingerTip, width=2)
jointShoulderMod=canvasMod.create_oval(xShoulder-5,yShoulder+5,xShoulder+5,yShoulder-5)
jointElbowMod=canvasMod.create_oval(xElbow-5,yElbow+5,xElbow+5,yElbow-5)
jointWristMod=canvasMod.create_oval(xWrist-5,yWrist+5,xWrist+5,yWrist-5)
jointFingerTipMod=canvasMod.create_oval(xFingerTip-5,yFingerTip+5,xFingerTip+5,yFingerTip-5)
pointAMod=canvasMod.create_oval(xAPoint-2,yAPoint+2,xAPoint+2,yAPoint-2)
pointBMod=canvasMod.create_oval(xBPoint-2,yBPoint+2,xBPoint+2,yBPoint-2)
pointCMod=canvasMod.create_oval(xCPoint-2,yCPoint+2,xCPoint+2,yCPoint-2)
pointDMod=canvasMod.create_oval(xDPoint-2,yDPoint+2,xDPoint+2,yDPoint-2)
pointCoMMod=canvasMod.create_oval(xCoMPoint-3,yCoMPoint+3,xCoMPoint+3,yCoMPoint-3,fill='#6fccdd')
lineBC=canvasMod.create_line(xBPoint,yBPoint,xCPoint,yCPoint,dash=(3,5))
lineAD=canvasMod.create_line(xAPoint,yAPoint,xDPoint,yDPoint,dash=(3,5))
lineMg=canvasMod.create_line(xCoMPoint,yCoMPoint,xCoMPoint,yCoMPoint+30,arrow=tk.LAST,fill='#6fccdd')
labelShoulderMod=canvasMod.create_text(xShoulder,yShoulder-10,text="Shoulder")
labelElbowMod=canvasMod.create_text(xElbow,yElbow-10,text="Elbow")
labelWristMod=canvasMod.create_text(xWrist,yWrist-10,text="Wrist")
labelFingerTipMod=canvasMod.create_text(xFingerTip,yFingerTip-10,text="Finger Tip")
labelAPoint=canvasMod.create_text(xAPoint,yAPoint+10,text="A")
labelBPoint=canvasMod.create_text(xBPoint,yBPoint+10,text="B")
labelCPoint=canvasMod.create_text(xCPoint,yCPoint+10,text="C")
labelDPoint=canvasMod.create_text(xDPoint,yDPoint+10,text="D")
labelCoMPoint=canvasMod.create_text(xCoMPoint,yCoMPoint+10,text="CoM")
labelAssumption = tk.Label(modellingUi, text="Assuming it's static gesture.")
VariableT_shoulder = tk.DoubleVar()
VariableStrength = tk.DoubleVar()
VariableEndurance = tk.DoubleVar()
labelTShoulderText = tk.Label(modellingUi,text="|T_shoulder| (Nm):", justify=tk.LEFT, anchor="w")
labelTShoulder = tk.Label(modellingUi, textvariable=VariableT_shoulder, justify=tk.LEFT,anchor="w")
labelSText = tk.Label(modellingUi,text="S (strength) (%):", justify=tk.LEFT, anchor="w")
labelS = tk.Label(modellingUi, textvariable=VariableStrength, justify=tk.LEFT,anchor="w")
labelEText = tk.Label(modellingUi,text="E (endurance) (s):", justify=tk.LEFT, anchor="w")
labelE = tk.Label(modellingUi, textvariable=VariableEndurance, justify=tk.LEFT,anchor="w")
canvasMod.grid(row=0,column=0,columnspan=2,padx=10,pady=10)
labelAssumption.grid(row=1, column=0, columnspan=2, padx=10, sticky=tk.EW)
labelTShoulderText.grid(row=2,column=0,padx=10,sticky=tk.E)
labelTShoulder.grid(row=2,column=1,padx=10,sticky=tk.W)
labelSText.grid(row=3,column=0,padx=10,sticky=tk.E)
labelS.grid(row=3,column=1,padx=10,sticky=tk.W)
labelEText.grid(row=4,column=0,padx=10,sticky=tk.E)
labelE.grid(row=4,column=1,padx=10,sticky=tk.W)

root.mainloop()
