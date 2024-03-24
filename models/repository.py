import dataclasses
import typing


@dataclasses.dataclass
class Contributor:
    username: str


@dataclasses.dataclass
class Model:
    link: str
    clone_link: str
    name: str
    readme: str  # possibly None
    first_time_seen: bool
    description: str  # possibly None
    stars: int
    contributors: typing.List[Contributor]  # possibly None
    owner: Contributor
