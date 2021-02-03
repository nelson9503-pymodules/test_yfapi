# Test on yfapi

This is a test on [yfapi](https://github.com/nelson9503-pymodules/yfapi), which ensure yfapi can access most symbols normally.

## Methodology

This test get the symbols from IEX Cloud and try to download histrical price of those symbols from the Yahoo! Finance.

Some symbols may not avalible on Yahoo! Finacne Server, so only 90% symbols pass the test is required for the whole test.

Since doing the full test on all symbols was taking too much times, we only extract 10% symbols randomly for the test.
