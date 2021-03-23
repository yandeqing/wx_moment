import math

from PIL import Image, ImageStat


def getBrightness(path):
    im = Image.open(path)
    stat = ImageStat.Stat(im)
    r, g, b = stat.mean
    return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))


def needBright(brightness):
    return brightness < 150


def changeBrightness(source, des, p_int=1.2):
    # open an image file (.jpg or.png) you have in the working folder
    im1 = Image.open(source)
    # multiply each pixel by 0.9 (makes the image darker)
    # works best with .jpg and .png files, darker < 1.0 < lighter
    # (.bmp and .gif files give goofy results)
    # note that lambda is akin to a one-line function
    im2 = im1.point(lambda p: p * p_int)
    # brings up the modified image in a viewer, simply saves the image as
    # a bitmap to a temporary file and calls viewer associated with .bmp
    # make certain you have associated an image viewer with this file type
    # save modified image to working folder as Audi2.jpg
    im2.save(des)


if __name__ == '__main__':
    changeBrightness('../aimages/test0.jpg', '../aimages/test3.jpg', p_int=1.3)
    f1 = getBrightness('../aimages/test0.jpg')
    f2 = getBrightness('../aimages/test3.jpg')
    print(f"【().getBrightness={f1}】")
    print(f"【().getBrightness={f2}】")
    changeBrightness('../aimages/test.jpg', '../aimages/test2.jpg', p_int=1.3)
    f1 = getBrightness('../aimages/test.jpg')
    f2 = getBrightness('../aimages/test2.jpg')
    print(f"【().getBrightness={f1}】")
    print(f"【().getBrightness={f2}】")
