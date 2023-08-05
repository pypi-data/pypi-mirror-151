from enum import Enum


class ComputerLanguage(Enum):
    UNKNOWN = "Unknown"
    C = "C"
    COBOL = "Cobol"
    CPP = "C++"
    CSS = "CSS"
    ERLANG = "Erlang"
    GOLANG = "Golang"
    HASKELL = "Haskell"
    HTML = "HTML"
    JAVA = "Java"
    JAVASCRIPT = "JavaScript"
    KOTLIN = "Kotlin"
    RUBY = "Ruby"
    RUST = "Rust"
    R = "R"
    PERL = "Perl"
    PHP = "PHP"
    PYTHON = "Python"
    TXT = "txt"
    SCALA = "Scala"
    SHELL = "Shell"
    YAML = "Yaml"
    XML = "XML"


class CeaderStatus(Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"
    SKIPPED = "Skipped"
