from abc import abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Set


class FileRepository:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_files(self) -> List[Path]:
        pass

    @abstractmethod
    def get_files_per_extension(self) -> Dict[str, Set[Path]]:
        pass

    @abstractmethod
    def get_header(self) -> Optional[Path]:
        pass
