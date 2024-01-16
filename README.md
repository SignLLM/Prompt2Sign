# Prompt2Sign

Welcome to Prompt2Sign!
This section stores the preprocessed data for the paper:
<br>[SignLLM: Sign Languages Production Large Language Models.]()

## Quick Start

**Download the CLI**  
Install the Prompt2Sign CLI using pip (ensure you have it in your Python environment):

```python
pip install prompt2sign-cli
```

Alternatively, follow the repository's guide to download the necessary tools and utilities: [Prompt2Sign CLI Tools](https://github.com/Prompt2Sign/cli-tools-link)

**Choose Your Subset**  
Whether you are interested in for ASL part or GSL part, our CLI makes it easy to specify and download just what you need without having to obtain the entirety of the large datasets.

```bash
prompt2sign --output_directory="~/prompt2sign_data" --datasets ASL_part GSL_part
```

Note: Download failed, please use the following Google hard drive/other network drive.

## Download Data

**Prompt2Sign ASL part for ASLP**

V1 News: After preprocessing [How2Sign](https://how2sign.github.io/) dataset, the condensed data set obtained is as follows:

- [https://drive.google.com/file/d/185RwUfBTJuUEibvAoABPe_aq39hsRjF-/view?usp=sharing](https://drive.google.com/file/d/185RwUfBTJuUEibvAoABPe_aq39hsRjF-/view?usp=sharing)

V2 News: Added the [OpenASL](https://github.com/chevalierNoir/OpenASL) dataset, the condensed data set obtained is as follows:

- [Coming soon]()

It can be used in the training of ASL production models. 

**Prompt2Sign GSL part for GSLP**

After preprocessing [Phoenix-14T](https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX-2014-T/) dataset, the condensed data set obtained is as follows:

- [https://drive.google.com/file/d/17qiIoJG7KyhfhDz9rOlYF4vDkcr2jmBd/view?usp=sharing](https://drive.google.com/file/d/17qiIoJG7KyhfhDz9rOlYF4vDkcr2jmBd/view?usp=sharing)

It can be used in the training of GSL production models.

## More Processed-Data

This unit includes some useful data sets for sign language preprocessing:

**How2Sign for SignDiff<sup>2</sup>**

After preprocessing [How2Sign](https://how2sign.github.io/) dataset, the condensed data set obtained is as follows:

- [https://drive.google.com/file/d/1DHmePcRpc5TJ1XkjOfA8VYKKLGCL8nlJ/view?usp=sharing](https://drive.google.com/file/d/1DHmePcRpc5TJ1XkjOfA8VYKKLGCL8nlJ/view?usp=sharing)

It can be used for the diffusion model training of pose2video in sign language. (Based on [ControlNet](https://github.com/lllyasviel/ControlNet/blob/main/docs/train.md))

**How2Sign for Vid2Vid**

After preprocessing [How2Sign](https://how2sign.github.io/) dataset, the condensed data set obtained is as follows:

- [https://aistudio.baidu.com/datasetdetail/220064](https://aistudio.baidu.com/datasetdetail/220064)

It can be used for the diffusion model training of pose2video in sign language. (Based on [Vid2Vid](https://github.com/NVIDIA/vid2vid))

## Tool for Data

Our pre-processing tools: the data Cleansing tool and the three-step 2Dto3D tool.

- [https://github.com/SignLLM/Tools/Clean](https://github.com/SignLLM/Prompt2Sign/Clean)

- [https://github.com/SignLLM/Tools/2Dto3D](https://github.com/SignLLM/Prompt2Sign/2Dto3D)

## Tool Usage
<!-- This section could provide foundational knowledge or context for the rest of the content -->

Coming Soon, you can take a look at our [project homepage](https://signllm.github.io/), which is actually quite detailed.

## FAQ
<!-- List out FAQs here -->
**Are there dataloaders available for the dataset.**

Two answers: Yes & coming soon. For each of the benchmarks, there is a dataloader available that was used to generate the benchmark results and that should cover most purposes. There's also a set of common dataloaders coming, which will be available sometime in next year.

## How To Cite

Please cite the following paper when using Prompt2Sign in your research:

```
@inproceedings{prompt2sign2023,
title={Prompt2Sign: A Multilingual Dataset for Sign Language Production},
author={XXXX},
booktitle={xxxx},
year={2023}
}
```

**Related Work**

<sup>1</sup>[SignLLM: Sign Languages Production Large Language Models.]()

<sup>2</sup>[SignDiff: Learning Diffusion Models for American Sign Language Production.](https://arxiv.org/abs/2308.16082)

## Contact Us
<!-- Insert contact details or a form link here -->
Join the conversation and contribute to the pioneering work we are doing at Prompt2Sign!

For questions/suggestions of data/code issues, please raise on issue on the [Code repo](https://github.com/SignLLM/Code) or [Tool repo](https://github.com/SignLLM/Prompt2Sign). For direct contact, press inquiries or any concerns: [Email Us](mailto:signllm@googlegroups.com).

## Acknowledgements

All data collection and processing are conducted in accordance with the relevant certificates/protocols of the used dataset, or are sourced or will be collected online.

**Licensing**

Prompt2Sign is made available under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/). For commercial use, please contact us directly.

![image](https://github.com/SignLLM/Prompt2Sign/assets/147891572/7bc0cb5c-ef77-4a15-87cb-e78cc01c8f76)












<!-- 

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
