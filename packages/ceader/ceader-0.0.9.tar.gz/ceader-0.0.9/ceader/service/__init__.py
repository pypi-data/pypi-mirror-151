from pathlib import Path
from typing import List

from ceader.adapters.file_disk_repo import FileDiskRepository
from ceader.app import Application


def new_application(
    files: List[str],
    header_path: Path,
    file_extensions: List[str],
    skip_hidden: bool,
    prefer_multiline_comment: bool,
    debug: bool,
) -> Application:
    file_repo = FileDiskRepository(
        files=[Path(f) for f in files],
        header_path=header_path,
        skip_hidden=skip_hidden,
        extensions_to_get=file_extensions,
        debug=debug,
    )
    return Application(
        file_repo=file_repo,
        prefer_multiline_comment=prefer_multiline_comment,
        debug=debug,
    )
