from dataclasses import field, dataclass
from typing import List, Iterator

from datagen import components
from datagen.components.datapoint.container import DatapointsContainer
from datagen.components.datasource import DataSource
from datagen.components.datapoint.base import DataPoint
from datagen.components.datasource import SourcesRepository
from datagen.components.scene import Scene


@dataclass
class DatasetConfig:
    imaging_library: str


@dataclass
class Dataset:
    config: DatasetConfig
    sources_repo: SourcesRepository = field(repr=False)
    scenes: List[Scene] = field(default_factory=list, repr=False)

    def __post_init__(self):
        for source in self.sources_repo.get_all():
            self._init(source)

    def _init(self, source: DataSource) -> None:
        self._init_datapoints_container(source)
        self.scenes.extend(source.init_scenes())

    def _init_datapoints_container(self, source: DataSource) -> None:
        container = DatapointsContainer(
            config={
                "environment": source.environment,
                "imaging_library": self.config.imaging_library
            }
        )
        container.wire(packages=[components])

    def __iter__(self) -> Iterator[DataPoint]:
        for scene in self.scenes:
            for datapoint in scene:
                yield datapoint

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._get_single_datapoint(key)
        elif isinstance(key, slice):
            return self._get_multiple_datapoints(key)

    def _get_single_datapoint(self, idx: int) -> DataPoint:
        idx = idx % len(self)
        assert 0 <= idx < len(self)
        [datapoint] = self._get_datapoints(start=idx, stop=idx + 1)
        return datapoint

    def _get_multiple_datapoints(self, key: slice) -> List[DataPoint]:
        start, stop = key.start if key.start is not None else 0, key.stop if key.stop is not None else len(self) - 1
        assert 0 <= start < stop < len(self)
        return self._get_datapoints(start, stop)

    def _get_datapoints(self, start: int, stop: int) -> List[DataPoint]:
        datapoints = []
        for idx, datapoint in enumerate(self):
            if start <= idx < stop:
                datapoints.append(datapoint)
        return datapoints

    def __len__(self):
        return sum(len(scene) for scene in self.scenes)
