import requests
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import numpy as np
import numpy

start_date = '2013-01-01'
end_date = datetime.date.today().isoformat()
fit_ranges = [30, 90, 180, 360, 720] # ranges in days that should show up as individual linear regressions
fit_forecast = 180 # how many days the fittet curves should be extrapolated
r = requests.get('http://api.coindesk.com/v1/bpi/historical/close.json?currency=EUR&start={1}&end={0}'
.format(end_date, start_date))
data = r.json()['bpi']
x = list(data.keys())
x.sort()
y = [data[e] for e in x]
# transform to date
t = [datetime.datetime.strptime(elm, '%Y-%m-%d') for elm in x]
dt = [(elm - t[0]).days for elm in t]

# polyfit 1D
coeff = np.polyfit(dt, y, 2)
fit_x = range(len(dt) + fit_forecast)
fit_y = [coeff[0] * (e ** 2) + coeff[1] * e + coeff[2] for e in fit_x]
# mean deviation from fit
errors = [y[i] - fit_y[i] for i in dt]
reg_error = numpy.mean(numpy.absolute(errors))

# plot
fg, ax = plt.subplots()
ax.plot(dt, y)

# 2 degree poly fit
ax.plot(fit_x, fit_y, 'k')
ax.plot(fit_x, fit_y + reg_error, 'k--')
ax.plot(fit_x, fit_y - reg_error, 'k--')

# fit ranges
color=iter(plt.cm.rainbow(np.linspace(0,1,len(fit_ranges))))
for start in fit_ranges:
    tr = range(start)
    yr = y[-start:]
    coeff = np.polyfit(tr, yr, 2)
    tr = range(start + fit_forecast)
    fit = [coeff[0] * (e ** 2) + coeff[1] * e + coeff[2] for e in tr]
    # print(start, sr, ir, y0, y1)
    ax.plot([e + dt[-start] for e in tr], fit, c=next(color))

ax.set_ylabel('price [USD]')
ax.set_xlabel('time')
ax.grid(True)

xlabels = [(t[0] + datetime.timedelta(tick)) for tick in ax.get_xticks()]
xlabels = [elm.strftime('%m/%y') for elm in xlabels]
ax.set_xticklabels(xlabels)
ax.set_ylim(0, 2000)
ax.set_xlim(0, dt[-1] + fit_forecast)

fg.savefig('temp.png', dpi=300)
