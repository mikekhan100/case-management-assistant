from pathlib import Path
from uuid import UUID


class FileStorageService:
    def __init__(self, storage_dir: str = "storage"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_case_dir(self, case_id: UUID) -> Path:
        case_dir = self.storage_dir / str(case_id)
        case_dir.mkdir(parents=True, exist_ok=True)
        return case_dir

    def save_file(self, case_id: UUID, document_id: UUID, filename: str, content: bytes) -> Path:
        """Saves file bytes to disk under storage/{case_id}/{document_id}_{filename}."""
        case_dir = self._get_case_dir(case_id)
        # Sanitise filename to prevent path traversal
        safe_filename = Path(filename).name
        file_path = case_dir / f"{document_id}_{safe_filename}"
        
        with open(file_path, "wb") as f:
            f.write(content)
            
        return file_path

    def read_file(self, file_path: str | Path) -> bytes:
        """Reads file bytes from disk."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found at path: {file_path}")
        with open(path, "rb") as f:
            return f.read()

    def delete_file(self, file_path: str | Path) -> bool:
        """Deletes a file from disk if it exists."""
        path = Path(file_path)
        if path.exists():
            path.unlink()
            return True
        return False