import cv2
import os
import argparse
from tqdm import tqdm

# Parameters
DATASETS = {
    'original_youtube_videos': 'misc/downloaded_youtube_videos.zip',
    'original_youtube_videos_info': 'misc/downloaded_youtube_videos_info.zip',
    'original': 'original_sequences/youtube',
    'DeepFakeDetection_original': 'original_sequences/actors',
    'Deepfakes': 'manipulated_sequences/Deepfakes',
    'DeepFakeDetection': 'manipulated_sequences/DeepFakeDetection',
    'Face2Face': 'manipulated_sequences/Face2Face',
    'FaceShifter': 'manipulated_sequences/FaceShifter',
    'FaceSwap': 'manipulated_sequences/FaceSwap',
    'NeuralTextures': 'manipulated_sequences/NeuralTextures'
    }
ALL_DATASETS = ['Deepfakes', 'NeuralTextures',  'original', 'Face2Face', 'FaceSwap']


def process_image(input_path, output_path):
    # 读取灰度图像
    mask = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    # 将掩码二值化
    _, binary_mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

    # 将操纵区域显示为白色，未操纵区域显示为黑色
    result = cv2.bitwise_not(binary_mask)

    # 保存结果
    cv2.imwrite(output_path, result)

def parse_args():
    parser = argparse.ArgumentParser(description='Convert images to binary masks.')
    parser.add_argument('-p', '--path', default='E:/GYH/FFPP', type=str, help='Input directory containing images.')
    parser.add_argument('-d', '--dataset',type=str,default='all',
                        choices=list(DATASETS.keys())+['all']
                        )
    args = parser.parse_args()
    return args

def main(args):
    # prompt
    print('now generate binary masks!')
    print('***')
    print('Press any key to continue, or CTRL-C to exit.')
    _ = input('')

    # Extract arguments
    c_datasets = [args.dataset] if args.dataset != 'all' else ALL_DATASETS
    path = args.path
    os.makedirs(path, exist_ok=True)



    for dataset in c_datasets:
        mask_inpath = os.path.join(path, DATASETS[dataset], 'masks', 'images')
        mask_outpath = os.path.join(path, DATASETS[dataset], 'masks', 'binary')

        flag = True
        existing_folders_data = []  # 用于记录已处理过的image
        existing_folders_output = []  # 用于记录已存在的binary文件夹
        # 创建输出路径
        os.makedirs(mask_outpath, exist_ok=True)

        # 遍历每个子文件夹
        for subdir in tqdm(os.listdir(mask_inpath)):
            subdir_path = os.path.join(mask_inpath, subdir)
            subdir_outpath = os.path.join(mask_outpath, subdir)

            if os.path.exists(subdir_outpath):
                tqdm.write('WARNING: Skipping image_file' + str(subdir) + ' which has been converted.')
                existing_folders_data.append(str(subdir_path))
                existing_folders_output.append(str(subdir_outpath))
                continue

            if flag:
                flag = False
                if len(existing_folders_data) != 0:
                    tqdm.write('WARNING: extracting the last image file ' + existing_folders_data[-1])
                    for filename in os.listdir(existing_folders_data[-1]):
                        input_image_path = os.path.join(existing_folders_data[-1], filename)
                        output_image_path = os.path.join(existing_folders_output[-1], filename)
                        process_image(input_image_path, output_image_path)
                    tqdm.write('WARNING: now last image file has been processed! Begin process other image file! ')

            # 创建每个子文件夹的输出路径
            os.makedirs(subdir_outpath, exist_ok=True)

            # 处理每个子文件夹中的图片
            tqdm.write('now processing ' + str(subdir))
            for filename in os.listdir(subdir_path):
                input_image_path = os.path.join(subdir_path, filename)
                output_image_path = os.path.join(subdir_outpath, filename)
                process_image(input_image_path, output_image_path)
if __name__ == "__main__":
    args = parse_args()
    main(args)

