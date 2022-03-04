import numpy as np
import imageio
from matplotlib import pyplot as  plt

"""
TODO
Implement the functions below using only numpy operations and functions.
DO NOT use any Python control flow (no cycles, no ifs, etc.) in any of the tasks.
"""


def max_row_index(x: np.ndarray) -> int:
    """
    Find the index of the row that contains the maximum value in `x`.
    You can assume that `x` is a 2D array and that there is only one maximal value.

    See tests for examples.
    """
    return np.argmax(np.max(x,axis=1))


def sum_edges(x: np.ndarray) -> int:
    """
    Sum the edges of the input array.
    The input will be a 2D array of arbitrary shape (each dimension will have at least a single element).

    DO NOT count any edge element more than once!
    See tests for examples.
    """
    # toto bylo puvodni reseni, samozrejme jsem se nachytal u [1].... :D
    # row1 = x[0]
    # col1 = x[:, [0]]
    # tmpRow = x[::-1]
    # row2 = tmpRow[0]
    # tmpCol = x[:,[-1]]
    # valRow1Col1 = (np.sum(col1) + np.sum(row1)) -row1[0]
    # tmpRow2 = row2[::-1]
    # valRow2Col2 = (np.sum(tmpCol) + np.sum(row2)) -tmpRow2[0]
    # rowobracene = row1[::-1]
    # valtmp = rowobracene[0] # tu je 6
    # valtmprow2 = row2[0]
    # result = valRow1Col1 + valRow2Col2 -valtmp - valtmprow2
    # xRev = x[::-1]

    sumAll = np.sum(x)
    sumStredy = np.sum(x[1:-1,1:-1])
    return sumAll - sumStredy

def display(img):
    plt.imshow(img)
    plt.axis('off')
    return plt.show()
def to_bw(img: np.ndarray) -> np.ndarray:
    """
    Convert the input np.uint8 RGB image to a black-and-white RGB image.
    The returned image should have shape (height, image, 3) and data type np.uint8.

    See data/fei.png -> data/fei-bg.png.
    """
    img = img.astype(np.float16)
    r = np.array(img[:, :, 0])
    g = np.array(img[:, :, 1])
    b = np.array(img[:, :, 2])
    #myslel jsem si, ze neco takoveho bude fungovat, ovsem nefunguje :(
    avg = (img[:, :, 0] +img[:, :, 1] +img[:, :, 2]) /3

    #stackoverflow :/
    # r = r * .299
    # g = g * .587
    # b = b * .114

    #avg = r + g + b
    gray = img.copy()

    gray[:, :, 0] = avg
    gray[:, :, 1] = avg
    gray[:, :, 2] = avg
    gray = gray.astype(np.uint8)
    return gray




def mirror(img: np.ndarray) -> np.ndarray:
    """
    Mirror the input np.uint8 RGB image along the vertical axis.

    See data/pyladies.png -> data/pyladies-mirrored.png.
    """
    imgTmp = img.copy()
    imgTmp = imgTmp[...,::-1,:]
    a = np.concatenate([img,imgTmp],axis=1)
    return a


def split_and_rotate(img: np.ndarray, n: int) -> np.ndarray:
    """
    Split the input np.uint8 RGB image into `n` parts horizontally.
    Then place the parts so that they lie below each other vertically.

    See data/pyladies.png -> data/pyladies-split-and-rotate.png.
    """
    tmp = np.split(img,n,axis=1)
    a = np.concatenate(tmp[:])
    return a



def apply_mask(img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Apply a binary mask to the input np.uint8 RGB image.
    The mask will have the same shape as the input image.

    All pixels in `img` that are not white in `mask` should be set to black color.

    See data/geralt.png (image) + data/geralt-mask.png (mask) -> data/geralt-masked.png.
    """
    tmpMask = np.bitwise_and(img,mask)
    return tmpMask


def blend(img_a: np.ndarray, img_b: np.ndarray, alpha: float) -> np.ndarray:
    """
    Blend the two input np.uint8 RGB images together using alpha blending.
    The `alpha` parameter will be in the interval [0.0, 1.0].
    It specifies how visible should `img_a` be.

    The returned image should have data type np.uint8.

    See data/geralt-a.png (img_a) + data/geralt-b.png (img_a) -> data/geralt-blend-{alpha}.png.
    """
    result = img_a * alpha + img_b*(1-alpha)
    result1 = result.astype(np.uint8)
    return result1
