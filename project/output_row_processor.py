from typing import Tuple
from constants import InputType


class OutputRowProcessor:
    """_summary_"""

    def __init__(self) -> None:
        # self.store = []
        pass

    def aggregate_order_book(self, bid_data, sell_data):
        # """Record the order book for output purposes"""
        # output_store = []

        # print("bid", bid_data)
        # print("sell", sell_data)
        # for item in sell_data:

        #         dict(
        #             item=item,
        #             # user_id=item,
        #             # status=item,
        #             # price_paid=item,
        #             # total_bid_count=item,
        #             # highest_bid=item,
        #             # lowest_bid=item,
        #         )
        #     )
        pass

    def format_output(self) -> str:
        # data = self.store
        # return ""
        pass

        # item
        # user_id
        # status
        # price_paid
        # total_bid_count
        # highest_bid
        # lowest_bid
        # 20|toaster_1|8|SOLD|12.50|3|20.00|7.50
        # 20|tv_1||UNSOLD|0.00|2|200.00|150.00
        # |{data["item"]}"
        # {data["user_id"]}|{data["status"]}|{data["price_paid"]}|{data["number"]}|{data["total_bid_count"]}|{data["highest_bid"]}|{data["lowest_bid"]}"
