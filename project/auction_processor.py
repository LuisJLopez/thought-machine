from input_row_processor import InputRowProcessor
from constants import SIXTEEN_MB_IN_BINARY_BYTES, InputType


class AuctionProcessor:
    """Auction House"""

    def __init__(self, input_file: str, input_row_processor: InputRowProcessor) -> None:
        self.input_file = input_file
        self.input_row_processor = input_row_processor
        self.buffer_capacity = SIXTEEN_MB_IN_BINARY_BYTES

    def process(self) -> None:
        input_row_processor: InputRowProcessor = self.input_row_processor()

        # process one line at a time - don't load everything into memory!
        # 16MB buffer for quicker file operations
        # assuming we aren't CPU limited but rather I/O limited
        with open(self.input_file, "r", buffering=self.buffer_capacity) as rows:
            for row in rows:
                _type, parsed_input = input_row_processor.parse_input_row(row)
                print(_type, parsed_input)
        # print(parsed_input)
