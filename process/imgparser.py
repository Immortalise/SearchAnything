from pathlib import Path
from typing import List, Dict
import sys
import os
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .parser_base import BaseParser
from utils import encode_image


class ImgParser(BaseParser):
    """
    Parser for image files
    """
    type = 'image'
    def __init__(self, file_path: str=None, model=None, out_path: str=None) -> None:
        super().__init__(file_path, model, out_path)
        
    def parse(self) -> List[Dict]:

        img = Image.open(self.file_path)
        
        self.parse_output = []
        file_dict = {}
        file_dict['content'] = None
        file_dict['embedding'] = encode_image(self.model, img)
        # print("embedding: ", type(file_dict['embedding']), file_dict['embedding'].shape)
        file_dict['file_path'] = self.file_path
            
        self.parse_output.append(file_dict)
        
        return self.parse_output


    def _check_format(self) -> bool:
        f_path: Path = Path(self.file_path)
        return f_path.exists() and f_path.suffix in ['png', 'jpg', 'jpeg']