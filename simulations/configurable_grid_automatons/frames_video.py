import os
import cv2

def make_video(dir_path):
    os.chdir(dir_path)
    img_array = []
    files = [file for file in os.listdir()]
    files.sort(key=lambda x: int(x[5:-4]))
    for filename in files:
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    
    out = cv2.VideoWriter('playback.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 20, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

if __name__ == '__main__':
    main_dir = 'D:/chaos'
    subdirs = os.listdir(main_dir)

    for frames_directory in subdirs:
        if 'playback.mp4' not in os.listdir(f'D:/chaos/{frames_directory}'):
            make_video(f'D:/chaos/{frames_directory}')
            print(f"\n\nVideo created in {frames_directory}.\n")
            break
        else:
            print(f"\nVideo is already in {frames_directory}, trying next")