from os import *


def the_general_daughter():
    v = r"C:\Users\Administrator\Videos\The General's Daughter"

    chdir(v)

    h = []
    for a in listdir("."):
        if path.isdir(a):
            continue

        aa = a.replace("_", " ")

        d = aa.split()[:3]

        last = d[-1]
        if "." in last:
            num = last.split(".")[0]
            d[-1] = num

        name = " ".join(d) + ".mp4"
        rename(a, name)

        h.append(name)
    h.sort()

    for hh in h:
        print(hh)


def photo_resizer():
    v = r"C:\Users\Administrator\Pictures\PhotoResizer"

    rm = "_copy_"

    chdir(v)

    for a in listdir(v):
        sp, e = path.splitext(a)
        sp = sp.split(rm)[0]

        n = sp + e

        rename(a, n)


photo_resizer()
