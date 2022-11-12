import sys

from input_row_processor import InputRowProcessor
from auction_processor import AuctionProcessor

INPUT_FILE: str = sys.argv[1]


def main():
    """_summary_"""

    auction_processor: AuctionProcessor = AuctionProcessor(
        INPUT_FILE, InputRowProcessor
    )
    auction_processor.process()


if __name__ == "__main__":
    """Script requires Python 3.9.5"""
    main()
