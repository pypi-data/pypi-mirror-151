"""..."""
from .Audio import Audio
from .Compress import Compress
from .Copy import Copy
from .Create import Create
from .Download import Download
from .Drive import Drive
from .File import File
from .Move import Move
from .Other import Other
from .Recyclebin import Recyclebin
from .Search import Search
from .Share import Share
from .Star import Star
from .User import User
from .Video import Video


class Core(
    Audio,
    Copy,
    Create,
    Drive,
    File,
    Move,
    Download,
    Recyclebin,
    Search,
    Share,
    User,
    Video,
    Star,
    Other,
    Compress,
):
    """..."""
