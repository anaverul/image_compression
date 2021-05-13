import os
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from joblib import dump
import time
import shutil

num_frames = 0

def pixelate(im):
    image=Image.open(im)
    image_pixels=np.asarray(image)
    image_height = image.height
    image_width = image.width
    image_pixels = np.reshape(image_pixels, (image_height * image_width, 3))
    pd.DataFrame(image_pixels, columns=["r", "g", "b"]).head()

    # run k-means clustering on the pixel data
    #num_of_centroids = 16 # a 4-bit image is represented by 2^4 colours
    #num_of_runs = 10 # number of times to run the k-means algorithm before determining the best centroids
    #max_iterations = 300 # number of iterations before k-means comes to an end for a single run
    #verbosity = 0 # show what's going on when the algorithm is running

    # initiate a kmeans object
    compressor = KMeans(n_clusters = 16, n_init = 10, max_iter = 300, verbose = 0)
    # run k-means clustering
    compressor.fit(image_pixels)
    dump(compressor, "compressor.joblib")
    pixel_centroid = np.array([list(compressor.cluster_centers_[label]) for label in compressor.labels_])
    pixel_centroid = pixel_centroid.astype("uint8")
    # reshape this array according to the height and width of our image
    pixel_centroids_reshaped = np.reshape(pixel_centroid, (image_height, image_width, 3), "C")
    # create the compressed image
    compressed_im = Image.fromarray(pixel_centroids_reshaped)
    # save compressed image
    compressed_im.save(repr(im).strip("'"))


def split_frames(im):
    if not os.path.isdir("frames"):
        os.mkdir("frames")
    gif = Image.open(im)
    num_frames=gif.n_frames
    print(num_frames)
    for i in range(num_frames):
        gif.seek(i)
        gif.save('frames/{}.png'.format(i))

def pixelate_frames(path):
    for filename in os.listdir(path):
        pixelate(path +"/"+ (repr(filename)).strip("'"))

def convert_to_jpg(path):
    if not os.path.isdir("jpg_frames"):
        os.mkdir("jpg_frames")
    for filename in os.listdir(path):
        if filename.endswith(".png"):
            jpg_extension=Image.open(path +"/"+ (repr(filename)).strip("'")).convert('RGB')
            jpg_extension.save("jpg_frames/"+ (repr(filename)).strip("'").replace("png","jpg"))

def create_gif(path):
    frames=[]
    for filename in os.listdir(path):
        if filename.endswith("jpg"):
            frames.append(filename)
    list.sort(frames, key=lambda x: int(x.split('.jpg')[0]))
    images = []
    for f in frames:
        frame=Image.open(path +"/"+ (repr(f)).strip("'"))
        images.append(frame)
    # Save the frames as an animated GIF
    images[0].save('compressed.gif',
               save_all=True,
               append_images=images[1:], duration=170,
                loop=0)
    
def gif_compressor(path):
        split_frames(path)
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
        end_time=time.time()
    else:
        print("hi")
        pixelate(args.inputFileName)
        end_time=time.time()
    print("time taken = ", end_time-start_time)
