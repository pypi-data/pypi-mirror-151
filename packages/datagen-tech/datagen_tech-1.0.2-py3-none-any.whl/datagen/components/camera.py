from dataclasses import dataclass, field
from typing import List

from dependency_injector.wiring import inject, Provide

from datagen.components.datapoint.base import DataPoint
from datagen.components.datapoint.repo import DatapointsRepository


@dataclass
class Camera:
    name: str
    scene_path: str
    datapoints: List[DataPoint] = field(init=False, repr=False)

    def __post_init__(self):
        self.datapoints = self._init_datapoints()

    @inject
    def _init_datapoints(self, repo: DatapointsRepository = Provide["repo"]) -> List[DataPoint]:
        return repo.get_datapoints(scene_path=self.scene_path, camera_name=self.name)

    def __iter__(self):
        for datapoint in self.datapoints:
            yield datapoint

    def __getitem__(self, key):
        return self.datapoints[key]

    def __len__(self):
        return len(self.datapoints)
