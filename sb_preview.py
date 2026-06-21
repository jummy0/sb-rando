import sb_util, sys
from sb_types import *

def main():
    if len(sys.argv) < 2:
        print('no mission file specified')
        exit()
    path = sys.argv[1]
    with open(path, 'rb') as file:
        data = bytearray(file.read())
        decor, big_decor, mobs, desc_file = sb_util.unpack(data)
        sb_util.render_preview(decor, big_decor, mobs, desc_file).show()

if __name__ == '__main__':
    main()