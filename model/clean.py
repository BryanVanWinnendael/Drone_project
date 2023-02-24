import os
import sys

def clean(hard=False):
    if os.path.exists("data/planes"):
        for filename in os.listdir('data/planes'):
            os.remove("data/planes/" + filename)
        os.removedirs("data/planes")

    if os.path.exists("data/meshes"):
        for filename in os.listdir('data/meshes'):
            os.remove("data/meshes/" + filename)
        os.removedirs("data/meshes")

    if hard:
        if os.path.exists("data/results"):
            for filename in os.listdir('data/results'):
                os.remove("data/results/" + filename)
            os.removedirs("data/results")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'hard':
            clean(hard=True)
    else:
        clean()