import sys

from auction_processor import AuctionProcessor
from input_row_processor import InputRowProcessor
from output_row_processor import OutputRowProcessor


def main():
    """Main project entrypoint"""

    # fetch input supplied path as cmd line argument
    input_file: str = sys.argv[1]

    auction_processor: AuctionProcessor = AuctionProcessor(
        input_file, InputRowProcessor, OutputRowProcessor
    )

    # output
    [print(i) for i in auction_processor.process()]


if __name__ == "__main__":
    """Script requires Python 3.9.5"""
    main()
