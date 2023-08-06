import torch
from torch import optim, nn

from .interface import TrainSiameseInterface
from definitions import MODEL_SIAMESE_PATH


class TrainSiamese(TrainSiameseInterface):
    def __init__(self, device) -> None:
        super().__init__()
        self.device = device

    def train(self, net, train_loader, epochs=15) -> None:
        optimizer = optim.Adam(net.parameters(), lr=0.00000001)
        # criterion = nn.BCEWithLogitsLoss()
        criterion = nn.BCELoss()
        # criterion = nn.CrossEntropyLoss()
        net=net.to(self.device)
        print(net)
        try:
            checkpoint = torch.load(MODEL_SIAMESE_PATH)
            net.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            epoch = checkpoint['epoch']
            best_loss = checkpoint['loss']
            print('best model epoch:{} loss:{}'.format(epoch, best_loss))
        except:
            print("Nenhum modelo salvo")

        for epoch in range(epochs):
            D_running_loss = 0
            for i, (img1_set, img2_set, labels) in enumerate(train_loader):
                #converte dados
                img1_set = img1_set.to(self.device)
                img2_set = img2_set.to(self.device)
                labels = labels.to(self.device)

                optimizer.zero_grad()
                outputs = net.forward(img1_set, img2_set)
                D_loss = criterion(outputs.view(*labels.shape), labels)

                D_loss.backward()
                optimizer.step()

                D_running_loss += D_loss.item()
                # print('train ',i,imagens_reais.shape,D_loss_reais,D_loss_falsos)

            net.train()
            D_running_loss /= len(train_loader)

            print('epoch -> {}/{} loss -> {} '.format(epoch,epochs, D_running_loss))
            torch.save({
                'epoch': epoch,
                'model_state_dict': net.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': D_running_loss
            }, MODEL_SIAMESE_PATH)

    def train_epoch(self, net, X) -> None:
        pass
