import sys

from latk.latk import *
import binvox_rw.binvox_rw

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

def main():
    model = binvox_rw.read_binvox('chair.binvox')
    model.voxels
    #data = Latk(inputDir)
    #data.clean()
    #data.write(outputDir)

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
