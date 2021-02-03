# Methodology
#
# This test get the symbols from IEX Cloud and try to download histrical price of those symbols from the Yahoo! Finance.
#
# Some symbols may not avalible on Yahoo! Finacne Server.
# So only 90% symbols pass the test is required for the whole test.
#
# Since doing the full test on all symbols was taking too much times,
# we only extract 10% symbols randomly for the test.

import iexcloudapi
import yfapi
import random


class RunTest:

    def __init__(self):
        self.get_symbols_from_iexcloud()
        self.choose_symbols_randomly()
        self.count_pass = 0
        self.count_fail = 0
        while len(self.symbols) > 0:
            print("pass: {} | fail: {} | remaining: {}".format(
                self.count_pass, self.count_fail, len(self.symbols)))
            check = self.try_request_to_yfserver()
            if check == True:
                self.count_pass += 1
            else:
                self.count_fail += 1
        if self.count_pass / (self.count_pass + self.count_fail) > 0.9:
            print("test result: PASS")
        else:
            print("test result: <<<<FAIL>>>>")

    def get_symbols_from_iexcloud(self):
        while True:
            try:
                token = input("Please enter IEX token: >")
                self.iexsymbols = iexcloudapi.getSymbols(token)
                break
            except:
                print()
                print("Error on token, Please try again:")

    def choose_symbols_randomly(self):
        # we randomly take 10% from all symbols
        random.shuffle(self.iexsymbols)
        self.symbols = self.iexsymbols[:int(len(self.iexsymbols)*0.1)]

    def try_request_to_yfserver(self) -> bool:
        symbol = self.symbols.pop()
        query = yfapi.YFAPI(symbol)
        self.result = query.price()
        if len(self.result) == 0:
            return False
        return True


if __name__ == "__main__":
    RunTest()
