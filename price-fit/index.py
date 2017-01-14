import requests
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import numpy

# fetch market price data
r = requests.get('https://api.blockchain.info/charts/market-price?timespan=2years&rollingAverage=1days')
# alternative: http://api.coindesk.com/v1/bpi/historical/close.json?currency=EUR&start=2013-01-01&end=2017-01-01
data = r.json()['values']

x = [elm['x'] for elm in data]
y = [elm['y'] for elm in data]

# transform to date
t = [datetime.date.fromtimestamp(elm) for elm in x]
dt = [(elm - t[0]).days for elm in t]

# linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(dt, y)
# print(slope, intercept, r_value, p_value, std_err)

# regression at random point
def regY(x):
    return intercept + x*slope

# std error
errors = [y[i] - regY(i) for i in dt]
reg_error = numpy.mean(numpy.absolute(errors))
# print(reg_error)
#exit()

# calculate price in one year
forecast = [30, 90, 180, 365] # forecast in days
win = [1.5, 2] # when will it reach X of current value

startValue = numpy.mean(y[-5:])
for days in forecast:
    value = startValue + days * slope;
    print('BTC will reach {0:.1f} in {1:.0f} days'.format(value, days))

for val in win:
    days = startValue * (val - 1) / slope
    print('BTC price will reach {0:.0f}% (base: {1:.1f}) in {2:.0f} days'.format(val*100, startValue, days))

# plot
fg, ax = plt.subplots()
ax.plot(dt, y)
x_min, x_max = ax.get_xlim()
ax.plot([0, x_max], [regY(0), regY(x_max)])
ax.plot([0, x_max], [regY(0) - reg_error, regY(x_max) - reg_error], 'r--')
ax.plot([0, x_max], [regY(0) + reg_error, regY(x_max) + reg_error], 'r--')
ax.set_ylabel('price [USD]')
ax.set_xlabel('time')
ax.grid(True)

xlabels = [(t[0] + datetime.timedelta(tick)) for tick in ax.get_xticks()]
xlabels = [elm.strftime('%m/%y') for elm in xlabels]
ax.set_xticklabels(xlabels)

plt.show()
