<img src="https://github.com/Immortalise/SearchAnything/assets/31989262/2ba3edd0-ae34-44ed-862d-c1f0eced29d3" width="400" height="160">

# SearchAnything

[UPD] This repository is no longer actively maintained. We encourage and appreciate all efforts to improve SearchAnything.

"SearchAnything" is a local semantic search engine, powered by various AI models, which allows you to search sentences and images based on their semantic meanings.

Check out our demo video to see how it works. [[Zhihu blog](https://zhuanlan.zhihu.com/p/641128049)] [[Twitter](https://twitter.com/jd92wang/status/1676114619168067585)]

https://github.com/Immortalise/SearchAnything/assets/31989262/76ab3ad4-1f57-453f-acfc-dea7a310ae1d

https://github.com/Immortalise/SearchAnything/assets/31989262/8a7e0234-a35f-4cd8-936b-ea1ae9e0089a



![pipeline](https://github.com/Immortalise/SearchAnything/assets/31989262/7705eec1-e6c7-426e-9095-f49df355ad4f)


## Installation

First, clone our repository: `git clone git@github.com:Immortalise/SearchAnything.git`

We recommend using a Conda environment to manage your Python dependencies as it allows you to isolate your Python environment.

Use the following commands to set up the environment for "SearchAnything":

```bash
conda env create -f env.yaml
conda activate anything
```

Please note that on MacOS systems, executing `conda env create -f env.yaml` may result in errors due to the CUDA packages and some other packages. We are currently addressing this issue and working on improving the MacOS environment compatibility.


## Running

### Adding Files

Start the application by running `python anything.py` in the console.

Upon running, you will see the following instructions:

```
[nltk_data] Downloading package punkt to /xxx/nltk_data... 
[nltk_data] Package punkt is already up-to-date! 
Adding text embedding model 
Adding image embedding model 
SearchAnything v1.0 Type 'exit' to exit.   
Type 'insert' to parse file.   
Type 'search' to search file.   
Type 'delete' to delete file. 
Instruction:
```

Type `insert`, followed by the file path. Please note that the file path can either be a single file or a directory. If a directory is specified, all supported files in the directory will be parsed and saved to the database.

### Search Files

When searching files, you can also use a more user-friendly web interface by running:

```
streamlit run app.py
```

In this local web interface, you can search files based on their semantic meanings.

## Supported File Types

We currently support the following file types:

- Text: pdf, txt, md
- Image: jpg, jpeg, png

## Implementation

"SearchAnything" primarily involves two steps:

### Embedding

Given a text or images, they are first processed into a vector (embedding). The main AI models for semantic search are based on the sentence-transformer [repository](https://github.com/UKPLab/sentence-transformers).

Semantic search for text: `all-mpnet-base-v2`

Semantic search for images: `clip-ViT-B-32`

### Save and Retrieve

After generating the embedding for each image and text, we save the embedding along with the file path into a database.

When given a query and a search type, we process the query into an embedding $e_q$, then retrieve all embeddings $[e_1, e_2, ..., e_n]$ from the database. We then calculate the cosine similarity between the query embedding `e_q` and each of $[e_1, e_2, ..., e_n]$, sort them in descending order, and return the results.

### Privacy Protection

SearchAnything downloads the most advanced AI models to run locally, so there's no need to worry about your private data being compromised!
Text semantic search only requires about 400MB of memory space, while image semantic search requires around 4GB of memory. We will add more models in the future to make it easier for users with different memory sizes to use.

## TODOs

We're eager to hear your valuable feedback and constructive suggestions!

Here are some features we plan to implement in the future:

### Functions

- [ ] Support for deleting files.
- [ ] Support audio input.
- [ ] Support image query.
- [ ] Autonomous monitoring of file changes and automatic add/delete files into database when files are added/deleted.
- [ ] Support for semantic search of audio resources.
- [ ] Test ImageBind model.
- [ ] Support for MacOS system.

### Text Semantic Search

- [ ] Support for .pptx and .docx formats.
- [ ] Integration with BM25 and Exact search.


## Related work

Note the recent Github library: [Semantra](https://github.com/freedmand/semantra) is similar to our SearchAnything and aims to facilitate semantic search of documents. SearchAnything differs from Semantra in the following ways:

* flexible file support: SearchAnything supports not only text files (PDF, TXT, MD), but also images (e.g. JPG, JPEG, PNG). We are constantly working on expanding the range of supported file types.
* Integration of different AI models: SearchAnything integrates different AI models based on the Sentence Transformer library. This approach ensures a powerful and versatile semantic understanding of a wide range of data.
* User-friendly interface: SearchAnything is equipped with a native interface provided by Streamlit, which is designed to be very friendly for non-technical users.



## Authors

* **Kaijie Zhu** - CASIA - [Immortalise](https://github.com/Immortalise)
* **Wenxin Hou** - STCA - [houwenxin](https://github.com/houwenxin)
* **Chuqi Zhang** - NUS - [Icegrave0391](https://github.com/Icegrave0391)
* **Jindong Wang** - MSRA - [jindongwang](https://github.com/jindongwang)
* **Yidong Wang** -PKU - [qianlanwyd](https://github.com/qianlanwyd)


## Acknowledgements

* [Sentence Transformers: Multilingual Sentence, Paragraph, and Image Embeddings using BERT & Co.](https://github.com/UKPLab/sentence-transformers)
* [SQLite3](https://www.sqlite.org/docs.html)
