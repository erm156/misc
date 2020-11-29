import os
import time

import cv2


def stream_video(source=0):
    stream = cv2.VideoCapture(source)

    while True:
        frame = stream.read()[1]               
        corners = get_subframe_corners(frame)
        filtered_frame = filter_subframes(frame, corners)

        if cv2.waitKey(1) & 0xFF == ord("c"):
            take_screenshot(filtered_frame)
        elif cv2.waitKey(1) & 0xFF == ord("q"):
            stop_video(stream)
            break
        else:
            cv2.imshow("video palette", filtered_frame)


def get_subframe_corners(frame):
    frame_height = frame.shape[0]
    frame_width = frame.shape[1]

    top_ul = (0, 0)
    top_br = (int(frame_width / 2), int(frame_height / 2))

    btm_ul = (0, int(frame_height / 2))
    btm_br = (int(frame_width / 2), frame_height)

    side_ul = (int(frame_width / 2), int(frame_height / 2))
    side_br = (frame_width, frame_height)

    return (top_ul, top_br, btm_ul, btm_br, side_ul, side_br)


def filter_subframes(frame, corners):
    subframe1 = frame[corners[0][1]:corners[1][1], corners[0][0]:corners[1][0]]
    subframe2 = frame[corners[2][1]:corners[3][1], corners[2][0]:corners[3][0]]
    subframe3 = frame[corners[4][1]:corners[5][1], corners[4][0]:corners[5][0]]

    sf1_filter = edge_detection(subframe1)
    sf2_filter = cv2.threshold(edge_detection(subframe2), 20, 255, cv2.THRESH_BINARY_INV)[1]
    sf3_filter = cv2.cvtColor(subframe3, cv2.COLOR_BGR2HSV)

    # 'insert' filtered subframes back into main/composite frame
    frame[corners[0][1]:corners[1][1], corners[0][0]:corners[1][0]] = cv2.cvtColor(sf1_filter, cv2.COLOR_GRAY2RGB)
    frame[corners[2][1]:corners[3][1], corners[2][0]:corners[3][0]] = cv2.cvtColor(sf2_filter, cv2.COLOR_GRAY2RGB)
    frame[corners[4][1]:corners[5][1], corners[4][0]:corners[5][0]] = sf3_filter

    return frame


def edge_detection(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray_frame, (7,7), 0)

    edges = cv2.Canny(gray_blur, 20, 150)
    return edges


def take_screenshot(frame):
    desktop = os.path.expanduser('~/Desktop/')
    local_time = time.asctime(time.localtime())
    filename = local_time.replace(" ", "_").replace(":", "")
    
    cv2.imwrite(desktop + filename + ".jpg", frame)
    print("\nFrame captured!\n")


def stop_video(stream):
    stream.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    stream_video()
