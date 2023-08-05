from dataclasses import dataclass

from datagen import modalities
from datagen.components.datapoint import base


@dataclass
class DataPoint(base.DataPoint):
    @modalities.textual_modality
    def actor_metadata(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="actor_metadata", file_name="actor_metadata.json")

    @modalities.textual_modality
    def face_bounding_box(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="face_bounding_box", file_name="face_bounding_box.json")

    @modalities.textual_modality
    def camera_metadata(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="camera_metadata", file_name="camera_metadata.json")

    @modalities.textual_modality
    def standard_keypoints(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="keypoints", file_name="standard_keypoints.json")

    @modalities.textual_modality
    def dense_keypoints(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="keypoints", file_name="dense_keypoints.json")

    @modalities.textual_modality
    def semantic_segmentation_color_map(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="segmentation", file_name="semantic_segmentation_metadata.json")

    @property
    def semantic_segmentation_metadata(self):
        """
        TODO: Deprecated, to remove
        """
        return self.semantic_segmentation_color_map

    @modalities.textual_modality
    def _environments(self) -> modalities.TextualModality:
        return modalities.TextualModality(factory_name="environments", file_name="environment.json")

    @property
    def environment(self):
        return self._environments[self.visible_spectrum_image]

