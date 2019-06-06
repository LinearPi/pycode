import cv2

cap = cv2.VideoCapture(1)
while (1):
    ret, frame = cap.read()
    # frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    # # dets = detector(frame, 1)
    # if dets:
    #     print("yourenzai")
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
