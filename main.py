import pygame
import time
import random
from pygame.locals import *

from question import *


Framerate = False

class game:
    def __init__(self,path=["base"]):
        pygame.init()
        self.window = pygame.display.set_mode((640,480), RESIZABLE)
        #self.DBackground = pygame.image.load("background.jpg").convert()
        self.finished = False
        #loading content
        appended = []
        for loop in path:
            appended.append(loop+"/question")
        self.q = questions(appended,False,False)
        self.mouse = 0#0 = None, 1 = Up, 2 = Down
        #for test only
        
        self.xSize, self.ySize = pygame.display.get_surface().get_size()
        self.BColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        #resize
        self.q.resize(self.xSize,self.ySize)
        
        self.randomQuestion()

    def getQuestion(self):
        return self.actualQuestion

    def randomQuestion(self):
        self.actualQuestion = self.q.getRandomQ()
        return self.actualQuestion
    
    def frame(self):
        if not(self.finished):
            if self.mouse==1:
                self.mouse=0
            #really fun
            ##self.BColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            resized = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.finished = True
                elif event.type == VIDEORESIZE:
                    resized = True
                    self.xSize = event.dict['size'][0]
                    self.ySize = event.dict['size'][1]
                    self.window = pygame.display.set_mode((self.xSize,self.ySize), RESIZABLE)
                    self.q.resize(self.xSize,self.ySize)
                elif event.type == pygame.MOUSEMOTION:
                    self.my, self.mx = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse = 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse = 2
            #self.window.blit(self.DBackground, (0,0))

            pygame.draw.rect(self.window,self.BColor,(0,0,self.xSize,self.ySize))
            
            #for test
            #self.randomQuestion()
            re = self.q.drawQ(self.window,self.getQuestion(),self.mx,self.my,self.mouse,resized)
            if re[0]:
                if re[1]:
                    print("bonne réponse")
                elif not re[1]:
                    print("mauvaise réponse")
                self.randomQuestion()
            #end for test
            pygame.display.flip()
            return True
        else:
            return False

if __name__ == "__main__":
    a=game()
    t=time.time()
    c=0
    while (a.frame()):
        if Framerate:
            clock = pygame.time.Clock()
            clock.tick(Framerate)
        c=c+1
        if time.time()-t>1:
            print(c)
            c=0
            t=time.time()
