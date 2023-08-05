from dataclasses import dataclass
from pathlib import Path
from typing import List, Iterator

from datagen.components.scene import Scene

# Older datasets scenes are named "environment_XXXXX".
SCENE_FOLDER_NAME_PATTERNS = ["scene_*", "environment_*"]


@dataclass
class DataSource:
    path: Path

    @property
    def environment(self) -> str:
        return "identities"

    def init_scenes(self) -> List[Scene]:
        scenes = [Scene(dir_) for dir_ in sorted(self.path.iterdir()) if self._matches_scene_name_pattern(dir_)]
        assert len(scenes) > 0, f"Invalid source structure: {self.path}"
        return scenes

    @staticmethod
    def _matches_scene_name_pattern(dir_) -> bool:
        return any(dir_.match(p) for p in SCENE_FOLDER_NAME_PATTERNS) and dir_.is_dir()


@dataclass
class SourcesRepository:
    sources_paths: List[str]

    def get_all(self) -> Iterator[DataSource]:
        for path in self.sources_paths:
            yield DataSource(path=Path(path))
