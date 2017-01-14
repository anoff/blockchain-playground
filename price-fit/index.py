import requests
import matplotlib.pyplot as plt
import datetime
from scipy import stats
from scipy import std

# fetch market price data
r = requests.get('https://api.blockchain.info/charts/market-price?timespan=2years&rollingAverage=1days')
data = r.json()['values']

x = [elm['x'] for elm in data]
y = [elm['y'] for elm in data]

# transform to date
t = [datetime.date.fromtimestamp(elm) for elm in x]
dt = [(elm - t[0]).days for elm in t]

slope, intercept, r_value, p_value, std_err = stats.linregress(dt, y)

print(slope, intercept, r_value, p_value, std_err)

# regression at random point
def regY(x):
    return intercept + x*slope

# std error
#errors = [elm - regY(x[y.index(elm)]) for elm in y]
errors = []
for i in dt:
    val = y[i] - regY(i)
    errors.append(val)

print(errors)
reg_error = std(errors)
print(reg_error)
#exit()


# plot
fg, ax = plt.subplots()
ax.plot(dt, y)
ax.plot([0, dt[-1]], [regY(0), regY(dt[-1])])
ax.plot([0, dt[-1]], [regY(0) - reg_error, regY(dt[-1]) - reg_error], 'r--')
ax.plot([0, dt[-1]], [regY(0) + reg_error, regY(dt[-1]) + reg_error], 'r--')
ax.set_ylabel('price [USD]')
ax.set_xlabel('time')
ax.grid(True)

xlabels = [(t[0] + datetime.timedelta(tick)) for tick in ax.get_xticks()]
xlabels = [elm.strftime('%m/%y') for elm in xlabels]
ax.set_xticklabels(xlabels)

plt.show()
