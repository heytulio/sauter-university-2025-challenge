from abc import ABC, abstractmethod
from pathlib import Path

class IBucketAdapter(ABC):
    
    @abstractmethod
    def upload_file(self, file_obj: Path, target_path: str):
        pass

    @abstractmethod
    def list_files(self):
        pass