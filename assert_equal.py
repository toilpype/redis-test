import argparse
import numpy as np
import cv2


def assert_equal(img_file1, img_file2):
    img_1 = cv2.imread(img_file1)
    img_2 = cv2.imread(img_file2)
    try:
        np.testing.assert_array_equal(img_1, img_2)
        print('Images are equal.')
    except:
        print('Emages are not equal.')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('img_file1')
    parser.add_argument('img_file2')
    args = parser.parse_args()
    assert_equal(args.img_file1, args.img_file2)
    