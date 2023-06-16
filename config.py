__version__ = "0.1.0"  

DATA_DIR = "./data"
INDEX_PATH = 'data/index_file.index'
BM25_INDEX_PATH = 'data/bm25.pkl'
DOCID_LIST_PATH = 'data/docid_list.pkl'
CONTENT_LIST_PATH = 'data/content_list.pkl'
DB_PATH = 'data/database/'
MONITORED_DIRS_PATH = 'data/monitor_dirs.pickle'
CHANGE_FILES = "data/changes.txt"




TEXT_EMBEDDING_MODELS = [
    "sentence-transformers/all-mpnet-base-v2",
    "sentence-transformers/all-MiniLM-L6-v2",
]

IMAGE_EMBEDDING_MODELS = [
    "clip-ViT-B-32",
]

SUPPORTED_FILE_TYPE = [
    'pdf',
    'md',
    'txt',
    'jpg',
    'jpeg',
    'png',
]