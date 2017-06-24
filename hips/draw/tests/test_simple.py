# Licensed under a 3-clause BSD style license - see LICENSE.rst
import pytest
import numpy as np
from astropy.tests.helper import remote_data
from ...tiles import HipsSurveyProperties, HipsTileMeta, HipsTile
from ..simple import make_sky_image, draw_sky_image
from ...utils.testing import get_hips_extra_file, make_test_wcs_geometry, requires_hips_extra


def get_test_tiles():
    # Could make manually a list of two tiles to draw
    # Pointing to FITS tiles in hips-extra like e.g.
    # hips-extra/datasets/samples//DSS2Red/Norder3/Dir0/Npix659.fits

    # TODO: check if this tile is inside our image
    tile1 = HipsTile.read(
        meta=HipsTileMeta(order=3, ipix=659, file_format='fits', tile_width=512),
        filename=get_hips_extra_file('datasets/samples//DSS2Red/Norder3/Dir0/Npix659.fits'),
    )

    # TODO: also fetch a second one.

    return [tile1]


@requires_hips_extra()
def test_draw_sky_image():
    # filename = get_pkg_data_filename('../../tiles/tests/data/properties.txt')
    # hips_survey = HipsSurveyProperties.read(filename)
    geometry = make_test_wcs_geometry(case=2)
    tiles = get_test_tiles()

    data = draw_sky_image(geometry, tiles)

    assert data.shape == geometry.shape
    assert data.dtype == np.float64

    assert data[100, 200] == 0


@pytest.mark.xfail
@remote_data
def test_make_sky_image():
    url = 'https://raw.githubusercontent.com/hipspy/hips/master/hips/tiles/tests/data/properties.txt'
    hips_survey = HipsSurveyProperties.fetch(url)
    geometry = make_test_wcs_geometry(case=2)

    data = make_sky_image(geometry, hips_survey)

    assert data.shape == geometry.shape
    assert data.dtype == np.float64

    assert data[100, 200] == 42
