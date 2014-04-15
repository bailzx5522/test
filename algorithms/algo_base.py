
class Algo_base(object):
    def __init__(self, data):
        self.data = data
    
    def algorithm(self):
        pass
    
    def _high_price_day(self, day):
        if day.close >= day.open:
            return day.close, day.open
        else:
            return day.open, day.close

    def _get_average_amplitude(self, data, leg=False):
        average = 0
        n = 0
        previous = 0
        for day in data:
            if previous == 0:
                if day.close == 0:
                    continue
                else:
                    previous = day.close
            
            if leg:
                average += (day.high - day.low)/2
            else:
                average += (day.open - day.close)/2
            n += 1
        return average/n
        