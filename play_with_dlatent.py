import pickle
import PIL.Image
import numpy as np
import dnnlib.tflib as tflib
from util.generator_model import Generator
import matplotlib.pyplot as plt

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

def generate_image(latent_vector, generator):
    latent_vector = latent_vector.reshape((1, 18, 512))
    generator.set_dlatents(latent_vector)
    img_array = generator.generate_images()[0]
    img = PIL.Image.fromarray(img_array, 'RGB')
    return img

def move_latent(latent_vector, direction, coeffs, generator):
    '''latent_vector是人脸潜编码，direction是人脸调整方向，coeffs是变化步幅的向量，generator是生成器'''
    for i, coeff in enumerate(coeffs):
        new_latent_vector = latent_vector.copy()
        new_latent_vector[:8] = (latent_vector + coeff*direction)[:8]
        result = generate_image(new_latent_vector, generator)

        # 显示图片
        # plt.imshow(result)
        # plt.show()
        # result.save('result_picture/result.png')
    return result

def face_model():
    # 在这儿选择生成器
    tflib.init_tf()
    print("open model")
    with open('model/animeface.pkl', "rb") as f:
        generator_network, discriminator_network, Gs_network = pickle.load(f)
    generator = Generator(Gs_network, batch_size=1, randomize_noise=False)
    return Gs_network

#Gs_network来自原生成模型.pkl；step传入coeffs表示调整的幅度；pic_num表示选择第几张图片；dir_flag选择调整的方向
def select_directions(Gs_network, step, pic_num, dir_flag):
    generator = Generator(Gs_network, batch_size=1, randomize_noise=False)

    # 在这儿选择人物的潜码，注意要与生成器相匹配。潜码来自生成目录下有个generate_codes文件夹里的txt文件。
    face_latent = read_feature('chosen_picture/generate_code/' + pic_num + '.txt')
    stack_latents = np.stack(face_latent for _ in range(1))
    face_dlatent = Gs_network.components.mapping.run(stack_latents, None)

    print("dir_flag", dir_flag)
    
    paths = [
        'latent_directions/beauty.npy',
        'latent_directions/angle_horizontal.npy',
        'latent_directions/gender.npy',
        'latent_directions/race_white.npy',
        'latent_directions/race_black.npy',
        'latent_directions/smile.npy',
        'latent_directions/race_yellow.npy'
    ]
    direction = np.load(paths[dir_flag-1])

    # 在这儿选择调整的大小，向量里面的值表示调整幅度，可以自行编辑，对于每个值都会生成一张图片并保存。
    coeffs = [step]
    # 开始调整并保存图片
    newImage = move_latent(face_dlatent, direction, coeffs, generator)
    print("save successfully")
    return newImage


def main():
    Gs = face_model()
    for i in range(3):
        select_directions(Gs, 1, 2)
        print("save successfully", i)



if __name__ == "__main__":
    main()