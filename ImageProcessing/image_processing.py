import skimage.io as io
import os.path as path
import scipy.ndimage as ndimage
import sklearn.preprocessing as ppr

import numpy

memes = 'sergey.jpg'
salem_sad = 'salem_sad.jpg'
salem_hangover = 'salem_hangover.jpg'
homer = 'homer.jpg'
harold = 'harold.jpg'
cwd = path.dirname(path.curdir)
sources = path.join(cwd, 'sources')
results = path.join(cwd, 'results')

matrix_for_blur = numpy.random.normal(size=(3, 3))


def gaussian_blur_greyscale(file_name, new_file_name=None):
    image = io.imread(path.join(sources, file_name), as_grey=True)
    out = numpy.zeros((len(image), len(image[0])))

    for i in range(len(matrix_for_blur) // 2, len(image)-1):
        for j in range(len(matrix_for_blur) // 2, len(image[i])-1):
            out[numpy.ix_([i - 1, i + 1], [j - 1, j + 1])] = ndimage.convolve(image[numpy.ix_([i - 1, i + 1],
                                                                                              [j - 1, j + 1])],
                                                                              matrix_for_blur)


    ppr.normalize(out)
    for i in range(0, len(out)):
        for j in range(0, len(out[0])):
            if out[i][j] > 1 or out[i][j] < -1:
                out[i][j] = 0
    print(out)
    io.imsave(path.join(results, file_name if new_file_name is None else new_file_name), out)


def negate(file_name, new_file_name=None):
    image = io.imread(path.join(sources, file_name))
    for row in image:
        for pixel in row:
            for i in range(3):
                pixel[i] = 255 - pixel[i]
    io.imsave(path.join(results, file_name if new_file_name is not None else new_file_name), image)


def main():
    gaussian_blur_greyscale(harold)


if __name__ == '__main__':
    main()
