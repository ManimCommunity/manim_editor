import os

from enum import Enum
from typing import List


class PresentationSectionType(str, Enum):
    # start, end, wait for continuation by user
    NORMAL = "presentation.normal"
    # start, end, immediately continue to next section
    SKIP = "presentation.skip"
    # start, end, restart, immediately continue to next section when continued by user
    LOOP = "presentation.loop"
    # start, end, restart, finish animation first when user continues
    COMPLETE_LOOP = "presentation.complete_loop"


class Section:
    """Representation of Manim :class:`.Section`.

    Attributes
    ----------
    name
        Human readable, non-unique name for this section.
    type
        How should this section be played?
    video
        Path to video file.

    See Also
    --------
    :class:`.PresentationSectionType`
    """

    def __init__(self, name: str, type: PresentationSectionType, video: str):
        self.name = name
        self.type = type
        self.video = video


class Index:
    """Representation of the entire section index of one scene.

    Attributes
    ----------
    path
        path to index JSON file
    sections
        list of sections in scene
    """

    def __init__(self, path: str, sections: List[Section]):
        self.path = path
        self.sections = sections
