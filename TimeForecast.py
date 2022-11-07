from tkinter import *
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from prophet.plot import add_changepoints_to_plot

df = pd.read_csv('C:/Users/YANHAN/PycharmProjects/FYP/purchase.csv')
df_names = ['ProductName', 'Brand', 'Qty', 'Date', 'Bill', 'Cashier', 'Status']
df = pd.read_csv('C:/Users/YANHAN/PycharmProjects/FYP/purchase.csv', header=None, skiprows=1, names=df_names)


df['Date'] = pd.to_datetime(df['Date'])

df.drop(['ProductName', 'Brand', 'Bill', 'Cashier', 'Status'], axis=1, inplace=True)
df.columns = ['y', 'ds']
# print(df.head())

m = Prophet(interval_width=0.99)
training_run = m.fit(df)

future = m.make_future_dataframe(periods=365, freq='D')

forecast = m.predict(future)

figure = m.plot(forecast)

figure.suptitle('dbshof', fontweight='bold')
figure.subplots_adjust(top=0.930,
                       bottom=0.098,
                       left=0.08,
                       right=0.985,
                       hspace=0.2,
                       wspace=0.2)
plt.xlabel('Date')
plt.ylabel('Quantity')

plt.show()

pro_change = Prophet(n_changepoints=20, yearly_seasonality=True, changepoint_prior_scale=0.001)
forecast = pro_change.fit(df).predict(future)
fig = pro_change.plot(forecast)
a = add_changepoints_to_plot(fig.gca(), pro_change, forecast)

figure.suptitle('Product', fontweight='bold')
figure.subplots_adjust(top=0.930,
                       bottom=0.098,
                       left=0.08,
                       right=0.985,
                       hspace=0.2,
                       wspace=0.2)
plt.title("Product")
plt.xlabel('Date')
plt.ylabel('Quantity')

plt.show()

# figure2 = m.plot_components(forecast)
# plt.xlabel("Day of year")
# plt.ylabel('Yearly')
# plt.show()
