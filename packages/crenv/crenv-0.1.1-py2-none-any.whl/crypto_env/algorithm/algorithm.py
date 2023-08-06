from abc import ABC, abstractmethod


class Algorithm(ABC):
    @abstractmethod
    def take_action(self, observation, info=None):
        """
        Return an action from the action space.
        """
        raise NotImplementedError
