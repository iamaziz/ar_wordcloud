import numpy as np
import PIL
import requests
from io import BytesIO


def read_mask_image(mask_img_url: str = None) -> np.array:
    """reads an image into numpy array for masking a WordCloud
    NOTE: Use a mask image! see Alice example here: https://github.com/amueller/word_cloud/blob/master/examples/alice_mask.png
    :param: mask_img_url: URL, make sure the
    """
    # image src: https://images.app.goo.gl/7JtyWX9HWe37c9ti9
    big_heart = "https://user-images.githubusercontent.com/3298308/82387916-42d5a380-9a06-11ea-8dc3-ab493228858e.png"
    if not mask_img_url:
        mask_img_url = big_heart

    response = requests.get(mask_img_url)
    img = PIL.Image.open(BytesIO(response.content))
    mask = np.array(img)
    return mask
