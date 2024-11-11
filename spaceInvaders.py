import pygame as pg
from pygame import math
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

import math

import random

from Vector2D import *

limiteEsq = 20
limiteDir = 480


def load_texture(file):
    im = Image.open(file)
    ix, iy, im_data = im.size[0], im.size[1], im.tobytes("raw", "RGBA", 0, -1)

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, im_data
    )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    return tex_id

def load_texturePNG(filename):
    texture_surface = pg.image.load(filename)
    texture_data = pg.image.tostring(texture_surface, "RGBA", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA,
                 GL_UNSIGNED_BYTE, texture_data)

    return texture_id

class Tiro:
    def __init__(self, xx, yy, limitYsup):
        self.pos = Vector2D(xx, yy) #posicao da base do tiro
        self.comp = 10
        self.vel = 10
        self.limSup = limitYsup
        self.vivo = True
        self.flag = "ship"

    def conferePosicaoTiro(self):
        if (self.pos.y > self.limSup):
            self.vivo = False

    def atualizaPosicao(self):
        self.pos.y += self.vel

    def desenha(self):
        glColor3f(1.0,0.0,0.0)
        self.conferePosicaoTiro()
        if (self.vivo==True):
            glPushMatrix()
            glTranslatef(self.pos.x, self.pos.y, 0.0)
            glBegin(GL_LINES)
            glVertex2f(0.0, 0.0)
            glVertex2f(0.0, 10.0)
            glEnd()
            glPopMatrix()
        self.atualizaPosicao()

class TiroParafuso(Tiro):
    def __init__(self, xx, yy, limitYinf):
        super(TiroParafuso, self).__init__(xx, yy, limitYinf)
        self.vel = -self.vel/2
        self.limInf = self.limSup
        self.comp = 20  #comprimento total
        self.flag = "parafuso"
        self.listaPontos = []
        self.h = self.comp/3.0   #comprimento do passo
        self.d = 7.0    #largura do tiro
        self.d2 = self.d/2.0
        self.criaListaPontos()

    def criaListaPontos(self):
        yPos = self.pos.y
        d2 = self.d/2.0
        delta = self.h/30.0
        P1 = Vector2D(self.pos.x + d2, yPos)
        P2 = Vector2D(self.pos.x - d2, yPos-self.h)
        
        while (yPos >= self.limInf):
                a = (P2.y - P1.y)/(P2.x - P1.x)
                b = P2.y - a*P2.x

                xPos = (yPos - b)/a
                ponto = Vector2D(xPos, yPos)
                self.listaPontos.append(ponto)

                yPos = yPos - delta
                if (yPos < P2.y):
                    P1.x = P2.x
                    P1.y = P2.y
                    if (P1.x < self.pos.x):
                        P2.x = self.pos.x + d2
                        P2.y = P1.y - self.h
                    else:
                        P2.x = self.pos.x - d2
                        P2.y = P1.y - self.h
    
    def desenhaPontos(self):
        glColor3f(0.0,0.0,1.0)
        glPushMatrix()
        glBegin(GL_POINTS)
        for p in self.listaPontos:
            glVertex2f(p.x, p.y)
        glEnd()
        glPopMatrix()
        
    def conferePosicaoTiro(self):
        if ( (self.pos.y-self.comp) < self.limInf):
            self.vivo = False

    def desenha(self):
        glColor4f(1.0,0.0,0.0,1.0)
        glDisable(GL_TEXTURE_2D)
        self.conferePosicaoTiro()
        if (self.vivo==True):
            glBegin(GL_POINTS)
            for p in self.listaPontos:
                if ((p.y <= self.pos.y) and (p.y >= self.pos.y - self.comp) ):
                    glVertex2f(p.x, p.y)
            glEnd()

        self.atualizaPosicao()
        glEnable(GL_TEXTURE_2D)
    

class Ship:
    def __init__(self, xx, yy, limXinf, limXsup, idTex, idTexExp):
        self.pos = Vector2D(xx,yy)
        self.larg = 22
        self.alt = 14
        self.larg2 = self.larg/2
        self.alt2 = self.alt/2
        self.textId = idTex
        self.limInf = limXinf
        self.limSup = limXsup
        self.velX = 5
        self.textExp = idTexExp  #textura da explosao
        self.explodindo = False
        self.vivo = True
        self.limiteFrames = 50 #frames durante explosao
        self.nFrames = 0 #quantidade de frames decorridos sem troca de textura
        
    def inicia_Explosao(self):
        if (self.explodindo == False):
            self.explodindo = True
        
    def moveEsquerda(self):
        if (self.explodindo == False):
            self.pos.x -= self.velX
            if (self.pos.x < self.limInf):
                self.pos.x = self.limInf
    
    def moveDireita(self):
        if (self.explodindo == False):
            self.pos.x += self.velX
            if (self.pos.x > self.limSup):
                self.pos.x = self.limSup

    def desenha(self):
        glColor4f(1.0,1.0,1.0,1.0)
        if (self.explodindo == False):
            glBindTexture(GL_TEXTURE_2D, self.textId)
        else:
            glBindTexture(GL_TEXTURE_2D, self.textExp)

        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, 0.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(-self.larg2, -self.alt2)

        glTexCoord2f(1, 0)
        glVertex2f(self.larg2, -self.alt2)

        glTexCoord2f(1, 1)
        glVertex2f(self.larg2, self.alt2)

        glTexCoord2f(0, 1)
        glVertex2f(-self.larg2, self.alt2)
        glEnd()

        glPopMatrix()

        if (self.explodindo == True):
            self.nFrames += 1
            if (self.nFrames > self.limiteFrames):
                self.explodindo = False
                self.nFrames = 0



class Alien:
    def __init__(self, xx, yy, ttipo, idTex01, idTex02, idTexExp):
        self.pos = Vector2D(xx,yy) #posicao do ponto central do Alien
        self.vel = Vector2D(0.7,0)
        
        self.tipo = ttipo  #valor numerico 1 a 2
        self.limiteFrames = 10 #quantidade de frames até trocar textura
        self.nFrames = 0 #quantidade de frames decorridos sem troca de textura
        self.textId01 = idTex01   #textura de animacao frame 1
        self.textId02 = idTex02   #textura de animacao frame 2
        self.textExp = idTexExp  #textura da explosao
        self.defineAtributos()
        self.textAtiva = 1
        self.larg2 = self.largura/2
        self.alt2 = self.altura/2
        self.explodindo = False
        self.vivo = True
        

    def defineAtributos(self):
        if (self.tipo==1):
            self.ProbTiro = 1
            self.largura = 24
            self.altura = 16  
        elif (self.tipo==2):
            self.ProbTiro = 2
            self.largura = 16
            self.altura = 16
        elif (self.tipo==3):
            self.ProbTiro = 3
            self.largura = 22
            self.altura = 16
        elif (self.tipo==4):
            self.ProbTiro = 4
            self.largura = 24
            self.altura = 16

    def checaColisao(self, xInf, yInf, xSup, ySup):
        colisao = False
        if (self.explodindo == False):
            posAlien_X_Inf = self.pos.x-self.larg2
            posAlien_Y_Inf = self.pos.y-self.alt2
            posAlien_X_Sup = self.pos.x+self.larg2
            posAlien_Y_Sup = self.pos.y+self.alt2
        
            if ((xInf >= posAlien_X_Inf) and (xInf <= posAlien_X_Sup)):
                if ((yInf >= posAlien_Y_Inf) and (yInf <= posAlien_Y_Sup)):
                    colisao = True
            if (colisao == False):
                if ((xSup >= posAlien_X_Inf) and (xSup <= posAlien_X_Sup)):
                    if ((ySup >= posAlien_Y_Inf) and (ySup <= posAlien_Y_Sup)):
                        colisao = True
            if (colisao == True):
                self.inicia_Explosao()
        
        return colisao

    def inicia_Explosao(self):
        self.nFrames = 0
        self.limiteFrames = 10
        self.explodindo = True
    
    def desenha(self):
        glColor4f(1.0,1.0,1.0,1.0)
        if (self.vivo == True):
            self.nFrames += 1
            if (self.explodindo == False):
                self.limiteFrames = int(10-abs(2*self.vel.x))
        
            if (self.nFrames>self.limiteFrames):
                if (self.explodindo==False):
                    self.textAtiva = -self.textAtiva
                    self.nFrames = 0
                else:
                    self.vivo = False
        
            if (self.explodindo == False):
                if (self.textAtiva==1):
                    text_iden = self.textId01
                else:
                    text_iden = self.textId02
            else:
                text_iden = self.textExp

            self.pos.x = self.pos.x + self.vel.x

            glBindTexture(GL_TEXTURE_2D, text_iden)
            glPushMatrix()
            glTranslatef(self.pos.x, self.pos.y, 0.0)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(-self.larg2, -self.alt2)

            glTexCoord2f(1, 0)
            glVertex2f(self.larg2, -self.alt2)

            glTexCoord2f(1, 1)
            glVertex2f(self.larg2, self.alt2)

            glTexCoord2f(0, 1)
            glVertex2f(-self.larg2, self.alt2)
            glEnd()

            glPopMatrix()

def confereFimdeCurso(listaA):
    ret = False
    for alien in listaA:
        if(alien.pos.x<limiteEsq) or (alien.pos.x>limiteDir):
            ret = True
            return ret
    return ret

def atualizaVelocidade_e_Altura_Aliens(listaA):
     for alien in listaA:
        alien.pos.y = alien.pos.y - 20
        if (alien.vel.x > 0):
            alien.vel.x += 0.12
        else:
            alien.vel.x -= 0.12
        alien.vel.x = -alien.vel.x

def atualizaVelocidadeAliens(listaA):
    for alien in listaA:
        if (alien.vel.x > 0):
            alien.vel.x += 0.03
        else:
            alien.vel.x -= 0.03
        
def criaAlien(lista, posX, posY, ttipo, tt1, tt2, tt3):
        novoAlien = Alien(posX, posY, ttipo, tt1, tt2, tt3)
        lista.append(novoAlien)

def checaColisaoTiroAliens(alien01, shot01):
    col = alien01.checaColisao(shot01.pos.x, shot01.pos.y, shot01.pos.x, shot01.pos.y+shot01.comp)
    return col

def eliminaMortos(lista):
    for alien in lista:
        if alien.vivo == False:
            lista.remove(alien)

def montaListaAlien(lista, janX, janY, t0, t1, t2, t3, t4, t5, t6, t7, t8):
        jj = 1
        for i in range (100, int(janX-100), 30):
            criaAlien(lista, i, int(janY) - 100, jj, t1, t2, t0)
        jj = 2
        for i in range (100, int(janX-100), 30):
            criaAlien(lista, i, int(janY - 120), jj, t3, t4, t0)
        jj = 3
        for i in range (100, int(janX-100), 30):
            criaAlien(lista, i, int(janY - 140), jj, t5, t6, t0)
        jj = 4
        for i in range (100, int(janX-100), 30):
            criaAlien(lista, i, int(janY - 160), jj, t7, t8, t0)

def checaTiroAliens(listaAl, listaT):
    for alien in listaAl:
        prob = random.randint(0,1000)
        if (prob <= alien.ProbTiro):
            listaT.append(TiroParafuso(alien.pos.x, alien.pos.y, 0.0))

def checaColisaoTiro(tiroShip, tiroParaf):
    #confere se o vertice superior do tiroShip está contido dentro do retangulo formado pelo TiroParafuso
    ret = False
    tiroParafD2 = tiroParaf.d2

    if ((tiroShip.pos.x < (tiroParaf.pos.x + tiroParafD2)) and (tiroShip.pos.x > (tiroParaf.pos.x - tiroParafD2)) and ((tiroShip.pos.y + tiroShip.comp) > (tiroParaf.pos.y - tiroParaf.comp)) and ((tiroShip.pos.y + tiroShip.comp) < (tiroParaf.pos.y))):
        ret = True

    return ret

def checaColisaoTirosNaLista(listaT):
    res = False
    for tiro in listaT:
        if (tiro.flag == "ship"):
            for ttiro in listaT:
                if (ttiro.flag != "ship"):
                    res = checaColisaoTiro(tiro, ttiro)
                    if (res == True):
                        tiro.vivo = False
                        ttiro.vivo = False
                        break

def checaPontoInteriorRetangulo(px, py, r1x, r1y, r3x, r3y):
    ret = False
    if (  (px < r3x) and (px > r1x) and (py > r1y) and (py < r3y) ):
        ret = True
    return ret

def checaColisaoTirosNaShip(ship, listaT):
    res = False
    for tiro in listaT:
        if (tiro.flag != "ship"):
            res = checaPontoInteriorRetangulo(tiro.pos.x-tiro.d2, tiro.pos.y, ship.pos.x-ship.larg2, ship.pos.y-ship.alt2, ship.pos.x+ship.larg2, ship.pos.y+ship.alt2)
            if (res == False):
                checaPontoInteriorRetangulo(tiro.pos.x+tiro.d2, tiro.pos.y, ship.pos.x-ship.larg2, ship.pos.y-ship.alt2, ship.pos.x+ship.larg2, ship.pos.y+ship.alt2)
            if (res == False):
                checaPontoInteriorRetangulo(tiro.pos.x-tiro.d2, tiro.pos.y-tiro.comp, ship.pos.x-ship.larg2, ship.pos.y-ship.alt2, ship.pos.x+ship.larg2, ship.pos.y+ship.alt2)
            if (res == False):
                checaPontoInteriorRetangulo(tiro.pos.x+tiro.d2, tiro.pos.y-tiro.comp, ship.pos.x-ship.larg2, ship.pos.y-ship.alt2, ship.pos.x+ship.larg2, ship.pos.y+ship.alt2)
            if (res == True):
                ship.inicia_Explosao()
                break

def checaColisaoAliensNaShip(ship, listaA):
    res = False
    if (ship.explodindo == False):
        for alien in listaA:
            res = checaPontoInteriorRetangulo(alien.pos.x-alien.larg2, alien.pos.y+alien.alt2, ship.pos.x-ship.larg2, ship.pos.y-ship.alt2, ship.pos.x+ship.larg2, ship.pos.y+ship.alt2)
            if (res==False):
                res = checaPontoInteriorRetangulo(alien.pos.x+alien.larg2, alien.pos.y+alien.alt2, ship.pos.x-ship.larg2, ship.pos.y-ship.alt2, ship.pos.x+ship.larg2, ship.pos.y+ship.alt2)
            if (res==False):
                res = checaPontoInteriorRetangulo(alien.pos.x-alien.larg2, alien.pos.y-alien.alt2, ship.pos.x-ship.larg2, ship.pos.y-ship.alt2, ship.pos.x+ship.larg2, ship.pos.y+ship.alt2)
            if (res==False):
                res = checaPontoInteriorRetangulo(alien.pos.x+alien.larg2, alien.pos.y-alien.alt2, ship.pos.x-ship.larg2, ship.pos.y-ship.alt2, ship.pos.x+ship.larg2, ship.pos.y+ship.alt2)
            if (res == True):
                ship.inicia_Explosao()
                alien.inicia_Explosao()
                break  
        
def main():
    pg.init()

    janelaX = 500.0   #dominio X de 0 a janelaX
    janelaY = 500.0   #Y vai de 0 a janelaY

    width = int(janelaX)
    height = int(janelaY)
    display = (width, height) 
    
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(1.0,1.0,1.0,0.0)

    textId_Alfa_01 = load_texture("alfa_01.jpg")
    textId_Alfa_02 = load_texture("alfa_02.jpg")
    textId_Bravo_01 = load_texture("bravo_01.jpg")
    textId_Bravo_02 = load_texture("bravo_02.jpg")
    textId_Charlie_01 = load_texture("charlie_01.jpg")
    textId_Charlie_02 = load_texture("charlie_02.jpg")
    textId_Delta_01 = load_texture("delta_01.jpg")
    textId_Delta_02 = load_texture("delta_02.jpg")
    textId_Explosao = load_texture("explosao.jpg")
    #textId_Ship = load_texturePNG("textTransp.png")    
    textId_Ship = load_texture("ship.jpg")    
    listaAliens = []
    listaTiros = []

    montaListaAlien(listaAliens, janelaX, janelaY, textId_Explosao, textId_Alfa_01, textId_Alfa_02, textId_Bravo_01, textId_Bravo_02, textId_Charlie_01, textId_Charlie_02, textId_Delta_01, textId_Delta_02)

    ship01 = Ship(janelaX/2.0, 30, 20, janelaX-20.0, textId_Ship, textId_Explosao)

    #alien01 = Alien(300,600,tipo, t1, t2)
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
                if event.key == pg.K_TAB:
                    tamLista = len(listaAliens)
                    if (tamLista>0):
                        sorteio = random.randint(0,tamLista-1)
                        alienExp = listaAliens[sorteio]
                        alienExp.inicia_Explosao()     
                 
        keys = pg.key.get_pressed()        
        if keys[pg.K_LEFT]:
            ship01.moveEsquerda()
        if keys[pg.K_RIGHT]:
            ship01.moveDireita()
        if ((keys[pg.K_SPACE]) or (keys[pg.K_UP])):
                tiroShip = -1
                for t in listaTiros:
                    if t.flag == "ship":
                        tiroShip = 1
                        break
                if ((tiroShip == -1) and (ship01.explodindo == False)):
                    listaTiros.append(Tiro(ship01.pos.x, ship01.pos.y+20, janelaY) )
        if keys[pg.K_TAB]:
            tiro02 = TiroParafuso(100.0, 400.0, 0.0)
            listaTiros.append(tiro02)

        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glOrtho(0.0, janelaX, 0.0, janelaY, -10.0, 10.0)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_BLEND)
        glEnable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        eliminaMortos(listaAliens)
        eliminaMortos(listaTiros)
        checaTiroAliens(listaAliens, listaTiros)
        checaColisaoTirosNaLista(listaTiros)
        checaColisaoTirosNaShip(ship01, listaTiros)
        checaColisaoAliensNaShip(ship01, listaAliens)

        if (len(listaTiros)>0):
            tiroShip = Tiro(0.0,0.0,100.0)
            acheiTiroShip = -1
            for ts in listaTiros:
                if ts.flag == "ship":
                    tiroShip = ts
                    acheiTiroShip = 1
                    break
            if (acheiTiroShip == 1):  
                for alien in listaAliens:
                    col = checaColisaoTiroAliens(alien, tiroShip)
                    if (col==True):
                        for ts in listaTiros:
                            if ts.flag == "ship":
                                ts.vivo = False
                                break
                        atualizaVelocidadeAliens(listaAliens)
                        break
    
        if(confereFimdeCurso(listaAliens)==True):
            atualizaVelocidade_e_Altura_Aliens(listaAliens)

        for shot in listaTiros:
            shot.desenha()
        
        for alien in listaAliens:
            alien.desenha()
        ship01.desenha()
        

        pg.display.flip()

        
        pg.time.delay(30)


if __name__ == "__main__":
    main()
        
        

