import requests
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import numpy as np
import numpy

start_date = '2013-01-01'
end_date = datetime.date.today().isoformat()
regression_ranges = [30, 90] # ranges in days that should show up as individual linear regressions

r = requests.get('http://api.coindesk.com/v1/bpi/historical/close.json?currency=EUR&start={1}&end={0}'
.format(end_date, start_date))
data = r.json()['bpi']
x = list(data.keys())
x.sort()
y = [data[e] for e in x]
# transform to date
t = [datetime.datetime.strptime(elm, '%Y-%m-%d') for elm in x]
dt = [(elm - t[0]).days for elm in t]

# linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(dt, y)

# polyfit 1D
coeff = np.polyfit(dt, y, 2)
print(coeff)
fit = [coeff[0] * (e ** 2) + coeff[1] * e + coeff[2] for e in dt]

# regression at random point
def regY(x):
    return intercept + x*slope

# std error
errors = [y[i] - regY(i) for i in dt]
reg_error = numpy.mean(numpy.absolute(errors))

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

# 2 degree poly fit
ax.plot(dt, fit, 'k')
ax.plot(dt, fit + reg_error, 'k--')
ax.plot(dt, fit - reg_error, 'k--')

color=iter(plt.cm.rainbow(np.linspace(0,1,len(regression_ranges))))
for start in regression_ranges:
    tr = range(start)
    yr = y[-start:]
    sr, ir, r_value, p_value, std_err = stats.linregress(tr, yr)
    y0 = ir
    y1 = ir + 2 * start * sr
    x0 = dt[-1] - start
    x1 = dt[-1] + start
    # print(start, sr, ir, y0, y1)
    ax.plot([x0, x1], [y0, y1], c=next(color))


# linear fit
#ax.plot([0, x_max], [regY(0), regY(x_max)])
#ax.plot([0, x_max], [regY(0) - reg_error, regY(x_max) - reg_error], 'r--')
#ax.plot([0, x_max], [regY(0) + reg_error, regY(x_max) + reg_error], 'r--')

ax.set_ylabel('price [USD]')
ax.set_xlabel('time')
ax.grid(True)

xlabels = [(t[0] + datetime.timedelta(tick)) for tick in ax.get_xticks()]
xlabels = [elm.strftime('%m/%y') for elm in xlabels]
ax.set_xticklabels(xlabels)

plt.show()
