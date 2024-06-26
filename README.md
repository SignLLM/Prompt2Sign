# Prompt2Sign

[Jupyter Notebook] [AutoDL Docker]

Welcome to Prompt2Sign!
This repository stores the preprocessed data for the paper:
<br>[SignLLM: Sign Languages Production Large Language Models.](https://arxiv.org/abs/2405.10718)

**Note: The release of our data is tentatively expected at the end of 2024, so don't rush.**

## Dataset Introduction

**Prompt2Sign** is first comprehensive multilingual sign language dataset, which uses tools to automate the acquisition and processing of sign language videos on the web, is an evolving data set that is efficient, lightweight, reducing the previous shortcomings. 
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
<!-- 

## Acknowledgements

All data collection and processing are conducted in accordance with the relevant certificates/protocols of the used dataset. For data sets that are public but require a license, we provide processing tools with the permission of the relevant certificate.

**Licensing**

Prompt2Sign is made available under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/). For commercial use, please [contact us](mailto:signllm@googlegroups.com) directly.

![image](https://github.com/SignLLM/Prompt2Sign/assets/147891572/7bc0cb5c-ef77-4a15-87cb-e78cc01c8f76)



We extend our gratitude to the National Sign Language Linguistics Society and XYZ University's Computational Linguistics Department for their support.
Contributions are welcome! Please read our [contribution guidelines](#) to get started.

**Ethics Statement**




Embark on your journey with the Prompt2Sign datasets and tools designed for advancing research in sign language production using large language models.

Follow this guide to get started with our resources:

1. **Familiarize with the Dataset and Tools**  
   Before diving in, take a moment to understand the offerings of Prompt2Sign. Review our resources, toolkits, and data sets tailored for Sign Language Production research.

2. **Accept the Usage Agreement**  
   To access the preprocessed datasets on this page, please accept our terms of use. It is at the end of this article.

3. **Download and Set Up the CLI**  
   Get our Command Line Interface (CLI) tool to interact with the datasets conveniently. This tool is integral for downloading and manipulating the data.

4. **Select Your Data Subset of Interest**  
   Choose the specific dataset or preprocessed subset you need for your research from our repository, whether it’s for diffusion model training or another aspect of sign language production.

5. **Obtain the Data**  
   Once you have your credentials and have selected your subset, use the CLI to download the data. The datasets, especially those preprocessed, are extensive and tailored for deep learning applications.

**Data and Usage Agreement**  
Begin by reviewing our terms at [Prompt2Sign Data Agreement](). Once accepted, you will receive an email with the necessary access credentials within 48 hours. Please note that these credentials are expected to be used for local data download and not for continuous data streaming.

**Browse and Select Datasets**  
Explore our repositories for SignLLM and [SignDiff](https://arxiv.org/abs/2308.16082) to understand the scope and details of the available data.
-->
