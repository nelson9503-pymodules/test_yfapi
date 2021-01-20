# Methodology
#
# We download the symbols from iexcloudapi and try to query them via yfapi.
# Some symbols may not avalible on Yahoo! Finance Server,
# so the test pass if more than 90% of symbols were query successfully.
#
# Since do the full test was taking too much time, we only do the sample test.
# We randomly choose 10% symbol to do the test.

import iexcloudapi
import yfapi
import random
import threading


def TestMain():

    token = input("Please enter IEX token: >")
    iexsymbols = iexcloudapi.getSymbols(token)

    # randomly take 10% samples
    random.shuffle(iexsymbols)
    global symbols
    symbols = iexsymbols[:int(len(iexsymbols)*0.1)]

    global total
    global success
    global fail
    global count
    global failsymbols
    total = len(symbols)
    success = 0
    fail = 0
    count = 0
    failsymbols = []

    def testrobert():
        global symbols
        global success
        global fail
        global count
        global failsymbols
        while len(symbols) > 0:
            symbol = symbols.pop()
            count += 1
            j = yfapi.query(symbol, 1000)
            # info
            info_check = False
            for item in j["info"]:
                if not j["info"][item] == None:
                    info_check = True
                    break
            # price
            price_check = False
            if not len(j["price"].keys()) == 0:
                price_check = True
            # result
            if info_check or price_check:
                success += 1
            else:
                fail += 1
                failsymbols.append(symbol)
            print("remain: {} | success: {} | fail: {}".format(
                total-count, success, fail))

    threads = []
    for _ in range(10):
        threads.append(threading.Thread(target=testrobert))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    with open("fail_symbols.txt", "w") as f:
        f.write("FAILS: {}\n".format(len(failsymbols)))
        for symbol in failsymbols:
            f.write(symbol+"\n")

    ratio = success/total
    if ratio > 0.9:
        print("test: PASS ({})".format(ratio))
    else:
        print("test: FAIL ({})".format(ratio))


if __name__ == "__main__":
    TestMain()
