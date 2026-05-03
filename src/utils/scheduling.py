BITMASK = [1, 2, 4, 8, 16, 32, 64]

def days_to_int(days: list[int]) -> int:
    return sum([BITMASK[day-1] for day in days])

def int_to_days(value: int) -> list[int]:
    result = []
    for item in BITMASK:
        if value & item:
            result.append(BITMASK.index(item)+1)
    return result