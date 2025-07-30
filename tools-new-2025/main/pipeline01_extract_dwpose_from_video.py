import os
import subprocess
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import numpy as np
import json
from easy_dwpose import DWposeDetector
from PIL import Image
from utils.util import read_frames
from utils.draw_dw_lib import draw_pose, process_pose_data

# Set distributed training environment variables
os.environ["NCCL_DEBUG"] = "INFO"
os.environ["NCCL_IB_DISABLE"] = "1"
os.environ["NCCL_P2P_DISABLE"] = "1"

def setup(rank, world_size):
    """Setup distributed training environment"""
    try:
        os.environ['MASTER_ADDR'] = '127.0.0.1'
        os.environ['MASTER_PORT'] = '23457'  # Use different port to avoid conflicts
        dist.init_process_group(
            "gloo",
            rank=rank, 
            world_size=world_size
        )
        return True
    except Exception as e:
        print(f"Failed to initialize process group: {str(e)}")
        return False

def cleanup():
    """Clean up distributed training environment"""
    dist.destroy_process_group()

def save_dwpose_data(pose_data, frame_idx, json_dir, npy_dir, npz_dir, img_dir, frame_pil, detector):
    """Save DWpose data to various formats - completely use new data structure"""
    try:
        frame_name = f"{frame_idx:08d}"
        
        # Detect number of persons
        num_persons = pose_data['faces'].shape[0] if 'faces' in pose_data else 0
        
        # Completely use new data structure
        new_pose_data = {
            'num_persons': num_persons
        }
        
        if num_persons > 0:
            # Reorganize body keypoint data
            bodies_reshaped = pose_data['bodies'].reshape(num_persons, 18, 2)
            
            # Add separate data for each person
            for person_id in range(num_persons):
                new_pose_data[f'person_{person_id}'] = {
                    'body_keypoints': bodies_reshaped[person_id],
                    'body_scores': pose_data['body_scores'][person_id],
                    'face_keypoints': pose_data['faces'][person_id],
                    'face_scores': pose_data['faces_scores'][person_id],
                    'left_hand_keypoints': pose_data['hands'][person_id * 2],
                    'left_hand_scores': pose_data['hands_scores'][person_id * 2],
                    'right_hand_keypoints': pose_data['hands'][person_id * 2 + 1],
                    'right_hand_scores': pose_data['hands_scores'][person_id * 2 + 1],
                }
        
        # Save NPY file - only save new format
        try:
            np.save(os.path.join(npy_dir, f"{frame_name}.npy"), new_pose_data)
        except Exception as e:
            print(f"Failed to save NPY file (frame {frame_idx}): {str(e)}")
        
        # Save NPZ file - only save new format
        try:
            np.savez(os.path.join(npz_dir, f"{frame_name}.npz"), **new_pose_data)
        except Exception as e:
            print(f"Failed to save NPZ file (frame {frame_idx}): {str(e)}")
        
        # Save visualization image
        try:
            # Use new visualization method
            try:
                width, height = frame_pil.size
                processed_pred = process_pose_data(new_pose_data, height, width)
                
                vis_img = draw_pose(
                    pose=processed_pred,
                    H=height,
                    W=width,
                    include_body=True,
                    include_hand=True,
                    include_face=True
                )
                
                # Handle channel order
                if isinstance(vis_img, np.ndarray):
                    if vis_img.shape[0] == 3 and len(vis_img.shape) == 3:
                        vis_img = np.transpose(vis_img, (1, 2, 0))
                    
                    if vis_img.dtype != np.uint8:
                        vis_img = (vis_img * 255).astype(np.uint8)
                    
                    pred_img = Image.fromarray(vis_img)
                else:
                    raise ValueError(f"draw_pose returned invalid type: {type(vis_img)}")
                    
            except Exception as viz_error:
                print(f"Warning: New visualization method failed ({str(viz_error)}), using original method")
                pred_img = detector(frame_pil, output_type="pil", include_hands=True, include_face=True)
            
            pred_img.save(os.path.join(img_dir, f"{frame_name}.jpg"))
            
        except Exception as e:
            print(f"Failed to save pose visualization image (frame {frame_idx}): {str(e)}")

        # Create overlay visualization image
        try:
            overlay_dir = os.path.join(os.path.dirname(os.path.dirname(img_dir)), "dwpose_overlay_img")
            os.makedirs(overlay_dir, exist_ok=True)

            processed_pred = process_pose_data(new_pose_data, height, width)
            transparent_vis = draw_pose(
                pose=processed_pred,
                H=height,
                W=width,
                include_body=True,
                include_hand=True,
                include_face=True,
                transparent=True
            )

            if isinstance(transparent_vis, np.ndarray):
                if transparent_vis.shape[0] == 4 and len(transparent_vis.shape) == 3:
                    transparent_vis = np.transpose(transparent_vis, (1, 2, 0))
                transparent_img = Image.fromarray(transparent_vis, 'RGBA')
            
            frame_rgba = frame_pil.convert('RGBA')
            overlay_img = Image.alpha_composite(frame_rgba, transparent_img)
            
            overlay_path = os.path.join(overlay_dir, f"{frame_name}.png")
            overlay_img.save(overlay_path)

        except Exception as e:
            print(f"Failed to create overlay visualization (frame {frame_idx}): {str(e)}")

        # Save JSON file - only save new format
        try:
            pose_data_json = {}
            for k, v in new_pose_data.items():
                if isinstance(v, np.ndarray):
                    pose_data_json[k] = v.tolist()
                elif isinstance(v, (np.int32, np.int64)):
                    pose_data_json[k] = int(v)
                elif isinstance(v, (np.float32, np.float64)):
                    pose_data_json[k] = float(v)
                elif isinstance(v, dict):
                    # Handle person_id dictionary
                    person_dict = {}
                    for pk, pv in v.items():
                        if isinstance(pv, np.ndarray):
                            person_dict[pk] = pv.tolist()
                        else:
                            person_dict[pk] = pv
                    pose_data_json[k] = person_dict
                else:
                    pose_data_json[k] = v
            
            json_path = os.path.join(json_dir, f"{frame_name}.json")
            with open(json_path, 'w') as f:
                json.dump(pose_data_json, f)
                
        except Exception as e:
            print(f"Failed to save JSON file (frame {frame_idx}): {str(e)}")
            
    except Exception as e:
        print(f"General error in save_dwpose_data (frame {frame_idx}): {str(e)}")

def process_video_with_dwpose(rank, video_path, output_base_dir, fps):
    """Process single video using specified GPU"""
    json_dir = os.path.join(output_base_dir, "json")
    npy_dir = os.path.join(output_base_dir, "npy")
    npz_dir = os.path.join(output_base_dir, "npz")
    img_dir = os.path.join(output_base_dir, "img")
    
    os.makedirs(json_dir, exist_ok=True)
    os.makedirs(npy_dir, exist_ok=True)
    os.makedirs(npz_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    print(f"GPU {rank}: DWpose - Output directories created")

    device = f"cuda:{rank}"
    detector = DWposeDetector(device=device)
    print(f"GPU {rank}: DWpose - Detector initialized on {device}")

    frames = read_frames(video_path)
    total_frames = len(frames)
    print(f"GPU {rank}: DWpose - Read {total_frames} frames from video")

    for i, frame_pil in enumerate(frames):
        pose_data = detector(frame_pil, draw_pose=False, include_hands=True, include_face=True)
        save_dwpose_data(pose_data, i + 1, json_dir, npy_dir, npz_dir, img_dir, frame_pil, detector)

        if (i + 1) % 50 == 0 or i == 0 or i == total_frames - 1:
            print(f"GPU {rank}: DWpose - Processed {i + 1}/{total_frames} frames ({(i + 1)/total_frames*100:.1f}%)")

    # Generate visualization video
    visualization_path = os.path.join(os.path.dirname(output_base_dir), "visualization_dwpose.mp4")
    print(f"GPU {rank}: DWpose - Creating visualization video...")
    try:
        cmd = f'ffmpeg -y -framerate {fps} -i {img_dir}/%08d.jpg -c:v libx264 -pix_fmt yuv420p {visualization_path}'
        subprocess.run(cmd, shell=True, check=True)
        print(f"GPU {rank}: DWpose - Successfully created visualization video: {visualization_path}")
    except Exception as e:
        print(f"GPU {rank}: DWpose - Failed to create visualization video: {str(e)}")

    # Generate overlay visualization video
    overlay_dir = os.path.join(os.path.dirname(output_base_dir), "dwpose_overlay_img")
    visualization_overlap_path = os.path.join(os.path.dirname(output_base_dir), "visualization_dwpose_overlap.mp4")
    print(f"GPU {rank}: DWpose - Creating overlay visualization video...")
    try:
        cmd = f'ffmpeg -y -framerate {fps} -i {overlay_dir}/%08d.png -c:v libx264 -pix_fmt yuv420p {visualization_overlap_path}'
        subprocess.run(cmd, shell=True, check=True)
        print(f"GPU {rank}: DWpose - Successfully created overlay visualization video: {visualization_overlap_path}")
    except Exception as e:
        print(f"GPU {rank}: DWpose - Failed to create overlay visualization video: {str(e)}")

def process_videos_distributed(rank, world_size, video_paths, dataset_name, fps):
    """Process videos in distributed manner"""
    if not setup(rank, world_size):
        return
        
    result_dir = f"../output/{dataset_name}_results"
    
    for i, (video_name, video_path) in enumerate(video_paths):
        if i % world_size == rank:
            print(f"GPU {rank} processing video: {video_name}")
            
            try:
                folder_path = f"{result_dir}/{video_name}"
                dwpose_results_dir = f"{folder_path}/results_dwpose"
                
                if not os.path.exists(os.path.join(dwpose_results_dir, "json")):
                    os.makedirs(dwpose_results_dir, exist_ok=True)
                    print(f"GPU {rank}: Created directory {dwpose_results_dir}")
                    process_video_with_dwpose(rank, video_path, dwpose_results_dir, fps)
                    print(f"GPU {rank}: Completed DWpose processing for {video_name}")
                    
                    with open(f"{result_dir}/processed_video_name_by_dwpose.txt", "a") as f:
                        f.write(f"{video_name}\n")
                else:
                    print(f"GPU {rank}: {video_name} already processed, skipping")
                            
            except Exception as e:
                print(f"GPU {rank}: Error processing video {video_name}: {str(e)}")
                continue

    cleanup()

def main():
    """Main function"""
    # Configure dataset name
    dataset_name = "test_dataset"
    # dataset_name = "how2sign_test"
    # dataset_name = "ncslgr_mp4"
    # dataset_name = "ncslgr_mp4_small"
    # dataset_name = "ASLLRP_batch_full_video_v1_1_small"
    # dataset_name = "ASLLRP_utterances_small"
    
    result_dir = f"../output/{dataset_name}_results"

    fps = 24

    # Collect videos to be processed
    video_paths = []
    processed_dwpose = set()
    
    # Read list of already processed videos
    dwpose_log = f"{result_dir}/processed_video_name_by_dwpose.txt"
    
    if os.path.exists(dwpose_log):
        with open(dwpose_log, 'r') as f:
            processed_dwpose = set(f.read().splitlines())

    # Check videos that need DWpose processing
    video_dir = f"../input/{dataset_name}"
    for video_file in os.listdir(video_dir):
        if video_file.endswith(".mp4"):
            video_name = os.path.splitext(video_file)[0]
            crop_video_path = os.path.join(result_dir, video_name, "crop_original_video.mp4")
            
            if os.path.exists(crop_video_path) and video_name not in processed_dwpose:
                video_paths.append((video_name, crop_video_path))
                print(f"Added video for DWpose processing: {video_name}")

    # Run DWpose processing
    if video_paths:
        print(f"Found {len(video_paths)} videos that need DWpose processing")
        
        world_size = torch.cuda.device_count()
        if world_size > 1:
            print(f"Found {world_size} GPUs, running distributed processing")
            mp.spawn(
                process_videos_distributed,
                args=(world_size, video_paths, dataset_name, fps),
                nprocs=world_size,
                join=True
            )
        else:
            print("Only one GPU available, running single GPU mode")
            process_videos_distributed(0, 1, video_paths, dataset_name, fps)
    else:
        print("All videos have already been processed with DWpose")

if __name__ == '__main__':
    main()