# 方法1 基于python（scipy.optimize）的实现代码如下
import pandas as pd
import numpy as np
import random
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore")
data = pd.read_csv(r'C:\Users\Admin\Desktop\diamonds.csv')

price = data.iloc[:, 0]
carat = data.iloc[:, 1]


# price = beta_0 + beta_1 * carat + epsilon

def func(carat, beta_0, beta_1, epsilon):
    price = beta_0 + beta_1 * carat + epsilon
    return price


popt, pcov = curve_fit(func, carat, price)
dat = []
for i in range(0, 500):
    data1 = data.sample(n=5000)
    price = data1.iloc[:, 0]
    carat = data1.iloc[:, 1]
    popt, pcov = curve_fit(func, carat, price)

    dat.append(popt)

dat = np.array(dat)
mean = np.average(dat[:, 1], axis=0)
var = np.var(dat[:, 1], axis=0)
std = np.std(dat[:, 1], axis=0)

# 方法2 基于python（sklearn库）的实现代码如下
import numpy as np
from sklearn import linear_model
import pandas as pd
import random
import matplotlib.pyplot as plt


def sam_calc(data, num=500, capacity=5000):
    sample_num = list(data.index)

    ans = []
    for i in range(num):
        sam = random.sample(sample_num, capacity)
        ans.append(data.iloc[sam])
    return ans


def fn(data, num):
    min = np.min(data)
    max = np.max(data)
    _range = (max - min) / num
    freq_y = [0 for _ in range(num)]
    freq_x = [min + _range * (i + 0.5) for i in range(num)]
    for i in range(num):
        for j in range(len(data)):
            if data[j] == max:
                freq_y[-1] += 1
            else:
                freq_y[int((data[j] - min) // _range)] += 1
    return freq_x, freq_y


data = pd.read_csv(r'C:\Users\Admin\Desktop\diamonds.csv')
samples = sam_calc(data)
betas = []
for data in samples:
    y = data.iloc[:, 0]
    x = data.iloc[:, [1]]
    model = linear_model.LinearRegression()
    model.fit(x, y)
    beta = model.coef_[0]
    betas.append(beta)
mean = np.mean(betas)
var = np.var(betas)
x, y = fn(betas, 20)
plt.plot(x, y)
plt.xlabel('beta value')
plt.ylabel('frequence')
plt.title('empirical distribution')
plt.show()