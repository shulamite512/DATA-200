# stock_console.py (Fully Implemented)

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData
from os import path
import stock_data

# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        elif option == "0":
            print("Goodbye!")

# Manage Stocks
def manage_stocks(stock_list):
    while True:
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Back to Main Menu")
        option = input("Enter option: ")
        if option == "1":
            symbol = input("Enter stock symbol: ").upper()
            name = input("Enter stock name: ")
            shares = float(input("Enter number of shares: "))
            stock_list.append(Stock(symbol, name, shares))
            print("Stock added!")
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            symbol = input("Enter stock symbol to delete: ").upper()
            stock_list[:] = [s for s in stock_list if s.symbol != symbol]
            print("Stock deleted.")
        elif option == "4":
            list_stocks(stock_list)
        elif option == "0":
            break
        input("\nPress Enter to continue...")

# Update shares

def update_shares(stock_list):
    symbol = input("Enter stock symbol: ").upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            action = input("Buy or Sell? (b/s): ").lower()
            amount = float(input("How many shares? "))
            if action == 'b':
                stock.buy(amount)
            else:
                stock.sell(amount)
            print("Shares updated.")
            return
    print("Stock not found.")

# List all stocks

def list_stocks(stock_list):
    print("\nTracked Stocks:")
    for stock in stock_list:
        print(f"{stock.symbol} - {stock.name} - {stock.shares} shares")

# Add Daily Stock Data
def add_stock_data(stock_list):
    symbol = input("Enter stock symbol to add data for: ").upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            date = datetime.strptime(input("Enter date (m/d/yy): "), "%m/%d/%y")
            price = float(input("Enter closing price: "))
            volume = float(input("Enter volume: "))
            stock.add_data(DailyData(date, price, volume))
            print("Daily data added.")
            return
    print("Stock not found.")

# Display Report
def display_report(stock_list):
    clear_screen()
    print("Stock Report ---")
    for stock in stock_list:
        print(f"\n{stock.symbol} - {stock.name}")
        for d in stock.DataList:
            print(f"{d.date.strftime('%m/%d/%y')} | Close: ${d.close:.2f} | Volume: {int(d.volume)}")
    input("\nPress Enter to continue...")

# Display Chart
def display_chart(stock_list):
    symbol = input("Enter stock symbol to chart: ").upper()
    display_stock_chart(stock_list, symbol)

# Manage Data Menu
def manage_data(stock_list):
    while True:
        clear_screen()
        print("Manage Data ---")
        print("1 - Save to Database")
        print("2 - Load from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV")
        print("0 - Back to Main Menu")
        option = input("Enter option: ")
        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Data saved.")
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            print("Data loaded.")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)
        elif option == "0":
            break
        input("Press Enter to continue...")

# Retrieve data from web
def retrieve_from_web(stock_list):
    dateFrom = input("Enter start date (m/d/yy): ")
    dateTo = input("Enter end date (m/d/yy): ")
    count=stock_data.retrieve_stock_web(dateFrom, dateTo, stock_list)
    print(f"{count} Data retrieved from web.")

# Import data from CSV
def import_csv(stock_list):
    symbol = input("Enter stock symbol: ").upper()
    filename = input("Enter path to CSV file: ")
    if not symbol.isalnum():
        print("Invalid symbol. Please enter letters or numbers only.")
        return
    if not filename.lower().endswith('.csv'):
        print("File must be a .csv file.")
        return
    if not path.exists(filename):
        print("File not found. Please check the path and try again.")
        return
    stock_data.import_stock_web_csv(stock_list, symbol, filename)
    print("CSV data imported.")

# Entry Point
def main():
    if not path.exists("stocks.db"):
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

if __name__ == "__main__":
    main()
