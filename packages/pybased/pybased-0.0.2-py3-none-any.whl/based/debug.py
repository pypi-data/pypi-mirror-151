DEBUG: bool = False

def _debugprint(*msg) -> None:
    if DEBUG:
        print(*msg)