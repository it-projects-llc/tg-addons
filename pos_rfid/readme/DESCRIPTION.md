Converts RFID scan result to a proper value.

It's not possible to make similar module that depends on `barcodes` only, because in some cases there is no way to automatically detect shall code be translated or not.
So in that cases we trigger several events: with original code and with translated ones.

Adapters
========

HEX to DEC
----------

E.g. `9cc29d808 >> 042080000008`
