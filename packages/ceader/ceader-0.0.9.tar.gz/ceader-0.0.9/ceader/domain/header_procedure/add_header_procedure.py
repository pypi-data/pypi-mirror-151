import os
from pathlib import Path
from typing import List

# fmt: off
#Black / isort are broken here :)
from ceader import get_logger
from ceader.domain.header_procedure import HeaderProcedure
# fmt: on
from ceader.domain.types.enums import CeaderStatus
from ceader.domain.utils import copy_permissions

logger = get_logger()


class AddHeaderProcedure(HeaderProcedure):
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

        if header_lines_in_file is None:
            self._add_header_to_file(filepath, header_lines)

        else:
            return CeaderStatus.SKIPPED

        return CeaderStatus.SUCCESS

    def _add_header_to_file(
        self, filepath: Path, lines_to_add: List[str]
    ) -> None:
        """Insert given lines as a new lines at the beginning of a file"""
        # TODO

        # define name of temporary dummy file
        dummy_file = Path(filepath.stem + ".bak")
        # open original file in read mode and dummy file in write mode

        # TODO move to fun add_to_stringIO(StringIO, lines_to_add)

        shebang_line = self._get_shebang_line(filepath)

        with open(filepath, "r") as read_obj, open(
            dummy_file, "w"
        ) as write_obj:
            # Write given line to the dummy file

            if shebang_line is not None:  # shebang must be always first

                write_obj.write(shebang_line)

            for line in lines_to_add:
                write_obj.write(line)
            # Read lines from original file one by one and append them to the dummy file
            for i, line in enumerate(read_obj):

                if (
                    i == 0 and shebang_line is not None
                ):  # shebang already added
                    continue
                write_obj.write(line)

        copy_permissions(dummy_file, filepath)

        # remove original file
        os.remove(filepath)
        # Rename dummy file as the original file
        os.rename(dummy_file, filepath)
        read_obj.close()
        write_obj.close()
