import os
from dataclasses import dataclass
from typing import List, Iterable

from dependency_injector import containers
from dependency_injector.wiring import inject

from datagen.components.datapoint.base import DataPoint


@inject
@dataclass
class DatapointsRepository:
    container: containers.DeclarativeContainer

    def get_datapoints(self, scene_path: str, camera_name: str) -> List[DataPoint]:
        datapoints = []
        for environment in self._get_environments(scene_path, camera_name):
            datapoints.append(
                self.container.factory(
                    scene_path=scene_path, camera=camera_name, visible_spectrum_image=environment.image_name
                )
            )
        return datapoints

    def _get_environments(self, scene_path: str, camera_name: str) -> Iterable:
        environments_file_path = os.path.join(scene_path, camera_name, "environment.json")
        return self.container.modalities().textual().environments(modality_file_path=environments_file_path)
