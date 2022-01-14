# -*- coding: utf-8 -*-
'''
    :file: predict.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2022/01/14 17:56:00
'''
import os
import torch
from PIL import Image
import numpy as np
from torch.autograd import Variable
from school_sdk.check_code import captcha_setting
from school_sdk.check_code.dataset import get_predict_data_loader
from school_sdk.check_code.model import CNN

data_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'model.pkl'

# device = torch.device("cpu")
# cnn = CNN().to(device=device)
cnn = CNN()
cnn.eval()
cnn.load_state_dict(torch.load(data_file, map_location="cpu"))


def check(image: Image) -> str:

    predict_dataloader = get_predict_data_loader(image)
    
    for i, (img) in enumerate(predict_dataloader):
        vimage = Variable(img)
        predict_label = cnn(vimage)
        c0 = captcha_setting.ALL_CHAR_SET[np.argmax(
            predict_label[0, 0:captcha_setting.ALL_CHAR_SET_LEN].data.numpy())]
        c1 = captcha_setting.ALL_CHAR_SET[np.argmax(
            predict_label[0, captcha_setting.ALL_CHAR_SET_LEN:2 * captcha_setting.ALL_CHAR_SET_LEN].data.numpy())]
        c2 = captcha_setting.ALL_CHAR_SET[np.argmax(
            predict_label[0, 2 * captcha_setting.ALL_CHAR_SET_LEN:3 * captcha_setting.ALL_CHAR_SET_LEN].data.numpy())]
        c3 = captcha_setting.ALL_CHAR_SET[np.argmax(
            predict_label[0, 3 * captcha_setting.ALL_CHAR_SET_LEN:4 * captcha_setting.ALL_CHAR_SET_LEN].data.numpy())]
        c4 = captcha_setting.ALL_CHAR_SET[np.argmax(
            predict_label[0, 4 * captcha_setting.ALL_CHAR_SET_LEN:5 * captcha_setting.ALL_CHAR_SET_LEN].data.numpy())]
        c5 = captcha_setting.ALL_CHAR_SET[np.argmax(
            predict_label[0, 5 * captcha_setting.ALL_CHAR_SET_LEN:6 * captcha_setting.ALL_CHAR_SET_LEN].data.numpy())]

        c = f'{c0}{c1}{c2}{c3}{c4}{c5}'

        return c
