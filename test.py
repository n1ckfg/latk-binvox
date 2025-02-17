import sys
import numpy as np
import scipy.ndimage as nd
from latk import *
from binvox_rw.binvox_rw import *
from kmeans import *
import h5py
import threading
import queue
import os

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputPath = argv[0]
dim = int(argv[1])

numThreads = 5

drawReps = dim #* dim 
allPoints = []
numCentroids = 40
numFillReps = 5

def lerp(a, b, f): 
    return (a * (1.0 - f)) + (b * f)

def lerp3d(a, b, f):
    x = (a[0] * (1.0 - f)) + (b[0] * f)   
    y = (a[1] * (1.0 - f)) + (b[1] * f)   
    z = (a[2] * (1.0 - f)) + (b[2] * f)   
    return (x, y, z)

def drawLine(data, dims, x1, y1, z1, x2, y2, z2):
    p1 = (x1, y1, z1)
    p2 = (x2, y2, z2)
    for i in range(0, drawReps):
        val = float(i) / float(drawReps) 
        p3 = lerp3d(p1, p2, val)
        x = int(p3[0] * (dims[0]-1))
        y = int(p3[1] * (dims[1]-1))
        z = int(p3[2] * (dims[2]-1))
        data[x][y][z] = True

def saveAsBinvox(bv, url):
    with open(url, 'wb') as f:
        bv.write(f)

def saveAsH5(bv, url):
    voxel_data = bv.data.astype(float)
    f = h5py.File(url, 'w')
    # more compression options: https://docs.h5py.org/en/stable/high/dataset.html
    f.create_dataset('data', data=voxel_data, compression='gzip')
    f.flush()
    f.close()    

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def process_file(file_path):
    saveBinvox = True
    saveH5 = False

    #doFill = False   
    doClean = False
    doNorm = False
    dims = (dim, dim, dim)
    data = np.zeros((dims[0], dims[1], dims[2]), dtype=bool)
    translate = (0, 0, 0)
    scale = 1
    axis_order = 'xzy'
    bv = Voxels(data, dims, translate, scale, axis_order)
    '''
    with open('chair.binvox', 'rb') as f:
        bv = read_as_3d_array(f)
        print(bv.data)
    '''

    '''
    for x in range(0, len(data)):
        for y in range(0, len(data[x])):
            for z in range(0, len(data[x][y])):
                data[x][y][z] = True
    '''
    print("Reading from : " + file_path)

    la = None

    file_path_split = file_path.split(".")
    ext = file_path_split[len(file_path_split)-1].lower()
    if (ext == "tilt"):
        la = Latk()
        la.readTiltBrush(file_path)
    elif (ext == "latk" or ext == "json"):
        la = Latk(file_path)

    if (doNorm):
        print("Normalizing...")
        la.normalize()

    # clean after normalize so min distance between points is known
    if (doClean):
        print("Cleaning...")
        la.clean()

    #la.write(outputPath)

    for layer in la.layers:
        for frame in layer.frames:
            for stroke in frame.strokes:
                if (len(stroke.points) > 1):
                    allPoints.append(stroke.points[0].co)
                    for i in range(1, len(stroke.points)):
                        allPoints.append(stroke.points[i].co)
                        p1 = stroke.points[i].co
                        p2 = stroke.points[i-1].co
                        drawLine(data, dims, p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])
                '''
                for point in stroke.points:
                    x = int(point.co[0] * (dims[0]-1))
                    y = int(point.co[1] * (dims[1]-1))
                    z = int(point.co[2] * (dims[2]-1))
                    data[x][y][z] = True
                '''
    url = ""
    outputPathArray = file_path.split(".")
    for i in range(0, len(outputPathArray)-1):
        url += outputPathArray[i]

    url1a = url + "-stroke.binvox"
    url1b = url + ".seg"
    url2a = url + "-fill.binvox"
    url2b = url + ".im"

    # ~ ~ ~   "THIN" version filters   ~ ~ ~
    for i in range(0, 1):
        nd.binary_dilation(bv.data.copy(), output=bv.data)

    for i in range(0, 0):
        nd.sobel(bv.data.copy(), output=bv.data)

    nd.median_filter(bv.data.copy(), size=2, output=bv.data)

    for i in range(0, 0):
        nd.laplace(bv.data.copy(), output=bv.data)

    for i in range(0, 0):
        nd.binary_erosion(bv.data.copy(), output=bv.data)
    # ~ ~ ~   ~ ~ ~   ~ ~ ~   ~ ~ ~

    if (saveBinvox == True):
        print("Writing to: " + url1a)
        saveAsBinvox(bv, url1a)
    
    if (saveH5 == True):
        print("Writing to: " + url1b)
        saveAsH5(bv, url1b)

    '''
    if (doFill == True):
        kmeans = Kmeans(allPoints, numCentroids)

    while (doFill == True):
        if (kmeans.ready == False):
            kmeans.run()
        else:     
            for cluster in kmeans.clusters:
                for i in range(0, len(cluster.points)):
                    p1 = cluster.points[i]
                    for j in range(0, numFillReps):
                        index = int(random(0, len(cluster.points)))
                        p2 = cluster.points[index]
                        drawLine(data, dims, p1[0], p1[1], p1[2], p2[0], p2[1], p2[2])

            doFill = False
    '''

    # ~ ~ ~   "FAT" version filters   ~ ~ ~
    for i in range(0, 1):
        nd.binary_dilation(bv.data.copy(), output=bv.data)

    for i in range(0, 3):
        nd.sobel(bv.data.copy(), output=bv.data)

    nd.median_filter(bv.data.copy(), size=4, output=bv.data)

    for i in range(0, 2):
        nd.laplace(bv.data.copy(), output=bv.data)

    for i in range(0, 0):
        nd.binary_erosion(bv.data.copy(), output=bv.data)
    # ~ ~ ~   ~ ~ ~   ~ ~ ~   ~ ~ ~

    if (saveBinvox == True):
        print("Writing to: " + url2a)
        saveAsBinvox(bv, url2a)
    
    if (saveH5 == True):
        print("Writing to: " + url2b)
        saveAsH5(bv, url2b)

def worker(file_queue):
    print("Initializing worker")
    # Take a file from the queue and process it.
    while True:
        try:
            file_path = file_queue.get_nowait()
        except queue.Empty:
            break  # If the queue is empty, exit the thread

        process_file(file_path)
        file_queue.task_done()

def process_directory(directory, num_threads):
    # Create a queue and add all file paths in the directory to it
    file_queue = queue.Queue()
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_queue.put(file_path)

    # Start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(file_queue,))
        thread.start()
        threads.append(thread)

    # Wait for threads to finish
    for thread in threads:
        thread.join()

def main():
    process_directory(inputPath, numThreads)

main()
