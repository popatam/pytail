import os
import time


def tail_python(files):
    tail_dict = dict()  # {file_path: (file_path, fd, inode)
    for file in files:
        tail_dict.update({file: (file,)})

    for file_path, data in tail_dict.items():
        file = data[0]
        fd = open(file, mode='r')
        fd.seek(0, 0)
        old_inode = os.stat(file).st_ino
        tail_dict.update({file: (file, fd, old_inode)})

    try:
        while True:
            for file_path, data in tail_dict.items():
                file = data[0]
                fd = data[1]
                old_inode = data[2]
                line_buffer = fd.readlines()
                if len(line_buffer) == 0:
                    try:
                        new_inode = os.stat(file).st_ino
                        if new_inode != old_inode:
                            fd = open(file, mode='r')
                            tail_dict.update({file: (file, fd, new_inode)})
                    except Exception as e:
                        print(e)
                    time.sleep(0.5)
                else:
                    if len(tail_dict) > 1:
                        for line in line_buffer:
                            yield (file, line)
                    else:
                        for line in line_buffer:
                            yield (line,)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('files', type=str, nargs='+', help='files to open')
    args = parser.parse_args()
    for line in tail_python(args.files):
        print(line, end='\n')
