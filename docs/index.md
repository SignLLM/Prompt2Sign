# Prompt2Sign

Welcome to Prompt2Sign!
This repository stores the preprocessed data for the paper:
<br>[SignLLM: Sign Languages Production Large Language Models.](https://arxiv.org/abs/2405.10718)

**Note: The release of our data is tentatively expected at the end of 2024, so don't rush.**

## News

[2025.05.24] We have recently developed a tool named <a href='https://github.com/FangSen9000/fast_dwpose'>fast_dwpose</a> for minimizing the extraction and visualization of DW Pose, and we hope it will be helpful to everyone.
[2025.04.18] Surprise: We have released How2Sign <a href='https://huggingface.co/datasets/FangSen9000/How2Sign-dwpose/tree/main'>new compressed data</a> based on <a href='https://github.com/IDEA-Research/DWPose'>DWPose</a>, and an upgraded version of the SignLLM-based application will be launched strongly in the future.<br>
[2025.04.01] **IMPORTANT:** We will try to provide a new compression solution (maybe based DWpose) at some point. Therefore, for unreleased preprocessed data and for existing data processing, the best approach is to download the original dataset and then process it using our processing tools.<br>
[2025.03.31] The prompt template has been updated, more data information has been updated. In the past, I've been wanting to optimize filtering, re-normalize according to body type and improve data quality, this make me have severe procrastination. And later I noticed that DWpose might be a better training method, so unreleased data will not be maintained because our time should spent on better data formats.<br>
[2024.06.30] The <a href='https://github.com/SignLLM/Prompt2Sign/blob/main/tools/2D_to_3D/run.ipynb'>Jupyer Notebook</a> and <a href='https://www.codewithgpu.com/i/SignLLM/Prompt2Sign/Prompt2Sign'>Docker</a> for data processing has been released.<br>
[2024.05.17] The <a href='https://arxiv.org/abs/2405.10718'>arXiv version</a> of the paper is now available.<br>
[2024.01.16] Prompt2Sign homepage is available and data is expected to be released after accept (maybe at the end of 2024, so don't rush).<br>
[2023.12.14] We have made supplementary materials and demo available at this page.<br>
[2023.11.04] We have made Prompt2Sign and Tools available at GitHub. Check out <a href='https://github.com/SignLLM/Prompt2Sign'>here</a>.<br>

## Superset Introduction

**Prompt2Sign** is first comprehensive multilingual sign language superset, which uses tools to automate the acquisition and processing of sign language videos on the web, is an evolving data set that is efficient, lightweight, reducing the previous shortcomings. 
The details of the  are available at https://signllm.github.io/Prompt2Sign/.

Current languages include: American Sign Language (ASL), German Sign Language (GSL, Alias DGS), Swiss German Sign Language (DSGS), French Sign Language of Switzerland (LSF-CH), Italian Sign Language of Switzerland (LIS-CH), Argentine Sign Language (Lengua de Señas Argentina, LSA), Korean Sign Language (KSL), and Turkish Sign Language (TSL).


[![Star History Chart](https://api.star-history.com/svg?repos=SignLLM/Prompt2Sign&type=Date)](https://star-history.com/#SignLLM/Prompt2Sign&Date)


## How To Cite

Please cite the following paper when using Prompt2Sign in your research:

```
@misc{fang2025signllmsignlanguageproduction,
      title={SignLLM: Sign Language Production Large Language Models}, 
      author={Sen Fang and Chen Chen and Lei Wang and Ce Zheng and Chunyu Sui and Yapeng Tian},
      year={2025},
      eprint={2405.10718},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2405.10718}, 
}

@misc{fang2025signdiffdiffusionmodelamerican,
      title={SignDiff: Diffusion Model for American Sign Language Production}, 
      author={Sen Fang and Chunyu Sui and Yanghao Zhou and Xuedong Zhang and Hongbin Zhong and Yapeng Tian and Chen Chen},
      year={2025},
      eprint={2308.16082},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2308.16082}, 
}
```
