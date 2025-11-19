from dataclasses import dataclass


@dataclass
class ProgressTracker:
    total: int
    finished: int

    def range(self):
        return range(self.total)
