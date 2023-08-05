import os
from pathlib import Path
from typing import List, Tuple

# fmt: off
#Black / isort are broken here :)
from ceader import get_logger
from ceader.domain.header_procedure import HeaderProcedure
# fmt: on
from ceader.domain.types.enums import CeaderStatus
from ceader.domain.utils import copy_permissions

logger = get_logger()


class RemoveHeaderProcedure(HeaderProcedure):
    def __init__(self) -> None:
        pass

    def run(
        self,
        filepath: Path,
        header_path: Path,
        prefer_multiline_comment: bool,
        debug: bool,
    ) -> CeaderStatus:
        cl = self._understand_computer_language(filepath, debug)
        if cl is None:
            return CeaderStatus.FAILURE

        cm_data = self._get_comment_data(cl)

        header_lines = self._create_header_lines(
            header_path=header_path,
            comment_data=cm_data,
            prefer_multiline_comment=prefer_multiline_comment,
        )

        if len(header_lines) == 0:
            raise ValueError("Header file is empty!")
        header_lines_in_file = self._get_header_lines_inside_file(
            filepath=filepath, header_lines=header_lines
        )
        if header_lines_in_file is not None:
            self._remove_header_from_file(filepath, header_lines_in_file)
        else:
            CeaderStatus.SKIPPED

        return CeaderStatus.SUCCESS

    def _print_lines(self, header_lines: List[str]) -> None:
        print("lines in total:", len(header_lines))
        for l in header_lines:
            print(l.replace("\n", ""))
        print()

    def _remove_header_from_file(
        self, filepath: Path, lines_to_remove: Tuple[int, int]
    ) -> None:
        """Remove given lines from file"""
        # header lines
        first_line = lines_to_remove[0]
        last_line = lines_to_remove[1]
        # define name of temporary dummy file
        dummy_file = Path(filepath.stem + ".bak")
        # open original file in read mode and dummy file in write mode
        with open(filepath, "r") as read_obj, open(
            dummy_file, "w"
        ) as write_obj:
            # Read lines from original file one by one and append them to the dummy file
            for i, line in enumerate(read_obj):
                if not (i >= first_line and i <= last_line):
                    write_obj.write(line)

        copy_permissions(dummy_file, filepath)
        # remove original file
        os.remove(filepath)
        # Rename dummy file as the original file
        os.rename(dummy_file, filepath)
        read_obj.close()
        write_obj.close()
