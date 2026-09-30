#!/usr/bin/env python3
import csv

from sor.db import EventResultSelector
from sor.common import PeriodRange
from sor.params import ANALYSIS_OUTPUT_FILE

K = 5

ratio = lambda a, b: "" if b == 0 else round(a / b, 4)


def main() -> None:
    period = PeriodRange()

    db = EventResultSelector()
    db.connect()

    period_end = period.end

    befores = sorted(
        day for day in period.range()
        if period.start <= day < period_end
    )

    with open(ANALYSIS_OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "period′", "period", "period-period′",
            "ΔL(zk-BAN)", "T(zk-BAN)",
            "ΔL_diff(related-work)", "T_diff(related-work)",
            "Innovation1(ΔL_diff/ΔL)",
            "Innovation2(ΔL/(T*K))",
            "Total(ΔL_diff/(T*K))",
        ])

        for before in befores:
            days = (period_end - before).days

            delta_l, t = db.select_zkban_params(before, period_end)
            delta_l_rw, t_rw = db.select_normal_params(before, period_end)

            w.writerow([
                before, period_end, days,
                delta_l, t,
                delta_l_rw, t_rw,
                ratio(delta_l_rw, delta_l),
                ratio(delta_l, t * K),
                ratio(delta_l_rw, t * K),
            ])

    print(f"period′ range: {period.start} <= period′ < {period_end}")
    print(f"wrote: {ANALYSIS_OUTPUT_FILE}")


if __name__ == "__main__":
    main()