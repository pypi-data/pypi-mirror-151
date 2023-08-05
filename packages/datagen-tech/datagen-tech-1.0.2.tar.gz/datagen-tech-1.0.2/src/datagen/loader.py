from datagen.components.dataset import Dataset, DatasetConfig
from datagen.containers import DatasetContainer


def load_dataset(*dataset_sources: str) -> Dataset:
    dataset = DatasetContainer()
    config = DatasetConfig(imaging_library="opencv")
    return dataset.create(config=config, sources_repo__sources_paths=dataset_sources)
