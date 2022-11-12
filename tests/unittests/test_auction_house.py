from unittest import TestCase

from project.auction_processor import AuctionProcessor
from project.input_row_processor import InputRowProcessor
from project.output_row_processor import OutputRowProcessor


class AuctionHouseTestCase(TestCase):
    def test_provided_input_passes(self):
        provided_input_file = "inputs/input.txt"

        auction_processor: AuctionProcessor = AuctionProcessor(
            provided_input_file, InputRowProcessor, OutputRowProcessor
        )
        results = auction_processor.process()
        self.assertEqual(
            results,
            [
                "20|toaster_1|8|SOLD|12.50|3|20.00|7.50",
                "20|tv_1||UNSOLD|0.00|2|200.00|150.00",
            ],
        )

    def test_complex_input_passes(self):
        provided_input_file = "inputs/input.txt"

        auction_processor: AuctionProcessor = AuctionProcessor(
            provided_input_file, InputRowProcessor, OutputRowProcessor
        )
        results = auction_processor.process()
        self.assertEqual(
            results,
            [
                "20|toaster_1|8|SOLD|12.50|3|20.00|7.50",
                "20|tv_1||UNSOLD|0.00|2|200.00|150.00",
            ],
        )
