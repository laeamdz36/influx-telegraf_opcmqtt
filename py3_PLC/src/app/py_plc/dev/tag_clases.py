"""Definition of tag clases"""
from dataclasses import dataclass
from typing import Any

# In order to make simple the access to data, define clases for tags
# with this class execute methodes to storage to InfluxDB
# methods to read from PLC with pycomm3
# The class is the general view on the data representation, not in the
# specific vendor technology or protocol, with this we unify data to add the value
# of Observability


@dataclass
class Tag:
    """A class to wrap data for a tag to make simple reading and storage"""

    name: str
    type: Any
    value: Any
