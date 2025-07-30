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
from easy_dwpose import DWposeDetector
from typing import List, Dict, Any, Optional, Tuple

from utils.draw_dw_lib import draw_pose, draw_bodypose, draw_handpose, draw_facepose, process_pose_data




def main():
    dataset_name = "how2sign_train"
    #dataset_name = "test_dataset"
    video_dir = ensure_dir(f"../input/{dataset_name}")
    result_dir = ensure_dir(f"../output/{dataset_name}_results")
    
    # Read processed videos lists
    dwpose_log = f"{result_dir}/processed_video_name_by_dwpose.txt"
    smplerx_log = f"{result_dir}/processed_video_name_by_smplerx.txt"
    
    # Process NPZ files regardless of whether new videos were processed
    print("\nStarting NPZ file processing...")
    
    # 读取已处理的视频列表
    dwpose_processed_file = os.path.join(result_dir, "processed_video_name_by_dwpose.txt")
    output_trg_file_path = f"../output/{dataset_name}.skels"
    
    # 确保输入文件存在
    if not os.path.exists(dwpose_processed_file):
        print(f"Error: Input file {dwpose_processed_file} not found")
        return
        
    # 读取需要处理的视频名称
    with open(dwpose_processed_file, 'r') as f:
        processed_video_names = f.read().splitlines()
    
    print(f"Found {len(processed_video_names)} videos to process NPZ files")
    
    # 处理每个视频的NPZ文件并收集输出
    all_outputs = []
    for video_name in processed_video_names:
        npz_folder_path = os.path.join(result_dir, video_name, "results_dwpose", "npz")
        
        if os.path.exists(npz_folder_path):
            try:
                output = process_npz_files(npz_folder_path, result_dir)
                all_outputs.append(output)
                print(f"Successfully processed NPZ files for {video_name}")
            except Exception as e:
                print(f"Error processing {video_name}: {str(e)}")
                # Add an empty line for failed processing
                all_outputs.append("\n")
        else:
            print(f"NPZ folder not found for video: {video_name}")
            # Add an empty line for missing NPZ folder
            all_outputs.append("\n")
    
    # 将所有输出写入单个文件
    with open(output_trg_file_path, 'w') as f:
        f.writelines(all_outputs)
    
    print(f"\nNPZ processing complete. Output saved to: {output_trg_file_path}")


if __name__ == '__main__':
    main()