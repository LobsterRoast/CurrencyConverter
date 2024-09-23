import json
import tkinter as tk
import os
import requests
from idlelib.colorizer import color_config
from multiprocessing.managers import Value
from tkinter import ttk

# Set the directory where the program will search for currencies.json
workingDirectory = os.path.dirname(os.path.abspath(__file__))
os.chdir(workingDirectory)

# Class that holds a currencies full name and the symbol associated with it
class Currency:
    def __init__(self, currencyName, currencyCode):
        self.currencyName = currencyName
        self.currencyCode = currencyCode

# Takes a currencies full name as an input and returns the symbol associated with it
def findCurrencySymbol(nameToSearchFor):
    for currency in currencies:
        if currency.currencyName == nameToSearchFor:
            return currency.currencyCode
    outputLabel.configure(text="Error! Could not find\nthe appropriate currency\nsymbol.")
    return 1


# Define variables globally
fAmountOfCurrency = None
currencyToConvertFrom = None
currencyToConvertTo = None
currencyList = None
conversionRate = None
outputText = None
currencies = []
currencyNames = []

# Load the contents of currencies.json into the currencyList variable
with open('currencies.json', 'r') as currencyListFile:
    currencyList = json.load(currencyListFile)
    # Populate currencies with every compatible currency
    for code, name in currencyList.items():
        newCurrency = Currency(currencyName=name, currencyCode=code)
        newCurrency.currencyCode = code
        newCurrency.currencyName = name
        currencies.append(newCurrency)
    # Populate currencyNames with every compatible currency name
    for currency in currencies:
        currencyNames.append(currency.currencyName)

# Updates fAmountOfCurrency with the inputted amount
def getCurrencyAmount():
    global fAmountOfCurrency
    try:
        fAmountOfCurrency = float(entAmountOfCurrency.get())
    # Returns an error if invalid or null number is inputted.
    except ValueError:
        outputLabel.configure(text="You have inputted an\ninvalid or null amount of currency.", anchor='w', justify='left')
        return 1

def getSelectedCurrencies():
        global currencyToConvertFrom, currencyToConvertTo
        currencyToConvertFrom = findCurrencySymbol(currency1Dropbox.get())
        currencyToConvertTo = findCurrencySymbol(currency2Dropbox.get())
        if currencyToConvertFrom == 1 or currencyToConvertTo == 1:
            return 1
        else:
            return 0

def convert():
    if getCurrencyAmount() == 1 or getSelectedCurrencies() == 1:
        return
    response = requests.get(f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{currencyToConvertFrom}.json")
    conversionRate = response.json()[currencyToConvertFrom].get(currencyToConvertTo, None)
    finalAmount = round(fAmountOfCurrency * conversionRate, 2)
    outputText = f"{fAmountOfCurrency} units of your\ninputted currency is\nworth {finalAmount} units of\nyour target currency."
    outputLabel.configure(text=outputText)
    return

root = tk.Tk()
w = root.winfo_height
root.geometry("400x400")
root.title('Currency Converter')
root.configure(bg='#333333')

style = ttk.Style()
style.configure("Button.TButton", foreground="black", background="black", font=("Helvetica", 12))

lab1 = tk.Label(root, text="Currency Converter", font="Helvetica 20", bg='#333333', fg='white')
lab1.place(x=10,y=0)

exitButton = ttk.Button(root, text="X", command=lambda: root.quit(), style="Button.TButton")
exitButton.place(x=280,y=8,)


currency1Label = tk.Label(root, text="Currency to convert from", font="Helvetica 10", bg='#333333', fg='white')
currency1Label.place(x=10, y=50)
currency1Dropbox = ttk.Combobox(root, values=currencyNames, state="readonly")
currency1Dropbox.place(x=10,y=75)
currency1Dropbox.current(1)

currency2Label = tk.Label(root, text="Currency to convert into", font="Helvetica 10", bg='#333333', fg='white')
currency2Label.place(x=10, y=125)
currency2Dropbox = ttk.Combobox(root, values=currencyNames, state="readonly")
currency2Dropbox.place(x=10,y=150)
currency2Dropbox.current(2)

currencyAmountLabel = tk.Label(root, text="Amount of currency to convert", font="Helvetica 10", bg='#333333', fg='white')
currencyAmountLabel.place(x=10, y=200)
entAmountOfCurrency = ttk.Entry(root, width=28)
entAmountOfCurrency.place(x=10,y=225)

conversionButton = ttk.Button(root, text="Convert Currency", command=lambda: convert(), style="Button.TButton")
conversionButton.place(x=10, y=300)
outputLabelBackground = tk.Label(root, bg='white', fg='black', borderwidth=2, relief="solid", width=22, height=12)
outputLabelBackground.place(x=205, y=55)
outputLabel = tk.Label(root, bg='white', fg='black', text=outputText, font="Helvetica 9", anchor='w', justify='left')
outputLabel.place(x=208, y=58)



root.mainloop()