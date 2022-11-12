from typing import List
from constants import StatusEnum


class OutputRowProcessor:
    """_summary_"""

    def process_output(self, sales_data, bids_data) -> List[str]:
        """_summary_

        Args:
            sales_data (_type_): _description_
            bids_data (_type_): _description_

        Returns:
            List[str]: _description_
        """
        results: List[str] = []

        for item, v in sales_data.items():
            close_time: int = v.get("close_time")
            highest_bid: float = self._format(bids_data[item]["highest_bid"])
            is_sold = (
                StatusEnum.SOLD.name
                if highest_bid > self._format(sales_data[item]["reserve_price"])
                else StatusEnum.UNSOLD.name
            )
            highest_bidder: str = (
                bids_data[item]["highest_bidder"]
                if is_sold == StatusEnum.SOLD.name
                else ""
            )
            bid_count: int = bids_data[item]["valid_bid_counter"]
            lowest_bid: float = self._format(bids_data[item]["lowest_bid"])
            price_paid: float = (
                self._format(0.00)
                if is_sold == StatusEnum.UNSOLD.name
                else self._format(float(highest_bid) - float(lowest_bid))
            )

            results.append(
                f"{close_time}|{item}|{highest_bidder}|{is_sold}|{price_paid}|{bid_count}|{highest_bid}|{lowest_bid}"
            )
        return results

    def _format(self, string: str) -> str:
        return "{:.2f}".format(string)
