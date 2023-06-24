# Anything

Anything is a local semantic search engine powered by different AI models.

Currently, we support search words (including pdfs, txt, and markdown formats) and images (including jpg, jpeg, png formats) by their semantic meanings.

See the video for an example.


## Installation

It is better to have a conda environment, conda allows you to split your python environment.

Follow the instruction below to create the environment for Anything:

```bash
conda create -n anything python=3.8
conda activate anything
pip install -r requirements.txt
```

## Running

You can running a user-friendly web interface.

```bash
streamlit run app.py
```

In this local website, you can

* add your files
* search files by their semantic meanings

## Implementation

The main AI models are based on sentence-transformer [repository](https://github.com/UKPLab/sentence-transformers).

Semantic search for text: `all-mpnet-base-v2`

Semantic search for image: `clip-ViT-B-32`

## TODOs

We look forward to your precious opinions and constructive suggestions!

Currently, we will try our best to implement these functions:

* [ ] For text semantic search, supports .pptx .docx format.
* [ ] Monitor the file changes.
* [ ] Supports semantic search for audio resources.
