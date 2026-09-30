import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from sor.common import PeriodRange
from sor.params import *


class SorFile:
    def __init__(self, date: date, dir: str, template: str):
        self.date = date
        self.dir = dir
        self.template = template

    @classmethod
    def from_path(cls, path: Path, template: str) -> "SorFile":
        path = Path(path)

        if "{}" not in template:
            raise ValueError(f"template must contain '{{}}': {template}")

        pattern = re.escape(template).replace(
            re.escape("{}"),
            r"(?P<date>\d{4}-\d{2}-\d{2})",
            1,
        )
        pattern = f"^{pattern}$"

        match = re.match(pattern, path.name)
        if match is None:
            raise ValueError(
                f"path name does not match template: "
                f"path={path.name}, template={template}"
            )

        parsed_date = date.fromisoformat(match.group("date"))

        return cls(
            date=parsed_date,
            dir=str(path.parent),
            template=template,
        )

    def path(self) -> Path:
        name = self.name()
        return Path(self.dir) / name

    def name(self) -> str:
        date_text = self.date.isoformat()
        return self.template.format(date_text)

    def __str__(self) -> str:
        return str(self.path())


class SorFileStream:
    def __init__(self, dir: str, template: str, range: PeriodRange):
        self.dir = dir
        self.template = template
        self.range = range

    def files(self) -> Iterable[SorFile]:
        for current in self.range.range():
            file = SorFile(current, self.dir, self.template)

            yield file


class CSVFilesStream(SorFileStream):
    def __init__(self, period: PeriodRange):
        super().__init__(CSV_FOLDER, CSV_NAME_TEMPLATE, period)

    def files(self) -> Iterable[SorFile]:
        for path in super().files():
            if not path.path().exists():
                continue

            files = path.path().rglob("*.csv")
            files = sorted(files)
            files = filter(Path.is_file, files)

            for file in files:
                yield SorFile(path.date, str(file.parent), file.name)


class ZIPFilesStream(SorFileStream):
    def __init__(self, period: PeriodRange):
        super().__init__(ZIP_FOLDER, ZIP_NAME_FORMAT, period)
    
    def files(self) -> Iterable[SorFile]:
        for path in super().files():
            if path.path().exists():
                continue
            yield path
