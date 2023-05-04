from typing import List, Any

class Parser:
    """
    Top class of data parser
    """
    def __init__(self, file_path: str, out_path: str) -> None:
        self.file_path: str = file_path
        self.out_path: str = out_path
        self.parse_output: Any = None

    def parse_to_text(self) -> List[str]:
        """
        Parse file to text
        """
        raise NotImplementedError()
    
    def _check_format(self) -> bool:
        """
        Check input file format
        """
        raise NotImplementedError()