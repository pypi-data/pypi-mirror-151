from dataclasses import dataclass

__version__ = "0.0.3"


@dataclass
class VersionInfo:
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


version_info = VersionInfo(1, 2, 1, "beta", 0)
