from typing import Tuple
from constants import InputType


class InputRowProcessor:
    """_summary_"""

    def __init__(self) -> None:
        pass

    def parse_input_row(self, row: str) -> Tuple[InputType, dict]:

        row = row.rstrip("\n").split("|")
        row_type: str = self._get_row_type(row)

        if InputType.HEARTBEAT.name == row_type:
            return InputType.HEARTBEAT.name, {"timestamp": int(row[0])}
        elif InputType.SELL.name == row_type:
            return (
                InputType.SELL.name,
                {
                    "timestamp": int(row[0]),
                    "user_id": row[1],
                    "action": row[2],
                    "item": row[3],
                    "reserve_price": float(row[4]),
                    "close_time": int(row[5]),
                },
            )

        elif InputType.BID.name == row_type:
            return (
                InputType.BID.name,
                {
                    "timestamp": int(row[0]),
                    "user_id": row[1],
                    "action": row[2],
                    "item": row[3],
                    "bid_amount": float(row[4]),
                },
            )

        else:
            # input row is not recognised - don't process it
            return

    def _get_row_type(self, input_row: list) -> str:
        if len(input_row) == 1:
            return InputType.HEARTBEAT.name
        if input_row[2] == InputType.SELL.name:
            return InputType.SELL.name
        if input_row[2] == InputType.BID.name:
            return InputType.BID.name
