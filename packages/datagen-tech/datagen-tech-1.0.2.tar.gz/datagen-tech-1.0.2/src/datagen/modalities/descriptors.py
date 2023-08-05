import abc
import os
from dataclasses import dataclass, field


class ModalityFileNotFoundError(RuntimeError):
    ...


@dataclass
class Modality(abc.ABC):
    file_name: str
    read_context: dict = field(default_factory=dict)


class ModalityDescriptor(abc.ABC):
    def __init__(self, fget=None, **kwargs):
        self._fget = fget

    def __get__(self, dp, *args):
        modality = self._fget(dp)
        modality_file_path = self._get_modality_file_path(dp, modality)
        return self._read(dp, modality, modality_file_path)

    @staticmethod
    def _get_modality_file_path(dp, modality: Modality) -> str:
        scene_modality_path = os.path.join(dp.scene_path, modality.file_name)
        cam_modality_path = os.path.join(dp.scene_path, dp.camera, modality.file_name)
        if os.path.exists(scene_modality_path):
            return scene_modality_path
        elif os.path.exists(cam_modality_path):
            return cam_modality_path
        else:
            raise ModalityFileNotFoundError(f"'{modality.file_name}' not found under {str(dp.scene_path)}")

    @abc.abstractmethod
    def _read(self, dp, modality: Modality, modality_file_path: str):
        ...


@dataclass
class TextualModality(Modality):
    factory_name: str = None


class TextualModalityDescriptor(ModalityDescriptor):
    def _read(self, dp, modality: TextualModality, modality_file_path: str):
        return dp.modalities_container.read_textual_modality(
            modality_factory_name=modality.factory_name,
            modality_file_path=modality_file_path,
            **modality.read_context,
        )


@dataclass
class VisualModality(Modality):
    ...


class VisualModalityDescriptor(ModalityDescriptor):
    def _read(self, dp, modality: VisualModality, modality_file_path: str):
        return dp.modalities_container.read_visual_modality(
            modality_file_path=modality_file_path, **modality.read_context
        )
