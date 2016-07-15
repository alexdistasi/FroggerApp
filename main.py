#########Project 3
##Author: Alex DiStasi
##Date: 5-5-2015
##Purpose: Recreate frogger using Kivy
#########


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import *
from random import randint
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.core.window import Window
from random import random
from math import *
from random import *


class froggerGame(App):
    def __init__(self, **kwargs):
        super(froggerGame, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1/60.)
        self.dist = 300
        self.radiusSum =301
        
    #checks for collisions between frog and car
    def collisionCheck(self):
        carYPos2 = 500
        for i in range(len(self.carList)):
            carCenterX= self.carList[i].xposCar + (self.car.width / 2)
            carCenterY=carYPos2 + (self.car.height / 2)
            frogCenterX= self.frog.xpos + self.frog.width
            frogCenterY= self.frog.ypos + self.frog.height
            frogRadius = self.frog.width/2
            xDist = (frogCenterX - carCenterX) ** 2
            yDist = (frogCenterY - carCenterY) ** 2
            #calculate the difference in position car and center
            self.dist = (sqrt(xDist + yDist))
            carRadius = self.car.height / 2
            #calculate the sum of the frog and car radius
            self.radiusSum = frogRadius + carRadius
            carYPos2 += 150

            #if the distance is less than the radius sum, there is a collision
            if self.dist < self.radiusSum:
                self.frog.collide()
                self.screen.remove_widget(self.frogLivesArray[self.strikes-1])
                self.strikes -= 1
                if self.strikes <= 0:
                    self.loseGame()
                
    #checks if the frog crossed the finish line
    def checkWin(self):
        crossLine = 1600
        if self.frog.ypos >= crossLine:
            self.winGame()

    #removes frog widget, adds winning text to screen
    def winGame(self):
        self.screen.remove_widget(self.frog)
    
      
        winText = Label(text = 'WINNER!',
                        font_size=300,
                        color = (0,0,1,1),
                        pos = (420,700))
        self.screen.add_widget(winText)
        
    #removes frog widgetm adds losing text to screen
    def loseGame(self):
        self.screen.remove_widget(self.frog)
        loseText = Label(text = 'LOSER!',
                        font_size=300,
                        color = (0,0,1,1),
                        pos = (420, 700))
        self.screen.add_widget(loseText)
        
    def build(self):
        self.screen = Widget()
        self.finLine = FinishLine()
        self.finLine.drawFinish()
        self.screen.add_widget(self.finLine)
        self.numCars = 7
        self.livesArray = []
        self.strikes = 4
        self.carInfo()
        self.frog = Frog()
        self.frog.drawFrog()
        self.screen.add_widget(self.frog)

        #creates an array of frog lives and adds them to the screen
        def lifeInfo():
            self.frogLivesArray = []
            xpos=50
            for i in range(self.strikes):
                myLives = frogStrikes()
                myLives.drawFrogLives(xpos)
                self.frogLivesArray.append(myLives)
                self.screen.add_widget(myLives)
                xpos += 120

        lifeInfo()

        #on key clicks, the frog will move in the x or y direction

        upKey = Button (text = "^",
                        size = (190,190),
                        pos = (750, 270),
                        background_color = (1,0,1,1))
        self.screen.add_widget(upKey)
        def gotClicked(obj):
            self.frog.moveUp()
            
          

        upKey.bind(on_release=gotClicked)
        

        downKey = Button (text = "v",
                        size = (190,190),
                        pos = (750, 35),
                        background_color = (1,0,1,1))
        self.screen.add_widget(downKey)
        def gotClicked(obj):
            self.frog.moveDown()
         
        downKey.bind(on_release=gotClicked)


        leftKey = Button (text = "<",
                        size = (190,190),
                        pos = (550, 150),
                        background_color = (1,0,1,1))
        self.screen.add_widget(leftKey)
        def gotClicked(obj):
            self.frog.moveLeft()
            
    
        leftKey.bind(on_release=gotClicked)

        rightKey = Button (text = ">",
                        size = (190,190),
                        pos = (950, 150),
                        background_color = (1,0,1,1))
        self.screen.add_widget(rightKey)
        def gotClicked(obj):
            self.frog.moveRight()
           
          
        rightKey.bind(on_release=gotClicked)

       

        return self.screen

 
    
   #creates the cars and adds them to the screen
    def carInfo(self):
        self.carList = []
        self.carYPos = 500
        for i in range(self.numCars):
            self.car = Car()
            self.car.drawCar(self.carYPos)
            self.screen.add_widget(self.car)
            self.carList.append(self.car)
            self.carYPos += 150           

    #moves car position, redraws frog widget, checks for collision,
    # and checks if won every second
    def update(self, *args):
        carYPos = 500
        for i in range(self.numCars):
            self.carList[i].eraseCar(carYPos)
            self.carList[i].moveCar()
            self.carList[i].drawCar(carYPos)
            carYPos += 150
        self.frog.drawFrog()
        self.collisionCheck()
        self.checkWin()
        
    

      
#draws the frog widget, erases frog widget, moves the frog widget   
class Frog(Widget):
    def __init__(self, **kwargs):
        super(Frog, self).__init__(**kwargs)
        self.xpos = 285
        self.ypos = 100
        self.height = 100
        self.width = 100
        


    def drawFrog(self):
        color=(1,0,1,1)
        with self.canvas:
            Color(*color, mode = 'rgba')
            Rectangle(pos=(self.xpos,self.ypos), size=(self.height, self.width))
    def eraseFrog(self):
        self.canvas.clear()

    def moveUp(self):
        self.eraseFrog()
        self.ypos+=70
        self.pos = (self.xpos, self.ypos)

       

    def moveDown(self):
        self.eraseFrog()
        self.ypos-=70
        self.pos = (self.xpos, self.ypos)


    def moveRight(self):
        self.eraseFrog()
        self.xpos+=70
        self.pos = (self.xpos, self.ypos)
 

    def moveLeft(self):
        self.eraseFrog()
        self.xpos-=70
        self.pos = (self.xpos, self.ypos)


    def collide(self):
        print "I got hit in the frog class!"
        self.eraseFrog()
        self.xpos = 100
        self.ypos = 100
        self.pos = (self.xpos, self.ypos)

        
#draws the car widget, moves the car widget, erases car widget
class Car(Widget):
    xVelocity = 5
    velocity = ListProperty([xVelocity, 5])


    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)
        self.xposCar = randint(-10, 900)
        self.yposCar = randint(420, 800)
        self.width = 200
        self.height = 120

    def eraseCar(self,ypos):
        self.canvas.clear()        
    
    def drawCar(self, ypos):
        color = (0,1,1,1)
        with self.canvas:
            Color(*color, mode = 'rgba')
            Rectangle(pos=(self.xposCar, ypos), size=(self.width, self.height))
        
    def moveCar(self):
        self.xposCar += self.velocity[0]
        
        if self.xposCar < 0 or (self.xposCar + self.width) > Window.width:
            self.velocity[0] *= -1        


#draws life widgets      
class frogStrikes(Widget):
    def __init__(self, **kwargs):
        super(frogStrikes,self).__init__(**kwargs)

    def drawFrogLives(self, xpos):
        color=(1,0,1,1)
        with self.canvas:
            Color(*color, mode = 'rgba')
            Rectangle(pos=(xpos, 1700), size=(100, 100))

  
#draws finish line
class FinishLine(Widget):
    def __init__(self, **kwargs):
        super(FinishLine, self).__init__(**kwargs)
        self.xposFinLine = 0
        self.yposFinLine = 1600


    def drawFinish(self):
        color = (1,0,0,1)
        with self.canvas:
            Color(*color, mode = 'rgba')
            Rectangle(pos=(self.xposFinLine,self.yposFinLine), size=(1300, 250))

    
#runs program
if __name__ == "__main__":
    froggerGame().run()

