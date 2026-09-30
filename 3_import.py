import sys
sys.path.insert(0, '')

from pathlib import Path

from sor.common import PeriodRange
from sor.files import CSVFilesStream
from sor.filter import SORFilter
from sor.parser import SORParser
from sor.db import SORDatabase, EventInserter
from sor.importer import SORImporter
from sor.params import DB_FILE


def main() -> None:
    period = PeriodRange()

    filter = SORFilter()
    parser = SORParser()

    files = CSVFilesStream(period)

    db = EventInserter(period)
    db.connect()
    db.create_schema()

    importer = SORImporter(files, parser, filter, db)
    importer.load()

    db.create_indexes()
    db.commit()

    print(f"done: db={DB_FILE} events={db.count_events()}")


if __name__ == "__main__":
    main()
