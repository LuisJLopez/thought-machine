import sys

from auction_processor import AuctionProcessor
from input_row_processor import InputRowProcessor
from output_row_processor import OutputRowProcessor

INPUT_FILE: str = sys.argv[1]


def main():
    """_summary_"""

    auction_processor: AuctionProcessor = AuctionProcessor(
        INPUT_FILE, InputRowProcessor, OutputRowProcessor
    )
    auction_processor.process()


if __name__ == "__main__":
    """Script requires Python 3.9.5"""
    main()
