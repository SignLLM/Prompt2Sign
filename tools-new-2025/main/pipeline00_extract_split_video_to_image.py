import os
import sys
import subprocess
from utils.preprocess_video import preprocess_videos, ensure_dir


def main(dataset_name="test_dataset", square_crop=False, target_fps=1, quality_preset="medium", target_resolution=None):
    """
    Enhanced video preprocessing script - supports quality and resolution control
    
    Args:
        dataset_name (str): Dataset name
        square_crop (bool): Whether to perform square cropping
        target_fps (int): Target frame rate
        quality_preset (str): Quality preset - "high", "medium", "low", "ultra_low"
        target_resolution (int): Target resolution (pixels), None to keep original resolution
    """
    # Configure dataset name options
    dataset_name = "test_dataset"
    # dataset_name = "ASLLRP"
    # dataset_name = "how2sign_test"
    # dataset_name = "ncslgr_mp4"
    # dataset_name = "ncslgr_mp4_small"
    # dataset_name = "ASLLRP_batch_full_video_v1_1_small"
    # dataset_name = "ASLLRP_utterances_small"
    #dataset_name = "OpenVidHD-camera"  # New large dataset
    
    # === Configure processing parameters ===
    square_crop = False      # Whether to perform square cropping, False to keep original aspect ratio
    target_fps = 24          # Target frame rate (recommended: 1-30)
    quality_preset = "medium" # Quality preset: "high", "medium", "low", "ultra_low"
    target_resolution = None  # Target resolution (pixels), e.g.: 512, 256, None for original resolution
    
    # === Common configuration combination examples ===
    
    # 1. High quality processing (suitable for small datasets)
    # quality_preset = "high"
    # target_resolution = None  # Keep original resolution
    
    # 2. Balance quality and space (recommended)
    # quality_preset = "medium"
    # target_resolution = 512
    
    # 3. Save space (suitable for large datasets)
    # quality_preset = "low" 
    # target_resolution = 384
    
    # 3.5 Maximum compression (suitable for very large datasets or limited storage)
    #quality_preset = "low"
    #target_resolution = 256

    # 4. Maximum compression (suitable for very large datasets or limited storage)
    # quality_preset = "ultra_low"
    # target_resolution = 256
    
    # 5. Special purpose: extremely low frame rate + small resolution (for rapid prototype testing)
    # target_fps = 1
    # quality_preset = "low"
    # target_resolution = 224
    
    # Set input and output directories
    video_dir = ensure_dir(f"../input/{dataset_name}")
    result_dir = ensure_dir(f"../output/{dataset_name}_results")
    
    # Display configuration information
    crop_status = "Square cropping" if square_crop else "Keep original aspect ratio"
    resolution_info = f"{target_resolution}px" if target_resolution else "Original resolution"
    
    print("=" * 60)
    print("Enhanced Video Preprocessing")
    print("=" * 60)
    print(f"Dataset name: {dataset_name}")
    print(f"Input directory: {video_dir}")
    print(f"Output directory: {result_dir}")
    print(f"Processing mode: {crop_status}")
    print(f"Target frame rate: {target_fps} FPS")
    print(f"Quality preset: {quality_preset}")
    print(f"Target resolution: {resolution_info}")
    
    # Estimate compression effect
    compression_estimates = {
        ("high", None): "File size approximately 80-100% of original",
        ("medium", None): "File size approximately 40-60% of original", 
        ("low", None): "File size approximately 20-40% of original",
        ("ultra_low", None): "File size approximately 10-20% of original",
        ("medium", 512): "File size approximately 15-25% of original",
        ("low", 384): "File size approximately 8-15% of original",
        ("ultra_low", 256): "File size approximately 3-8% of original"
    }
    
    estimate_key = (quality_preset, target_resolution)
    if estimate_key in compression_estimates:
        print(f"Estimated effect: {compression_estimates[estimate_key]}")
    else:
        print("Estimated effect: Custom compression based on settings")
    
    print("=" * 60)
    
    # Execute video preprocessing
    try:
        preprocess_videos(
            video_dir=video_dir, 
            dataset_name=dataset_name, 
            square_crop=square_crop, 
            fps=target_fps,
            quality_preset=quality_preset,
            target_resolution=target_resolution
        )
        print("\n" + "=" * 60)
        print("Video preprocessing completed!")
        
        # Statistics of processing results
        processed_count = 0
        total_size = 0
        
        for video_file in os.listdir(video_dir):
            if video_file.endswith(".mp4"):
                video_name = os.path.splitext(video_file)[0]
                output_video_path = os.path.join(result_dir, video_name, "crop_original_video.mp4")
                
                if os.path.exists(output_video_path):
                    processed_count += 1
                    total_size += os.path.getsize(output_video_path)
        
        total_size_gb = total_size / (1024**3)
        
        print(f"Successfully processed {processed_count} videos")
        print(f"Total output video size: {total_size_gb:.2f} GB")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error occurred during preprocessing: {str(e)}")


def print_usage():
    """Print usage instructions"""
    print("""
Usage:
1. Basic usage (with default parameters):
   python script.py

2. Specify dataset:
   python script.py dataset_name

3. Full parameters:
   python script.py dataset_name square_crop fps quality_preset resolution

Parameter descriptions:
- dataset_name: Dataset name (e.g.: "test_dataset")
- square_crop: true/false (whether to perform square cropping)
- fps: Frame rate (e.g.: 30, 15, 1)
- quality_preset: high/medium/low/ultra_low (quality preset)
- resolution: Target resolution in pixels (e.g.: 512, 256, or none to keep original resolution)

Examples:
python script.py OpenVidHD false 1 low 384
python script.py test_dataset true 30 medium 512
python script.py my_dataset false 15 ultra_low 256

Recommended configurations:
- Small datasets: medium quality + original resolution
- Large datasets: low quality + 512 resolution  
- Very large datasets: ultra_low quality + 256 resolution
""")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            print_usage()
            sys.exit(0)
            
        dataset_name = sys.argv[1]
        square_crop = sys.argv[2].lower() == 'true' if len(sys.argv) > 2 else False
        target_fps = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        quality_preset = sys.argv[4] if len(sys.argv) > 4 else "medium"
        
        # Handle resolution parameter
        if len(sys.argv) > 5:
            resolution_str = sys.argv[5].lower()
            target_resolution = None if resolution_str in ['none', 'null', 'original'] else int(resolution_str)
        else:
            target_resolution = None
            
        main(dataset_name, square_crop, target_fps, quality_preset, target_resolution)
    else:
        main()