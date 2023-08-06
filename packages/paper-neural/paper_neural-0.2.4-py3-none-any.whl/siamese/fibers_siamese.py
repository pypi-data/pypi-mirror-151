import torch
from torch import nn
from torchsummary import summary
import torch.nn.functional as F

from definitions import MODEL_YOLO_PATH


class feature(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        # load resnet-18

        # primeiras camadas conv do resnet
        # resnet18 = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
        # in_channels=64
        # self.layer1 = nn.Sequential(
        #     resnet18.conv1,
        #     resnet18.bn1,
        #     resnet18.relu,
        #     resnet18.maxpool
        #   )

        in_channels = 64
        model = torch.hub.load('ultralytics/yolov5', 'custom', MODEL_YOLO_PATH)
        self.layer1 = model.model.model.model[0:2]
        self.layer2 = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=32, kernel_size=(3, 3), padding=1),
            nn.Conv2d(in_channels=32, out_channels=16, kernel_size=(3, 3), padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(num_features=16),
            nn.MaxPool2d(kernel_size=(2, 2)),
            nn.Flatten()
        )
        # size = 3600
        size = 784
        self.dropout = nn.Dropout(0.1)
        self.dense1 = nn.Linear(in_features=size, out_features=512)
        self.dense2 = nn.Linear(in_features=512, out_features=128)
        self.layer1.training = False


    def forward(self, X):
        X_ = self.layer1(X)
        X_ = self.layer2(X_)
        X_ = self.dropout(F.leaky_relu(self.dense1(X_), 0.1))
        X_ = F.leaky_relu(self.dense2(X_), 0.1)
        return X_


class discriminator(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.flatten = nn.Flatten()
        # size = 3600
        self.dense1 = nn.Linear(in_features=128*2, out_features=128)
        self.dense2 = nn.Linear(in_features=128, out_features=256)
        self.dense3 = nn.Linear(in_features=256, out_features=64)
        self.dense4 = nn.Linear(in_features=64, out_features=1)
        self.dropout = nn.Dropout(0.1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, X1, X2):
        # X1_ = self.flatten(X1)
        # X2_ = self.flatten(X2)
        # X1 = X1.view(X1.size()[0], -1)
        # X2 = X2.view(X2.size()[0], -1)
        x = torch.cat((X1, X2), 1)
        x = self.dropout(F.leaky_relu(self.dense1(x), 0.1))
        x = self.dropout(F.leaky_relu(self.dense2(x), 0.1))
        x = self.dropout(F.leaky_relu(self.dense3(x), 0.1))
        x = F.leaky_relu(self.dense4(x), 0.1)
        x = self.sigmoid(x)
        return x


class FibersSiamese(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.feature = feature()
        self.discriminator = discriminator()

    def forward(self, X1, X2):
        X1_ = self.feature(X1)
        X2_ = self.feature(X2)
        # print(X1_.shape)
        X = self.discriminator(X1_, X2_)
        return X