import os
import random

import cv2
import pandas as pd
from roboflow import Roboflow
from skimage import io
import numpy as np
import torch
from PIL import Image
from pylabel import importer
from torchvision import transforms
from definitions import FIBERS_REPO
from PIL import ImageEnhance

class FibersDataset(torch.utils.data.Dataset):
    """Fibers dataset. to train neural net"""

    def __init__(self, transform=None, random_aug=False):
        # rf = Roboflow(api_key="JhqX7HlUL57cmzbBqIav")
        # project = rf.workspace().project("fibberpaper")
        # dataset = project.version(1).download(model_format="yolov5",location=FIBERS_REPO)
        dataset1 = importer.ImportYoloV5(path=FIBERS_REPO + '{0}test{0}labels'.format(os.sep),
                                         path_to_images=FIBERS_REPO + '{0}test{0}images'.format(os.sep))
        dataset2 = importer.ImportYoloV5(path=FIBERS_REPO + '{0}train{0}labels'.format(os.sep),
                                         path_to_images=FIBERS_REPO + '{0}train{0}images'.format(os.sep))
        dataset3 = importer.ImportYoloV5(path=FIBERS_REPO + '{0}valid{0}labels'.format(os.sep),
                                         path_to_images=FIBERS_REPO + '{0}valid{0}images'.format(os.sep))
        dataset = pd.concat([dataset1.df, dataset3.df, dataset2.df])

        self.mapa, self.data = self.extractFibersOfImagens(dataset)
        self.sourceTransform = transform
        self.rootDir = '.'
        self.random_aug = random_aug
        self.random_aug_prob = 0.5

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        image = Image.fromarray(self.data[idx]).copy()
        pos = random.randrange(0, len(self.data))
        sim = random.randrange(0,2)
        if (sim == 1) & (pos != idx):
            image2 = Image.fromarray(self.data[pos]).copy()
            class_id = torch.tensor([0.9])
        else:
            image2 = image.copy()
            class_id = torch.tensor([0.])

        if self.random_aug:
            image2 = self.random_augmentation(image2, self.random_aug_prob)

        if self.sourceTransform:
            image = self.sourceTransform(image)
            image2 = self.sourceTransform(image2)

        return image, image2, class_id

    # extrar o conjunto de pixel das fibras contidas no boundbox descrito no dataframe
    def extractFibersOfImagens(self, df):
        mapa = {}
        fibers = []
        # para cada linha
        for index, row in df.iterrows():

            # if "idoc" in row.img_filename:
            #     continue

            # ler a imagem e salva no map
            path_full = '{}/{}'.format(row.img_folder, row.img_filename)
            if mapa.get(row.img_filename) is None:
                img = io.imread(path_full)
                mapa[row.img_filename] = img
            # recorta o box da fibra
            x1, y1, x2, y2 = int(row.ann_bbox_xmin), int(row.ann_bbox_ymin), int(row.ann_bbox_xmax), int(
                row.ann_bbox_ymax)
            fibers.append(mapa[row.img_filename][y1:y2, x1:x2])
            # normaliza a imagem com o transforms
            # tenta remover o fundo
        return mapa, np.array(fibers, dtype=object)

    def random_augmentation(self, img, prob):
        def rotate(img):
            degrees = [90, 180, 270]
            index = random.randrange(0, len(degrees))
            return img.rotate(degrees[index])

        def flip_tb(img):
            return img.transpose(Image.FLIP_TOP_BOTTOM)

        def flip_lr(img):
            return img.transpose(Image.FLIP_LEFT_RIGHT)

        def translate(img):
            d_x = random.randrange(-5, 5)
            d_y = random.randrange(-5, 5)
            img = np.array(img)
            mat = np.float32([[1, 0, d_x], [0, 1, d_y]])
            num_rows, num_cols = img.shape[:2]
            img = cv2.warpAffine(img, mat, (num_cols, num_rows))
            return Image.fromarray(np.uint8(img))

        def scale(img):
            scale = 0.7 + 0.6 * random.random()
            img = np.array(img)
            mat = np.float32([[scale, 0, 0], [0, scale, 0]])
            num_rows, num_cols = img.shape[:2]
            img = cv2.warpAffine(img, mat, (num_cols, num_rows))
            return Image.fromarray(np.uint8(img))

        def contrast(img):
            levels = [0.3, 0.5, 0.7,1.4]
            index = random.randrange(0, len(levels))
            enh = ImageEnhance.Contrast(img)
            new_img=enh.enhance(levels[index])
            return new_img

        def color(img):
            levels = [0.3, 0.5, 0.7,1.4]
            index = random.randrange(0, len(levels))
            enh = ImageEnhance.Color(img)
            new_img=enh.enhance(levels[index])
            return new_img

        def brightness(img):
            levels = [0.3, 0.5, 0.7,1.4]
            index = random.randrange(0, len(levels))
            enh = ImageEnhance.Brightness(img)
            new_img=enh.enhance(levels[index])
            return new_img

        def sharpness(img):
            levels = [0.3, 0.5, 0.7,1.4]
            index = random.randrange(0, len(levels))
            enh = ImageEnhance.Sharpness(img)
            new_img=enh.enhance(levels[index])
            return new_img

        if random.random() > prob:
            return img

        # transform_ops = [flip_tb, flip_lr, rotate,rotate,rotate]
        transform_ops = [contrast,color,brightness,sharpness,flip_tb, flip_lr]
        op_len = random.randrange(1, len(transform_ops) + 1)
        ops = random.sample(transform_ops, op_len)
        ops.append(rotate)
        for op in ops:
            img = op(img)
        return img


if __name__ == '__main__':

    preprocess = transforms.Compose([
        transforms.Resize(128),
        transforms.CenterCrop(120),
        transforms.ToTensor(),
        # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    train = FibersDataset(transform=preprocess, random_aug=True)
    train_loader = torch.utils.data.DataLoader(train, batch_size=4)
    for i, (img1_set, img2_set, labels) in enumerate(train_loader):
        print(img1_set.shape, img2_set.shape, labels)
        # img1.show()
        # img2.show()
