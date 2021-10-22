import os
from fractions import Fraction

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
    id
        unique id for this section
    name
        Human readable, non-unique name for this section.
    type
        How should this section be played?
    video
        Path to video file.
    width
        width of the video
    height
        height of the video
    fps
        frame rate of the video as :class:`.Fraction`
    duration
        duration of the video in seconds

    See Also
    --------
    :class:`.PresentationSectionType`
    """

    def __init__(self,
                 id: int,
                 name: str,
                 type: PresentationSectionType,
                 video: str,
                 width: int,
                 height: int,
                 fps: Fraction,
                 duration: float):
        self.id = id
        self.name = name
        self.type = type
        self.video = video
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration


class Scene:
    """Representation of the entire section index of one scene.

    Attributes
    ----------
    id
        unique id for this scene
    name
        name for the represented scene
    path
        path to index JSON file
    sections
        list of sections in scene
    """

    def __init__(self, id: int, name: str, path: str, sections: List[Section]):
        self.id = id
        self.name = name
        self.path = path
        self.sections = sections
