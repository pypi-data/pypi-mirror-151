import getopt
import sys

from generate import generate


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["input=", "output="])
    except getopt.GetoptError:
        print("test.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("test.py -i <inputfile> -o <outputfile>")
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
        else:
            print('cairo_type_hints.py --help')
            sys.exit(2)

    if inputfile == "":
        print("Input file not set")
        sys.exit(2)

    if outputfile == "":
        print("Output file not set")
        sys.exit(2)

    generate(inputfile, outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
