
from skimage.measure import compare_ssim as ssim
import cv2



def most_similar(original,files):
    results = ssim_compare(original,files)
    sorted_images = sorted(results.items(),reverse = True, key=lambda val: val[1])
    return sorted_images[1]


def ssim_compare(original,files):
    retVal = {}
    original_image = cv2.imread(original)

    for file in files:
        temp_cv2 = cv2.imread(file)
        temp_original = original_image

        temp_original,temp_cv2 = size_match_images(temp_original,temp_cv2)

        height1, width1, channel1 = temp_original.shape
        height2, width2, channel2 = temp_cv2.shape

        retVal[file] = str(ssim(temp_original,temp_cv2,multichannel=True))

    return retVal



def size_match_images(image1,image2):
    height1, width1, channel1 = image1.shape
    height2, width2, channel2 = image2.shape

    new_height = min(height1,height2)
    new_width = min(width1,width2)

    image1 = cv2.resize(image1,(new_width, new_height))
    image2 = cv2.resize(image2,(new_width, new_height))

    return image1, image2
