#!/usr/bin/env python

# With modifications by Daniel Holth

# MIT License

# Copyright (c) 2016 Danyaal Rangwala

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import matplotlib.pyplot as plt

from multiprocessing import Pool

SIZE = 1024  # always square
CHUNK_SIZE = 16

# counts the number of iterations until the function diverges or
# returns the iteration threshold that we check until
def countIterationsUntilDivergent(c, threshold):
    z = complex(0, 0)
    for iteration in range(threshold):
        z = (z * z) + c

        if abs(z) > 4:
            break
            pass
        pass
    return iteration


class mandelbrotlines:
    """
    Return a function to make single lines of mandelbrot on demand.
    """

    def __init__(self, threshold, density, cx, cy, scale):
        print("init brot", threshold, density)

        self.threshold = threshold

        # a colormap and a normalization instance
        self.cmap = plt.cm.jet
        self.norm = plt.Normalize(vmin=0, vmax=threshold)

        self.realAxis = np.linspace(cx, cx + scale, density)
        self.imaginaryAxis = np.linspace(cy, cy + scale, density)

        self.row = np.empty(len(self.imaginaryAxis))

    def __call__(self, line_number):
        ix = line_number
        for iy in range(len(self.imaginaryAxis)):
            cx = self.realAxis[ix]
            cy = self.imaginaryAxis[iy]
            c = complex(cx, cy)
            self.row[iy] = countIterationsUntilDivergent(c, self.threshold)

        image = self.cmap(self.norm(self.row))
        image = image[0:, 0:3]  # remove alpha channel
        flat = np.array(image.flatten() * 255, dtype=np.uint8)
        return flat


cache = None


def mandelbrotlines_cached(threshold, density, cx, cy, scale):
    """
    If we store the class in Pool() it may be pickled repeatedly.
    Use global variable to avoid that overhead.
    """
    global cache
    cache = mandelbrotlines(threshold, density, cx, cy, scale)


def callcache(line_number):
    return cache(line_number)


def mandelbrot_parallel(cx, cy, scale):
    with Pool(
        initializer=mandelbrotlines_cached,
        initargs=(120, SIZE, cx, cy, scale),
    ) as pool:
        yield from pool.imap(callcache, range(SIZE), CHUNK_SIZE)
