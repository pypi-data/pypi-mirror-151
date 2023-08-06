import cv2
import numpy as np
from pathlib import Path
from unrest.image import merge_image, paste_image

DIR = Path(__file__).parent.absolute()

def test_merge_image():
    back = cv2.imread(str(DIR / 'lz.png'))
    ball = cv2.imread(str(DIR / 'morphball.png'), cv2.IMREAD_UNCHANGED)
    print(back.shape)
    print(ball.shape)
    result = merge_image(back, ball, 50, 50)
    cv2.imwrite('result_merge.png', result)


def test_add():
    result = cv2.imread(str(DIR / 'lz.png'))
    ball = cv2.imread(str(DIR / 'morphball.png'))
    for i in range(10):
        empty = result.copy()
        empty[:,:,:] = 0
        empty = merge_image(empty, ball, i * 16, 70)
        result = result + (empty * (i+1))
    cv2.imwrite('result_add.png', result)


def test_overflow_add():
    result = cv2.imread(str(DIR / 'lz.png'))
    result = result.astype('int32')
    ball = cv2.imread(str(DIR / 'morphball.png')).astype('int32')
    for i in range(20):
        empty = result.copy()
        empty[:,:,:] = 0
        empty = paste_image(empty, ball, i * 16, 70)
        result = result + (empty * (i+1))
    mask = result[:,:,:] > 255
    print(np.amax(result))
    result[mask] = 255
    cv2.imwrite('result_overflow.png', result)
    arst
