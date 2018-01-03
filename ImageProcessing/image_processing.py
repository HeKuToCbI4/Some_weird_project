import skimage.io as io
import os.path as path
import scipy.ndimage as ndimage

import numpy as np

memes = 'sergey.jpg'
salem_sad = 'salem_sad.jpg'
salem_hangover = 'salem_hangover.jpg'
homer = 'homer.jpg'
harold = 'harold.jpg'
cwd = path.dirname(path.curdir)
sources = path.join(cwd, 'sources')
results = path.join(cwd, 'results')


def convolve_as_grey(file_name, kernel, new_file_name=None, save=False):
    image = io.imread(path.join(sources, file_name), as_grey=True)
    out = ndimage.convolve(image, kernel)
    if save:
        if new_file_name is None:
            io.imsave(path.join(results, file_name), out)
        else:
            io.imsave(path.join(results, new_file_name), out)
    return out


def gaussian(file_name, sigma, new_file_name=None, save=False):
    image = io.imread(path.join(sources, file_name))
    image = ndimage.gaussian_filter(image, sigma)
    if save:
        io.imsave(path.join(results, file_name if new_file_name is None else new_file_name), image)
    return image


def negate(file_name, new_file_name=None, save=False):
    image = io.imread(path.join(sources, file_name))
    for row in image:
        for pixel in row:
            for i in range(3):
                pixel[i] = 255 - pixel[i]
    if save:
        io.imsave(path.join(results, file_name if new_file_name is None else new_file_name), image)
    return image


def sharpen(file_name, new_file_name=None, save=False):
    kernel = np.array([[-1/9, -1/9, -1/9], [-1/9, 1, -1/9], [-1/9, -1/9, -1/9]])
    convolve_as_grey(file_name, kernel, new_file_name=new_file_name, save=save)


def blur(file_name, new_file_name=None, save=False):
    kernel = np.array([[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]])
    convolve_as_grey(file_name, kernel, new_file_name=new_file_name, save=save)


def main():
    blur(salem_sad, save=True)


if __name__ == '__main__':
    main()
