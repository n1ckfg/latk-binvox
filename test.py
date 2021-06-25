import sys

from latk.latk import *
from binvox_rw.binvox_rw import *
from kmeans import *

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

dim = 64
drawReps = dim #* dim 
kmeans = None
doFill = True
allPoints = []
numCentroids = 20
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

def main():
    la = Latk(inputDir)
    la.clean()
    la.normalize()
    #la.write(outputDir)

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
    kmeans = Kmeans(allPoints, numCentroids)

    with open(outputDir, 'wb') as f:
        bv.write(f)

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
