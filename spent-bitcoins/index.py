from blockchain import blockexplorer
from lib.analyze import Counter, analyze as analyze_block

import matplotlib.pyplot as plt

print('Hello, world!')

# loop over a bunch of blocks :o
totalUnspent = Counter('totalUnspent')
totalSpent = Counter('totalSpent')
# init with latest block
hash = blockexplorer.get_latest_block().hash
x = []
y = []
total_runs = 500
for i in range(total_runs):
    print(i+1, '/', total_runs)
    result = analyze_block(hash)

    totalUnspent.count += result['unspent'].count
    totalUnspent.value += result['unspent'].value

    totalSpent.count += result['spent'].count
    totalSpent.value += result['spent'].value
    hash = result['previous_block']

    x.append(hash)
    y.append(result['unspent'].value/(result['unspent'].value + result['spent'].value))
print("\n\n")

print("unspent: {0} transactions, total {1:.0f} btc".format(totalUnspent.count, totalUnspent.value))
print("spent: {0} transactions, total {1:.0f} btc".format(totalSpent.count, totalSpent.value))


plt.plot(y)
plt.ylabel('% of unspent coins')
plt.xlabel('transaction')
plt.show()
