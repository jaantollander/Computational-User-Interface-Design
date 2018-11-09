from tempfile import NamedTemporaryFile

import cv2
import numpy as np
import skimage.io
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt


def header_image_text(v):
    assert 0.0 <= v <= 1.0
    # Grayscale colors
    r = int(255 * v)
    color = (r, r, r)
    header_text = "Jaan Tollander de Balsch"
    xy = (40, 20)

    font = ImageFont.truetype("arial.ttf", 70)
    image = Image.open("figures/header.jpg")
    draw = ImageDraw.Draw(image)
    draw.text(xy, header_text, font=font, fill=color)
    return image


def header_image_text_mask():
    color = "black"
    header_text = "Jaan Tollander de Balsch"
    xy = (40, 20)

    font = ImageFont.truetype("arial.ttf", 70)
    header = Image.open("figures/header.jpg")
    image = Image.new('RGB', header.size, color="white")
    draw = ImageDraw.Draw(image)
    draw.text(xy, header_text, font=font, fill=color)
    with NamedTemporaryFile() as file:
        image.save(file, format='png')
        arr = skimage.io.imread(file.name, as_gray=True)
    # Return a mask of dark pixels, i.e. the text pixels.
    return arr < 0.1


if __name__ == '__main__':
    mask = header_image_text_mask()
    vs = []
    means = []

    n = 20
    for i in range(n+1):
        v = i/n
        header = header_image_text(v)
        header.save(f"figures/input_{i}.png")
        image = cv2.imread(f"figures/input_{i}.png")

        # https://www.pyimagesearch.com/2018/07/16/opencv-saliency-detection/
        # initialize OpenCV's static fine grained saliency detector and
        # compute the saliency map
        saliency = cv2.saliency.StaticSaliencyFineGrained_create()
        _, saliencyMap = saliency.computeSaliency(image)

        skimage.io.imsave(f"figures/saliencyMap_{i}.png", saliencyMap)

        text = saliencyMap[mask]
        vs.append(v)
        means.append(np.mean(text))
        print(f"v: {v:.2f}: mean: {np.mean(text):.3f}")

    plt.plot(vs, means, label="Mean")
    plt.xlabel("$v$")
    plt.ylabel("Objective")
    plt.legend()
    # plt.savefig("figures/objective.png", dpi=300)
    plt.show()
