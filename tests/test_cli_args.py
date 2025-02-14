"""Tests related parsing input from CLI arguments."""
from typing import List, Union
import pytest
from cpp_linter.run import cli_arg_parser


class Args:
    """A pseudo namespace declaration. Each attribute is initialized with the
    corresponding CLI arg's default value."""

    verbosity: int = 10
    database: str = ""
    style: str = "llvm"
    tidy_checks: str = (
        "boost-*,bugprone-*,performance-*,readability-*,portability-*,modernize-*,"
        "clang-analyzer-*,cppcoreguidelines-*"
    )
    version: str = ""
    extensions: List[str] = [
        "c",
        "h",
        "C",
        "H",
        "cpp",
        "hpp",
        "cc",
        "hh",
        "c++",
        "h++",
        "cxx",
        "hxx",
    ]
    repo_root: str = "."
    ignore: str = ".github"
    lines_changed_only: int = 0
    files_changed_only: bool = False
    thread_comments: str = "false"
    step_summary: bool = False
    file_annotations: bool = True
    extra_arg: List[str] = []
    no_lgtm: bool = True


def test_defaults():
    """test default values"""
    args = cli_arg_parser.parse_args("")
    for key in args.__dict__.keys():
        assert args.__dict__[key] == getattr(Args, key)


@pytest.mark.parametrize(
    "arg_name,arg_value,attr_name,attr_value",
    [
        ("verbosity", "20", "verbosity", 20),
        ("database", "build", "database", "build"),
        ("style", "file", "style", "file"),
        ("tidy-checks", "-*", "tidy_checks", "-*"),
        ("version", "14", "version", "14"),
        ("extensions", ".cpp, .h", "extensions", ["cpp", "h"]),
        ("extensions", "cxx,.hpp", "extensions", ["cxx", "hpp"]),
        ("repo-root", "src", "repo_root", "src"),
        ("ignore", "!src|", "ignore", "!src|"),
        ("lines-changed-only", "True", "lines_changed_only", 2),
        ("lines-changed-only", "difF", "lines_changed_only", 1),
        ("files-changed-only", "True", "files_changed_only", True),
        ("thread-comments", "true", "thread_comments", "true"),
        ("thread-comments", "false", "thread_comments", "false"),
        ("thread-comments", "update", "thread_comments", "update"),
        ("no-lgtm", "true", "no_lgtm", True),
        ("no-lgtm", "false", "no_lgtm", False),
        ("step-summary", "True", "step_summary", True),
        ("file-annotations", "False", "file_annotations", False),
        ("extra-arg", "-std=c++17", "extra_arg", ["-std=c++17"]),
        ("extra-arg", '"-std=c++17 -Wall"', "extra_arg", ['"-std=c++17 -Wall"']),
    ],
)
def test_arg_parser(
    arg_name: str,
    arg_value: str,
    attr_name: str,
    attr_value: Union[int, str, List[str], bool],
):
    """parameterized test of specific args compared to their parsed value"""
    args = cli_arg_parser.parse_args([f"--{arg_name}={arg_value}"])
    assert getattr(args, attr_name) == attr_value
