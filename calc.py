import sys
import argparse
import json
import datetime
from os import getcwd, chdir, path

class BrokerageCalculator:
    def __init__(self, buyPrice, sellPrice, qty):
        chdir(path.dirname(path.abspath(__file__)))
        self.buyPrice = float(buyPrice)
        self.sellPrice = float(sellPrice)
        self.qty = int(qty)
        self.turnover = (self.buyPrice * self.qty) + (self.sellPrice * self.qty)
        self.avgPrice = self.turnover / (self.qty * 2)
        self.order: str = ""
        directory = getcwd()
        self.journalFile = directory + "/journal.json"

    def _getMaxBrokerage(self, brokerage: float) -> float:
        return 40.0 if brokerage > 40.0 else brokerage

    def _getRiskRewardRatio(self, orderType: str, secondLeg: str) -> float:
        secondLeg = float(secondLeg)
        reward: float = 0.0
        risk: float = 0.0
        if orderType.lower() != 'b' and orderType.lower() != 's':
            print("Invalid order type.")
        if orderType.lower() == "b":
            risk = self.buyPrice - secondLeg
            reward = self.sellPrice - self.buyPrice
        else:
            risk = secondLeg - self.sellPrice
            reward = self.sellPrice - self.buyPrice

        return reward / risk

    def addOrder(self, orderType: str, secondLeg: str) -> None:
        ratio = self._getRiskRewardRatio(orderType, secondLeg)
        if ratio == 0.0:
            print("Something went wrong. Use -h for usage.")
        print(f"Reward:Risk ratio: {ratio}")
        now = datetime.datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")

        data = {
                "orderType": self.order,
                "position": orderType.lower(),
                "ratio": ratio,
                "time": time,
                "result": "P" if self.netProfit > 0 else "L",
                "netPL": self.netProfit,
                "quantity": self.qty
                }
        try:
            f = open(self.journalFile, "r")
            jsonD = json.load(f)
            if date not in jsonD:
                jsonD[date] = []
            f.close()
        except FileNotFoundError:
            jsonD = {}
            jsonD[date] = []
            pass

        f = open(self.journalFile, "w")
        jsonD[date].append(data)
        json.dump(jsonD, f, indent=4)

    def intradayEquity(self) -> None:
        self.order = "Intraday"
        brokerage = self.turnover * 0.0002
        brokerage = self._getMaxBrokerage(brokerage)
        sttCharges = self.qty * self.avgPrice * 0.00025
        sebiCharges = self.turnover * 0.000002
        stampCharges = self.qty * self.avgPrice * 0.00003
        exchangeCharges = self.turnover * 0.0000325

        totalCharges = brokerage + sttCharges + sebiCharges + stampCharges + exchangeCharges
        gst = totalCharges * 0.18
        self.netProfit = ((self.sellPrice - self.buyPrice) * self.qty) - (totalCharges + gst)
        pointsToBreakeven = (totalCharges + gst) / self.qty
        print(f"Total charges: {(totalCharges + gst)}")
        print(f"Points to break even: {pointsToBreakeven}")
        print(f"Net profit: {self.netProfit}")

    def deliveryEquity(self, days: int = 0, isCashPlus: bool = False) -> None:
        self.order = "Delivery"
        brokerage = self.turnover * 0.002
        brokerage = self._getMaxBrokerage(brokerage)
        sttCharges = self.qty * self.avgPrice * 0.00025
        sebiCharges = self.turnover * 0.000002
        stampCharges = self.qty * self.avgPrice * 0.00003
        exchangeCharges = self.turnover * 0.0000325
        if isCashPlus:
            self.order = "Delivery (Cash+)"
            interest = (self.turnover * 0.00025) * days
        else:
            interest = 0

        totalCharges = brokerage + sttCharges + sebiCharges + stampCharges + exchangeCharges + interest

        gst = totalCharges * 0.18

        self.netProfit = ((self.sellPrice - self.buyPrice) * self.qty) - (totalCharges + gst)
        pointsToBreakeven = (totalCharges + gst) / self.qty

        print(f"Total charges: {(totalCharges + gst)}")
        print(f"Points to break even: {pointsToBreakeven}")
        if isCashPlus:
            print(f"Total interest for {days} days: {interest}")
        print(f"Net profit: {self.netProfit}")

    def options(self) -> None:
        self.order = "Options"
        brokerage = 40.0
        sttCharges = self.qty * self.avgPrice * 0.0005
        sebiCharges = self.turnover * 0.000002
        stampCharges = self.qty * self.avgPrice * 0.00003
        exchangeCharges = self.turnover * 0.00053

        totalCharges = brokerage + sttCharges + sebiCharges + stampCharges + exchangeCharges
        gst = totalCharges * 0.18

        self.netProfit = ((self.sellPrice - self.buyPrice) * self.qty) - (totalCharges + gst)
        pointsToBreakeven = (totalCharges + gst) / self.qty

        print(f"Total charges: {(totalCharges + gst)}")
        print(f"Points to break even: {pointsToBreakeven}")
        print(f"Net profit: {self.netProfit}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brokerage Calculator")
    parser.add_argument("-i", "--intraday", help="For equities intraday.", nargs="*")
    parser.add_argument("-d", "--delivery", help="For equities delivery.", nargs="*")
    parser.add_argument("-c", "--cashplus", help="For cashplus delivery.", nargs="*")
    parser.add_argument("-o", "--options", help="For options delivery.", nargs="*")
    parser.add_argument("-a", "--addorder", help="Add this order to journal.", nargs="*")

    args = parser.parse_args()

    if args.intraday is not None:
        if len(sys.argv) < 5:
            print("Usage: calc -i [buyPrice] [sellPrice] [Qty]")
        else:
            calc = BrokerageCalculator(args.intraday[0], args.intraday[1], args.intraday[2])
            calc.intradayEquity()
            if args.addorder is not None:
                if len(args.addorder) < 2:
                    print("Usage: calc ... -a [orderType] B/S [TP/SL]")
                else:
                    calc.addOrder(args.addorder[0], args.addorder[1])

    elif args.delivery is not None:
        if len(sys.argv) < 5:
            print("Usage: calc -D [buyPrice] [sellPrice] [Qty]")
        else:
            calc = BrokerageCalculator(args.delivery[0], args.delivery[1], args.delivery[2])
            calc.deliveryEquity()
            if args.addorder is not None:
                if len(args.addorder) < 2:
                    print("Usage: calc ... -a [orderType] B/S [TP/SL]")
                else:
                    calc.addOrder(args.addorder[0], args.addorder[1])

    elif args.cashplus is not None:
        if len(sys.argv) < 6:
            print("Usage: calc -c [buyPrice] [sellPrice] [Qty] [Days]")
        else:
            calc = BrokerageCalculator(args.cashplus[0], args.cashplus[1], args.cashplus[2])
            calc.deliveryEquity(days=args.cashplus[3], isCashPlus=True)
            if args.addorder is not None:
                if len(args.addorder) < 2:
                    print("Usage: calc ... -a [orderType] B/S [TP/SL]")
                else:
                    calc.addOrder(args.addorder[0], args.addorder[1])

    elif args.options is not None:
        if len(sys.argv) < 5:
            print("Usage: calc -o [buyPrice] [sellPrice] [Qty]")
        else:
            calc = BrokerageCalculator(args.options[0], args.options[1], args.options[2])
            calc.options()
            if args.addorder is not None:
                if len(args.addorder) < 2:
                    print("Usage: calc ... -a [orderType] B/S [TP/SL]")
                else:
                    calc.addOrder(args.addorder[0], args.addorder[1])

    else:
        print("Something went wrong. Please refer to help menu.")

