from typing import List
from input_row_processor import InputRowProcessor
from output_row_processor import OutputRowProcessor
from constants import SIXTEEN_MB_IN_BINARY_BYTES, InputType


class AuctionProcessor:
    """Auction House"""

    def __init__(
        self,
        input_file: str,
        input_row_processor: InputRowProcessor,
        output_row_processor: OutputRowProcessor,
    ) -> None:
        # review if storing all of this here is ok
        self.input_file = input_file
        self.input_row_processor = input_row_processor
        self.output_row_processor = output_row_processor
        self.buffer_capacity = SIXTEEN_MB_IN_BINARY_BYTES
        self.sell_order_registry = dict()
        self.bid_order_registry = dict()

    def process(self):
        # FIXME RETURN TYPE
        input_row_processor: InputRowProcessor = self.input_row_processor()
        output_row_processor: OutputRowProcessor = self.output_row_processor()

        # process one line at a time - don't load everything into memory!
        # 16MB buffer for quicker file operations
        # assuming we aren't CPU limited but rather I/O limited
        with open(self.input_file, "r", buffering=self.buffer_capacity) as rows:
            for row in rows:

                row_type, parsed_input = input_row_processor.parse_input_row(row)

                if row_type == InputType.SELL.name:
                    self._store_sell_orders(parsed_input)

                # make sure you invalid bids before sales
                # invalid bids before sales
                if row_type == InputType.BID.name:
                    if valid_bid := self._validate_bid(parsed_input):
                        self._process_bid(valid_bid)

        return self._process_output()

    def _store_sell_orders(self, order: dict) -> None:
        self.sell_order_registry[order["item"]] = dict(
            opening=order["timestamp"],
            close_time=order["close_time"],
            reserve_price=order["reserve_price"],
        )
        # Acting like the auction house bid
        self.bid_order_registry[order["item"]] = dict(
            reserve_price=order["reserve_price"],
            highest_bid=0.00,  # fix this magical float number
            highest_bidder="",
            lowest_bid=980989080989080.00,  # remove magic default number DEFAULT
            valid_bid_counter=0,
        )

    def _validate_bid(self, bid: dict) -> bool:
        # FIXME return type
        # Should I rename this to process bid?
        # when did the sell started?
        # check in self.sell_time

        # Validating the bid happens after SELL before CLOSE tie
        # get the sell order we are bidding for and check if valid

        sell_order: dict = self.sell_order_registry[bid["item"]]
        current_highest_big: float = self.bid_order_registry[bid["item"]]["highest_bid"]
        new_bid_amount: float = bid["bid_amount"]

        # add a test for this logic
        ## if we have a higher bid, above reserve_price, within the time correct frames
        if (
            sell_order["opening"] < bid.get("timestamp") <= sell_order["close_time"]
        ) and (new_bid_amount > current_highest_big):
            # Your bid is valid
            return bid

        return False

    def _process_bid(self, bid: dict) -> None:
        # WE ASSUME THERE IS ALREADY A SALE
        #  AND ALL BIDS ARE VALID == new highest bid
        # aggregate data while running - update counters
        bid_details = self.bid_order_registry[bid["item"]]
        current_bid_counter: int = bid_details["valid_bid_counter"]

        # update bid store
        self.bid_order_registry[bid["item"]].update(
            highest_bid=bid["bid_amount"],
            highest_bidder=bid["user_id"],
            valid_bid_counter=current_bid_counter + 1,
        )
        # only update bid store with lowest bid when the bid is lower
        if bid["bid_amount"] < bid_details["lowest_bid"]:
            self.bid_order_registry[bid["item"]].update(lowest_bid=bid["bid_amount"])

    def _process_output(self):
        results: List[str] = []
        sales: dict = self.sell_order_registry
        bids: dict = self.bid_order_registry
        for item, v in sales.items():
            close_time: int = v.get("close_time")
            highest_bid: float = "{:.2f}".format(bids[item]["highest_bid"])
            is_sold = (
                "SOLD"
                if highest_bid > "{:.2f}".format(sales[item]["reserve_price"])
                else "UNSOLD"
            )
            highest_bidder: str = (
                bids[item]["highest_bidder"] if is_sold == "SOLD" else ""
            )
            bid_count: int = bids[item]["valid_bid_counter"]
            lowest_bid: float = "{:.2f}".format(bids[item]["lowest_bid"])
            price_paid: float = (
                "{:.2f}".format(0.00)
                if is_sold == "UNSOLD"
                else "{:.2f}".format(float(highest_bid) - float(lowest_bid))
            )

            results.append(
                f"{close_time}|{item}|{highest_bidder}|{is_sold}|{price_paid}|{bid_count}|{highest_bid}|{lowest_bid}"
            )
        return results
        # 20|toaster_1|8|SOLD|12.50|3|20.00|7.50
        # 20|tv_1||UNSOLD|0.00     |2|200.00|150.00
