import cv2
from PIL import Image, ImageFont, ImageDraw
import skimage.io


def grayscale(v):
    """
    http://www.perbang.dk/rgb/3F3F3F/

    :param v: v=0 -> white, v=1 -> black
    :return:
    """
    assert 0 <= v <= 1
    r = int(255 * v)
    return "#{0}{0}{0}".format(hex(r)[2:])


def header_image_text(v):
    color = grayscale(v)
    header_text = "Jaan Tollander de Balsch"
    xy = (40, 20)

    font = ImageFont.truetype("arial.ttf", 70)
    image = Image.open("figures/header.jpg")
    # TODO: image shading
    draw = ImageDraw.Draw(image)
    draw.text(xy, header_text, font=font, fill=color)
    return image


if __name__ == '__main__':
    n = 10
    for i in range(n+1):
        v = i/n
        header = header_image_text(v)
        header.save(f"figures/input_{i}.png")
        image = cv2.imread(f"figures/input_{i}.png")

        # https://www.pyimagesearch.com/2018/07/16/opencv-saliency-detection/
        # initialize OpenCV's static fine grained saliency detector and
        # compute the saliency map
        saliency = cv2.saliency.StaticSaliencyFineGrained_create()
        (success, saliencyMap) = saliency.computeSaliency(image)

        # if we would like a *binary* map that we could process for contours,
        # compute convex hull's, extract bounding boxes, etc., we can
        # additionally threshold the saliency map
        # threshMap = cv2.threshold(saliencyMap, 0, 255,
        #                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        skimage.io.imsave(f"figures/saliencyMap_{i}.png", saliencyMap)
