from typing import Dict, Tuple

from ceader.domain.types.enums import ComputerLanguage

# https://gist.github.com/ppisarczyk/43962d06686722d26d176fad46879d41


COMPUTER_LANGUAGE_TO_EXTENSION_MAPPING: Dict[
    ComputerLanguage, Tuple[str, ...]
] = {
    ComputerLanguage.C: tuple(
        [
            ".c",
            # ".cats",
            ".h",
            # ".idc",
            # ".w"
        ]
    ),
    ComputerLanguage.COBOL: tuple(
        [
            ".cob",
            #  ".cbl",
            #  ".ccp",
            #  ".cobol",
            #   ".cpy"
        ]
    ),
    ComputerLanguage.CPP: tuple(
        [
            ".cpp",
            ".c++",
            ".cc",
            ".cp",
            ".cxx",
            ".h",
            ".h++",
            # ".hh",
            # ".hpp",
            # ".hxx",
            # ".inc",
            # ".inl",
            # ".ipp",
            # ".tcc",
            # ".tpp",
        ]
    ),
    ComputerLanguage.CSS: tuple([".css"]),
    ComputerLanguage.ERLANG: tuple(
        [
            ".erl",
            # ".hrl"
        ]
    ),
    ComputerLanguage.GOLANG: tuple([".go"]),
    ComputerLanguage.HASKELL: tuple(
        [
            ".hs",
            # ".hsc"
        ]
    ),
    ComputerLanguage.HTML: tuple(
        [
            ".html",
            ".htm",
            # ".html.hl",
            # ".inc",
            # ".st",
            # ".xht",
            # ".xhtml"
        ]
    ),
    ComputerLanguage.JAVA: tuple([".jsp"]),
    ComputerLanguage.JAVASCRIPT: tuple(
        [
            ".js",
            # "._js",
            # ".bones",
            # ".es",
            # ".es6",
            # ".frag",
            # ".gs",
            # ".jake",
            # ".jsb",
            # ".jscad",
            # ".jsfl",
            # ".jsm",
            # ".jss",
            # ".njs",
            # ".pac",
            # ".sjs",
            # ".ssjs",
            # ".sublime-build",
            # ".sublime-commands",
            # ".sublime-completions",
            # ".sublime-keymap",
            # ".sublime-macro",
            # ".sublime-menu",
            # ".sublime-mousemap",
            # ".sublime-project",
            # ".sublime-settings",
            # ".sublime-theme",
            # ".sublime-workspace",
            # ".sublime_metrics",
            # ".sublime_session",
            # ".xsjs",
            # ".xsjslib",
        ]
    ),
    ComputerLanguage.KOTLIN: tuple(
        [
            ".kt",
            # ".ktm",
            # ".kts"
        ]
    ),
    ComputerLanguage.R: tuple(
        [
            ".r",
            # ".rd",
            # ".rsx"
        ]
    ),
    ComputerLanguage.RUBY: tuple(
        [
            ".rb",
            # ".builder",
            # ".fcgi",
            # ".gemspec",
            # ".god",
            # ".irbrc",
            # ".jbuilder",
            # ".mspec",
            # ".pluginspec",
            # ".podspec",
            # ".rabl",
            # ".rake",
            # ".rbuild",
            # ".rbw",
            # ".rbx",
            # ".ru",
            # ".ruby",
            # ".thor",
            # ".watchr",
        ]
    ),
    ComputerLanguage.RUST: tuple(
        [
            ".rs",
            # ".rs.in"
        ]
    ),
    ComputerLanguage.SHELL: tuple(
        [
            ".sh",
            ".bash",
            ".bats",
            ".cgi",
            ".command",
            ".fcgi",
            ".ksh",
            # ".sh.in",
            ".tmux",
            ".tool",
            ".zsh",
        ]
    ),
    ComputerLanguage.SCALA: tuple([".scala", ".sbt", ".sc"]),
    ComputerLanguage.TXT: tuple([".txt"]),
    ComputerLanguage.PYTHON: tuple(
        [
            ".py",
            # ".bzl",
            # ".cgi",
            # ".fcgi",
            # ".gyp",
            # ".lmi",
            # ".pyde",
            # ".pyp",
            # ".pyt",
            # ".pyw",
            # ".rpy",
            # ".tac",
            # ".wsgi",
            # ".xpy",
        ]
    ),
    ComputerLanguage.PERL: tuple(
        [
            ".pl",
            # ".al",
            # ".cgi",
            # ".fcgi",
            # ".perl",
            # ".ph",
            # ".plx",
            # ".pm",
            # ".pod",
            # ".psgi",
            # ".t",
        ]
    ),
    ComputerLanguage.PHP: tuple(
        [
            ".php",
            # ".aw",
            # ".ctp",
            # ".fcgi",
            # ".inc",
            # ".php3",
            # ".php4",
            # ".php5",
            # ".phps",
            # ".phpt",
        ]
    ),
    ComputerLanguage.YAML: tuple([".yaml", ".yml"]),
    ComputerLanguage.XML: tuple([".xml"]),
}

EXTENSION_TO_PROGRAMMING_LANGUAGE_MAPPING: Dict[str, ComputerLanguage] = {
    k: cl
    for cl, vs in COMPUTER_LANGUAGE_TO_EXTENSION_MAPPING.items()
    for k in vs
}
