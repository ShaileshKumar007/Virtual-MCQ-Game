import cv2
import csv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

# Capturing image and hand tracking
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)


class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns = None

    def update(self, cursor, bboxs):

        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), cv2.FILLED)


# Importing csv file data in our program
pathCSV = "Ques.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]

# Creating Objects for each Question
mcqList = []
for q in dataAll:
    mcqList.append(MCQ(q))

print("Let's start the Quiz!!")
print("Total Number of Questions = ", len(mcqList))

qNo = 0
qTotal = len(dataAll)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if qNo < qTotal:
        mcq = mcqList[qNo]

        img, bbox = cvzone.putTextRect(img, mcq.question, [90, 80], 1, 1, offset=25, border=5)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [90, 150], 1, 1, offset=12, border=2)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [320, 150], 1, 1, offset=12, border=2)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [90, 250], 1, 1, offset=12, border=2)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [320, 250], 1, 1, offset=12, border=2)

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, info = detector.findDistance(lmList[8], lmList[12])

            if length < 35:
                mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                if mcq.userAns is not None:
                    time.sleep(0.5)
                    qNo += 1
    else:
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.userAns:
                score += 1
        score = round((score / qTotal) * 100, 2)
        img, _ = cvzone.putTextRect(img, "You've Completed the Quiz!!", [100, 130], 2, 2, offset=30, border=5)
        img, _ = cvzone.putTextRect(img, f'You Scored {score}%', [150, 240], 2, 2, offset=30, border=5)

    # Code for making Progress bar
    barValue = 150 + (350 // qTotal) * qNo
    cv2.rectangle(img, (150, 400), (barValue, 350), (255, 69, 0), cv2.FILLED)
    cv2.rectangle(img, (150, 400), (500, 350), (0, 0, 255), 2)
    img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [520, 390], 2, 2, offset=5)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

    #color code is BGR
