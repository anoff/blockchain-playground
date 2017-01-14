import requests
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import numpy

# fetch market price data
r = requests.get('https://api.blockchain.info/charts/market-price?timespan=2years&rollingAverage=1days')
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
