import matplotlib
import numpy as np
import torch
from torchsummary import summary
from torchvision import transforms

from siamese.fibers_siamese import FibersSiamese
from repository import FibersDataset
from siamese import TrainSiamese
import matplotlib.pyplot as plt

from paper_neural.siamese_util import plot_match


def plot_result(input_image,conv_unif):
  plt.style.use('classic')
  matplotlib.use('TkAgg')
  fig, (ax1, ax2) = plt.subplots(1, 2)
  # ax1.imshow(input_image.transpose(2, 0))
  ax1.imshow(transforms.ToPILImage()(input_image))
  ax2.imshow(conv_unif)
  plt.show()


def extract_feature(model1,input_image):
    input_batch = input_image.unsqueeze(0)
    # move the input and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model1.to('cuda')
    with torch.no_grad():
        output = model1(input_batch)
        out1 = output.cpu().numpy()
    conv_unif = np.sum(out1[0], axis=0) / out1[0].shape[0]
    return conv_unif

if __name__ == '__main__':
    # criar transformador
    # transform = transforms.ToTensor()
    preprocess = transforms.Compose([
        transforms.Resize(64),
        transforms.CenterCrop(60),
        transforms.ToTensor(),
        # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    net = FibersSiamese()

    device = torch.device('cuda') if torch.cuda.is_available else torch.device('cpu')

    img1 = (3, 60, 60)
    summary(net.to('cpu'), [img1, img1], device='cpu')

    train = FibersDataset(transform=preprocess, random_aug=True)
    # criar loader
    train_loader = torch.utils.data.DataLoader(train, batch_size=128)
    TrainSiamese(device=device).train(net=net, train_loader=train_loader, epochs=5000)



    # for input_image1,input_image2, classe in train:
    #     # input_image,_ = next(iter(train))
    #     input_batch1 = input_image1.unsqueeze(0)
    #     input_batch2 = input_image2.unsqueeze(0)
    #     print(input_batch1.shape)
    #     # move the input and model to GPU for speed if available
    #     if torch.cuda.is_available():
    #         input_batch1 = input_batch1.to('cuda')
    #         input_batch2 = input_batch2.to('cuda')
    #         net = net.to('cuda')
    #     with torch.no_grad():
    #         output = net(input_batch1, input_batch2)
    #         res = output.cpu().numpy()[0][0]
    #         ver = classe.cpu().numpy()[0]
    #         print('e - > r {}=>{}'.format(ver, res))
    #         plot_match(input_image1,input_image2,ver,res)


    # model1 = net.feature
    # from PIL import Image

    # with Image.open("../data/images/IMG_2043.jpg") as im:
    #     im.rotate(45).show()
    #
    # im1 = preprocess(im)
    # im2 = preprocess(im.rotate(90))
    #
    # conv_unif = extract_feature(model1, im1)
    # plot_result(im1, conv_unif)
    #
    # conv_unif = extract_feature(model1, im2)
    # plot_result(im2, conv_unif)
    #
    # for input_image, _ in train:
    #     # input_image,_ = next(iter(train))
    #     conv_unif = extract_feature(model1,input_image)
    #     plot_result(input_image, conv_unif)

