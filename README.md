# SearchAnything

"SearchAnything" is a local semantic search engine, powered by various AI models, which allows you to search sentences and images based on their semantic meanings.

Check out our demo video to see how it works.

https://github.com/Immortalise/SearchAnything/assets/31989262/c7c2a3cf-154e-4249-a568-b769b6bc6308

https://github.com/Immortalise/SearchAnything/assets/31989262/c59ae640-3b26-4e04-9fd1-0759a2bd2c84

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
- [ ] Autonomous monitoring of file changes and automatic add/delete files into database when files are added/deleted.
- [ ] Support for semantic search of audio resources.

### Text Semantic Search

- [ ] Support for .pptx and .docx formats.
- [ ] Integration with BM25 and Exact search.
