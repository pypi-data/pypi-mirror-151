import re
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple

from ceader import get_logger
from ceader.domain.knowledge.extensions_to_language import (
    EXTENSION_TO_PROGRAMMING_LANGUAGE_MAPPING,
)
from ceader.domain.knowledge.language_to_comment import (
    COMPUTER_LANGUAGE_TO_COMMENT_DATA_MAPPING,
    CommentData,
)
from ceader.domain.types.enums import CeaderStatus, ComputerLanguage
from ceader.domain.utils import get_file_lines

logger = get_logger()


class HeaderProcedure(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(
        self,
        filepath: Path,
        header_path: Path,
        prefer_multiline_comment: bool,
        debug: bool,
    ) -> CeaderStatus:
        pass

    def _print_lines(self, header_lines: List[str]) -> None:
        print("lines in total:", len(header_lines))
        for l in header_lines:
            print(l.replace("\n", ""))
        print()

    def _create_header_lines(
        self,
        header_path: Path,
        comment_data: CommentData,
        prefer_multiline_comment: bool,
    ) -> List[str]:
        """
        Reading header file + adding comments
        """

        def get_header_lines(header_path: Path) -> List[str]:
            return get_file_lines(header_path)

        def use_single_line_comment_method(
            single_line_comment: str, lines: List[str]
        ) -> List[str]:

            for i, line in enumerate(lines):
                lines[i] = single_line_comment + line
            return lines

        def use_multi_line_comment_method(
            multi_line_comment: Tuple[str, str], lines: List[str]
        ) -> List[str]:
            return (
                [multi_line_comment[0] + "\n"]
                + lines
                + [multi_line_comment[1] + "\n"]
            )

        header_lines = get_header_lines(header_path)
        if not prefer_multiline_comment:
            if comment_data.single_line_comment is not None:
                ceader_lines = use_single_line_comment_method(
                    single_line_comment=comment_data.single_line_comment,
                    lines=header_lines,
                )
            elif comment_data.multi_line_comment is not None:
                ceader_lines = use_multi_line_comment_method(
                    multi_line_comment=comment_data.multi_line_comment,
                    lines=header_lines,
                )
            else:
                raise ValueError("Something wrong with CommentData")
            return ceader_lines

        else:

            if comment_data.multi_line_comment is not None:
                ceader_lines = use_multi_line_comment_method(
                    multi_line_comment=comment_data.multi_line_comment,
                    lines=header_lines,
                )
            elif comment_data.single_line_comment is not None:
                ceader_lines = use_single_line_comment_method(
                    single_line_comment=comment_data.single_line_comment,
                    lines=header_lines,
                )
            else:
                raise ValueError("Something wrong with CommentData")
            return ceader_lines

    def _get_header_lines_inside_file(
        self, filepath: Path, header_lines: List[str]
    ) -> Optional[Tuple[int, int]]:
        """
        If header is already in file - return number of lines
        If header is not in file - return None
        """

        def get_file_lines(filepath: Path) -> List[str]:
            file = open(filepath, "r")
            file_lines = file.readlines()
            file.close()

            return file_lines

        file_lines = get_file_lines(filepath)

        first_line: Optional[int] = None
        last_line: Optional[int] = None
        correct_line_counter = 0

        for i, line in enumerate(file_lines):

            if first_line is None and (
                self._is_empty_line(line) or self._is_shebang_line(line)
            ):
                # ignoring all blank lines
                continue
            else:
                if first_line is None:
                    first_line = i
                if line.replace(" ", "") == header_lines[
                    correct_line_counter
                ].replace(
                    " ", ""
                ):  # TODO QUICK FIX - Make lint removes/adds spaces sometimes!
                    correct_line_counter += 1
                else:  # lines are different
                    return None

                if correct_line_counter == len(
                    header_lines
                ):  # if last line was good, return Tuple
                    last_line = i
                    return first_line, last_line
        return None

    def _is_shebang_line(self, line: str) -> bool:
        return bool(re.search("^[#][!]", line))

    def _is_empty_line(self, line: str) -> bool:
        return bool(re.search("^\s*$", line))

    def _get_shebang_line(self, filepath: Path) -> Optional[str]:
        lines = get_file_lines(filepath)
        if len(lines) == 0:
            return None
        elif self._is_shebang_line(lines[0]):
            return lines[0]
        else:
            return None

    def _understand_computer_language(
        self, filepath: Path, debug: bool
    ) -> Optional[ComputerLanguage]:
        suffix = filepath.suffix
        try:
            computer_language = EXTENSION_TO_PROGRAMMING_LANGUAGE_MAPPING[
                suffix
            ]
        except:
            if debug:
                logger.warning(f"{filepath.stem} has unknown suffix! {suffix}")
                return None

        return computer_language

    def _get_comment_data(
        self, computer_language: ComputerLanguage
    ) -> CommentData:
        try:
            cd = COMPUTER_LANGUAGE_TO_COMMENT_DATA_MAPPING[computer_language]
        except:
            raise ValueError(
                f"CommentData not found - add data for language: {computer_language.value}"
            )

        return cd

    def _copy_permissions(self, target: Path, source: Path) -> None:
        # st = os.stat(source)
        # os.chown(target, st.st_uid, st.st_gid)
        # os.chmod(target, st.st_mode)
        shutil.copymode(src=source, dst=target)
