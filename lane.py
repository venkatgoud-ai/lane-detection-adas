import cv2
import numpy as np


def extrapolate_line(lines, y_bottom, y_top):
    slopes, intercepts = [], []
    for x1, y1, x2, y2 in lines:
        if x2 - x1 == 0:
            continue
        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1
        slopes.append(slope)
        intercepts.append(intercept)
    slope = np.mean(slopes)
    intercept = np.mean(intercepts)
    x_bottom = int((y_bottom - intercept) / slope)
    x_top = int((y_top - intercept) / slope)
    return (x_bottom, y_bottom, x_top, y_top)


cap = cv2.VideoCapture("lane.mp4")

# remember last good lines
last_left = None
last_right = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (1280, 720))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 120, 240)

    # trapezoid mask
    polygon = np.array([[
        (200, 580),
        (480, 320),
        (700, 320),
        (1100, 580)
    ]])
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, polygon, 255)
    masked_edges = cv2.bitwise_and(edges, mask)

    # detect lines
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi/180,
                            threshold=50,
                            minLineLength=40,
                            maxLineGap=5)

    # separate left and right
    left_lines = []
    right_lines = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 - x1 == 0:
                continue
            slope = (y2 - y1) / (x2 - x1)
            if slope < -0.3:
                left_lines.append((x1, y1, x2, y2))
            elif slope > 0.3:
                right_lines.append((x1, y1, x2, y2))

    y_bottom = 580
    y_top = 330

    # update last good lines — or fall back to previous
    if left_lines:
        last_left = extrapolate_line(left_lines,  y_bottom, y_top)
    if right_lines:
        last_right = extrapolate_line(right_lines, y_bottom, y_top)

    # draw using last known good lines
    if last_left and last_right:
        lx1, ly1, lx2, ly2 = last_left
        rx1, ry1, rx2, ry2 = last_right

        lane_polygon = np.array([[
            (lx1, ly1),
            (lx2, ly2),
            (rx2, ry2),
            (rx1, ry1)
        ]])

        overlay = frame.copy()
        cv2.fillPoly(overlay, lane_polygon, (0, 255, 0))
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

        cv2.line(frame, (lx1, ly1), (lx2, ly2), (0, 255, 0), 4)
        cv2.line(frame, (rx1, ry1), (rx2, ry2), (0, 255, 0), 4)

    cv2.imshow("Lane Detection", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
