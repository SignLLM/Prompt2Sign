import os
import shutil
import subprocess
import av
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel
from utils.util import get_fps, read_frames, save_videos_from_pil
from utils.preprocess_video import *
from PIL import Image
import numpy as np
import json

def ensure_dir(directory):
    if os.path.exists(directory):
        print(f"Directory already exists: {directory}")
    else:
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    return directory

# [previous helper functions remain the same]
def get_video_dimensions(video_path):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    width, height = map(int, result.stdout.strip().split(','))
    return width, height

def compile_frames_to_video(frame_dir, output_path, fps=30):
    """Compile frames into a video using H.264 codec."""
    cmd = [
        'ffmpeg', '-y',
        '-f', 'image2',
        '-r', str(fps),
        '-i', f'{frame_dir}/%08d.jpg',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Successfully compiled video: {output_path}")

def preprocess_videos(video_dir, dataset_name, square_crop=False, fps=24, quality_preset="medium", target_resolution=None):
    """
    Preprocess all videos with optional square cropping, customizable FPS, quality, and resolution.
    
    Args:
        video_dir (str): Directory containing input videos
        dataset_name (str): Name of the dataset
        square_crop (bool): Whether to crop videos to 1:1 aspect ratio (default: True)
        fps (int): Target frames per second (default: 30)
        quality_preset (str): Quality preset - "high", "medium", "low", "ultra_low" (default: "medium")
        target_resolution (int): Target resolution for the shorter side (e.g., 512, 256). None for original
    """
    result_dir = ensure_dir(f"../output/{dataset_name}_results")

    # 质量设置
    quality_settings = {
        "high": {"qscale": "2", "crf": "18"},      # 高质量
        "medium": {"qscale": "5", "crf": "23"},    # 中等质量
        "low": {"qscale": "10", "crf": "28"},      # 低质量
        "ultra_low": {"qscale": "15", "crf": "35"} # 超低质量
    }
    
    current_quality = quality_settings.get(quality_preset, quality_settings["medium"])

    for video_file in os.listdir(video_dir):
        if not video_file.endswith(".mp4"):
            continue

        video_name = os.path.splitext(video_file)[0]
        video_full_path = os.path.join(video_dir, video_file)
        folder_path = f"{result_dir}/{video_name}"
        
        frame_path = f"{folder_path}/crop_frame"
        output_video_path = f"{folder_path}/crop_original_video.mp4"

        # Skip if already processed
        if os.path.exists(frame_path) and os.listdir(frame_path) and os.path.exists(output_video_path):
            crop_status = "cropped" if square_crop else "original"
            print(f"{crop_status.capitalize()} frames and video already exist for {video_name}. Skipping preprocessing.")
            continue

        try:
            # Create output directory
            os.makedirs(frame_path, exist_ok=True)

            # Get video dimensions
            width, height = get_video_dimensions(video_full_path)
            
            # 构建视频滤镜
            filters = []
            
            if square_crop:
                # Calculate crop dimensions
                if width < height:
                    crop_size = width
                    x_offset = 0
                    y_offset = (height - width) // 2
                else:
                    crop_size = height
                    x_offset = (width - height) // 2
                    y_offset = 0
                filters.append(f'crop={crop_size}:{crop_size}:{x_offset}:{y_offset}')
            
            # 添加分辨率缩放
            if target_resolution:
                if square_crop:
                    # 方形裁剪后直接缩放到目标分辨率
                    filters.append(f'scale={target_resolution}:{target_resolution}')
                else:
                    # 保持宽高比缩放
                    filters.append(f'scale=-2:{target_resolution}:force_original_aspect_ratio=decrease')
            
            # 添加帧率
            filters.append(f'fps={fps}/1')
            
            # 组合所有滤镜
            filter_complex = ','.join(filters)

            # 提取帧的命令
            cmd = [
                'ffmpeg', '-i', video_full_path,
                '-vf', filter_complex,
                '-f', 'image2',
                '-qscale', current_quality["qscale"],  # 使用可调节的质量
                f'{frame_path}/%08d.jpg'
            ]
            
            resolution_info = f" (Resolution: {target_resolution})" if target_resolution else ""
            crop_info = "with square cropping" if square_crop else "without cropping"
            print(f"Processing {video_file} {crop_info} (FPS: {fps}, Quality: {quality_preset}{resolution_info})")

            subprocess.run(cmd, check=True)
            print(f"Successfully extracted frames for {video_file}")

            # Compile frames back into a video with optimized settings
            compile_frames_to_video_optimized(frame_path, output_video_path, fps, quality_preset)

        except Exception as e:
            print(f"Error preprocessing {video_file}: {str(e)}")
            continue

def compile_frames_to_video_optimized(frame_dir, output_path, fps=30, quality_preset="medium"):
    """Compile frames into a video with optimized quality settings."""
    
    # 质量设置 - CRF值（越高质量越低，文件越小）
    quality_crf = {
        "high": "18",
        "medium": "23", 
        "low": "28",
        "ultra_low": "35"
    }
    
    crf_value = quality_crf.get(quality_preset, "23")
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'image2',
        '-r', str(fps),
        '-i', f'{frame_dir}/%08d.jpg',
        '-c:v', 'libx264',
        '-preset', 'medium',  # 可以改为 'fast' 加速编码
        '-crf', crf_value,
        '-pix_fmt', 'yuv420p',
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Successfully compiled optimized video: {output_path} (Quality: {quality_preset})")

# 使用示例：

# 1. 保持原分辨率，降低质量
# preprocess_videos(video_dir, dataset_name, square_crop=True, fps=30, quality_preset="low")

# 2. 降低分辨率到512x512（方形裁剪）
# preprocess_videos(video_dir, dataset_name, square_crop=True, fps=30, quality_preset="medium", target_resolution=512)

# 3. 极度压缩：低分辨率 + 超低质量
# preprocess_videos(video_dir, dataset_name, square_crop=True, fps=30, quality_preset="ultra_low", target_resolution=256)

# 4. 不裁剪，但缩放到较小尺寸
# preprocess_videos(video_dir, dataset_name, square_crop=False, fps=30, quality_preset="low", target_resolution=480)

def process_npz_files(input_folder_path, output_folder_path):
    """
    Process all NPZ files in the specified folder and generate the required output format.
    
    Args:
        input_folder_path (str): Path to the folder containing NPZ files
        output_folder_path (str): Path where output files will be saved
    """
    # Get all NPZ files in the folder
    npz_files = sorted([f for f in os.listdir(input_folder_path) if f.endswith('.npz')])
    total_frames = len(npz_files)
    
    output = []
    
    for idx, npz_file in enumerate(npz_files):
        file_path = os.path.join(input_folder_path, npz_file)
        data = np.load(file_path, allow_pickle=True)
        
        # Process bodies data
        bodies = data['bodies']
        body_scores = data['body_scores'][0]
        
        # Process hands data
        hands = data['hands']
        hands_scores = data['hands_scores']
        
        # Process faces data
        faces = data['faces'][0]
        faces_scores = data['faces_scores'][0]
        
        # Convert coordinates to strings with space separation
        frame_data = []
        
        # Add body coordinates and scores
        for i in range(bodies.shape[0]):
            frame_data.extend([f"{bodies[i][0]:.8f}", f"{bodies[i][1]:.8f}"])
        for score in body_scores:
            frame_data.append(f"{score:.8f}")
            
        # Add hand coordinates and scores
        for hand in hands:
            for point in hand:
                frame_data.extend([f"{point[0]:.8f}", f"{point[1]:.8f}"])
        for hand_score in hands_scores:
            frame_data.extend([f"{score:.8f}" for score in hand_score])
            
        # Add face coordinates and scores
        for point in faces:
            frame_data.extend([f"{point[0]:.8f}", f"{point[1]:.8f}"])
        for score in faces_scores:
            frame_data.append(f"{score:.8f}")
            
        # Add frame count
        frame_count = idx / (total_frames - 1) if total_frames > 1 else 0
        frame_data.append(f"{frame_count:.8f}")
        
        # 验证这一帧的数据点数是否为385
        if len(frame_data) != 385:
            print(f"Warning: Frame {idx} in {input_folder_path} has {len(frame_data)} values instead of 385")
            continue  # 跳过这一帧

        # Join all data with spaces
        output.append(" ".join(frame_data))
    
    return " ".join(output) + "\n"