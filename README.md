# FaceForensics++_Enhanced_Toolkit
## Overview:

This repo is an enhanced toolkit with some updated methods processing original [FaceForensics++ dataset](https://github.com/ondyari/FaceForensics).

> The [FaceForensics++ dataset](https://github.com/ondyari/FaceForensics) is designed for facial manipulation detection, offering real and altered videos using methods like FaceSwap and DeepFakes. It’s widely used to benchmark deepfake detection models.

#### **BUT~**

There exists some awkward problems when you first dive into the field of` Deepfake Detection`, especially `Deepfake binary mask location`, like me🫠🫠

* How to download original dataset **completely** and **uninterruptedly**.
* How to extract frames and  masks form videos which **can be interrupted** and **finally no-repeated**.
* How to convert  extracted masks to **binary** masks

> [!NOTE]
>
> These functions maybe unobtrusive, but they can greatly increase your efficiency and improve your workflow progress!

## Quick Start:

There are 4 files totally.

> [!TIP]
>
> To run them on your own machine, you will need to modify args_config.
1. download dataset script. [download-FaceForensics.py](https://github.com/Gnonymous/FFPP/blob/9b7db2893f81fdf993b95c384197ac1965308911/download-FaceForensics.py)
2. extract frames from videos (no repeat). [extract_frame.py](https://github.com/Gnonymous/FFPP/blob/9b7db2893f81fdf993b95c384197ac1965308911/extract_frame.py)
3. extract binary masks from mask_videos (no repeat). [extract_frame.py](https://github.com/Gnonymous/FFPP/blob/9b7db2893f81fdf993b95c384197ac1965308911/extract_frame.py)
4. convert a mask to binary mask. [generate_binary_mask.py](https://github.com/Gnonymous/FFPP/blob/9b7db2893f81fdf993b95c384197ac1965308911/generate_binary_mask.py)

## Acknowledgement:

Many thanks to the [FaceForensics++](https://github.com/ondyari/FaceForensics) dateset for contributing to the field of Deepfake Detection!

You can get original methods on their official repository [FaceForensics](https://github.com/ondyari/FaceForensics).

