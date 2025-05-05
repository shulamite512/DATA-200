import matplotlib.pyplot as plt
from os import system, name

# Clear the terminal screen
def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# Sort stock list alphabetically
def sortStocks(stock_list):
    stock_list.sort(key=lambda stock: stock.symbol)

# Sort daily data by date for each stock
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda d: d.date)

# Display stock price chart using matplotlib
def display_stock_chart(stock_list, symbol):
    for stock in stock_list:
        if stock.symbol == symbol:
            if not stock.DataList:
                print("No data available for chart.")
                return
            dates = [d.date for d in stock.DataList]
            prices = [d.close for d in stock.DataList]
            plt.figure(figsize=(10, 5))
            plt.plot(dates, prices, marker='o')
            plt.title(f"{symbol} - Price History")
            plt.xlabel("Date")
            plt.ylabel("Closing Price")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()
