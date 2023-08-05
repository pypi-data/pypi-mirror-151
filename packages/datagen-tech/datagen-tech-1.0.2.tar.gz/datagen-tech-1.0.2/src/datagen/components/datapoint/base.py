import os
from dataclasses import dataclass, field
from pathlib import Path

import cv2
from deprecated.classic import deprecated

from datagen import modalities
from datagen.modalities.containers import ModalitiesContainer


@dataclass
class DataPoint:
    visible_spectrum_image: str
    camera: str
    scene_path: Path
    modalities_container: ModalitiesContainer = field(repr=False)

    @modalities.visual_modality
    def visible_spectrum(self) -> modalities.VisualModality:
        return modalities.VisualModality(self.visible_spectrum_image)

    @modalities.visual_modality
    def semantic_segmentation(self) -> modalities.VisualModality:
        if self._semantic_seg_as_png:
            return modalities.VisualModality(
                "semantic_segmentation.png", read_context={"opencv_reading_flags": cv2.IMREAD_UNCHANGED}
            )
        else:
            return modalities.VisualModality("semantic_segmentation.exr")

    @property
    def _semantic_seg_as_png(self) -> bool:
        semantic_seg_as_png_path = os.path.join(self.scene_path, self.camera, "semantic_segmentation.png")
        return os.path.exists(semantic_seg_as_png_path)

    @modalities.visual_modality
    def depth(self) -> modalities.VisualModality:
        return modalities.VisualModality("depth.exr")

    @modalities.visual_modality
    @deprecated(reason="Modality name changed to 'normals_map', please use new name instead")
    def normal_maps(self) -> modalities.VisualModality:
        return modalities.VisualModality("normal_maps.exr")

    @modalities.visual_modality
    def normals_map(self) -> modalities.VisualModality:
        return modalities.VisualModality("normal_maps.exr")

    @modalities.visual_modality
    def infra_red(self) -> modalities.VisualModality:
        return modalities.VisualModality("infra_red.png")
