from dataclasses import dataclass
from enum import Enum


@dataclass
class JobStatus:
    """Contains the status of a job in a more readable format."""
    status: str
    date: str


class TimeRange(Enum):
    """Enum to help with the time range field in the public job search."""
    ANY = "Any time"
    DAY = "Past 24 hours"
    WEEK = "Past week"
    MONTH = "Past month"
    YEAR = "Past year"
