__version__ = "1.0.0"  

DATA_DIR = "./data"

INDEX_PATH = {
    'text': {'semantic': 'data/text_semantic.index',},
    'image': {'semantic': 'data/image_semantic.index',},
}

BM25_INDEX_PATH = 'data/bm25.pkl'
DOCID_LIST_PATH = 'data/docid_list.pkl'
CONTENT_LIST_PATH = 'data/content_list.pkl'
DB_PATH = 'data/database.db'
MONITORED_DIRS_PATH = 'data/monitor_dirs.pickle'
CHANGE_FILES = "data/changes.txt"

DATA_TYPES = ["text", "image"]
TEXT_TYPES = ["pdf", "txt", "md"]
IMAGE_TYPES = ["png", "jpg", "jpeg"]



TEXT_EMBEDDING_MODELS = [
    "sentence-transformers/all-mpnet-base-v2",
    "sentence-transformers/all-MiniLM-L6-v2",
]

IMAGE_EMBEDDING_MODELS = [
    "clip-ViT-B-32",
]