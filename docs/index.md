# Prompt2Sign

Welcome to Prompt2Sign!
This repository stores the preprocessed data for the paper:
<br>[SignLLM: Sign Languages Production Large Language Models.](https://arxiv.org/abs/2405.10718)

**Note: The release of our data is tentatively expected at the end of 2024, so don't rush.**

## News

[2024.06.30] The <a href='https://github.com/SignLLM/Prompt2Sign/blob/main/tools/2D_to_3D/run.ipynb'>Jupyer Notebook</a> for data processing has been released.<br>
[2024.05.17] The <a href='https://arxiv.org/abs/2405.10718'>arXiv version</a> of the paper is now available.<br>
[2024.01.16] Prompt2Sign homepage is available and data is expected to be released after accept (maybe at the end of 2024, so don't rush).<br>
[2023.12.14] We have made supplementary materials and demo available at this page.<br>
[2023.11.04] We have made Prompt2Sign and Tools available at GitHub. Check out <a href='https://github.com/SignLLM/Prompt2Sign'>here</a>.<br>

**Prompt2Sign** is first multilingual sign language dataset, which uses tools to automate the acquisition and processing of sign language videos on the web, is an evolving data set that is efficient, lightweight, reducing the previous shortcomings. 
The details of the dataset are available at https://signllm.github.io/Prompt2Sign/.

Current languages include: American Sign Language (ASL), German Sign Language (GSL, Alias DGS), Swiss German Sign Language (DSGS), French Sign Language of Switzerland (LSF-CH), Italian Sign Language of Switzerland (LIS-CH), Argentine Sign Language (Lengua de Señas Argentina, LSA), Korean Sign Language (KSL), and Turkish Sign Language (TSL).

<details>
<summary><b>Dataset Summary</b></summary>

| Name | Language | Vocab. | Duration (h) | Signers | Multiview | Transcription | Gloss | Pose | Depth | Speech | Prompt | Compress |
|------|----------|--------|--------------|----------|-----------|----------------|-------|------|-------|--------|--------|----------|
| Video-Based CSL | CSL | 178 | 100 | 50 | :x: | :heavy_check_mark: | :x: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | :x: |
| SIGNUM | GSL | 450 | 55 | 25 | :x: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | :x: | :x: | :x: |
| RWTH-Phoenix-2014T | GSL | 3k | 11 | 9 | :x: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | :x: | :x: | :x: |
| Public DGS Corpus | GSL | -- | 50 | 327 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | :x: | :x: |
| BSL Corpus | BSL | 5k | -- | 249 | :x: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | :x: | :x: | :x: |
| NCSLGR | ASL | 1.8k | 5.3 | 4 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: | :x: | :x: | :x: |
| How2Sign | ASL | 16k | 79 | 11 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: |
| **Prompt2Sign (ours)** | Multilingual | 40k | 200 | 40 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
 
</details>

[![Star History Chart](https://api.star-history.com/svg?repos=SignLLM/Prompt2Sign&type=Date)](https://star-history.com/#SignLLM/Prompt2Sign&Date)


## How To Cite

Please cite the following paper when using Prompt2Sign in your research:

```
@misc{fang2024signllm,
      title={SignLLM: Sign Languages Production Large Language Models}, 
      author={Sen Fang and Lei Wang and Ce Zheng and Yapeng Tian and Chen Chen},
      year={2024},
      eprint={2405.10718},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}

@misc{fang2023signdiff,
      title={SignDiff: Learning Diffusion Models for American Sign Language Production}, 
      author={Sen Fang and Chunyu Sui and Xuedong Zhang and Yapeng Tian},
      year={2023},
      eprint={2308.16082},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```