from dependency_injector import containers, providers

from datagen.components.datapoint import IdentitiesDataPoint
from datagen.components.datapoint.repo import DatapointsRepository
from datagen.modalities.containers import ModalitiesContainer


class DatapointsContainer(containers.DeclarativeContainer):

    __self__ = providers.Self()

    config = providers.Configuration()

    modalities = providers.Container(ModalitiesContainer, config=config)

    factory = providers.Selector(
        config.environment, identities=providers.Factory(IdentitiesDataPoint, modalities_container=modalities)
    )

    repo = providers.Factory(DatapointsRepository, __self__)
