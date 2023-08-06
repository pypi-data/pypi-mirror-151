import cv2
import numpy as np


__all__ = ['hstack', 'vstack']


def vstack(imgs):
    min_width = min([img.shape[1] for img in imgs])

    imgs_to_stack = []
    for img in imgs:
        if img.shape[1] != min_width:
            f = min_width / img.shape[1]
            img_resized = cv2.resize(img, (0, 0), fx=f, fy=f)
            imgs_to_stack.append(img_resized)
        else:
            imgs_to_stack.append(img)

    stacked = np.vstack(imgs_to_stack)
    return stacked


def hstack(imgs):
    min_height = min([img.shape[0] for img in imgs])

    imgs_to_stack = []
    for img in imgs:
        if img.shape[0] != min_height:
            f = min_height / img.shape[0]
            img_resized = cv2.resize(img, (0, 0), fx=f, fy=f)
            imgs_to_stack.append(img_resized)
        else:
            imgs_to_stack.append(img)

    stacked = np.hstack(imgs_to_stack)
    return stacked


if __name__ == '__main__':
    img_paths = ['D:/data/asd/images/pano1 kopia.png',
                 'D:/data/asd/images/pano1.png']

    imgs = [cv2.imread(p) for p in img_paths]

    stacked = vstack(imgs)

    cv2.imshow('stacked', stacked)
    cv2.waitKey(0)
