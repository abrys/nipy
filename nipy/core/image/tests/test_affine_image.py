from nipy.core.image import affine_image, affine_imageII
import nipy.io.api as A
import numpy as np
import nipy.testing as niptest

def test_affine_image():

    # The file dummy.mnc is available here:
    #
    # http://kff.stanford.edu/~jtaylo/affine_image_testfiles


    im=A.load_image('/home/jtaylo/dummy.mnc')

    a = affine_image.AffineImage(np.array(im), im.affine, im.coordmap.input_coords.name)
    aII = affine_imageII.AffineImage(np.array(im), im.affine, im.coordmap.input_coords.coord_names)

    a_cmap = a.spatial_coordmap
    aII_cmap = aII.spatial_coordmap

    yield niptest.assert_true,  a_cmap.input_coords.coord_names == ('axis0', 'axis1', 'axis2')
    yield niptest.assert_true,  aII_cmap.input_coords.coord_names == ('i','j','k')

    yield niptest.assert_true,  a_cmap.output_coords.coord_names == ('x','y','z')
    yield niptest.assert_true,  aII_cmap.output_coords.coord_names == ('x','y','z')

    b=a.xyz_ordered()
    bII = aII.xyz_ordered()

    # The coordmap property of AffineImage could overwrite Image's
    # I haven't tried to do that yet.

    b_cmap = b.spatial_coordmap
    bII_cmap = bII.spatial_coordmap

    # I prefer the affine_imageII implementation
    # because you see that the axes have reversed order.
    # Just using a name for the coordinate system
    # loses this information

    yield niptest.assert_true,  b_cmap.input_coords.coord_names == ('axis0', 'axis1', 'axis2')
    yield niptest.assert_true,  bII_cmap.input_coords.coord_names == ('k','j','i')

    yield niptest.assert_true,  b_cmap.output_coords.coord_names == ('x','y','z')
    yield niptest.assert_true,  bII_cmap.output_coords.coord_names == ('x','y','z')

    np.testing.assert_almost_equal(b.affine, bII.affine)
    np.testing.assert_almost_equal(a.affine, aII.affine)

    yield niptest.assert_true,  a.shape == im.shape
    yield niptest.assert_true,  aII.shape == im.shape

    yield niptest.assert_true,  b.shape == im.shape[::-1]
    yield niptest.assert_true,  bII.shape == im.shape[::-1]


