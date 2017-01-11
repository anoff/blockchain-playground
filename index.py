from blockchain import blockexplorer
import math
import json
import redis

print('Hello, world!')
r = redis.StrictRedis(host='localhost', port=6379, db=0)

class Counter:
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.value = 0

    def add_value(self, val):
        self.count += 1
        self.value += val / math.pow(10, 8)

def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__,
        sort_keys=True, indent=4)

def get_block(hash):
    res = r.get(hash)
    if res == None:
        res = blockexplorer.get_block(hash)
        r.set(hash, toJSON(res))
        print("\t\t\tadded to cache")
    else:
        print("\t\t\tfound in cache")
        res = json.loads(res)
    return res


def analyze(hash):
    unspent = Counter("unspent")
    spent = Counter("spent")
    data = get_block(hash)

    for tx in data.transactions:
        for o in tx.outputs:
            if o.spent == True:
                spent.add_value(o.value)
            else:
                unspent.add_value(o.value)

    # print("spent: {0} transactions, total {1} btc".format(spent.count, spent.value))
    # print("unspent: {0} transactions, total {1} btc".format(unspent.count, unspent.value))
    ratio = spent.count / (spent.count + unspent.count)
    ratioV = spent.value / (spent.value + unspent.value)

    print("spent {0:.0f}% ({1:.0f}:{2:.0f}) TX\t{3:.0f}% ({4:.1f}:{5:.1f}) BTC".format(ratio * 100, spent.count, unspent.count, ratioV * 100, spent.value, unspent.value))
    return [unspent, spent, data.previous_block]

# loop over a bunch of blocks :o
totalUnspent = Counter('totalUnspent')
totalSpent = Counter('totalSpent')
# init with latest block
hash = blockexplorer.get_latest_block().hash
for i in range(20):
    result = analyze(hash)
    totalUnspent.count += result[0].count
    totalUnspent.value += result[0].value

    totalSpent.count += result[1].count
    totalSpent.value += result[1].value
    hash = result[2]

print("\n\n")

print("unspent: {0} transactions, total {1:.0f} btc".format(totalUnspent.count, totalUnspent.value))
print("spent: {0} transactions, total {1:.0f} btc".format(totalSpent.count, totalSpent.value))
