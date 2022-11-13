from unittest import TestCase

from project.auction_processor import AuctionProcessor
from project.input_row_processor import InputRowProcessor
from project.output_row_processor import OutputRowProcessor


class AuctionHouseTestCase(TestCase):
    def test_provided_input_pass(self):
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

    def test_bids_before_during_pass(self):
        provided_input_file = "inputs/input_bid_on_heartbeat.txt"

        auction_processor: AuctionProcessor = AuctionProcessor(
            provided_input_file, InputRowProcessor, OutputRowProcessor
        )
        results = auction_processor.process()
        self.assertEqual(
            results,
            [
                "20|toaster_1|8|SOLD|20.01|5|22.22|7.50",
            ],
        )

    def test_bid_on_close_pass(self):
        # bid on close is valid
        # only one bid = winner = price to pay is reserve price
        provided_input_file = "inputs/input_bid_after_close.txt"

        auction_processor: AuctionProcessor = AuctionProcessor(
            provided_input_file, InputRowProcessor, OutputRowProcessor
        )
        results = auction_processor.process()
        self.assertEqual(
            results,
            [
                "20|toaster_1|8|SOLD|10.00|1|22.00|22.00",
            ],
        )

    def test_sold_unsold_pass(self):
        provided_input_file = "inputs/input_sold_unsold.txt"

        auction_processor: AuctionProcessor = AuctionProcessor(
            provided_input_file, InputRowProcessor, OutputRowProcessor
        )
        results = auction_processor.process()
        self.assertEqual(
            results,
            [
                "8|macbook_1||UNSOLD|0.00|0|0.00|0.00",
                "7|fridge_1||UNSOLD|0.00|0|0.00|0.00",
                "20|coffee_machine_1||UNSOLD|0.00|0|0.00|0.00",
                "20|toaster_1|8|SOLD|12.50|3|20.00|7.50",
                "22|tv_1|3|SOLD|200.00|3|300.00|150.00",
            ],
        )

    def test_multiple_bidders_pass(self):
        # first highest bidder is the winner
        # also if there is only one bidder - reserve price is the paid price
        provided_input_file = "inputs/input_multiple_bidders.txt"

        auction_processor: AuctionProcessor = AuctionProcessor(
            provided_input_file, InputRowProcessor, OutputRowProcessor
        )
        results = auction_processor.process()
        self.assertEqual(
            results,
            [
                "20|toaster_1|2|SOLD|11.11|1|22.00|22.00",
            ],
        )

    def test_second_highest_bid_pass(self):
        # second biggest bid is the price to pay
        # if SOLD and there is 1 valid bid - then reserve price else 0.00
        provided_input_file = "inputs/input_second_bid.txt"

        auction_processor: AuctionProcessor = AuctionProcessor(
            provided_input_file, InputRowProcessor, OutputRowProcessor
        )
        results = auction_processor.process()
        self.assertEqual(
            results,
            [
                "20|toaster_1|2|SOLD|1000.00|1|2000.00|2000.00",
            ],
        )
