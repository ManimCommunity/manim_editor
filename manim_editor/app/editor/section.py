import os

from enum import Enum
from collections.abc import Iterable
import json
from typing import Dict, Any, Optional, List


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


def get_section(raw_section: Dict[str, Any]) -> Optional[Section]:
    """Create :class:`.Section` from dict read from an section index.
    Return ``None`` if dict is invalid. This happens when a JSON file that isn't a section index gets read.
    """

    for key, req_type in {
        "name": str,
        "type": str,
        "video": str,
        "codec_name": str,
        "width": int,
        "height": int,
        "avg_frame_rate": str,
        "duration": str,
        "nb_frames": str,
    }.items():
        if key not in raw_section:
            return None
        if type(raw_section[key]) is not req_type:
            return None
    return Section(
        raw_section["name"],
        raw_section["type"],
        os.path.abspath(raw_section["video"])
    )


def get_index(path: str) -> Optional[Index]:
    """Check if path points to a valid section index file.
    Return None if it is invalid. Return a list of :class:`.Section` otherwise.
    """
    with open(path, "r") as file:
        try:
            raw_sections = json.load(file)
        except json.decoder.JSONDecodeError:
            return None
    if not isinstance(raw_sections, Iterable):
        return None

    sections: List[Section] = []
    for raw_section in raw_sections:
        if not isinstance(raw_section, dict):
            return None
        section = get_section(raw_section)
        if section is None:
            return None
        sections.append(section)
    return Index(os.path.abspath(path), sections)
