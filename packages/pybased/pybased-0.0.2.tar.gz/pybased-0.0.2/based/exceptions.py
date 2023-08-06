

class InvalidArgumentError(Exception):
    pass

class NotWholeNumberError(Exception):
    def __init__(self, stdid: str, attr: str, value: float) -> None:
        super().__init__(stdid, attr, value) 
        self.stdid: str = stdid
        self.attr: str = attr
        self.value: float = value

    def __str__(self) -> str:
        return f'Cannot use _SlidingWindowBaseConverter for {self.stdid}: {self.attr} == {self.value!r}, which is not a whole number.'
