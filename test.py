import sys

from latk.latk import *
from binvox_rw.binvox_rw import *

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

dim = 128
drawReps = dim * dim 

def lerp(x1, x2, y1, y2, x):
    return ((y2 - y1) * x + x2 * y1 - x1 * y2) / (x2 - x1)

def drawLine(x1, y1, z1, x2, y2, z2):
    p1 = (x1, y1, z1)
    p2 = (x2, y2, z2)
    for i in range(0, drawReps):
        val = float(i) / float(drawReps) 
        p3 = p1.lerp(p2, val)
        x = int(p3[0])
        y = int(p3[1])
        z = int(p3[2])
        voxelOn(x, y, z)

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
                for point in stroke.points:
                    x = int(point.co[0] * (dims[0]-1))
                    y = int(point.co[1] * (dims[1]-1))
                    z = int(point.co[2] * (dims[2]-1))
                    data[x][y][z] = True

    with open(outputDir, 'wb') as f:
        bv.write(f)

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
