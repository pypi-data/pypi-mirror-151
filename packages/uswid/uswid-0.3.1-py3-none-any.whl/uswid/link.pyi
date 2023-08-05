from .enums import uSwidGlobalMap as uSwidGlobalMap
from .errors import NotSupportedError as NotSupportedError
from _typeshed import Incomplete
from enum import IntEnum
from typing import Optional

class uSwidLinkRel(IntEnum):
    ANCESTOR: int
    COMPONENT: int
    FEATURE: int
    INSTALLATIONMEDIA: int
    PACKAGEINSTALLER: int
    PARENT: int
    PATCHES: int
    REQUIRES: int
    SEE_ALSO: int
    SUPERSEDES: int
    SUPPLEMENTAL: int

class uSwidLink:
    href: Incomplete
    rel: Incomplete
    def __init__(self, href: Optional[str] = ..., rel: Optional[str] = ...) -> None: ...
