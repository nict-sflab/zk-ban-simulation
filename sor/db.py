from datetime import date
from pathlib import Path
import sqlite3

from sor.common import Event, PeriodRange
from sor.params import BATCH_SIZE, DB_FILE

DBRow = tuple[str, str, str, str, str, str, str]

class SORDatabase:
    def __init__(self, file_name: Path | str = DB_FILE):
        self.file_name = Path(file_name)
        self.db: sqlite3.Connection | None = None

    def connect(self) -> None:
        db = sqlite3.connect(self.file_name)
        db.execute("PRAGMA journal_mode=WAL").fetchall()
        db.execute("PRAGMA synchronous=NORMAL").fetchall()
        db.execute("PRAGMA temp_store=MEMORY").fetchall()

        self.db = db

    def create_schema(self) -> None:
        self.db.executescript(
            """
            DROP TABLE IF EXISTS events;

            CREATE TABLE events (
            analysis_from TEXT NOT NULL,
            analysis_to TEXT NOT NULL,
            event_id TEXT NOT NULL,
            periodAuth TEXT NOT NULL,
            periodRevoke TEXT NOT NULL,
            decision_text TEXT NOT NULL,
            content_type TEXT,
            PRIMARY KEY (analysis_from, analysis_to, event_id)
            );
            """
        )


    def create_indexes(self) -> None:
        self.db.executescript(
            """
            CREATE INDEX idx_events_analysis ON events(analysis_from, analysis_to);
            CREATE INDEX idx_events_revoke ON events(periodRevoke);
            CREATE INDEX idx_events_auth ON events(periodAuth);
            CREATE INDEX idx_events_revoke_auth ON events(periodRevoke, periodAuth);
            """
        )

    def insert(self, rows: list[DBRow]) -> int:
        before = self.db.total_changes
        self.db.executemany(
            """
            INSERT OR IGNORE INTO events
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        inserted = self.db.total_changes - before
        rows.clear()
        return inserted

    def commit(self) -> None:
        self.db.commit()

    def count_events(self) -> int:
        return int(self.db.execute("SELECT COUNT(*) FROM events").fetchone()[0])


class EventInserter(SORDatabase):
    def __init__(self, period: PeriodRange, file_name: Path | str = DB_FILE):
        super().__init__(file_name)
        self.rows: list[DBRow] = []
        self.period = period
        self._inserted = 0

    def __call__(self, event: Event) -> None:
        self.rows.append(self.row(event))

        if len(self.rows) >= BATCH_SIZE:
            self.flush()

    def flush(self) -> int:
        if not self.rows:
            return self._inserted

        self._inserted += self.insert(self.rows)
        return self._inserted

    def row(self, event: Event) -> DBRow:
        return (
            self.period.analysis_from,
            self.period.analysis_to,
            event.event_id,
            event.periodAuth,
            event.periodRevoke,
            event.decision_text,
            event.content_type,
        )


class EventResultSelector(SORDatabase):
    def select_zkban_params(self, before: date, after: date):
        # zk-BAN ΔRL:
        #   period′ <= periodRevoke < period
        #   periodAuth <= period′
        delta_l, t = self.db.execute(
            """
            SELECT COUNT(*), COUNT(DISTINCT periodAuth)
            FROM events
            WHERE periodRevoke >= ?
                AND periodRevoke < ?
                AND periodAuth <= ?
            """,
            (before, after, before),
        ).fetchone()

        return delta_l, t

    def select_normal_params(self, before: date, after: date):
        # related-work diff:
        #   period′ <= periodRevoke < period
        delta_l, t = self.db.execute(
            """
            SELECT COUNT(*), COUNT(DISTINCT periodAuth)
            FROM events
            WHERE periodRevoke >= ?
                AND periodRevoke < ?
            """,
            (before, after),
        ).fetchone()
        return delta_l, t
