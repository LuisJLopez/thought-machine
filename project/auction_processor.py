from typing import List

from constants import SIXTEEN_MB_IN_BINARY_BYTES, ZERO_FLOAT, ZERO_INT, InputType
from input_row_processor import InputRowProcessor
from output_row_processor import OutputRowProcessor


class AuctionProcessor:
    def __init__(
        # """A class to represent the auction house"""
        self,
        input_file: str,
        input_row_processor: InputRowProcessor,
        output_row_processor: OutputRowProcessor,
    ) -> None:
        self.input_file: str = input_file
        self.input_row_processor: InputRowProcessor = input_row_processor
        self.output_row_processor: OutputRowProcessor = output_row_processor
        self.buffer_capacity: int = SIXTEEN_MB_IN_BINARY_BYTES
        self.sell_registry: dict = dict()
        self.bid_registry: dict = dict()

    def process(self) -> List[str]:
        input_row_processor: InputRowProcessor = self.input_row_processor()

        # assuming we aren't CPU limited but rather I/O limited - faster file operations
        with open(self.input_file, "r", buffering=self.buffer_capacity) as rows:
            # process one line at a time - avoiding loading everything into memory
            for row in rows:
                row_type, parsed_input = input_row_processor.parse_input_row(row)

                if row_type == InputType.SELL.name:
                    self._store_sell_orders(parsed_input)

                if row_type == InputType.BID.name:
                    self._process_bid(parsed_input)

        output_row_processor: OutputRowProcessor = self.output_row_processor()

        return output_row_processor.process_output(
            self.sell_registry, self.bid_registry
        )

    def _store_sell_orders(self, sell_order: dict) -> None:
        # keep sell registry updated with all sell orders
        self.sell_registry[sell_order["item"]] = dict(
            opening=sell_order["timestamp"],
            close_time=sell_order["close_time"],
            reserve_price=sell_order["reserve_price"],
        )
        # add bid registery sekelton
        self.bid_registry[sell_order["item"]] = dict(
            reserve_price=sell_order["reserve_price"],
            highest_bid=ZERO_FLOAT,  # fix this magical float number
            highest_bidder="",  # remove magic default number DEFAULT
            valid_bid_counter=ZERO_INT,
        )

    def _process_bid(self, bid: dict) -> None:
        """
        Responsabilities:
            - validate bids
            - update bid order registry with latest data for future data aggregation
        """

        # ignore when bid is done before sell is live
        if bid["item"] not in self.sell_registry.keys():
            return

        sell_order: dict = self.sell_registry[bid["item"]]
        current_highest_big: float = self.bid_registry[bid["item"]]["highest_bid"]
        new_bid_amount: float = bid["bid_amount"]

        # bid validation
        if (
            sell_order["opening"] < bid.get("timestamp") <= sell_order["close_time"]
        ) and (new_bid_amount > current_highest_big):

            bid_details: dict = self.bid_registry[bid["item"]]
            current_bid_counter: int = bid_details["valid_bid_counter"]

            # update bid registry with validated bid
            self.bid_registry[bid["item"]].update(
                highest_bid=bid["bid_amount"],
                highest_bidder=bid["user_id"],
                valid_bid_counter=current_bid_counter + 1,
            )

            # only update bid registry whith lowest bid or if there is not lowest bid
            if (
                "lowest_bid" not in bid_details.keys()
                or bid["bid_amount"] < bid_details["lowest_bid"]
            ):
                self.bid_registry[bid["item"]].update(lowest_bid=bid["bid_amount"])
