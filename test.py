import sys

from latk.latk import *
from binvox_rw.binvox_rw import *

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

def main():
    la = Latk(inputDir)
    la.clean()
    la.normalize()
    #la.write(outputDir)

    bv = None
    with open('chair.binvox', 'rb') as f:
        bv = read_as_3d_array(f)
        print(bv.data)

    with open('chair_out.binvox', 'wb') as f:
        bv.write(f)

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
