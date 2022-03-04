import os

import numpy as np
import imageio
import pytest

from tasks import max_row_index, sum_edges, to_bw, mirror, split_and_rotate, apply_mask, blend


def test_max_row_index():
    assert max_row_index(np.array([
        [1, 2, 3],
        [4, 8, 0],
        [7, 6, 2]
    ])) == 1

    assert max_row_index(np.array([
        [1, 2, 3],
    ])) == 0

    assert max_row_index(np.array([
        [1, 2, 3],
        [1, 2, 3],
        [1, 2, 3],
        [1, 2, 3],
        [1, 2, 8],
    ])) == 4


def test_sum_edges_simple():
    assert sum_edges(np.array([
        [1, 2, 3],
        [4, 8, 0],
        [7, 6, 2]
    ])) == 25

    assert sum_edges(np.array([
        [1, 2, 3, 6],
        [4, 8, 0, 4],
        [7, 6, 2, 9],
        [7, 3, 0, 8]
    ])) == 54

    assert sum_edges(np.array([
        [1, 2, 3, 6],
        [4, 8, 0, 4],
        [7, 6, 2, 9],
    ])) == 44

    assert sum_edges(np.array([
        [1, 2, 3, 6],
        [7, 6, 2, 9],
    ])) == 36


def test_sum_edges_square():
    assert sum_edges(np.array([
        [1, 2],
        [7, 6],
    ])) == 16


def test_sum_edges_row():
    assert sum_edges(np.array([
        [1, 2],
    ])) == 3


def test_sum_edges_col():
    assert sum_edges(np.array([
        [1],
        [2]
    ])) == 3


def test_sum_edges_single():
    assert sum_edges(np.array([
        [1],
    ])) == 1


def test_bw():
    image = load_image("fei.png")
    check_image_result("bw", "fei-bw.png", lambda: to_bw(image))


def test_mirror():
    image = load_image("pyladies.png")
    check_image_result("mirror", "pyladies-mirrored.png", lambda: mirror(image))


def test_split_and_rotate_1():
    image = load_image("pyladies.png")
    check_image_result("split-and-rotate", "pyladies-split-and-rotate.png", lambda: split_and_rotate(image, 8))


def test_split_and_rotate_2():
    image = load_image("lol.png")
    check_image_result("split-and-rotate", "lol-split-and-rotate.png", lambda: split_and_rotate(image, 17))


def test_apply_mask():
    image = load_image("geralt.png")
    mask = load_image("geralt-mask.png")
    check_image_result("apply-mask", "geralt-masked.png", lambda: apply_mask(image, mask))


@pytest.mark.parametrize("alpha", (0, 0.25, 0.5, 0.75, 1))
def test_blend(alpha):
    a = load_image("geralt-a.png")
    b = load_image("geralt-b.png")
    check_image_result("blend", f"geralt-blend-{alpha}.png", lambda: blend(a, b, alpha=alpha))


def check_image_result(name: str, reference_path: str, fn):
    reference = load_image(reference_path)
    output = fn()

    if reference.shape != output.shape or not (reference == output).all():
        try:
            imageio.imwrite(f"{name}-output.png", output)
        except BaseException as e:
            print(e)

        raise Exception(f"{name}: Image output does not match reference.")


def load_image(path: str) -> np.ndarray:
    return np.array(imageio.imread(os.path.join("data", path)))
