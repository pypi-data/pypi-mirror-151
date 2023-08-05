from pathlib import Path
from typing import Dict, List, Optional, Set

from ceader import get_logger
from ceader.domain.repositories import FileRepository
from ceader.domain.utils import find_file

logger = get_logger()


class FileDiskRepository(FileRepository):
    def __init__(
        self,
        files: List[Path],
        header_path: Path,
        extensions_to_get: List[str],
        skip_hidden: bool = True,
        debug: bool = False,
    ) -> None:

        for path in files:
            if not (Path(path).is_file() or Path(path).is_dir()):
                raise ValueError(f"{path} is not a file!")

        if len(extensions_to_get) == 0:
            raise ValueError(
                f"{extensions_to_get} extensions list cannot be empty!"
            )

        self.skip_hidden = skip_hidden
        self.files = files
        self.header_path = header_path
        self.extensions_to_get = set(
            [self._normalize_extension(ext) for ext in extensions_to_get]
        )
        self.debug = debug

        for extension in self.extensions_to_get:
            if extension[0] != ".":
                raise ValueError(f"Extension must start with '.'")

    def get_files(self) -> List[Path]:
        res: Set[Path] = set()
        header = self.get_header()

        for file_path in self.files:
            if file_path.is_dir():
                for ext in self.extensions_to_get:
                    found_files = find_file(
                        file_path,
                        f"*{ext}",
                        relative=False,
                        skip_hidden=self.skip_hidden,
                    )
                    if self.debug:
                        logger.debug(
                            f"found {len(found_files)} files for extension: {ext}"
                        )
                    res.update(found_files)
            elif file_path.is_file():
                if self.skip_hidden and file_path.stem[0] == ".":
                    continue
                if file_path.suffix in self.extensions_to_get:
                    res.update([file_path])

        return list([r for r in res if r != header])

    def get_header(self) -> Optional[Path]:

        files = find_file(
            self.header_path.parent,
            f"{self.header_path.stem}{self.header_path.suffix}",
            relative=False,
            skip_hidden=False,
        )
        if len(files) == 0:
            return None
        elif len(files) > 1:
            raise ValueError("Something wrong with header file!")
        else:
            header = files[0]
            if header.is_file() and header.suffix == ".txt":
                return header
            else:

                return None

    def get_files_per_extension(self) -> Dict[str, Set[Path]]:

        res: Dict[str, Set[Path]] = {}
        for ext in self.extensions_to_get:
            res[ext] = set()

        header = self.get_header()
        for file_path in self.files:
            if file_path.is_dir():
                for ext in self.extensions_to_get:
                    found_files = find_file(
                        file_path,
                        f"*{ext}",
                        relative=False,
                        skip_hidden=self.skip_hidden,
                    )
                    if self.debug:
                        logger.debug(
                            f"found {len(found_files)} files for extension: {ext}"
                        )
                    res[ext].update(
                        set([file for file in found_files if file != header])
                    )

            elif file_path.is_file():
                if self.skip_hidden and file_path.stem[0] == ".":
                    continue
                if file_path.suffix in self.extensions_to_get:
                    res[file_path.suffix].update([file_path])

        return res

    def _normalize_extension(self, suffix: str) -> str:
        return suffix.lower()
