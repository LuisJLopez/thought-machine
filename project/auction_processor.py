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
        # output_row_processor: OutputRowProcessor = self.output_row_processor()

        # process one line at a time - don't load everything into memory!
        # 16MB buffer for quicker file operations
        # assuming we aren't CPU limited but rather I/O limited
        with open(self.input_file, "r", buffering=self.buffer_capacity) as rows:
            for row in rows:

                row_type, parsed_input = input_row_processor.parse_input_row(row)
                # print(row_type, parsed_input)

                current_time = parsed_input.get("timestamp")

                if row_type == InputType.SELL.name:
                    self._store_sell_orders(parsed_input)

                # make sure you invalid bids before sales
                # invalid bids before sales
                if row_type == InputType.BID.name:
                    if valid_bid := self._validate_bid(current_time, parsed_input):
                        self._process_bid(valid_bid)
                # bid_expirery_store = {}

                # you can only bid if there is a sell (which means open and it has not closed yet)

                # print(row_type, parsed_input)

    def _store_sell_orders(self, order: dict) -> None:
        self.sell_order_registry[order["item"]] = dict(
            opening=order["timestamp"],
            close_time=order["close_time"],
            reserve_price=order["reserve_price"],
        )
        # Acting like the auction house bid
        self.bid_order_registry[order["item"]] = dict(
            current_highest_bid=order["reserve_price"],
        )

    def _validate_bid(self, current_time, bid: dict) -> bool:
        # FIXME return type
        # Should I rename this to process bid?
        # when did the sell started?
        # check in self.sell_time

        # Validating the bid happens after SELL before CLOSE tie
        # get the sell order we are bidding for and check if valid
        sell_order: dict = self.sell_order_registry[bid["item"]]

        # print("#", sell_order)
        # print("####", bid)

        # add a test for this logic
        #
        if sell_order["opening"] < bid.get("timestamp") <= sell_order["close_time"]:
            # you can still bid
            return bid

        return False

    def _process_bid(self, bid: dict) -> None:
        # WE ASSUME THERE IS ALREADY A SALE
        # if the BID IS BIGGER than the existing one
        # if the Bid above the reserve price?
        # only a new highest bidder if
        # aggregate data while running - update counters

        # if we have a higher bid, above reserve_price, process it
        if (
            bid["bid_amount"]
            > self.bid_order_registry[bid["item"]]["current_highest_bid"]
        ) and (
            bid["bid_amount"] > self.sell_order_registry[bid["item"]]["reserve_price"]
        ):

            self.bid_order_registry[bid["item"]] = dict(
                current_highest_bid=bid["bid_amount"]
            )
            # CALL CLASS OUTPUT and update values each time for output
            # close_time
            # item
            # user_id
            # status
            # price_paid
            # number
            # total_bid_count
            # highest_bid
            # lowest_bid
