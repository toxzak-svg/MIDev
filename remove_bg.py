#!/usr/bin/env python3
from PIL import Image
from collections import Counter
import math

IN = '1765211253368.jpg'
OUT = 'logo.png'
THRESHOLD = 60  # color distance threshold (0-441) — adjust if needed

def color_dist(c1, c2):
    return math.sqrt(sum((a-b)**2 for a,b in zip(c1,c2)))

def main():
    img = Image.open(IN).convert('RGBA')
    w,h = img.size
    pixels = img.load()

    # sample corners to estimate background color
    corners = [pixels[0,0][:3], pixels[w-1,0][:3], pixels[0,h-1][:3], pixels[w-1,h-1][:3]]
    most_common = Counter(corners).most_common(1)[0][0]
    bg = tuple(most_common)

    # make near-bg pixels transparent
    for y in range(h):
        for x in range(w):
            r,g,b,a = pixels[x,y]
            if color_dist((r,g,b), bg) <= THRESHOLD:
                pixels[x,y] = (r,g,b,0)

    # trim transparent border
    bbox = img.split()[-1].getbbox()
    if bbox:
        img = img.crop(bbox)

    # optionally resize if image is very large — keep within 360px
    max_dim = 360
    if max(img.size) > max_dim:
        img.thumbnail((max_dim, max_dim), Image.LANCZOS)

    img.save(OUT)
    print('Saved', OUT)

if __name__ == '__main__':
    main()
