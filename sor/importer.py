import csv
from typing import Callable
from collections import deque

from sor.common import Event
from sor.files import SorFileStream
from sor.params import *


class SORImporter:
    def __init__(
        self,
        files: SorFileStream,
        parser: Callable[[dict[str, str]], Event | None],
        filter: Callable[[Event | None], bool],
        importer: Callable,
    ):
        self.files = files
        self.parser = parser
        self.filter = filter
        self.importer = importer


    def load(self) -> None:
        for table_file in self.files.files():
            with table_file.path().open("r", encoding=ENCODING, newline="") as f:
                print(f"name:{table_file}")
                reader = csv.DictReader(f)

                parsered = map(self.parser, reader)
                filtered = filter(self.filter, parsered)
                deque(map(self.importer, filtered), maxlen=0)

            self.importer.flush()
