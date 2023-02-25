import numpy as np
import cv2
from skimage.measure import block_reduce


def from_png_to_jpg(map):
    color = map[:, :, 0:3].astype(np.float) / 255.0
    alpha = map[:, :, 3:4].astype(np.float) / 255.0
    reversed_color = 1 - color
    return (255.0 - reversed_color * alpha * 255.0).clip(0,255).astype(np.uint8)


def k_resize(x, k):
    if x.shape[0] < x.shape[1]:
        s0 = k
        s1 = int(x.shape[1] * (k / x.shape[0]))
        s1 -= s1 % 64
        _s0 = 16 * s0
        _s1 = int(x.shape[1] * (_s0 / x.shape[0]))
        _s1 = (_s1 + 32) - (_s1 + 32) % 64
    else:
        s1 = k
        s0 = int(x.shape[0] * (k / x.shape[1]))
        s0 -= s0 % 64
        _s1 = 16 * s1
        _s0 = int(x.shape[0] * (_s1 / x.shape[1]))
        _s0 = (_s0 + 32) - (_s0 + 32) % 64
    new_min = min(_s1, _s0)
    raw_min = min(x.shape[0], x.shape[1])
    interpolation = cv2.INTER_AREA if new_min < raw_min else cv2.INTER_LANCZOS4
    return cv2.resize(x, (_s1, _s0), interpolation=interpolation)


def sk_resize(x, k):
    if x.shape[0] < x.shape[1]:
        s0 = k
        s1 = int(x.shape[1] * (k / x.shape[0]))
        s1 -= s1 % 16
        _s0 = 4 * s0
        _s1 = int(x.shape[1] * (_s0 / x.shape[0]))
        _s1 = (_s1 + 8) - (_s1 + 8) % 16
    else:
        s1 = k
        s0 = int(x.shape[0] * (k / x.shape[1]))
        s0 -= s0 % 16
        _s1 = 4 * s1
        _s0 = int(x.shape[0] * (_s1 / x.shape[1]))
        _s0 = (_s0 + 8) - (_s0 + 8) % 16
    new_min = min(_s1, _s0)
    raw_min = min(x.shape[0], x.shape[1])
    interpolation = cv2.INTER_AREA if new_min < raw_min else cv2.INTER_LANCZOS4
    return cv2.resize(x, (_s1, _s0), interpolation=interpolation)


def d_resize(x, d):
    new_min = min(d[1], d[0])
    raw_min = min(x.shape[0], x.shape[1])
    interpolation = cv2.INTER_AREA if new_min < raw_min else cv2.INTER_LANCZOS4
    return cv2.resize(x, (d[1], d[0]), interpolation=interpolation)


def n_resize(x, d):
    return cv2.resize(x, (d[1], d[0]), interpolation=cv2.INTER_NEAREST)


def s_resize(x, s):
    if x.shape[0] < x.shape[1]:
        s0 = x.shape[0]
        s1 = int(float(s0) / float(s[0]) * float(s[1]))
    else:
        s1 = x.shape[1]
        s0 = int(float(s1) / float(s[1]) * float(s[0]))
    new_max = max(s1, s0)
    raw_max = max(x.shape[0], x.shape[1])
    interpolation = cv2.INTER_AREA if new_max < raw_max else cv2.INTER_LANCZOS4
    return cv2.resize(x, (s1, s0), interpolation=interpolation)


def m_resize(x, m):
    if x.shape[0] < x.shape[1]:
        s0 = m
        s1 = int(float(m) / float(x.shape[0]) * float(x.shape[1]))
    else:
        s0 = int(float(m) / float(x.shape[1]) * float(x.shape[0]))
        s1 = m
    new_max = max(s1, s0)
    raw_max = max(x.shape[0], x.shape[1])
    interpolation = cv2.INTER_AREA if new_max < raw_max else cv2.INTER_LANCZOS4
    return cv2.resize(x, (s1, s0), interpolation=interpolation)


def s_enhance(x, k):
    p = cv2.cvtColor(x, cv2.COLOR_RGB2HSV).astype(np.float)
    p[:, :, 1] *= k
    p = p.clip(0, 255).astype(np.uint8)
    return cv2.cvtColor(p, cv2.COLOR_HSV2RGB).clip(0, 255)


def cv_denoise(x):
    return cv2.fastNlMeansDenoisingColored(x, None, 3, 3, 7, 21)


def k_down_hints(x):
    RGB = x[:, :, 0:3].astype(np.float)
    A = x[:, :, 3:4].astype(np.float)
    RGB = RGB * A / 255.0
    RGB = block_reduce(RGB, (2, 2, 1), np.max)
    A = block_reduce(A, (2, 2, 1), np.max)
    return np.concatenate([RGB, A], axis=2)


def k8_down_hints(x):
    RGB = x[:, :, 0:3].astype(np.float)
    A = x[:, :, 3:4].astype(np.float)
    RGB = RGB * A / 255.0
    RGB = block_reduce(RGB, (4, 4, 1), np.min)
    RGB = block_reduce(RGB, (2, 2, 1), np.max)
    A = block_reduce(A, (4, 4, 1), np.min)
    A = block_reduce(A, (2, 2, 1), np.max)
    return np.concatenate([RGB, A], axis=2)
