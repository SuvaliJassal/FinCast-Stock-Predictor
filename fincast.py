import sys
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
from PyQt5 import QtCore, QtGui, QtWidgets

class Finance():
    def __init__(self):
        plt.style.use('ggplot')
        self.start = dt.datetime(2015, 1, 1)
        self.end = dt.datetime.now()
    
    def get_stock_price(self, ticker):
        try: 
            df = yf.download(ticker, start=self.start, end=self.end)
            if df.empty: return None
            df.reset_index(inplace=True)
            return df
        except Exception: return None 
    
    def get_moving_avg(self, ticker):
        df = self.get_stock_price(ticker)
        if df is None: return
            
        df['MA'] = df['Close'].rolling(window=5, min_periods=0).mean()
        
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['Close'].values, label='Stock Price', color='gold')
        plt.plot(df['Date'], df['MA'].values, label='5d Moving Avg', color='cyan')
        
        latest_close = df['Close'].iloc[-1]
        latest_ma = df['MA'].iloc[-1]
        
        
        if hasattr(latest_close, "__len__"): latest_close = latest_close.iloc[0]
        if hasattr(latest_ma, "__len__"): latest_ma = latest_ma.iloc[0]

        action = 'BUY/HOLD' if latest_close > latest_ma else 'SELL'
        plt.title(f"Ticker: {ticker} | Recommendation: {action}")
        plt.legend()
        
        
        plt.show(block=False)
        plt.pause(0.1)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("FinCast")
        MainWindow.resize(803, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: white;")
        
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(190, 50, 441, 461))
        # Cerulean Frame with Rounded Corners
        self.frame.setStyleSheet("background-color:rgb(0, 123, 167); border-radius: 20px;")
        
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(90, 50, 281, 71))
        self.label.setFont(QtGui.QFont("Arial", 36, QtGui.QFont.Bold))
        self.label.setStyleSheet("color:white; background: transparent;")
        self.label.setText("FinCast")
        
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(80, 200, 261, 45))
        self.lineEdit.setStyleSheet("background-color: white; color: rgb(0, 123, 167); border-radius: 10px; padding-left: 10px; font-size: 14pt;")
        self.lineEdit.setPlaceholderText("TICKER (e.g., AAPL)")
        
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(150, 290, 140, 45))
        self.pushButton.setStyleSheet("background-color: #004B63; color: white; border-radius: 15px; font-weight: bold; font-size: 14pt;")
        self.pushButton.setText("PREDICT")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton.clicked.connect(self.pressed)

    def pressed(self):
        ticker = self.lineEdit.text().upper()
        if ticker:
            f = Finance()
            f.get_moving_avg(ticker)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
