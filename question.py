# -*- coding: cp1252 -*-
import os
import random
import pygame

class questions:
    def __init__(self, path, debug=False, qDebug=False):
        if debug:
            print("initialisation de la classe questions")
            print("path :")
            print(path)
        self.debug = debug
        self.path = path
        self.questionList=[]

        for loop in path:
            
            LDir = os.listdir(loop)
            for loop2 in LDir:
                
                if debug:
                    print("lecture de " + loop + "/" + loop2 )
                self.questionList.append(question(loop + "/" + loop2, qDebug))
        self.resetList()

        #graphic

        self.QFont = pygame.font.SysFont('freesans', 36)#police utilisé pour la question
        self.QTextColor = 255, 100, 0#couleur du texte de la question
        self.QText = False#Contient les ligne à afficher dans les questions
        self.QTextPos = (0,0)
        self.QTextQ = False#sert à verifier que le calcul de l'affichage est à jour
        self.QFond = 255,255,255#couleur par défaut du fond de la réponse
        self.AFont = pygame.font.SysFont('freesans', 36)#police utilisé pour la réponse
        self.AFontColor = 255, 100, 0#couleur du texte de la réponse
        self.AFond = 0,0,0#couleur du fond de la réponse
        self.AVFond = 255,255,255#couleur de la validation de la réponse
        if debug:
            print("fin de la créations des question")

    def getRandomQ(self):
        if len(self.undone)==0:
            self.resetList()
        res = random.randint(0,len(self.undone)-1)
        cop = []
        for loop in range(len(self.undone)):
            if res == loop:
                self.done.append(self.undone[loop])
                pass
            else:
                cop.append(self.undone[loop])
        self.undone = cop
        return res

    def resetList(self):
        self.undone = []
        for loop in range(len(self.questionList)):
            self.undone.append(loop)
        self.done = []
    def resize(self,x,y):
        self.xSize = x
        self.ySize = y
        
    def drawQ(self,window,nb,mx,my,mouse,resized=True):
        reponse = [False,True]#1 : validation, 2 : réponse ( vrai ou faux )
        Fwidth = self.xSize-100
        if self.QText == False or self.QTextQ != nb:
            resized=True
            self.QTextQ = nb
        if resized:
            texte = self.questionList[nb].QQuestion
            self.QText=[]
            temp=""
            temp3=0
            for loop in texte:
                temp=temp+loop
                if len(temp)>int(Fwidth)/16:
                    temp2=self.QFont.render(temp,True,self.QTextColor)
                    temp_width, temp_height = self.QFont.size(temp)
                    self.QText.append([temp2,temp_height])
                    temp=""
                    temp3=temp3+temp_height
            if len(temp)!=0:
                temp2=self.QFont.render(temp,True,self.QTextColor)
                temp_width, temp_height = self.QFont.size(temp)
                self.QText.append([temp2,temp_height])
                temp3=temp3+temp_height
            self.QT=temp3

            answer = self.questionList[nb].QAnswer #traitement des réponse
            self.QAnswer = []#sera append à QAnswer, contient toute les donné graphique des réponse
            biggest=0
            for loop in answer:
                temp_width, temp_height = self.AFont.size(loop[0])
                temp2 = self.AFont.render(loop[0],True,self.AFontColor)
                self.QAnswer.append([temp2,temp_height,loop])
                if temp_width>biggest:
                    biggest=temp_width
            self.ABiggest=biggest
                
        pygame.draw.rect(window, self.QFond, (50,80,Fwidth,self.QT+10))
        temp = 0
        for loop in self.QText:
            #print(loop[1])
            window.blit(loop[0], (self.xSize/2-loop[0].get_rect().width/2,temp+80))
            temp=temp+loop[1]
        temp=temp+loop[1]*2+20

        for loop in self.QAnswer:
            mod=0
            mod2=0
            if mx>temp and mx<temp+loop[1]:
                mod=4
                mod2=5
                if mouse == 2:
                    mod=-3
                    mod2=-20
                if mouse == 1:
                    reponse[1] = loop[2][1]
                    reponse[0] = True
                    print(reponse)
            pygame.draw.rect(window,self.AFond, (self.xSize/2-self.ABiggest/2-20-mod2,temp-mod-3,self.ABiggest+40+mod2*2,loop[1]+mod*2+6))
            AVx = self.xSize/2-self.ABiggest/2-20-loop[1]*1.5
            if AVx>0:
                pygame.draw.rect(window,self.AVFond, (AVx-mod-3, temp-mod-3, loop[1]+mod*2+6, loop[1]+mod*2+6))
            window.blit(loop[0], (self.xSize/2-loop[0].get_rect().width/2,temp))
            temp=temp+loop[1]+16
            
        return reponse
    
    def printQ(self,nb=0):
        self.questionList[nb].printQ()
            
class question:
    def __init__(self,url,debug=False):
        if debug:
            print("question " + url + " créer")
        self.debug = debug
        self.url = url

        if debug:
            print("ouverture de " + url)

        fichier = open(url,"r")
        self.base = fichier.read()
        fichier.close()

        if debug:
            print("contenu du fichier :")
            for loop in self.base.split("\n"):
                print("    " + loop)
            print("lecture du fichier")

        self.QType = "#ERROR"
        self.QQuestion = "#ERROR"
        self.QAnswer = []
        self.id = "#ERROR"
        
        for loop in self.base.split("\n"):
            if debug:
                print("analyse de :")
                print(loop)
                
            splited = loop.split(" ")
            
            if splited[0] == ":":
                if debug:
                    print("type de question : " + splited[1])
                self.QType = splited[1]
                
            if splited[0] == "(":
                if debug:
                    print("question : " + loop[2:len(loop)])
                self.QQuestion = loop[2:len(loop)]

            if splited[0] == "-" or splited[0] == "+":
                if splited[0] == "-":
                    answerT = False
                else:
                    answerT = True
                if debug:
                    print("réponse : " + loop[2:len(loop)] + " --- " + str(answerT))
                self.QAnswer.append([loop[2:len(loop)],answerT])
                
            if splited[0] == "i":
                if debug:
                    print("id : " + splited[1])
                self.id = splited[1]
        if debug:
            print("-------------\ncréation de la question fini")
            print("type : " + self.QType)
            print("question : " + self.QQuestion)
            print("réponse : ")
            print(self.QAnswer)
                
    def printQ(self):
        print("type : " + self.QType)
        print("question : " + self.QQuestion)
        print("réponse : ")
        print(self.QAnswer)
        
        
        
if __name__=="__main__":
    a=questions(["base/question"], True)
    for loop in range(10):
        a.printQ(a.getRandomQ())
