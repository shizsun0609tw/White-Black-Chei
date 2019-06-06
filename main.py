import pygame as pg
from pygame.locals import *
from draw import *
from judge import *
#--------------------------------const var--------------------------------#
GAMEMODE_INIT = 0
GAMEMODE_GAMMING = 1
GAMEMODE_END = 2

STARTBUTTON = 0
QUITBUTTON = 1
RESTARTBUTTON = 2

GAME_STATE_HAND = 1
GAME_STATE_HEAD_WIN = 2
GAME_STATE_HEAD_LOSE = 3
GAME_STATE_LOSE = 4
GAME_STATE_WIN = 5

NEED_INIT = 0
N_NEED_INIT = 1

#--------------------------------screen init--------------------------------#
pg.init()

width, height = 1080, 720
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Hello Game!")
# init screen #
button = []
button.append(Button((700, 300), (200, 50), "Start", STARTBUTTON))
button.append(Button((700, 400), (200, 50), "Quit", QUITBUTTON))
# gamming screen #
reStartButton = Button((500, 600), (250, 50), "Restart", RESTARTBUTTON)
RPSText = Text((800, 300), (100, 50), "RPS:")
FingerText = Text((800, 350), (100, 50), "Finger:")
HeadText = Text((800, 400), (100, 50), "Head:")
revText = Text((200, 500), (100,50), "Rev:")
titleText = Text((350, 300), (100, 100), "Black White Chei")
authorText = Text((350, 400), (100, 100), "Autor: Zhen-Hua Chen")
timeText = Text((1000, 50), (30, 30), "")
winText = Text((300, 600), (100, 50), "You WIN!!!")
loseText = Text((300, 600), (100, 50), "You LOSE!!!")
imgPaper = Image((50, 200), (100, 100), "paper.png")
imgStone = Image((50, 200), (100, 100), "stone.png")
imgScissor = Image((50, 200), (100, 100), "scissor.png")
imgHandMask = Image((50, 200), (100, 100), "handMask.png")
imgFaceUp = Image((300, 200), (100, 100), "face_up.png")
imgFaceDown = Image((300, 200), (100, 100), "face_down.png")
imgFaceRight = Image((300, 200), (100, 100), "face_right.png")
imgFaceLeft = Image((300, 200), (100, 100), "face_left.png")
imgFaceMask = Image((300, 200), (100, 100), "faceMask.png")
imgFingerUp = Image((550, 200), (100, 100), "finger_up.png")
imgFingerDown = Image((550, 200), (100, 100), "finger_down.png")
imgFingerLeft = Image((550, 200), (100, 100), "finger_left.png")
imgFingerRight = Image((550, 200), (100, 100), "finger_right.png")
imgFingerMask = Image((550, 200), (100, 100), "handMask.png")

imgCurrentHand = imgHandMask
imgCurrentHead = imgFaceMask
imgCurrentFinger = imgFingerMask
#--------------------------------musci init--------------------------------#
pg.mixer.init()
pg.mixer.music.load('Assets\\How_it_Began.mp3')
pg.mixer.music.play()
#--------------------------------game init--------------------------------#
running = True
roundTime = 3

switch = NEED_INIT
gameMode = GAMEMODE_INIT
gameState = GAME_STATE_HAND
#--------------------------------game procedure--------------------------------#
def changeImg():
    global imgCurrentHand, imgCurrentHead, imgCurrentFinger
    face = Judge.getFaceDir()
    finger = Judge.getFingerDir()
    rps = Judge.getRPS()

    if rps == Judge.PAPER:
        imgCurrentHand = imgPaper
    elif rps == Judge.SCISSOR:
        imgCurrentHand = imgScissor
    elif rps == Judge.STONE:
        imgCurrentHand = imgStone
    elif rps == Judge.INIT:
        imgCurrentHand = imgHandMask

    if face == Judge.UP:
        imgCurrentHead = imgFaceUp
    elif face == Judge.DOWN:
        imgCurrentHead = imgFaceDown
    elif face == Judge.LEFT:
        imgCurrentHead = imgFaceLeft
    elif face == Judge.RIGHT:
        imgCurrentHead = imgFaceRight
    elif face == Judge.INIT:
        imgCurrentHead = imgFaceMask

    if finger == Judge.UP:
        imgCurrentFinger = imgFingerUp
    elif finger == Judge.LEFT:
        imgCurrentFinger = imgFingerLeft
    elif finger == Judge.RIGHT:
        imgCurrentFinger = imgFingerRight
    elif finger == Judge.DOWN:
        imgCurrentFinger = imgFingerDown
    elif finger == Judge.INIT:
        imgCurrentFinger = imgFingerMask

def gameProcedure():
    global switch, timer, gameState, gameMode, imgCurrentHand, imgCurrentHead
    
    Judge.readCamera()

    # round init
    if switch == NEED_INIT:
        switch = N_NEED_INIT
        timer = pg.time.get_ticks() // 1000
    
    # game judge
    passTime = pg.time.get_ticks() // 1000 - timer
    
    if passTime > 0.5:
        Judge.setInit()

    if passTime > roundTime - 1:
        switch = NEED_INIT
        ##################################
        if gameState == GAME_STATE_HAND:
            rev = Judge.judgeHand(revText)
            if rev == Judge.WIN:
                RPSText.setText((str)("RPS:WIN"))
                gameState = GAME_STATE_HEAD_WIN
            elif rev == Judge.LOSE:
                RPSText.setText((str)("RPS:LOSE"))
                gameState = GAME_STATE_HEAD_LOSE
            elif rev == Judge.DRAW:
                RPSText.setText((str)("RPS:DRAW"))
                gameState = GAME_STATE_HAND
        elif gameState == GAME_STATE_HEAD_WIN:
            rev = Judge.judgeHeadWin(revText)
            if rev == Judge.WIN:
                FingerText.setText((str)("Finger:WIN"))
                gameMode = GAMEMODE_END
                gameState = GAME_STATE_WIN
            elif rev == Judge.DRAW:
                FingerText.setText((str)("Finger:DRAW"))
                gameState = GAME_STATE_HAND
        elif gameState == GAME_STATE_HEAD_LOSE:
            rev = Judge.judgeHeadLose(revText)
            if rev == Judge.LOSE:
                HeadText.setText((str)("Head:LOSE"))
                gameMode = GAMEMODE_END
                gameState = GAME_STATE_LOSE
            elif rev == Judge.DRAW:
                HeadText.setText((str)("Head:DRAW"))
                gameState = GAME_STATE_HAND
                
    timeText.setText((str)(roundTime - passTime))
    changeImg()
    
    Judge.showCamera()

#--------------------------------game draw--------------------------------#
def drawGame():
    timeText.draw(screen)
    RPSText.draw(screen)
    FingerText.draw(screen)
    HeadText.draw(screen)
    revText.draw(screen)
    imgCurrentHand.draw(screen)
    imgCurrentHead.draw(screen)
    imgCurrentFinger.draw(screen)

def drawWin():
    drawGame()
    winText.draw(screen)
    reStartButton.draw(screen)

def drawLose():
    drawGame()
    loseText.draw(screen)
    reStartButton.draw(screen)

#--------------------------------game running--------------------------------#
while running:
    screen.fill((222, 212, 197))

    #----------start screen----------#
    if gameMode == GAMEMODE_INIT:
        #-----event handler-----#
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            for b in button:
                rev = b.event_handler(event)
                if rev == QUITBUTTON:
                    pg.quit()
                elif rev == STARTBUTTON:
                    gameMode = GAMEMODE_GAMMING
                elif rev == RESTARTBUTTON:
                    gameMode = GAMEMODE_GAMMING
        #-----draw-----#
        titleText.draw(screen)
        authorText.draw(screen)
        for b in button:
            b.draw(screen)
    #----------game screen----------#
    elif gameMode == GAMEMODE_GAMMING:
        #-----event handler-----#
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        #-----draw-----#
        gameProcedure()
        drawGame()
      
    # game end
    elif gameState == GAME_STATE_WIN:
        drawWin()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if reStartButton.event_handler(event) == RESTARTBUTTON:
                gameMode = GAMEMODE_INIT
                gameState = GAME_STATE_HAND
    elif gameState == GAME_STATE_LOSE:
        drawLose()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if reStartButton.event_handler(event) == RESTARTBUTTON:
                gameMode = GAMEMODE_INIT
                gameState = GAME_STATE_HAND
        

    pg.display.update()
