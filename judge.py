import cv2
import random
import numpy as np
import dlib

class Judge(object):
    # WIN and LOSE depend on player
    INIT = -1

    WIN = 0
    LOSE = 1
    DRAW = 2

    PAPER = 0
    SCISSOR = 1
    STONE = 2

    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    rps = INIT
    faceDir = INIT
    fingerDir = INIT

    cameraImg = []
    processCameraImg = []

    _cap = cv2.VideoCapture(0)
    _detector = dlib.get_frontal_face_detector()
    _predictor = dlib.shape_predictor( 'Assets\\shape_predictor_68_face_landmarks.dat')

    @staticmethod
    def handDetection():
        img = cv2.cvtColor(Judge.processCameraImg[280:480, 450:640], cv2.COLOR_BGR2HSV)

        lower1 = np.array([0, 48, 50])
        upper1 = np.array([20, 256, 256])

        img = cv2.inRange(img, lower1, upper1)

        img = cv2.dilate(img, np.ones((5, 5)))
        img = cv2.erode(img, np.ones((5, 5)))
        img = cv2.medianBlur(img, 5)
        
        img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if(len(contours) == 0): return Judge.PAPER
        
        maxArea = contours[0]
        for i in range(len(contours)):
            if cv2.contourArea(contours[i]) > cv2.contourArea(maxArea):
                maxArea = contours[i] 

        hull = cv2.convexHull(maxArea)
        contourLen = cv2.arcLength(hull, True)
        approx = cv2.approxPolyDP(hull, 0.01 * contourLen, True)

        M = cv2.moments(approx)
        center = np.array([int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])])
        cv2.circle(Judge.processCameraImg, (center[0], center[1]), 5, (255, 0, 0), 3)
        
        count = 0
        for i in range(len(approx)):
            if cv2.norm(approx[i] - center) > 90:
                count += 1

        if count == 0:
            return Judge.STONE
        elif count > 0 and count < 6:
            return Judge.SCISSOR
        else:
            return Judge.PAPER

    @staticmethod
    def handDirDetection():
        img = cv2.cvtColor(Judge.processCameraImg[280:480, 450:640], cv2.COLOR_BGR2HSV)
        
        lower1 = np.array([0, 48, 50])
        upper1 = np.array([20, 256, 256])
        
        img = cv2.inRange(img, lower1, upper1)

        img = cv2.dilate(img, np.ones((5, 5)))
        img = cv2.erode(img, np.ones((5, 5)))
        img = cv2.medianBlur(img, 5)

        img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if(len(contours) == 0): return Judge.PAPER
        
        maxArea = contours[0]
        for i in range(len(contours)):
            if cv2.contourArea(contours[i]) > cv2.contourArea(maxArea):
                maxArea = contours[i] 


        hull = cv2.convexHull(maxArea)
        contourLen = cv2.arcLength(hull, True)
        approx = cv2.approxPolyDP(hull, 0.01 * contourLen, True)
        
        M = cv2.moments(approx)
        center = np.array([int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])])
        cv2.circle(Judge.processCameraImg, (center[0], center[1]), 5, (255, 0, 0), 3)
        
        farPoint = np.array(approx[0])
        for i in range(len(approx)):
            if cv2.norm(farPoint - center) < cv2.norm(approx[i] - center):
                farPoint = approx[i]

        if cv2.norm(farPoint - center) < 90:
            return Judge.DOWN
        elif farPoint[0][1] - center[1] < -90:
            return Judge.UP
        elif (farPoint - center)[0][0] < 0:
            return Judge.LEFT
        elif (farPoint - center)[0][0] > 0:
            return Judge.RIGHT


    @staticmethod
    def headDetection():
        face_rects, scores, idx = Judge._detector.run(Judge.processCameraImg, 0)

        for i, d in enumerate(face_rects):
            x1 = d.left()
            y1 = d.top()
            x2 = d.right()
            y2 = d.bottom()
            
            cv2.rectangle(Judge.processCameraImg, (x1, y1), (x2, y2), ( 0, 255, 0), 4, cv2. LINE_AA)
        
            landmarks_frame = cv2.cvtColor(Judge.processCameraImg, cv2. COLOR_BGR2RGB)
            shape = Judge._predictor(landmarks_frame, d)

            # nose center idx: 30
            cv2.circle(Judge.processCameraImg, (shape.part(30).x, shape.part(30).y), 5, (255, 0, 0), 3)
            if shape.part(30).x < 320:
                return Judge.LEFT
            elif shape.part(30).x > 360:
                return Judge.RIGHT
            elif shape.part(30).y > 230:
                return Judge.DOWN
            else:
                return Judge.UP

        

    @staticmethod
    def judgeHand(revText):
        Judge.randomRPS()
        rev = Judge.handDetection()
        if(Judge.rps == Judge.SCISSOR):
            if(rev == Judge.SCISSOR):
                revText.setText("Rev:scissor")
                return Judge.DRAW
            elif(rev == Judge.STONE):
                revText.setText("Rev:stone")
                return Judge.WIN
            elif(rev == Judge.PAPER):
                revText.setText("Rev:papper")
                return Judge.LOSE
        elif(Judge.rps == Judge.STONE):
            if(rev == Judge.SCISSOR):
                revText.setText("Rev:scissor")
                return Judge.LOSE
            elif(rev == Judge.STONE):
                revText.setText("Rev:stone")
                return Judge.DRAW
            elif(rev == Judge.PAPER):
                revText.setText("Rev:papper")
                return Judge.WIN
        elif(Judge.rps == Judge.PAPER):
            if(rev == Judge.SCISSOR):
                revText.setText("Rev:scissor")
                return Judge.WIN
            elif(rev == Judge.STONE):
                revText.setText("Rev:stone")
                return Judge.LOSE
            elif(rev == Judge.PAPER):
                revText.setText("Rev:papper")
                return Judge.DRAW 

    @staticmethod
    def judgeHeadWin(revText):
        Judge.randomFaceDir()
        rev = Judge.handDirDetection()

        if(rev == Judge.RIGHT):
            revText.setText("Rev:Hand_Right")
            if(Judge.faceDir == Judge.RIGHT):
                return Judge.WIN
            else:
                return Judge.DRAW
        elif(rev == Judge.LEFT):
            revText.setText("Rev:Hand_Left")
            if(Judge.faceDir == Judge.LEFT):
                return Judge.WIN
            else:
                return Judge.DRAW
        elif(rev == Judge.UP):
            revText.setText("Rev:Hand_Up")
            if(Judge.faceDir == Judge.UP):
                return Judge.WIN
            else:
                return Judge.DRAW
        elif(rev == Judge.DOWN):
            revText.setText("Rev:Hand_Down")
            if(Judge.faceDir == Judge.DOWN):
                return Judge.WIN
            else:
                return Judge.DRAW
    
    @staticmethod
    def judgeHeadLose(revText):
        Judge.randomFinger()
        rev = Judge.headDetection()
        if(rev == Judge.RIGHT):
            revText.setText("Rev:Head_Right")
            if(Judge.fingerDir == Judge.RIGHT):
                return Judge.LOSE
            else:
                return Judge.DRAW
        elif(rev == Judge.LEFT):
            revText.setText("Rev:Head_Left")
            if(Judge.fingerDir == Judge.LEFT):
                return Judge.LOSE
            else:
                return Judge.DRAW
        elif(rev == Judge.UP):
            revText.setText("Rev:Head_Up")
            if(Judge.fingerDir == Judge.UP):
                return Judge.LOSE
            else:
                return Judge.DRAW
        elif(rev == Judge.DOWN):
            revText.setText("Rev:Head_Down")
            if(Judge.fingerDir == Judge.DOWN):
                return Judge.LOSE
            else:
                return Judge.DRAW

    @staticmethod
    def randomFaceDir():
        Dir = (int)(random.random() * 10) % 4
        
        if Dir == 0:
            Judge.faceDir = Judge.UP
        elif Dir == 1:
            Judge.faceDir =  Judge.DOWN
        elif Dir == 2:
            Judge.faceDir = Judge.LEFT
        elif Dir == 3:
            Judge.faceDir = Judge.RIGHT

    @staticmethod
    def randomFinger():
        Dir = (int)(random.random() * 10) % 4
        
        if Dir == 0:
            Judge.fingerDir = Judge.UP
        elif Dir == 1:
            Judge.fingerDir =  Judge.DOWN
        elif Dir == 2:
            Judge.fingerDir = Judge.LEFT
        elif Dir == 3:
            Judge.fingerDir = Judge.RIGHT
        
    @staticmethod
    def randomRPS():
        RPS = (int)(random.random() * 10) % 3
        
        if RPS == 0:
            Judge.rps = Judge.PAPER
        elif RPS == 1:
            Judge.rps = Judge.SCISSOR
        elif RPS == 2:
            Judge.rps = Judge.STONE

    @staticmethod
    def readCamera():
        ret, Judge.cameraImg = Judge._cap.read()
        Judge.processCameraImg = Judge.cameraImg
        Judge.processCameraImg = cv2.flip(Judge.processCameraImg, 1)

    @staticmethod
    def showCamera():
        cv2.rectangle(Judge.processCameraImg, (450, 280), (640, 480), (0, 0, 255), 2)
        cv2.rectangle(Judge.processCameraImg, (250, 100), (420, 270), (0, 0, 255), 2)
        cv2.imshow("frame", Judge.processCameraImg)

    @staticmethod
    def getRPS():
        return Judge.rps
    
    @staticmethod
    def getFingerDir():
        return Judge.fingerDir
    
    @staticmethod
    def getFaceDir():
        return Judge.faceDir
    
    @staticmethod
    def setInit():
        Judge.rps = Judge.INIT
        Judge.faceDir = Judge.INIT
        Judge.fingerDir = Judge.INIT