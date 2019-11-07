import os
import cv2

def make_video(dir_path):
    os.chdir(dir_path)
    video_name = dir_path[9:]
    img_array = []
    files = [file for file in os.listdir()]
    if 'playback.mp4' not in files:
        files.sort(key=lambda x: int(x[5:-4]))
        #collect frames
        for filename in files:
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        #set output
        os.chdir('D:/chaos/videos')    
        out = cv2.VideoWriter(f'{video_name}.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 30, size)
        #write each frame and finish
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
    else: #if video already exists, just move it
        os.rename(f'{dir_path}/playback.mp4', f'D:/chaos/videos/{video_name}.mp4')


if __name__ == '__main__':
    main_dir = 'D:/chaos'
    subdirs = os.listdir(main_dir)
    subdirs.pop(subdirs.index('videos'))
    for frames_directory in subdirs:
        if f'{frames_directory}.mp4' not in os.listdir(f'D:/chaos/videos'):
            make_video(f'D:/chaos/{frames_directory}')
            print(f"\n\n{frames_directory}.mp4 created in video directory.\n")
            break
        else:
            print(f"\n{frames_directory}.mp4 is already in video directory, trying next frames directory")