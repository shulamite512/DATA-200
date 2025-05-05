# stock_GUI.py (Modernized GUI with Style Enhancements)

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk, messagebox, simpledialog, filedialog
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        if not path.exists("stocks.db"):
            stock_data.create_database()

        self.root = Tk()
        self.root.title("📈 Smart Stock Tracker")
        self.root.geometry("750x500")
        self.root.configure(bg="#f0f4f8")

        # Setup Menubar
        self.menubar = Menu(self.root, bg="#d9e4f5", fg="black")

        filemenu = Menu(self.menubar, tearoff=0, bg="white")
        filemenu.add_command(label="📂 Load Data", command=self.load)
        filemenu.add_command(label="💾 Save Data", command=self.save)
        self.menubar.add_cascade(label="File", menu=filemenu)

        webmenu = Menu(self.menubar, tearoff=0, bg="white")
        webmenu.add_command(label="🌐 Scrape Data from Yahoo! Finance", command=self.scrape_web_data)
        webmenu.add_command(label="📁 Import CSV", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web", menu=webmenu)

        chartmenu = Menu(self.menubar, tearoff=0, bg="white")
        chartmenu.add_command(label="📊 Show Stock Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=chartmenu)

        self.root.config(menu=self.menubar)

        # Setup Heading
        self.headingLabel = Label(self.root, text="📊 Stock Portfolio", font=("Segoe UI", 18, "bold"), bg="#f0f4f8", fg="#003366")
        self.headingLabel.pack(pady=10)

        # Stock List
        self.stockList = Listbox(self.root, width=50, font=("Segoe UI", 12), fg="#003366", selectbackground="#add8e6")
        self.stockList.pack(padx=10, pady=5)
        self.stockList.bind('<<ListboxSelect>>', self.update_data)

        # Add Tabs
        self.tabs = ttk.Notebook(self.root)

        self.mainTab = Frame(self.tabs, bg="#ffffff")
        self.tabs.add(self.mainTab, text="📌 Main")

        self.historyTab = Frame(self.tabs, bg="#ffffff")
        self.tabs.add(self.historyTab, text="📜 History")

        self.reportTab = Frame(self.tabs, bg="#ffffff")
        self.tabs.add(self.reportTab, text="📈 Report")

        self.tabs.pack(expand=1, fill="both")

        # Main Tab - Add stock
        Label(self.mainTab, text="Symbol", bg="#ffffff", font=("Segoe UI", 10)).grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Label(self.mainTab, text="Name", bg="#ffffff", font=("Segoe UI", 10)).grid(row=1, column=0, sticky=W, padx=10, pady=5)
        Label(self.mainTab, text="Shares", bg="#ffffff", font=("Segoe UI", 10)).grid(row=2, column=0, sticky=W, padx=10, pady=5)

        self.addSymbolEntry = Entry(self.mainTab)
        self.addNameEntry = Entry(self.mainTab)
        self.addSharesEntry = Entry(self.mainTab)
        self.addSymbolEntry.grid(row=0, column=1, padx=10, pady=5)
        self.addNameEntry.grid(row=1, column=1, padx=10, pady=5)
        self.addSharesEntry.grid(row=2, column=1, padx=10, pady=5)

        Button(self.mainTab, text="➕ Add Stock", command=self.add_stock, bg="#4CAF50", fg="white", font=("Segoe UI", 10)).grid(row=3, column=1, padx=10, pady=5)

        # Buy/Sell Shares
        Label(self.mainTab, text="Update Shares", bg="#ffffff", font=("Segoe UI", 10)).grid(row=4, column=0, sticky=W, padx=10, pady=5)
        self.updateSharesEntry = Entry(self.mainTab)
        self.updateSharesEntry.grid(row=4, column=1, padx=10, pady=5)

        Button(self.mainTab, text="Buy", command=self.buy_shares, bg="#2196F3", fg="white", font=("Segoe UI", 10)).grid(row=5, column=0, padx=10, pady=5)
        Button(self.mainTab, text="Sell", command=self.sell_shares, bg="#f44336", fg="white", font=("Segoe UI", 10)).grid(row=5, column=1, padx=10, pady=5)

        # History Tab
        self.dailyDataList = Text(self.historyTab, width=85, height=15, bg="#e9f1f7", font=("Consolas", 10))
        self.dailyDataList.pack(padx=10, pady=10)

        # Report Tab
        self.stockReport = Text(self.reportTab, width=85, height=15, bg="#f7f7f7", font=("Consolas", 10))
        self.stockReport.pack(padx=10, pady=10)

        self.root.mainloop()

    def load(self):
        self.stockList.delete(0, END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)
        messagebox.showinfo("Load Data", "Data Loaded Successfully")

    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data", "Data Saved Successfully")

    def update_data(self, evt):
        self.display_stock_data()

    def display_stock_data(self):
        if not self.stockList.curselection():
            return
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = f"{stock.name} - {stock.shares} Shares"
                self.dailyDataList.delete("1.0", END)
                self.stockReport.delete("1.0", END)

                self.dailyDataList.insert(END, "- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END, "=================================\n")
                for daily in stock.DataList:
                    row = daily.date.strftime("%m/%d/%y") + "   " + f"${daily.close:,.2f}" + "   " + f"{int(daily.volume)}\n"
                    self.dailyDataList.insert(END, row)

                self.stockReport.insert(END, f"Report for {stock.symbol} - {stock.name}\n")
                self.stockReport.insert(END, f"Total Entries: {len(stock.DataList)}\n")
                closes = [d.close for d in stock.DataList]
                if closes:
                    self.stockReport.insert(END, f"Min: ${min(closes):.2f} | Max: ${max(closes):.2f} | Avg: ${sum(closes)/len(closes):.2f}\n")

    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get().upper(), self.addNameEntry.get(), float(self.addSharesEntry.get()))
        self.stock_list.append(new_stock)
        self.stockList.insert(END, new_stock.symbol)
        self.addSymbolEntry.delete(0, END)
        self.addNameEntry.delete(0, END)
        self.addSharesEntry.delete(0, END)

    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = f"{stock.name} - {stock.shares} Shares"
        self.updateSharesEntry.delete(0, END)

    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = f"{stock.name} - {stock.shares} Shares"
        self.updateSharesEntry.delete(0, END)

    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Start Date", "Enter start date (m/d/yy)")
        dateTo = simpledialog.askstring("End Date", "Enter end date (m/d/yy)")
        try:
            stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
            self.display_stock_data()
            messagebox.showinfo("Success", "Data scraped from Yahoo! Finance")
        except:
            messagebox.showerror("Error", "Failed to retrieve data. Check ChromeDriver setup.")

    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title=f"Select CSV for {symbol}", filetypes=[('CSV Files', '*.csv')])
        if filename:
            stock_data.import_stock_web_csv(self.stock_list, symbol, filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete", f"{symbol} data imported successfully")

    def display_chart(self):
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list, symbol)

# Entry Point
if __name__ == "__main__":
    app = StockApp()
