import MetaTrader5 as mt5

connected = mt5.initialize()

if connected:
    print("Connected to MetaTrader")
else:
    print("Error connecting to MetaTrader")
    print(mt5.last_error())
