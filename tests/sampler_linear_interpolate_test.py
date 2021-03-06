# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

import tensorflow as tf

from niftynet.engine.sampler_linear_interpolate import LinearInterpolateSampler
from niftynet.io.image_reader import ImageReader
from tests.test_util import ParserNamespace

MULTI_MOD_DATA = {
    'T1': ParserNamespace(
        csv_file=os.path.join('testing_data', 'T1sampler.csv'),
        path_to_search='testing_data',
        filename_contains=('_o_T1_time',),
        filename_not_contains=('Parcellation',),
        interp_order=3,
        pixdim=None,
        axcodes=None,
        spatial_window_size=(7, 10, 2)
    ),
    'FLAIR': ParserNamespace(
        csv_file=os.path.join('testing_data', 'FLAIRsampler.csv'),
        path_to_search='testing_data',
        filename_contains=('FLAIR_',),
        filename_not_contains=('Parcellation',),
        interp_order=3,
        pixdim=None,
        axcodes=None,
        spatial_window_size=(7, 10, 2)
    )
}
MULTI_MOD_TASK = ParserNamespace(image=('T1', 'FLAIR'))


def get_3d_reader():
    reader = ImageReader(['image'])
    reader.initialise_reader(MULTI_MOD_DATA, MULTI_MOD_TASK)
    return reader


class LinearInterpolateSamplerTest(tf.test.TestCase):
    def test_init(self):
        sampler = LinearInterpolateSampler(
            reader=get_3d_reader(),
            data_param=MULTI_MOD_DATA,
            batch_size=1,
            n_interpolations=8,
            queue_length=1)
        with self.test_session() as sess:
            coordinator = tf.train.Coordinator()
            sampler.run_threads(sess, coordinator, num_threads=2)
            out = sess.run(sampler.pop_batch_op())
            self.assertAllClose(out['image'].shape, [1, 256, 168, 256, 2])
        sampler.close_all()


if __name__ == '__main__':
    tf.test.main()
