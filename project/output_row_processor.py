from typing import List

from constants import ZERO_FLOAT, StatusEnum


class OutputRowProcessor:
    """
    The responsabilty of this class is to group and calculate all values and return
    the formatted output.
    """

    def process_output(self, sales_data, bids_data) -> List[str]:
        results: List[str] = []

        for item, v in sales_data.items():
            close_time: int = v.get("close_time")
            highest_bid: float = self._decimal_format(bids_data[item]["highest_bid"])
            reserve_price = self._decimal_format(sales_data[item]["reserve_price"])
            # determine if item has been sold
            is_sold = (
                StatusEnum.SOLD.name
                if highest_bid > reserve_price
                else StatusEnum.UNSOLD.name
            )
            # determine highest bidder
            highest_bidder: str = (
                bids_data[item]["highest_bidder"]
                if is_sold == StatusEnum.SOLD.name
                else ""
            )
            bid_count: int = bids_data[item]["valid_bid_counter"]
            lowest_bid: float = self._decimal_format(
                bids_data[item].get("lowest_bid", ZERO_FLOAT)
            )
            second_highest_bid = self._decimal_format(
                float(bids_data[item].get("second_highest_bid", ZERO_FLOAT))
            )

            # determine the price paid
            price_paid: float = (
                self._decimal_format(ZERO_FLOAT)
                if is_sold == StatusEnum.UNSOLD.name
                and second_highest_bid < reserve_price
                else self._decimal_format(float(bids_data[item]["second_highest_bid"]))
            )

            # output string
            results.append(
                f"{close_time}|{item}|{highest_bidder}|{is_sold}|{price_paid}|{bid_count}|{highest_bid}|{lowest_bid}"
            )
        return results

    def _decimal_format(self, string: str) -> str:
        return "{:.2f}".format(string)
