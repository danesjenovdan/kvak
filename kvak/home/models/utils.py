from dataclasses import dataclass


@dataclass
class ProgressTracker:
    total: int
    finished: int
    total_ids: list[str] | None = None
    finished_ids: list[str] | None = None

    def range(self):
        return range(self.total)
