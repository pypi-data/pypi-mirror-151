from abc import ABC, abstractmethod

from torch import nn


class DeepNeuralInterface(ABC, nn.Module):
    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def get_transforms(self):
        pass


class TrainSiameseInterface(ABC):
    @abstractmethod
    def train(self, net: nn.Module, X) -> None:
        pass

    @abstractmethod
    def train_epoch(self, net: nn.Module, X) -> None:
        pass