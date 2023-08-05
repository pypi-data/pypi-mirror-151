from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from ceader.domain.types.enums import ComputerLanguage


@dataclass
class CommentData:
    single_line_comment: Optional[str]
    multi_line_comment: Optional[Tuple[str, str]]


COMPUTER_LANGUAGE_TO_COMMENT_DATA_MAPPING: Dict[
    ComputerLanguage, CommentData
] = {
    ComputerLanguage.C: CommentData("//", ("/*", "*/")),
    ComputerLanguage.COBOL: CommentData("*", None),
    ComputerLanguage.CPP: CommentData("//", ("/*", "*/")),
    ComputerLanguage.CSS: CommentData(None, ("/*", "*/")),
    ComputerLanguage.ERLANG: CommentData("%", None),
    ComputerLanguage.GOLANG: CommentData("//", ("/*", "*/")),
    ComputerLanguage.HASKELL: CommentData("--", ("{-", "-}")),
    ComputerLanguage.HTML: CommentData(None, ("<!--", "-->")),
    ComputerLanguage.JAVA: CommentData("//", ("/*", "*/")),
    ComputerLanguage.JAVASCRIPT: CommentData("//", ("/*", "*/")),
    ComputerLanguage.KOTLIN: CommentData("//", ("/*", "*/")),
    ComputerLanguage.R: CommentData("#", None),
    ComputerLanguage.RUBY: CommentData("#", ("=begin", "=end")),
    ComputerLanguage.RUST: CommentData("//", ("/*", "*/")),
    ComputerLanguage.SHELL: CommentData("#", ("<<COMMENT", "COMMENT")),
    ComputerLanguage.SCALA: CommentData("//", ("/*", "*/")),
    ComputerLanguage.TXT: CommentData("", None),
    ComputerLanguage.PERL: CommentData("#", ("=begin", "=end")),
    ComputerLanguage.PHP: CommentData("//", ("/*", "*/")),
    ComputerLanguage.PYTHON: CommentData("#", ('"""', '"""')),
    ComputerLanguage.XML: CommentData(None, ("<!-", "->")),
    ComputerLanguage.YAML: CommentData("#", None),
}
