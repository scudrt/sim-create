import pickle
import PIL.Image
import numpy as np
import dnnlib.tflib as tflib
from util.generator_model import Generator
import matplotlib.pyplot as plt

model = 0
model_res = 0
latent = []
dlatent = []

#初始化调参变量
def init(_model, _latent, _res):
    global model, model_res, latent, dlatent
    model = _model
    model_res = _res
    latent = _latent
    dlatent = []

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
    # latent_vector = latent_vector.reshape((1, 18, 512))
    generator.set_dlatents(latent_vector)
    img_array = generator.generate_images()[0]
    img = PIL.Image.fromarray(img_array, 'RGB')
    return img

def move_latent(latent_vector, direction, coeffs, generator):
    '''latent_vector是人脸潜编码，direction是人脸调整方向，coeffs是变化步幅的向量，generator是生成器'''
    k = min(len(latent_vector[0]), len(direction))
    for i, coeff in enumerate(coeffs):
        print('step ' + str(coeff))
        latent_vector[:] = (latent_vector + coeff*direction[:k])[:]
        result = generate_image(latent_vector, generator)
    return result

#Gs_network来自原生成模型.pkl；step传入coeffs表示调整的幅度；pic_num表示选择第几张图片；dir_flag选择调整的方向
def select_directions(dir_path, step):
    global dlatent, latent, model, model_res

    if len(dlatent) == 0:
        dlatent = model.components.mapping.run(np.array(latent), None)
    
    direction = np.load(dir_path)
    
    print(latent)
    print(dlatent)
    print(direction)

    #调整幅度
    coeffs = [step]

    #生成器，不知道为什么第一次调参会导致图像发生一定变形
    generator = Generator(model, batch_size=1, model_res=model_res, randomize_noise=False)

    newImage = move_latent(dlatent, direction, coeffs, generator)
    return newImage

def main():
    Gs = face_model()
    for i in range(3):
        select_directions(Gs, 1, 2)
        print("save successfully", i)

if __name__ == "__main__":
    main()