from dataclasses import dataclass


@dataclass
class ProgressTracker:
    total: int
    finished: int
