import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import yfinance as yf
from PIL import Image, ImageTk

class FinanceTracker:
    def __init__(self, rootWindow):
        self.rootWindow = rootWindow
        self.rootWindow.title("Stock Portfolio Manager")
        self.rootWindow.geometry("700x700")  # Set the window size
        
        # Load the background image
        self.bg_image = Image.open("bg2.jpg")  # Replace with the path to your image
        self.bg_image = self.bg_image.resize((700, 700), Image.LANCZOS)  # Resize image to fit window
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a label for the background image
        self.bg_label = tk.Label(self.rootWindow, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Stretch the image to fill the window

        self.Portfolio = []  # Initialize the portfolio to store user info
        
        # Create and pack the label
        hello_label = tk.Label(self.rootWindow, text="Stock Portfolio Manager", font=("Monaco", 30), bg="#153042", fg="lightgray",relief="ridge")
        hello_label.pack(pady=30)

        # Add buttons for managing stocks
        addStockButton = tk.Button(self.rootWindow, text="Add Stock", font=("Monaco", 10), bg="#153042", fg="lightgray", command=self.addStockPortfolio)
        addStockButton.pack(pady=40)

        removeStockButton = tk.Button(self.rootWindow, text="Remove Stock", font=("Monaco", 10), bg="#153042", fg="lightgray", command=self.removeStockPortfolio)
        removeStockButton.pack(pady=50)

        viewPortfolioButton = tk.Button(self.rootWindow, text="View Portfolio", font=("Monaco", 10), bg="#153042", fg="lightgray", command=self.viewPortfolio)
        viewPortfolioButton.pack(pady=60)

        plotStockPerformanceButton = tk.Button(self.rootWindow, text="Plot Stock Performance", font=("Monaco", 10), bg="#153042", fg="lightgray", command=self.plotStockPerformance)
        plotStockPerformanceButton.pack(pady=70)

    # Add stock function
    def addStockPortfolio(self):
        addStockWindow = tk.Toplevel(self.rootWindow)
        addStockWindow.title("Add Stock")
        addStockWindow.geometry("500x400")
        addStockWindow.configure(bg="#153042")

        # Ticker symbol
        tickerSymbolLabel = tk.Label(addStockWindow, text="Ticker Symbol", font=("Monaco", 10), bg="#153042", fg="lightgray")
        tickerSymbolLabel.pack(pady=20)
        ticker_entry = tk.Entry(addStockWindow)
        ticker_entry.pack(pady=10)

        # Number of Shares
        numSharesLabel = tk.Label(addStockWindow, text="Number of Shares", font=("Monaco", 10), bg="#153042", fg="lightgray")
        numSharesLabel.pack(pady=40)
        quantity_entry = tk.Entry(addStockWindow)
        quantity_entry.pack(pady=5)

        # Take user input
        def addStockUser():
            ticker = ticker_entry.get()
            quantity = quantity_entry.get()

            # Get most recent data from yfinance
            stockData = yf.Ticker(ticker)
            if stockData.history(period="1d").empty:  # If no data available
                messagebox.showerror("Invalid input", "No data available for inputted ticker symbol")
                return
            
            # Get the current price
            currentPrice = stockData.history(period="1d")['Close'][0]

            # Add inputs to portfolio
            newStockInfo = {
                "Ticker Symbol": ticker,
                "Number of Shares": int(quantity),
                "Current cost per share": currentPrice
            }
            self.Portfolio.append(newStockInfo)
            messagebox.showinfo("Success", f"Added {quantity} shares of {ticker} to your portfolio.")
            addStockWindow.destroy()

        # Submit button
        submitButton = tk.Button(addStockWindow, text="Submit", command=addStockUser)
        submitButton.pack(pady=20)

    # Remove stock function
    def removeStockPortfolio(self):
        removeStockWindow = tk.Toplevel(self.rootWindow)
        removeStockWindow.title("Remove Stock")
        removeStockWindow.geometry("500x500")
        removeStockWindow.configure(bg="#153042")

        # Ticker symbol    
        tickerSymbolLabel = tk.Label(removeStockWindow, text="Ticker Symbol", font=("Monaco", 10), bg="#153042", fg="lightgray")
        tickerSymbolLabel.pack(pady=20)
        ticker_entry = tk.Entry(removeStockWindow)
        ticker_entry.pack(pady=10)

        # Number of Shares
        numSharesLabel = tk.Label(removeStockWindow, text="Number of Shares", font=("Monaco", 10), bg="#153042", fg="lightgray")
        numSharesLabel.pack(pady=40)
        quantity_entry = tk.Entry(removeStockWindow)
        quantity_entry.pack(pady=5)

        # Take user input
        def removeStockUser():
            ticker = ticker_entry.get()
            quantity = quantity_entry.get()

            # Check if quantity is valid
            try:
                quantity = int(quantity)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number for quantity.")
                return

            foundStock = False
            for stock in self.Portfolio:
                if stock["Ticker Symbol"].upper() == ticker.upper():
                    foundStock = True
                    if stock["Number of Shares"] > quantity:
                        stock["Number of Shares"] -= quantity
                        messagebox.showinfo("Success", f"Removed {quantity} shares of {ticker} from your portfolio.")
                    elif stock["Number of Shares"] == quantity:
                        self.Portfolio.remove(stock)
                        messagebox.showinfo("Success", f"Removed all shares of {ticker} from your portfolio.")
                    else:
                        messagebox.showerror("Invalid input", "Input exceeds quantity of shares in portfolio")
                    break

            if not foundStock:
                messagebox.showerror("Invalid input", "Stock not found in portfolio")

            removeStockWindow.destroy()

        # Submit button
        submitButton = tk.Button(removeStockWindow, text="Submit", command=removeStockUser)
        submitButton.pack(pady=20)

    # View portfolio function
    def viewPortfolio(self):
        viewPortfolio = tk.Toplevel(self.rootWindow)
        viewPortfolio.title("Portfolio")
        viewPortfolio.geometry("500x400")
        viewPortfolio.configure(bg="#153042")

        # Create a Text widget to display the portfolio
        portfolioText = tk.Text(viewPortfolio, bg="#153042", fg="lightgray", font=("Monaco", 10))
        portfolioText.pack(expand=True, fill=tk.BOTH)

        # Clear any previous content
        portfolioText.delete(1.0, tk.END)

        # Print current portfolio
        if not self.Portfolio:
            portfolioText.insert(tk.END, "Your portfolio is empty.\n")
        else:
            portfolioText.insert(tk.END, "Current Portfolio\n")
            totalPortfolioValue = 0
            for stock in self.Portfolio:
                totalPortfolioValue += (stock['Number of Shares'] * stock['Current cost per share'])
                portfolioText.insert(tk.END, f"Ticker Symbol: {stock['Ticker Symbol']}\n")
                portfolioText.insert(tk.END, f"Number of Shares: {stock['Number of Shares']}\n")
                portfolioText.insert(tk.END, f"Current Cost per Share: ${stock['Current cost per share']:.2f}\n")
                portfolioText.insert(tk.END, "-" * 30 + "\n")
            portfolioText.insert(tk.END, f"Current Total Portfolio Value: ${totalPortfolioValue:.2f}\n")

        # Exit button
        exitButton = tk.Button(viewPortfolio, text="Exit", command=viewPortfolio.destroy)
        exitButton.pack(pady=20)

    # Plot stock performance
    def plotStockPerformance(self):
        plotStockPerformance = tk.Toplevel(self.rootWindow)
        plotStockPerformance.title("Plot Stock Performance")
        plotStockPerformance.geometry("500x400")
        plotStockPerformance.configure(bg="#153042")

        # Ticker symbol    
        tickerSymbolLabel = tk.Label(plotStockPerformance, text="Ticker Symbol:", font=("Monaco", 10), bg="#153042", fg="lightgray")
        tickerSymbolLabel.pack(pady=20)
        ticker_entry = tk.Entry(plotStockPerformance)
        ticker_entry.pack(pady=10)

        # Start Date  
        startDateLabel = tk.Label(plotStockPerformance, text="Start Date (YYYY-MM-DD):", font=("Monaco", 10), bg="#153042", fg="lightgray")
        startDateLabel.pack(pady=20)
        startDate_entry = tk.Entry(plotStockPerformance)
        startDate_entry.pack(pady=10)

        # End Date 
        endDateLabel = tk.Label(plotStockPerformance, text="End Date (YYYY-MM-DD):", font=("Monaco", 10), bg="#153042", fg="lightgray")
        endDateLabel.pack(pady=20)
        endDate_entry = tk.Entry(plotStockPerformance)
        endDate_entry.pack(pady=10)

        # Plot function
        def plotData():
            ticker = ticker_entry.get()
            start_date = startDate_entry.get()
            end_date = endDate_entry.get()

            # Retrieve stock data with validation
            if ticker and start_date and end_date:
                stock_data = yf.Ticker(ticker).history(start=start_date, end=end_date)
                if not stock_data.empty:
                    plt.figure(figsize=(10, 5))
                    plt.plot(stock_data.index, stock_data['Close'], label=f"{ticker} Closing Prices")
                    plt.xlabel("Date")
                    plt.ylabel("Close Price")
                    plt.title(f"{ticker} Stock Performance from {start_date} to {end_date}")
                    plt.legend()
                    plt.grid()
                    plt.show()
                else:
                    messagebox.showerror("Data Error", "No data available for the specified range.")
            else:
                messagebox.showerror("Input Error", "Please enter all fields correctly.")

        # Plot button
        plotButton = tk.Button(plotStockPerformance, text="Plot", command=plotData)
        plotButton.pack(pady=20)

        # Exit button
        exitButton = tk.Button(plotStockPerformance, text="Exit", command=plotStockPerformance.destroy)
        exitButton.pack(pady=20)

if __name__ == "__main__":
    rootWindow = tk.Tk()
    finance_app = FinanceTracker(rootWindow)
    rootWindow.mainloop()
