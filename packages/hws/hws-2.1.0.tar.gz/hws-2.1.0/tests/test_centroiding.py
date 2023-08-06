import HWS
import numpy as np
import pytest

from HWS.HS_Centroids import HS_Centroids
from HWS.HS_Image import HS_Image
import matplotlib.pyplot as plt


@pytest.mark.parametrize('N', [2, 4, 7])
@pytest.mark.parametrize('xc', [100, 300.333])
@pytest.mark.parametrize('yc', [100, 300.333])
@pytest.mark.parametrize('dx', [40, 33.33])
@pytest.mark.parametrize('dy', [40, 33.33])
def test_centroiding(N, xc, yc, dx, dy):
    x = np.arange(0, 900)
    y = np.arange(0, 1101)
    X, Y = np.meshgrid(x, y)

    image = np.zeros_like(X, dtype=float)
    to_test = []
    for n in range(1, N+1):
        dI = 100*np.exp(-((X-xc-dx*n)/10)**2 - ((Y-yc-dy*n)/10)**2)
        to_test.append([xc+dx*n, yc+dy*n])
        image += dI
        
    to_test = np.array(to_test, dtype=float)
    print("IN", to_test)
    hsi = HS_Image()
    hsi.original_image = image.astype(float)
    hsi.background = 0
    hsi.process_image()

    hsc = HS_Centroids()
    hsc.hsimage = hsi
    hsc.radius=20
    hsc.find_centroids_from_image()
    print("OUT", hsc.centroids)
    print("RELERR", abs(to_test - hsc.centroids)/abs(to_test))
    assert(len(hsc.centroids) == N)
    assert(np.all(abs(to_test - hsc.centroids)/abs(to_test) < 0.01))