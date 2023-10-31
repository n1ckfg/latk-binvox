import sys
sys.path.append("latkpy")
import latk

argv = sys.argv
argv = argv[argv.index("--") + 1:] # get all args after "--"

inputPath = argv[0]
precision = int(argv[1])

def main():
    print("Reading from : " + inputPath)
    la = latk.Latk()
    la.readTiltBrush(inputPath)

    la.normalize()

    url = ""
    outputPathArray = inputPath.split(".")
    for i in range(0, len(outputPathArray)-1):
        url += outputPathArray[i]
    url += ".latk"

    print("Writing to: " + url)
    la.write(url, precision=precision)

main()
