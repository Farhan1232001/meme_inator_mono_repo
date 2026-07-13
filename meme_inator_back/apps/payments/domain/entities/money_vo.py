from dataclasses import dataclass


@dataclass(frozen=True)
class MoneyVo:
    amt_cents: int
    currency: str

    def to_major_units(self) -> float:
        return self.amt_cents / 100.0

    def format(self) -> str:
        return f"${self.to_major_units():.2f} {self.currency}"