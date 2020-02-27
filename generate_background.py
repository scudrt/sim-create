# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""Minimal script for generating an image using pre-trained StyleGAN generator."""

import os
import pickle
import numpy as np
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import config


#存储每个图片的latents
def save_latents(i, latents):
    if i == 0:
        global latents0
        latents0 = latents
    if i == 1:
        global latents1
        latents1 = latents
    if i == 2:
        global latents2
        latents2 = latents
    if i == 3:
        global latents3
        latents3 = latents
    if i == 4:
        global latents4
        latents4 = latents

def select_latents(pic_num):
    latents = {
        '0': latents0,
        '1': latents1,
        '2': latents2,
        '3': latents3,
        '4': latents4,
    }
    return latents.get(pic_num, None)

def select_path(model_flag):
    path = {
        0: 'model/bedroom_generator.pkl',
        #1: 'model/',未完成
        #2: 'model/',
        #3: 'model/',
    }
    return path.get(model_flag, None)

def read_feature(file_name):
    file = open(file_name, mode='r')
    # 使用readlines() 读取所有行的数据，会返回一个列表，列表中存放的数据就是每一行的内容
    contents = file.readlines()
    # 准备一个列表，用来存放取出来的数据
    code = np.zeros((512, ))
    # for循环遍历列表，去除每一行读取到的内容
    for i in range(512):
        name = contents[i]
        name = name.strip('\n')
        code[i] = name
    code = np.float32(code)
    file.close()
    return code

def text_save(file, data):  # save generate code, which can be modified to generate customized style
    for i in range(len(data[0])):
        s = str(data[0][i])+'\n'
        file.write(s)

#两种生成，type=0:生成5张随机产生图片，返回latents type=1:根据前一次pic_name的生成1张
def generate_bg(type, Gs, pic_num, slider):
    #生成5张
    if type == 0:
        for i in range(5):
            # Pick latent vector.
            rnd = np.random.RandomState(None)
            print(i)
            latents = rnd.randn(1, Gs.input_shape[1])

            # Save latent.
            #txt_filename = os.path.join('chosen_picture/generate_code/' + str(i) + '.txt')
            #file = open(txt_filename, 'w')
            #text_save(file, latents)
            save_latents(i, latents)

            # Generate image.
            fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
            images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=True, output_transform=fmt)

            # Save image.
            os.makedirs(config.result_dir, exist_ok=True)
            png_filename = os.path.join(config.result_dir, str(i) + '.png')
            PIL.Image.fromarray(images[0], 'RGB').save(png_filename)

        #return latents
    #生成1张
    else:
        #读出latents
        #print('read latents')
        #latents = read_feature('input_latent/' + pic_num + '.txt')
        #for j in range(len(latents)):
        #    latents[j] /= 50
        #print(type(latents))
        #print("pic_num:", pic_num)
        #rnd = np.random.RandomState(None)

        latents = select_latents(pic_num)

        #latents = rnd.randn(1, Gs.input_shape[1])
        for j in range(len(latents)):
            latents[j] = latents[j] + slider/500
        # Generate image.
        fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=True, output_transform=fmt)

        # Save image.
        return PIL.Image.fromarray(images[0])



#选择读入哪个模型
def bg_select(model_flag):
    # Initialize TensorFlow.
    tflib.init_tf()

    # Load pre-trained network.
    # url = 'https://drive.google.com/uc?id=1MEGjdvVpUsu1jB4zrXZN7Y4kBBOzizDQ' # karras2019stylegan-ffhq-1024x1024.pkl
    #mypath = os.path.abspath('results\\00000-sgan-realface-1gpu\\network-snapshot-000140.pkl')
    mypath = select_path(model_flag)
    # with dnnlib.util.open_url(url, cache_dir=config.cache_dir) as f:
    with open(mypath, 'rb') as f:
        _G, _D, Gs = pickle.load(f)
        # _G = Instantaneous snapshot of the generator. Mainly useful for resuming a previous training run.
        # _D = Instantaneous snapshot of the discriminator. Mainly useful for resuming a previous training run.
        # Gs = Long-term average of the generator. Yields higher-quality results than the instantaneous snapshot.

    # Print network details.
    Gs.print_layers()
    #generate_bg(1, Gs, '1', 26)
    return Gs


def main():
    bg_select(0)

if __name__ == "__main__":
    main()
