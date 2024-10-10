from numpy import ndarray
from stable_baselines3 import PPO


class DecisionFun:

    def decide(self, obs: ndarray) -> int:
        return 0

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_file_name(self) -> str:
        return self.get_name()


class HeuristicDecisionFun(DecisionFun):

    def __init__(self, relative_activation_distance: float = 0.5) -> None:
        super().__init__()
        self._relative_activation_distance = relative_activation_distance

    def decide(self, obs: ndarray) -> int:
        # obs[2] is the relative distance of the av to the junction
        if obs[2] < self._relative_activation_distance:
            return 1
        return 0

    def get_name(self) -> str:
        return 'H' + str(self._relative_activation_distance).ljust(4, '0')

    def get_file_name(self) -> str:
        return self.get_name()


class ModelDecisionFun(DecisionFun):

    def __init__(self, model: PPO, model_name: str) -> None:
        super().__init__()
        self._model = model
        self._model_name = model_name

    def decide(self, obs: ndarray) -> int:
        action, _ = self._model.predict(obs, deterministic=True)
        return action

    def get_name(self) -> str:
        return 'AI'

    def get_file_name(self) -> str:
        return 'AI_' + self._model_name
