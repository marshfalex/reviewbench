from enum import Enum


class SortColumn(str, Enum):
    """The only columns a list endpoint may sort by. Values are trusted SQL identifiers."""
    NAME = "name"
    CREATED = "created_at"
    PRICE = "price_cents"


def parse_sort(raw: str | None) -> SortColumn:
    """Map a ?sort= query value to a column; anything unknown falls back to NAME."""
    try:
        return SortColumn(raw)
    except ValueError:
        return SortColumn.NAME
