import numpy as np
import random

from ...utils import SAMPLER


class SemSegRandomSampler(object):
    """Random sampler for semantic segmentation datsets"""

    def __init__(self, dataset_split):
        self.dataset_split = dataset_split
        self.length = len(dataset_split)

    def __len__(self):
        return self.length

    def initialize_with_dataloader(self, dataloader):
        self.length = len(dataloader)

    def get_cloud_sampler(self):

        def gen():
            ids = np.random.permutation(self.length)
            for i in ids:
                yield i

        return gen()

    def get_point_sampler(self):

        def _random_centered_gen(**kwargs):
            pc = kwargs.get('pc', None)
            num_points = kwargs.get('num_points', None)
            search_tree = kwargs.get('search_tree', None)
            if pc is None or num_points is None or search_tree is None:
                raise KeyError("Please provide pc, num_points, and search_tree \
                    for point_sampler in SemSegRandomSampler")

            center_idx = np.random.choice(len(pc), 1)
            center_point = pc[center_idx, :].reshape(1, -1)

            if (pc.shape[0] < num_points):
                idxs = np.array(range(pc.shape[0]))
                idxs = list(idxs) + list(random.choices(idxs, k=diff))
            else:
                idxs = search_tree.query(center_point, k=num_points)[1][0]
            random.shuffle(idxs)
            pc = pc[idxs]
            return pc, idxs, center_point

        return _random_centered_gen


SAMPLER._register_module(SemSegRandomSampler)