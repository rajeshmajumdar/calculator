import sys
import argparse

class BrokerageCalculator:
    def __init__(self, buyPrice, sellPrice, qty):
        self.buyPrice = float(buyPrice)
        self.sellPrice = float(sellPrice)
        self.qty = int(qty)
        self.turnover = (self.buyPrice * self.qty) + (self.sellPrice * self.qty)
        self.avgPrice = self.turnover / (self.qty * 2)

    def _getMaxBrokerage(self, brokerage: float) -> float:
        return 40.0 if brokerage > 40.0 else brokerage

    def intradayEquity(self) -> None:
        brokerage = self.turnover * 0.0002
        brokerage = self._getMaxBrokerage(brokerage)
        sttCharges = self.qty * self.avgPrice * 0.00025
        sebiCharges = self.turnover * 0.000002
        stampCharges = self.qty * self.avgPrice * 0.00003
        exchangeCharges = self.turnover * 0.0000325

        totalCharges = brokerage + sttCharges + sebiCharges + stampCharges + exchangeCharges
        gst = totalCharges * 0.18
        netProfit = ((self.sellPrice - self.buyPrice) * self.qty) - (totalCharges + gst)
        pointsToBreakeven = (totalCharges + gst) / self.qty
        print(f"Total charges: {(totalCharges + gst)}")
        print(f"Points to break even: {pointsToBreakeven}")
        print(f"Net profit: {netProfit}")

    def deliveryEquity(self, days: int = 0, isCashPlus: bool = False) -> None:
        brokerage = self.turnover * 0.002
        brokerage = self._getMaxBrokerage(brokerage)
        sttCharges = self.qty * self.avgPrice * 0.00025
        sebiCharges = self.turnover * 0.000002
        stampCharges = self.qty * self.avgPrice * 0.00003
        exchangeCharges = self.turnover * 0.0000325
        if isCashPlus:
            interest = (self.turnover * 0.00025) * days
        else:
            interest = 0

        totalCharges = brokerage + sttCharges + sebiCharges + stampCharges + exchangeCharges + interest

        gst = totalCharges * 0.18

        netProfit = ((self.sellPrice - self.buyPrice) * self.qty) - (totalCharges + gst)
        pointsToBreakeven = (totalCharges + gst) / self.qty

        print(f"Total charges: {(totalCharges + gst)}")
        print(f"Points to break even: {pointsToBreakeven}")
        if isCashPlus:
            print(f"Total interest for {days} days: {interest}")
        print(f"Net profit: {netProfit}")

    def options(self) -> None:
        brokerage = 40.0
        sttCharges = self.qty * self.avgPrice * 0.0005
        sebiCharges = self.turnover * 0.000002
        stampCharges = self.qty * self.avgPrice * 0.00003
        exchangeCharges = self.turnover * 0.00053

        totalCharges = brokerage + sttCharges + sebiCharges + stampCharges + exchangeCharges
        gst = totalCharges * 0.18

        netProfit = ((self.sellPrice - self.buyPrice) * self.qty) - (totalCharges + gst)
        pointsToBreakeven = (totalCharges + gst) / self.qty

        print(f"Total charges: {(totalCharges + gst)}")
        print(f"Points to break even: {pointsToBreakeven}")
        print(f"Net profit: {netProfit}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Samco Brokerage Calculator")
    parser.add_argument("-i", "--intraday", help="For equities intraday.", nargs="*")
    parser.add_argument("-d", "--delivery", help="For equities delivery.", nargs="*")
    parser.add_argument("-c", "--cashplus", help="For cashplus delivery.", nargs="*")
    parser.add_argument("-o", "--options", help="For options intraday/delivery.", nargs="*")

    args = parser.parse_args()

    if args.intraday is not None:
        if len(sys.argv) != 5:
            print("Usage: calc -i [buyPrice] [sellPrice] [Qty]")
        else:
            calc = BrokerageCalculator(args.intraday[0], args.intraday[1], args.intraday[2])
            calc.intradayEquity()
    elif args.delivery is not None:
        if len(sys.argv) != 5:
            print("Usage: calc -D [buyPrice] [sellPrice] [Qty]")
        else:
            calc = BrokerageCalculator(args.delivery[0], args.delivery[1], args.delivery[2])
            calc.deliveryEquity()
    elif args.cashplus is not None:
        if len(sys.argv) != 6:
            print("Usage: calc -c [buyPrice] [sellPrice] [Qty] [Days]")
        else:
            calc = BrokerageCalculator(args.cashplus[0], args.cashplus[1], args.cashplus[2])
            calc.deliveryEquity(days=args.cashplus[3], isCashPlus=True)
    elif args.options is not None:
        if len(sys.argv) != 5:
            print("Usage: calc -o [buyPrice] [sellPrice] [Qty]")
        else:
            calc = BrokerageCalculator(args.options[0], args.options[1], args.options[2])
            calc.options()
    else:
        print("Something went wrong. Please refer to help menu.")

