import json
import tkinter as tk
import os
import requests
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

# Sets currencyToConvertFrom and currencyToConvertTo to the relevant currencies selected by the user
def getSelectedCurrencies():
        global currencyToConvertFrom, currencyToConvertTo
        currencyToConvertFrom = findCurrencySymbol(currency1Dropbox.get())
        currencyToConvertTo = findCurrencySymbol(currency2Dropbox.get())
        # Returns 1 if the currency is invalid or null (shouldn't be possible but error handling is good)
        if currencyToConvertFrom == 1 or currencyToConvertTo == 1:
            return 1
        else:
            return 0

# Convert function that runs when user clicks the "Convert" button
def convert():
    # Returns immediately if an error is found
    if getCurrencyAmount() == 1 or getSelectedCurrencies() == 1:
        return
    # If no errors are found, send a request to the API. A json is returned containing the exchange rate to every currency other than the one being converted from.
    response = requests.get(f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{currencyToConvertFrom}.json")
    # Find the conversion rate for the target currency and set conversionRate to the conversion rate
    conversionRate = response.json()[currencyToConvertFrom].get(currencyToConvertTo, None)
    # Multiplies the amount of the input currency by the conversion rate of the output currency and then rounds it to 2 digits
    finalAmount = round(fAmountOfCurrency * conversionRate, 2)
    # Output the final amount of output currency
    outputText = f"{fAmountOfCurrency} units of your\ninputted currency is\nworth {finalAmount} units of\nyour target currency."
    outputLabel.configure(text=outputText)
    return

# Create a tkinter window
root = tk.Tk()
w = root.winfo_height
root.geometry("400x400")
root.title('Currency Converter')
root.configure(bg='#333333')

# Create a style to be applied to various buttons
style = ttk.Style()
style.configure("Button.TButton", foreground="black", background="black", font=("Helvetica", 12))

# Header label
lab1 = tk.Label(root, text="Currency Converter", font="Helvetica 20", bg='#333333', fg='white')
lab1.place(x=10,y=0)

# Button to exit the application
exitButton = ttk.Button(root, text="X", command=lambda: root.quit(), style="Button.TButton")
exitButton.place(x=280,y=8,)

# Label and dropbox for the input currency
currency1Label = tk.Label(root, text="Currency to convert from", font="Helvetica 10", bg='#333333', fg='white')
currency1Label.place(x=10, y=50)
currency1Dropbox = ttk.Combobox(root, values=currencyNames, state="readonly")
currency1Dropbox.place(x=10,y=75)
currency1Dropbox.current(1)

# Label and dropbox for the output currency
currency2Label = tk.Label(root, text="Currency to convert into", font="Helvetica 10", bg='#333333', fg='white')
currency2Label.place(x=10, y=125)
currency2Dropbox = ttk.Combobox(root, values=currencyNames, state="readonly")
currency2Dropbox.place(x=10,y=150)
currency2Dropbox.current(2)

# Label and text box for the user to specify how much currency is being converted
currencyAmountLabel = tk.Label(root, text="Amount of currency to convert", font="Helvetica 10", bg='#333333', fg='white')
currencyAmountLabel.place(x=10, y=200)
entAmountOfCurrency = ttk.Entry(root, width=28)
entAmountOfCurrency.place(x=10,y=225)

# Button to carry out the conversion
conversionButton = ttk.Button(root, text="Convert Currency", command=lambda: convert(), style="Button.TButton")
conversionButton.place(x=10, y=300)

# Label to output text to dynamically, i.e. after converting currency or after encountering an error
outputLabelBackground = tk.Label(root, bg='white', fg='black', borderwidth=2, relief="solid", width=22, height=12)
outputLabelBackground.place(x=205, y=55)
outputLabel = tk.Label(root, bg='white', fg='black', text=outputText, font="Helvetica 9", anchor='w', justify='left')
outputLabel.place(x=208, y=58)


# Runs the main tkinter loop
root.mainloop()