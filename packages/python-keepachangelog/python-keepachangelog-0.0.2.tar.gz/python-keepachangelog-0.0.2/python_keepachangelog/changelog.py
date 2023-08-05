from __future__ import annotations

import os
import re
from datetime import date
from io import TextIOWrapper
from typing import Dict, List, Union

import semver

SEMVER_RE = re.compile(
    r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?"
)
HEADER_LINE_RE = re.compile(
    r"^## \[{}\] ".format(SEMVER_RE.pattern)
    + r"- (?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})$"
)


class ChangelogEntry:
    version: semver.VersionInfo
    date: date
    changes: Dict[str, List[str]]

    def __init__(
        self,
        version: str | semver.VersionInfo,
        date_in: date | str,
        changes: Dict[str, List[str]] = None,
    ) -> None:
        if isinstance(version, semver.VersionInfo):
            self.version = version
        else:
            self.version = semver.VersionInfo.parse(version)
        if isinstance(date_in, date):
            self.date = date_in
        else:
            self.date = date.fromisoformat(date_in)
        self.date = date_in
        self.changes = changes or {}

    def __lt__(self, __o: ChangelogEntry) -> bool:
        return self.version < __o.version

    def __eq__(self, __o: ChangelogEntry) -> bool:
        return self.version == __o.version

    def add_change(self, section: str, change: str) -> None:
        if section not in self.changes.keys():
            self.changes[section] = []
        self.changes[section].append(change)

    @staticmethod
    def _header_match_to_version(header_match: re.Match) -> str:
        return "{}.{}.{}".format(
            *[header_match.group(group) for group in ("major", "minor", "patch")]
        )

    @staticmethod
    def _header_match_to_date(header_match: re.Match) -> date:
        return date(
            *[int(header_match.group(group)) for group in ("year", "month", "day")]
        )

    @classmethod
    def from_header_match(cls, header_match: re.Match) -> ChangelogEntry:
        if not isinstance(header_match, re.Match):
            raise TypeError("re.Match was not passed")
        return ChangelogEntry(
            ChangelogEntry._header_match_to_version(header_match),
            ChangelogEntry._header_match_to_date(header_match),
        )

    def __str__(self) -> str:
        out = f"## [{self.version}] - {self.date}\n"
        for section in self.changes.keys():
            out += f"### {section}\n"
            for change in self.changes[section]:
                out += f"- {change}\n"

        return out

    def __repr__(self) -> str:
        return f"ChangelogEntry({self.version} - {self.date} ({self.changes})"


class Changelog:
    original_content: str = None
    name: str
    _entries: List[ChangelogEntry] = None

    header: str = """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)."""

    def __init__(
        self,
        name: str = None,
        file: Union[str, TextIOWrapper, None] = None,
        source: str = None,
    ) -> None:
        if isinstance(source, str) and file:
            raise ValueError("`file` and `source` cannot be used together")
        elif isinstance(source, str):
            with open(source) as f:
                self.original_content = f.read()
            if not name:
                dir_path = os.path.dirname(source)
                name = os.path.basename(dir_path)
        elif file:
            if isinstance(file, str):
                self.original_content = file
            elif isinstance(file, TextIOWrapper):
                self.original_content = file.read()
            else:
                raise TypeError("`file` is not a string, or a file-like object", file)

        self.name = name
        self._entries = []

    @property
    def entries(self):
        return sorted(self._entries)

    def add_entry(self, entry: ChangelogEntry) -> None:
        self._entries.append(entry)

    def parse_original_content(self):
        header_lines = []
        header_end_line_no: int = None
        for idx, line in enumerate(self.original_content.splitlines()):
            if HEADER_LINE_RE.match(line):
                header_end_line_no = idx
                break
            header_lines.append(line)
        self.header = "\n".join(header_lines).rstrip()

        non_header_lines = self.original_content.splitlines()[header_end_line_no:]

        entry: ChangelogEntry = None
        changes_section = None
        for line in non_header_lines:
            header_match = HEADER_LINE_RE.match(line)
            if header_match:
                entry = ChangelogEntry.from_header_match(header_match)
                self._entries.append(entry)
                changes_section = None
            if line.startswith("###"):
                changes_section = line.split(" ", 1)[1]
            if line.startswith("-"):
                entry.add_change(changes_section, line.split(" ", 1)[1])

    def to_string(self) -> str:
        out = self.header + "\n\n"

        for entry in reversed(self.entries):
            out += str(entry) + "\n"

        return out.rstrip() + "\n"
