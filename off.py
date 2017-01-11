import math
import json
from pprint import pprint

data_file = open('block.json');
data = json.load(data_file);
data_file.close()

class Counter:
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.value = 0

    def add_value(self, val):
        self.count += 1
        self.value += val / math.pow(10, 8)

unspent = Counter("unspent")
spent = Counter("spent")
for tx in data["tx"]:
    for o in tx["out"]:
        if o["spent"] == True:
            spent.add_value(o["value"])
        else:
            unspent.add_value(o["value"])

print("spent: {0} transactions, total {1} btc".format(spent.count, spent.value))
print("unspent: {0} transactions, total {1} btc".format(unspent.count, unspent.value))
