from enum import Enum, auto


class InputType(Enum):
    SELL: str = auto()
    BID: str = auto()
    HEARTBEAT: str = auto()


SIXTEEN_MB_IN_BINARY_BYTES: int = 16777216  # 16MB
