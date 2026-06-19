from decimal import Decimal


def rupees_to_paise(amount: Decimal) -> int:
    return int(amount * 100)


def paise_to_rupees(paise: int) -> Decimal:
    return Decimal(paise) / Decimal(100)
