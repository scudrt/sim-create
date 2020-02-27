"""Minimal script for generating an image using pre-trained StyleGAN generator."""

import os
import pickle
import numpy as np
import PIL.Image
import dnnlib.tflib as tflib
import multiprocessing
import time

synthesis_kwargs = dict(output_transform=dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True), minibatch_size=8)

def text_save(file, data):  # save generate code, which can be modified to generate customized style
    for i in range(len(data[0])):
        s = str(data[0][i])+'\n'
        file.write(s)

def select_path(model_flag):
    path = {
        0: 'model/generator_yellow.pkl',
        1: 'model/generator_model.pkl',
        2: 'model/generator_anime.pkl',
        3: 'model/generator_ancient.pkl'
    }
    return path.get(model_flag, None)

def generate(Gs):
    # Prepare result folder
    result_dir = 'result_picture'
    os.makedirs(result_dir, exist_ok=True)
    os.makedirs(result_dir + '/generate_code', exist_ok=True)
    for i in range(5):
        # Generate latent.
        latents = np.random.randn(1, Gs.input_shape[1])

        # Save latent.
        txt_filename = os.path.join('chosen_picture/generate_code/' + str(i) + '.txt')
        file = open(txt_filename, 'w')
        text_save(file, latents)

        # Generate image.
        fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
        images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=True, output_transform=fmt)

        # Save image.
        png_filename = os.path.join(result_dir, str(i) + '.png')
        test = PIL.Image.fromarray(images[0], 'RGB')
        print(type(test))
        test.save(png_filename)

        # Close file.
        file.close()

#def face_select(model_flag):
def face_select(model_flag):
    # Initialize TensorFlow.
    time_start1 = time.time()#第一段开始计时
    tflib.init_tf()
    time_end1 = time.time()#第一段结束计时
    time1 = time_end1 - time_start1
    print('initiate_time_cost:', time1, 's')

    # Select and load pre-trained network through model_flag

    model_path = select_path(model_flag)

    time_start2 = time.time()  # 第二段开始计时
    with open(model_path, "rb") as f:
        _G, _D, Gs = pickle.load(f, encoding='latin1')
    time_end2 = time.time()  # 第二段结束计时
    time2 = time_end2 - time_start2
    print('open_model_time_cost:', time2, 's')

    # Print network details.
    # Gs.print_layers()
    return Gs

def func1(Gs):
    for i in range(10):
        generate(Gs)

def main():
    Gs = face_select(1)
    p = multiprocessing.Process(target=func1)
    p.start()
    p.join()
    func1(Gs)
    p.kill()

if __name__ == "__main__":
    main()

