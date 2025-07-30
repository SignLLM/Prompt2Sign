# Usage

cd `Prompt2Sign/tools-new-2025/main`

## Env

```code
conda env create -f env/environment01_dwpose.yml
conda activate dwpose
pip install -r env/requirements01_dwpose.txt
pip install matplotlib-inline ipython
conda install -n dwpose -c conda-forge ffmpeg -y
```
## Extract

```code
python pipeline00_extract_split_video_to_image.py
python pipeline01_extract_dwpose_from_video.py

# This requires a separate posture folder for each video, and obtaining the corresponding text description. Then, each line should correspond accordingly.
# Since each dataset is different, please handle it by yourself.
python pipeline02_obtain_trg384_data.py

#Later, we realized that fully extending the posture and performing a sequence-to-sequence transformation might not be the optimal solution. Perhaps the third step was not very necessary.
```
