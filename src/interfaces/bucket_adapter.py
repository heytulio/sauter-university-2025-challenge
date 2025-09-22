from abc import ABC, abstractmethod
from pathlib import Path

class IBucketAdapter(ABC):
    """
        Interface for a cloud storage bucket adapter.

        This abstract class defines the contract for any class that needs
        to perform basic operations on a storage bucket, such as getting,
        uploading, and listing files. All concrete implementations must
        adhere to this interface.
    """
    @abstractmethod
    def upload_file(self, file_obj: Path, target_path: str):
        pass

    @abstractmethod
    def list_files(self):
        pass