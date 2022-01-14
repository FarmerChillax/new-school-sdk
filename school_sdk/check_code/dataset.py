from email import header


# -*- coding: utf-8 -*-
'''
    :file: dataset.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2022/01/13 15:37:31
'''
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as transforms
from torch.utils.data.dataloader import DataLoader

transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.ToTensor(),
])


class MyDataset(Dataset):
    def __init__(self, image: Image = None, transform=None) -> None:
        self.image = image
        self.transform = transform

    def get_img(self):
        if self.transform is not None:
            self.image = self.transform(self.image)
        return self.image

    def __len__(self):
        return 1

    def __getitem__(self, index):
        if self.transform is not None:
            image = self.transform(self.image)

        return image

def get_predict_data_loader(img: Image):
    dataset = MyDataset(img, transform=transform)
    return DataLoader(dataset, batch_size=1, shuffle=True)
