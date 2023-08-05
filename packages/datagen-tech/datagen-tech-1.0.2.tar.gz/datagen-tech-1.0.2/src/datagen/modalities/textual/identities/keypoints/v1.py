from typing import List

import marshmallow_dataclass
from marshmallow import pre_load
from datagen.modalities.textual.common import NumpyArray


@marshmallow_dataclass.dataclass
class Keypoints:
    coords_2d: NumpyArray
    coords_3d: NumpyArray
    is_visible: NumpyArray

    @pre_load
    def rearrange_fields(self, in_data: dict, **kwargs) -> dict:
        coords_2d_dict = in_data.pop("keypoints_2d_coordinates")
        coords_3d_dict = in_data.pop("keypoints_3d_coordinates")
        is_visible_dict = in_data.pop("is_visible")
        return {
            "coords_2d": _to_list(coords_2d_dict),
            "coords_3d": _to_list(coords_3d_dict),
            "is_visible": _to_list(is_visible_dict)
        }


def _to_list(dict_: dict) -> list:
    list_ = []
    for keypoint_idx in _get_sorted_keys(dict_):
        list_.append(dict_[str(keypoint_idx)])
    return list_


def _get_sorted_keys(dict_) -> List[int]:
    return sorted(int(s) for s in dict_.keys())
