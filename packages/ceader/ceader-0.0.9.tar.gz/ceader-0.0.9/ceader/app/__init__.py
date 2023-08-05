from __future__ import annotations

import pickle  # nosec
import re
from multiprocessing import Pool
from pathlib import Path
from typing import Callable, Dict, Iterable, Iterator, List, TypeVar

from ceader import get_logger
from ceader.domain.header_procedure.add_header_procedure import (
    AddHeaderProcedure,
)
from ceader.domain.header_procedure.remove_header_procedure import (
    RemoveHeaderProcedure,
)
from ceader.domain.repositories import FileRepository
from ceader.domain.types.enums import CeaderStatus
from ceader.domain.utils import get_file_lines

A = TypeVar("A")
T = TypeVar("T")

logger = get_logger()


class Application:
    def __init__(
        self,
        file_repo: FileRepository,
        prefer_multiline_comment: bool,
        debug: bool = False,
    ) -> None:
        self.file_repo = file_repo
        self.prefer_multiline_comment = prefer_multiline_comment
        self.debug = debug

        # TODO add postinit fun
        header = self.file_repo.get_header()
        if header is None:
            raise ValueError("Cannot find header!")
        _validate_header_lines(get_file_lines(header))

    def add_header_to_file(
        self, filepath: Path, header_path: Path
    ) -> CeaderStatus:
        return _add_header_to_file(
            filepath,
            header_path,
            prefer_multiline_comment=self.prefer_multiline_comment,
            debug=self.debug,
        )

    def add_header_to_files(
        self, files_to_change: List[Path], header_path: Path
    ) -> int:

        res_dict: Dict[CeaderStatus, int] = {
            CeaderStatus.SUCCESS: 0,
            CeaderStatus.SKIPPED: 0,
            CeaderStatus.FAILURE: 0,
        }

        for filepath in files_to_change:
            status = self.add_header_to_file(filepath, header_path)
            res_dict[status] += 1
        if self.debug:
            for key, value in res_dict.items():
                logger.info(f"{key.value}:{value}")

        if res_dict[CeaderStatus.FAILURE] > 0:
            return 1
        return 0

    def remove_header_from_file(
        self, filepath: Path, header_path: Path
    ) -> CeaderStatus:
        return _remove_header_from_file(
            filepath,
            header_path,
            prefer_multiline_comment=self.prefer_multiline_comment,
            debug=self.debug,
        )

    def remove_header_from_files(
        self, files_to_change: List[Path], header_path: Path
    ) -> int:

        res_dict: Dict[CeaderStatus, int] = {
            CeaderStatus.SUCCESS: 0,
            CeaderStatus.SKIPPED: 0,
            CeaderStatus.FAILURE: 0,
        }
        for filepath in files_to_change:
            status = self.remove_header_from_file(filepath, header_path)
            res_dict[status] += 1
        if self.debug:
            for key, value in res_dict.items():
                logger.info(f"{key.value}:{value}")
        if res_dict[CeaderStatus.FAILURE] > 0:
            return 1
        return 0


def _remove_header_from_file(
    filepath: Path,
    header_path: Path,
    prefer_multiline_comment: bool = False,
    debug: bool = False,
) -> CeaderStatus:
    header_procedure = RemoveHeaderProcedure()
    return header_procedure.run(
        filepath=filepath,
        header_path=header_path,
        prefer_multiline_comment=prefer_multiline_comment,
        debug=debug,
    )


def _add_header_to_file(
    filepath: Path,
    header_path: Path,
    prefer_multiline_comment: bool = False,
    debug: bool = False,
) -> CeaderStatus:
    header_procedure = AddHeaderProcedure()

    return header_procedure.run(
        filepath=filepath,
        header_path=header_path,
        prefer_multiline_comment=prefer_multiline_comment,
        debug=debug,
    )


def _validate_header_lines(header_lines: List[str]) -> None:
    if len(header_lines) == 0:
        raise ValueError("Header file cannot be empty!")
    elif re.search("^\s*$", header_lines[0]):
        raise ValueError("First header line cannot be empty!")


def _run_in_parallel(
    arguments: Iterable[A], fun: Callable[[A], T], processes: int
) -> Iterator[T]:
    """
    allows to run given function `fun` in parallel on given arguments `arguments`.
    parallelism is set by `processes` parameter.
    keep in mind that the function needs to be pickable.
    results are yielded one by one from each process and are not sorted.
    """
    # max tasks per child - keep this as 1 to force cleaning
    # of ram after each diagram
    with Pool(processes, maxtasksperchild=1) as pool:
        for result in pool.imap_unordered(fun, arguments):
            try:
                yield result
            except Exception as e:
                logger.error(
                    f"Failure while processing in parallel, one of the jobs failed with: {e}",
                    exc_info=True,
                )
                raise e
