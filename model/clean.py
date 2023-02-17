import os
import sys

def clean(hard=False):
    for filename in os.listdir('data/planes'):
        os.remove("data/planes/" + filename)
    for filename in os.listdir('meshes'):
        os.remove("data/meshes/" + filename)
    if hard:
        for filename in os.listdir('data/results'):
            os.remove("data/results/" + filename)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'hard':
            clean(hard=True)
    else:
        clean()