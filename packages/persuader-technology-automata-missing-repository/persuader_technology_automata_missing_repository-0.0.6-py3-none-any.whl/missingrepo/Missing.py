from dataclasses import dataclass

from core.market.Market import Market
from core.missing.Context import Context


@dataclass
class Missing:
    missing: str
    context: Context
    market: Market
    description: str

    def __eq__(self, other):
        return f'{self.missing}{self.context.value}{self.market.value}' == f'{other.missing}{other.context.value}{other.market.value}'
