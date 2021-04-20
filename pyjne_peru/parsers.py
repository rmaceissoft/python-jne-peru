from typing import Optional, Union

from .entities import Entity, EntityFactory, ResultSet
from .error import JNEException


EntityParserResult = Union[Entity, ResultSet, None]


class EntityParser:

    def __init__(self):
        self.entity_factory = EntityFactory

    def parse(
        self, json: dict, payload_list: bool = False, payload_type: Optional[str] = None
    ) -> EntityParserResult:
        try:
            if payload_type is None:
                return None
            entity = getattr(self.entity_factory, payload_type)
        except AttributeError:
            raise JNEException(f'No entity for this payload type: {payload_type}')

        data = json.get('data')
        if payload_list:
            result = entity.parse_list(data)
        else:
            result = entity.parse(data)
        return result
