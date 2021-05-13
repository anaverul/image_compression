import os
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from joblib import dump
import time
import shutil

def pixelate(im):
    """compresses an image using k-means clustering and saves it

    Parameters
    ----------
    im : str
    the image to be processed
    Returns
    -------
    No returns
    """
    image = Image.open(im)
    image_pixels = np.asarray(image)
    image_height = image.height
    image_width = image.width
    image_pixels = np.reshape(image_pixels, (image_height * image_width, 3))  #reshape into a matrix
    #pd.DataFrame(image_pixels, columns=["r", "g", "b"]).head()
    # run k-means clustering algorithm
    compressor = KMeans(n_clusters = 16, n_init = 10, max_iter = 300, verbose = 0)
    #n_clusters: a 4-bit image is represented by 2^4 colors, so we will have 16 clusters/centroids
    #n_init: k-means will run 10 times prior to determining the best centroid positions
    #max_iter: number of iterations in a single run of k-means algorithm
    compressor.fit(image_pixels)
    dump(compressor, "compressor.joblib")
    #swap pixel data with corresponding cluster centroid
    centroid = np.array([list(compressor.cluster_centers_[label]) for label in compressor.labels_])
    centroid = centroid.astype("uint8") #convert to an unsigned integer type
    #reshape array to match height and width
    reshaped_centroids = np.reshape(centroid, (image_height, image_width, 3), "C")
    compressed_image = Image.fromarray(reshaped_centroids)
    compressed_image.save(repr(im).strip("'"))

def split_frames(im):
    """splits gifs into separate frames and saves them
    in a directory named "frames"

    Parameters
    ----------
    im : str
    the image to be processed
    Returns
    -------
    No returns
    """
    if not os.path.isdir("frames"):
        os.mkdir("frames")
    gif = Image.open(im)
    num_frames=gif.n_frames
    print(num_frames)
    for i in range(num_frames):
        gif.seek(i)
        gif.save('frames/{}.png'.format(i))

def pixelate_frames(path):
    """compresses multiple frames using k-means clustering and saves them

    Parameters
    ----------
    path : str
    path to the directory of frames
    Returns
    -------
    No returns
    """
    for filename in os.listdir(path):
        pixelate(path +"/"+ (repr(filename)).strip("'"))

def convert_to_jpg(path):
    """converts png files to jpg format and saves them
    in a directory named "jpg_frames"

    Parameters
    ----------
    path : str
    path to the directory of image files
    Returns
    -------
    No returns
    """
    if not os.path.isdir("jpg_frames"):
        os.mkdir("jpg_frames")
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            jpg_extension = Image.open(path +"/"+ (repr(filename)).strip("'")).convert('RGB')
            jpg_extension.save("jpg_frames/"+ (repr(filename)).strip("'").replace("png","jpg"))

def create_gif(path):
    """creates a gif file using multiple frames

    Parameters
    ----------
    path : str
    path to the directory of frames
    Returns
    -------
    No returns
    """
    frames = []
    for filename in os.listdir(path):
        if filename.endswith("jpg"):
            frames.append(filename)
    #frames in the directory are sorted alphabetically, so the following
    #line is meant to sort them in the correct order
    #before creating a gif
    list.sort(frames, key = lambda x: int(x.split('.jpg')[0]))
    images = []
    for f in frames:
        frame = Image.open(path +"/"+ (repr(f)).strip("'"))
        images.append(frame)
    # Save the frames as an animated GIF
    images[0].save('compressed.gif',
               save_all = True,
               append_images = images[1:], duration=170,
                loop = 0)

def gif_compressor(im):
    """gif compressor to be used in compress_gui.py
    calls functions in the correct order to compress a gif

    Parameters
    ----------
    im : str
    image file to be processed
    Returns
    -------
    No returns
    """
    split_frames(im)
    convert_to_jpg("frames")
    pixelate_frames("jpg_frames")
    create_gif("jpg_frames")
    shutil.rmtree("frames")
    shutil.rmtree("jpg_frames")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='quicksort')
    parser.add_argument('-i','--inputFileName', type=str, help='input file', required=True)
    args = parser.parse_args()

    start_time=time.time()
    if (args.inputFileName).endswith(".gif"):
        gif_compressor(args.inputFileName)
        end_time = time.time()
    else:
        pixelate(args.inputFileName)
        end_time = time.time()
    print("time taken = ", end_time-start_time)

