from ImageProcessing.ImageProcessor import ImageProcessor

memes = 'sergey.jpg'
salem_sad = 'salem_sad.jpg'
salem_hangover = 'salem_hangover.jpg'
homer = 'homer.jpg'
harold = 'harold.jpg'


image_processor = ImageProcessor()

def main():
    image_processor.gaussian(salem_hangover, 1, new_file_name='HANGOVER.jpg', save=True)


if __name__ == '__main__':
    main()
