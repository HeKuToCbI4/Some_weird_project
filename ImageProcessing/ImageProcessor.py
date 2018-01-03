import os.path as path

import numpy as np
import scipy.ndimage as ndimage
import skimage.io as io

cwd = path.dirname(path.curdir)
sources = path.join(cwd, 'sources')
results = path.join(cwd, 'results')


class ImageProcessor:
    def convolve_as_grey(self, file_name, kernel, new_file_name=None, save=False):
        image = io.imread(path.join(sources, file_name), as_grey=True)
        out = ndimage.convolve(image, kernel)
        if save:
            if new_file_name is None:
                io.imsave(path.join(results, file_name), out)
            else:
                io.imsave(path.join(results, new_file_name), out)
        return out

    def gaussian(self, file_name, sigma, new_file_name=None, save=False):
        image = io.imread(path.join(sources, file_name))
        image = ndimage.gaussian_filter(image, sigma)
        if save:
            io.imsave(path.join(results, file_name if new_file_name is None else new_file_name), image)
        return image

    def negate(self, file_name, new_file_name=None, save=False):
        image = io.imread(path.join(sources, file_name))
        for row in image:
            for pixel in row:
                for i in range(3):
                    pixel[i] = 255 - pixel[i]
        if save:
            io.imsave(path.join(results, file_name if new_file_name is None else new_file_name), image)
        return image

    def sharpen(self, file_name, new_file_name=None, save=False):
        kernel = np.array([[-1 / 9, -1 / 9, -1 / 9], [-1 / 9, 1, -1 / 9], [-1 / 9, -1 / 9, -1 / 9]])
        return self.convolve_as_grey(file_name, kernel, new_file_name=new_file_name, save=save)

    def blur(self, file_name, new_file_name=None, save=False):
        kernel = np.array([[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]])
        return self.convolve_as_grey(file_name, kernel, new_file_name=new_file_name, save=save)
