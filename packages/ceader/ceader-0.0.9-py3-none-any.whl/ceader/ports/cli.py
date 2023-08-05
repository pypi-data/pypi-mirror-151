# CLI mode of work

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from ceader import get_logger
from ceader.app import Application

logger = get_logger()

from ceader.service import new_application


class Cli:
    modes = {
        "add_header",
        "remove_header",
    }

    def __init__(self, app: Application, mode: str = "add_header") -> None:
        self.app = app
        self.mode = mode

        self.mode_to_flow = {
            "add_header": self.add_header_flow,
            "remove_header": self.remove_header_flow,
        }
        if not self.modes == set(self.mode_to_flow.keys()):
            raise ValueError("modes must be equal")

    @classmethod
    def new_cli_app(cls, args: List[str]) -> Cli:
        parsed_args = Cli.parse_args(*args)
        app = new_application(
            files=parsed_args.files,
            header_path=Path(parsed_args.header_path),
            file_extensions=parsed_args.extensions,
            skip_hidden=parsed_args.skip_hidden,
            prefer_multiline_comment=parsed_args.prefer_multiline_comment,
            debug=parsed_args.debug,
        )

        mode = parsed_args.mode
        return cls(app, mode)

    def run(self) -> int:
        files_to_change = self.app.file_repo.get_files()
        header_file = self.app.file_repo.get_header()

        if header_file is None:
            raise ValueError(f"Can't find header!")

        run_fun = self.mode_to_flow.get(self.mode)
        if run_fun is None:
            raise ValueError(f"Mode {self.mode} not found")

        return run_fun(files_to_change, header_file)

    def add_header_flow(
        self, files_to_change: List[Path], header_path: Path
    ) -> int:

        return self.app.add_header_to_files(
            files_to_change=files_to_change, header_path=header_path
        )

        # if not success:
        #     raise ValueError(f"failed to add header to files, see previous logs")

    def remove_header_flow(
        self, files_to_change: List[Path], header_path: Path
    ) -> int:

        return self.app.remove_header_from_files(
            files_to_change=files_to_change, header_path=header_path
        )

        # if not success:
        #     raise ValueError(f"failed to remove header from files, see previous logs")

    @staticmethod
    def parse_args(*args: str) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="This app adds headers to the beginning of specific files."
        )
        parser.add_argument(
            "--mode",
            choices=Cli.modes,
            help="what is the desired mode. ['add_header', 'remove_header']",
            default="add_header",
            required=True,
        )

        parser.add_argument(
            "--files",
            type=str,
            nargs="+",
            help=("List of paths to files and folders "),
            default=[],
            required=True,
        )

        parser.add_argument(
            "--header-path",
            type=str,
            help=("root path to txt header file."),
            required=True,
        )

        parser.add_argument(
            "--extensions",
            type=str,
            nargs="+",
            help=("file extensions which ll be changed by ceader."),
            default=[],
            required=True,
        )

        parser.add_argument(
            "--prefer-multiline-comment",
            help=("Some languages support multiline and single line comments"),
            action="store_true",
            default=False,
        )

        parser.add_argument(
            "--skip-hidden",
            help="adding header to hidden files",
            action="store_true",
        )

        parser.add_argument(
            "--debug",
            help="used to enable debug output, temp images etc.",
            action="store_true",
        )

        namespace = parser.parse_args(args)

        file_paths: List[str] = list(namespace.files)
        for path in file_paths:
            if not (Path(path).is_file() or Path(path).is_dir()):
                raise ValueError(f"{path} doesn't exist!")

        header_path = Path(namespace.header_path)

        if not (header_path.is_file() and header_path.suffix == ".txt"):
            raise ValueError(f"{header_path} is not a txt file!")

        return namespace
