from typing import List

from constants import ZERO_FLOAT, StatusEnum


class OutputRowProcessor:
    """
    The responsabilty of this class is to group and calculate all values and return
    the formatted output.
    """

    def process_output(self, sales: dict, bids: dict) -> List[str]:
        results: List[str] = []

        for item, data in sales.items():
            # for every item - we only have one sell order and one bid order stored
            bid_order: dict = bids[item]
            close_time: int = data.get("close_time")

            highest_bid: float = self._decimal_format(bid_order["highest_bid"])
            reserve_price: float = self._decimal_format(sales[item]["reserve_price"])

            is_sold = (
                StatusEnum.SOLD.name
                if highest_bid > reserve_price
                else StatusEnum.UNSOLD.name
            )

            highest_bidder: str = (
                bid_order["highest_bidder"] if is_sold == StatusEnum.SOLD.name else ""
            )
            bid_count: int = bid_order["valid_bid_counter"]

            lowest_bid: float = self._decimal_format(
                bid_order.get("lowest_bid", ZERO_FLOAT)
            )
            second_highest_bid = self._decimal_format(
                float(bid_order.get("second_highest_bid", ZERO_FLOAT))
            )

            # determine the price paid
            price_paid: float = (
                self._decimal_format(ZERO_FLOAT)
                if is_sold == StatusEnum.UNSOLD.name
                and second_highest_bid < reserve_price
                else self._decimal_format(float(bid_order["second_highest_bid"]))
            )
            if bid_count == 1 and is_sold == StatusEnum.SOLD.name:
                price_paid = reserve_price

            # output string
            results.append(
                f"{close_time}|{item}|{highest_bidder}|{is_sold}|{price_paid}|{bid_count}|{highest_bid}|{lowest_bid}"
            )
        return results

    def _decimal_format(self, string: str) -> str:
        return "{:.2f}".format(string)
