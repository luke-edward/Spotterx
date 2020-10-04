import numpy as np
import cv2 as cv

white = (255, 255, 255)

lower_red = np.array([0,0,200])
upper_red = np.array([100,255,255])

lower_blue = np.array([200,0,0])
upper_blue = np.array([255,255,100])

window_x = 750
window_y = 600


class Joint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y


def gather_points(frame, lower, upper):
    mask = cv.inRange(frame, lower, upper)

    active = []
    for row in range(0, window_x, 10):
        for col in range(0, window_y, 10):
            if mask[col, row] == 255:
                active.append([row, col])
    return mask, active


def find_joint_average(mask_list):
    average = average_point(mask_list)
    joint = Joint(x=average[0], y=average[1])
    return joint


def average_point(list):
    total_x = 0
    total_y = 0
    count = 0

    for element in list:
        total_x += element[0]
        total_y += element[1]
        count += 1

    if count > 0:
        return [int(total_x/count), int(total_y/count)]
    else:
        return[0,0]


def draw_joint(joint, frame, colour):
    if joint.x != 0 or joint.y != 0:
        cv.circle(frame, (joint.x, joint.y), 10, colour, 2)


cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame. Terminating")
        break

    frame = cv.resize(frame, (window_x, window_y))
    frame = cv.flip(frame, 1)

    mask_blue, mask_list_blue = gather_points(frame, lower_blue, upper_blue)
    joint_blue = find_joint_average(mask_list_blue)
    draw_joint(joint_blue, frame, white)

    mask_red, mask_list_red = gather_points(frame, lower_red, upper_red)
    joint_red = find_joint_average(mask_list_red)
    draw_joint(joint_red, frame, white)

    if (joint_blue.get_pos() != (0,0)) and (joint_red.get_pos() != (0,0)):
        cv.line(frame, joint_blue.get_pos(), joint_red.get_pos(), white, 5)

    if joint_red.get_pos() != (0, 0):
        cv.line(frame, (250,575), joint_red.get_pos(), white, 5)

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
