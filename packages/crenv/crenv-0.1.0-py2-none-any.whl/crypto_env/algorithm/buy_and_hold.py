import numpy as np
from . import Algorithm


class BuyAndHold(Algorithm):
    def __init__(self, buy_amount: float):
        """
        :param buy_amount: unit in cryptocurrency
        """
        self.buy_amount = buy_amount

    def take_action(self, observation, info=None):
        idx = observation['index'][0]
        if idx == 0:
            return dict(
                signal=0,
                value=np.array([self.buy_amount], dtype=np.float)
            )
        else:
            return dict(
                signal=2,
                value=np.array([0], dtype=np.float)
            )
