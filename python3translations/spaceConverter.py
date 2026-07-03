import sys
import os

#converting all 4 space blocks in a file to tabs
def convertFile(filePath):
    try:
        with open(filePath, 'r', encoding = 'utf-8') as f:
            content = f.read()

        fixedContent = content.replace('    ', '\t')

        if content != fixedContent:
            with open(filePath, 'w', encoding = 'utf-8') as f:
                f.write(fixedContent)
                print("successful conversion")
        else:
            print("already clean")
    except Exception as e:
        print("error processing file")


def main():
    if len(sys.argv) == 2:
        target = sys.argv[1]
        if os.path.isfile(target):
            convertFile(target)
    else:
        print ("error with arguments/file")


if __name__ == "__main__":
    main()



