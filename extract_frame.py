"""
Extracts images from (compressed) videos, used for the FaceForensics++ dataset

Usage: see -h or https://github.com/ondyari/FaceForensics

Author: Andreas Roessler
Date: 25.01.2019
"""

import os
from os.path import join
import argparse
import subprocess
import cv2
from tqdm import tqdm


DATASET_PATHS = {
    'original': 'original_sequences/youtube',
    'Deepfakes': 'manipulated_sequences/Deepfakes',
    'Face2Face': 'manipulated_sequences/Face2Face',
    'FaceSwap': 'manipulated_sequences/FaceSwap'
}
COMPRESSION = ['raw', 'c23', 'c40','masks']



def extract_frames(data_path, output_path, method='cv2'):
    """Method to extract frames, either with ffmpeg or opencv. FFmpeg won't
    start from 0 so we would have to rename if we want to keep the filenames
    coherent."""
    os.makedirs(output_path, exist_ok=True)
    if method == 'ffmpeg':
        subprocess.check_output(
            'ffmpeg -i {} {}'.format(
                data_path, join(output_path, '%04d.png')),
            shell=True, stderr=subprocess.STDOUT)
    elif method == 'cv2':
        reader = cv2.VideoCapture(data_path)
        frame_num = 0
        while reader.isOpened():
            success, image = reader.read()
            if not success:
                break

            cv2.imwrite(join(output_path, '{:04d}.png'.format(frame_num)),
                        image)
            frame_num += 1
        reader.release()
    else:
        raise Exception('Wrong extract frames method: {}'.format(method))

existing_folders_data = []  # 用于记录已处理过的视频
existing_folders_output = [] #用于记录已存在的image文件夹
def extract_method_videos(data_path, dataset, compression):
    flag = True
    """Extracts all videos of a specified method and compression in the
    FaceForensics++ file structure"""
    videos_path = join(data_path, DATASET_PATHS[dataset], compression, 'videos')
    images_path = join(data_path, DATASET_PATHS[dataset], compression, 'images')
    for video in tqdm(os.listdir(videos_path)):
        image_folder = video.split('.')[0] #去后缀.mp4
        data_path = join(videos_path,video)#源文件路径
        output_folder = join(images_path, image_folder)#输出路径

        # 检查输出文件夹是否已经存在
        if os.path.exists(output_folder):
            # print(f"Skipping video {video} as images are already extracted.")
            tqdm.write('WARNING: Skipping video'+str(video)+' which has been extracted.')
            existing_folders_data.append(data_path)
            existing_folders_output.append(output_folder)
            continue
        #对最后一个文件夹单独处理一次，防止之前停止时未处理完
        if flag:
            flag=False
            if(len(existing_folders_data)!=0):
                # print(f"extracting the last video {existing_folders_data[-1]}")
                tqdm.write('WARNING: extracting the last video ' + existing_folders_data[-1])
                extract_frames(existing_folders_data[-1],existing_folders_output[-1])
                # print(f"now last video has been extracted! Begin process other videos!")
                tqdm.write('WARNING: now last video has been extracted! Begin process other videos! ')

        # 对剩余视频进行处理
        extract_frames(data_path, output_folder)


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    p.add_argument('--data_path','-dp',default='E:/GYH/FFPP', type=str)
    p.add_argument('--dataset', '-d', type=str,
                   choices=list(DATASET_PATHS.keys()) + ['all'],
                   default='all')
    p.add_argument('--compression', '-c', type=str, choices=COMPRESSION,
                   default='c0')
    args = p.parse_args()

    if args.dataset == 'all':
        for dataset in DATASET_PATHS.keys():
            args.dataset = dataset
            extract_method_videos(**vars(args))
    else:
        extract_method_videos(**vars(args))