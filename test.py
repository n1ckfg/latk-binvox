import sys

from latk.latk import *
from binvox_rw.binvox_rw import *

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputDir = argv[0]
outputDir = argv[1]

def main():
    with open('chair.binvox', 'rb') as f:
        m1 = read_as_3d_array(f)
        print(m1.data)
    #data = Latk(inputDir)
    #data.clean()
    #data.write(outputDir)

print("Reading from : " + inputDir)
print("Writing to: " + outputDir)

main()
