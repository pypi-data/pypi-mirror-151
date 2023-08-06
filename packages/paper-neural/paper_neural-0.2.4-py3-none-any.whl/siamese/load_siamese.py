import numpy as np
import torch
from torchvision import transforms

from paper_neural.siamese_util import get_model_siamese, match_fibers, plot_pair_match
from siamese.repository import FibersDataset


device = torch.device('cuda') if torch.cuda.is_available else torch.device('cpu')
net = get_model_siamese(device)
net.eval()

preprocess = transforms.Compose([
    transforms.Resize(64),
    transforms.CenterCrop(60),
    transforms.ToTensor(),
    # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

train = FibersDataset(transform=preprocess, random_aug=False)


lista_fibras = torch.tensor([]);
for idx,(input_image1, input_image2, classe) in enumerate(train):
    input_batch1 = input_image1.unsqueeze(0)
    lista_fibras= torch.cat((input_batch1, lista_fibras), 0)
    print(lista_fibras.shape)
    if lista_fibras.shape[0]==300:
        break

lista_a = lista_fibras[240:265]
lista_b = lista_fibras[240:265]

rotaciona = transforms.Compose([
    transforms.RandomVerticalFlip(p=0.5),
    transforms.RandomHorizontalFlip(p=0.5),
])
# lista_b = rotaciona(lista_b)

distances = np.ones(shape=(lista_a.shape[0],lista_b.shape[0]))

if torch.cuda.is_available():
    net = net.to('cuda')
for i in range(lista_a.shape[0]):
    img_i = lista_a[i]
    input_batch1 = img_i.unsqueeze(0)
    if torch.cuda.is_available():
        input_batch1 = input_batch1.to('cuda')
    for j in range(lista_b.shape[0]):
        img_j = lista_b[j]
        input_batch2 = img_j.unsqueeze(0)
        if torch.cuda.is_available():
            input_batch2 = input_batch2.to('cuda')
        with torch.no_grad():
            output = net(input_batch1, input_batch2)
            out1 = net.feature(input_batch1)
            out2 = net.discriminator(out1,out1)
        distances[i][j]= output.cpu().numpy()[0][0]

matches = match_fibers(distances,max_distance=0.30)
print(matches)
plot_pair_match(matches,lista_a,lista_b)
print('fim')