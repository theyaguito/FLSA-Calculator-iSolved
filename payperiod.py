from __future__ import annotations
from typing import List


class PayPeriod:

    frequencies: List[str] = [
        "weekly",
        "biweekly",
        "semimonthly",
        "monthly",
        "quarterly",
        "annually",
    ]

    def __init__(self, frequency: str | None) -> None:
        if frequency is None:
            raise TypeError("Frequency cannot be None type")
        if frequency not in self.frequencies:
            raise ValueError("Invalid frequency type")
        self.frequency: str = frequency
        self.threshold: float | None = None
        match frequency:
            case "weekly":
                self.threshold = 40.00
            case "biweekly":
                self.threshold = 80.00
            case "semimonthly":
                self.threshold = 86.67
            case "monthly":
                self.threshold = 173.33
            case "quarterly":
                self.threshold = 520.00
            case "annually":
                self.threshold = 2080.00
