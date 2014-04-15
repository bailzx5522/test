from algo_base import Algo_base

class Bounce(Algo_base):
    """
    Algorithm       _                            
              -    -
             - -  -
       -    -   ** Entry point in this algorithm
      - -  -
     -   -
    -
    It's a little tricky.
    """
    def __init__(self, data):
        super(Bounce, self).__init__(data)
        
    def algorithm(self):
        # high price in 30 days
        high_wave = 0
        low_wave = 0
        for day in self.data:
            high_day,low_day = self._high_price_day(day)
            if not (high_wave and low_wave):
                high_wave = high_day
                low_wave = low_day
                continue
            
            if high_day > high_wave:
                high_wave = high_day
            if low_day < low_wave:
                low_wave = low_day
                
            
        
    def related_algorithm(self):
        pass
        
        