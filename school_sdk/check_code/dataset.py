from email import header


# -*- coding: utf-8 -*-
'''
    :file: dataset.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2022/01/13 15:37:31
'''
transform = transforms.Compose([
    transforms.Grayscale(),
    transforms.ToTensor(),
])


class MyDataset(Dataset):
    def __init__(self, image: bytes = None, transform=None) -> None:
        self.image = image
        self.transform = transform

    def get_img(self):
        image = Image.open(self.image)
        if self.transform is not None:
            image = self.transform(image)

        return image

    def __len__(self):
        return 1

    def __getitem__(self, index):
        image = Image.open(captcha_setting.PREDICT_DATASET_PATH +
              os.sep + 'p_123.jfif')
        if self.transform is not None:
            image = self.transform(image)

        return image


def get_predict_data_loader(img: bytes):
    dataset = MyDataset(img, transform=transform)
    return DataLoader(dataset, batch_size=1, shuffle=True)
