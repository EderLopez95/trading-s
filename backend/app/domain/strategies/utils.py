class Utils:
    def __init__(self):
        self.EPS = 0.1 # minimum price difference to consider a crossover valid
        self.MIN_DISTANCE = 0.25 # minimum distance between two series to consider a crossover valid

    def calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def crossover(self, a, b):
        prev = a.shift(1).iloc[-1] < b.shift(1).iloc[-1] - self.EPS
        curr = a.iloc[-1] > b.iloc[-1] + self.EPS
        distance = abs(a.iloc[-1] - b.iloc[-1]) > self.MIN_DISTANCE
        return prev and curr and distance

    def crossunder(self, a, b):
        prev = a.shift(1).iloc[-1] > b.shift(1).iloc[-1] + self.EPS
        curr = a.iloc[-1] < b.iloc[-1] - self.EPS
        distance = abs(a.iloc[-1] - b.iloc[-1]) > self.MIN_DISTANCE
        return prev and curr and distance
