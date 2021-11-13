import os
import time
from enum import Enum
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List

from .commands import run_ffmpeg

__all__ = ["PresentationSectionType", "Slide", "Section", "Scene"]


class PresentationSectionType(str, Enum):
    # start, end, wait for continuation by user
    NORMAL = "presentation.normal"
    # start, end, immediately continue to next section
    SKIP = "presentation.skip"
    # start, end, restart, immediately continue to next section when continued by user
    LOOP = "presentation.loop"
    # start, end, restart, finish animation first when user continues
    COMPLETE_LOOP = "presentation.complete_loop"

    # same as above but define sub section
    SUB_NORMAL = "presentation.sub.normal"
    SUB_SKIP = "presentation.sub.skip"
    SUB_LOOP = "presentation.sub.loop"
    SUB_COMPLETE_LOOP = "presentation.sub.complete_loop"


class Slide:
    """An instance of this class is represented as one element in the timeline of the presenter.
    It can hold one full section or one full section and multiple sub sections.
    A presentation consists of multiple slides.

    Attributes
    ----------
    sections
        List of sections in this slide
    """

    def __init__(self):
        self.sections: List[Section] = []

    def populate_main_section(self, main_section: "Section", project_name: str, in_project_id: int) -> bool:
        """Load first section."""
        if not main_section.set_project(project_name, in_project_id, in_project_id):
            return False
        self.sections = [main_section]
        return True

    def populate_sub_section(self, sub_section: "Section") -> bool:
        """meth:`populate` must have been executed first."""
        if not sub_section.set_project(
            self.sections[0].project_name, self.sections[-1].in_project_id + 1, self.sections[0].in_project_id
        ):
            return False
        self.sections.append(sub_section)
        return True

    def get_dict(self) -> Dict[str, Any]:
        """Get dictionary representation."""
        return {
            "sections_len": len(self.sections),
            "sections": [section.get_dict() for section in self.sections],
        }

    def __load_section(self, raw_section: Dict[str, Any]) -> "Section":
        """Create :class:`.Section` from dict read from a project json file created by the Manim Editor.
        Assumes the input data to be valid.
        """

        return Section(
            int(raw_section["id"]),
            raw_section["name"],
            raw_section["type"],
            raw_section["is_sub_section"],
            raw_section["original_video"],
            int(raw_section["width"]),
            int(raw_section["height"]),
            Fraction(raw_section["fps"]),
            float(raw_section["duration"]),
            # this hasn't been created by Manim directly
            raw_section["project_name"],
            raw_section["in_project_video"],
            raw_section["in_project_thumbnail"],
            int(raw_section["in_project_id"]),
        )

    def load(self, raw_slide: Dict[str, Any]) -> None:
        """Create :class:`.Slide` from dict read from a project json file created by the Manim Editor.
        Assumes the input data to be valid.
        """
        for section in raw_slide["sections"]:
            self.sections.append(self.__load_section(section))


class Section:
    """Representation of Manim :class:`.Section`.
    It can either be a full section of a sub section.

    Attributes
    ----------
    id
        Unique id for this section.
    name
        Human readable, non-unique name for this section.
    type
        How should this section be played?
    is_sub_section
        ``True`` when this is a subsection rather than a section.
    original_video
        Path to original video file.
    width
        width of the video
    height
        Height of the video.
    fps
        Frame rate of the video as :class:`.Fraction`.
    duration
        Duration of the video in seconds.
    project_name
        Name of the project this section is used in.
    in_project_video
        Path to copied video file relative to project file.
    in_project_thumbnail
        Path to thumbnail file relative to project file.
    in_project_id
        Id for this section that is unique in its project.
    parent_id
        In project id of the section this sub-section belongs to.
        When this is not a sub section it holds its own id.
        This is similar to a union-find structure.

    See Also
    --------
    :class:`.PresentationSectionType`
    """

    def __init__(
        self,
        id: int,
        name: str,
        type: str,
        is_sub_section: bool,
        original_video: Path,
        width: int,
        height: int,
        fps: Fraction,
        duration: float,
        # only to be used when loading from project file
        project_name: str = "",
        in_project_video: Path = Path(),
        in_project_thumbnail: Path = Path(),
        in_project_id: int = -1,
        parent_id: int = -1,
    ):
        self.id = id
        self.name = name
        self.type = type
        self.is_sub_section = is_sub_section
        self.original_video = original_video
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
        # to be set once project is being populated
        self.project_name = project_name
        self.in_project_video = in_project_video
        self.in_project_thumbnail = in_project_thumbnail
        self.in_project_id = in_project_id
        self.parent_id = parent_id

    def get_in_project_video_abs(self) -> Path:
        return Path(self.project_name) / self.in_project_video

    def get_in_project_thumbnail_abs(self) -> Path:
        return Path(self.project_name) / self.in_project_thumbnail

    def set_project(self, project_name: str, in_project_id: int, parent_id: int) -> bool:
        """Hand this video over to a project.
        Update attributes and copy assets.
        """
        self.project_name = project_name
        self.in_project_id = in_project_id
        self.in_project_video = Path(f"video_{in_project_id:04}.mp4")
        self.in_project_thumbnail = Path(f"thumb_{in_project_id:04}.jpg")
        self.parent_id = parent_id

        return self.convert_video() and self.extract_thumbnail()

    def convert_video(self) -> bool:
        """Convert original video into fragmented format that can be played by the video player.
        According to https://developer.mozilla.org/en-US/docs/Web/API/Media_Source_Extensions_API/Transcoding_assets_for_MSE.
        Also copy it to project dir.
        Return False at failure.
        """
        # TODO: this doesn't work for some versions of Chromium
        print(f"Converting video to '{self.in_project_video}' for section '{self.name}'.")
        if not run_ffmpeg(
            [
                "-i",
                str(self.original_video),
                "-movflags",
                "frag_keyframe+empty_moov+default_base_moof",
                str(self.get_in_project_video_abs()),
                "-y",
            ]
        ):
            print("Video Conversion failed.")
            return False
        return True

    def extract_thumbnail(self) -> bool:
        """Create thumbnail for section in project dir.
        Return False at failure.
        """
        print(f"Extracting thumbnail '{self.in_project_thumbnail}' from video for section '{self.name}'.")
        if not run_ffmpeg(
            [
                "-sseof",
                "-3",
                "-i",
                str(self.original_video),
                "-update",
                "1",
                "-q:v",
                "1",
                str(self.get_in_project_thumbnail_abs()),
                "-y",
            ]
        ):
            print("Thumbnail extraction failed.")
            return False
        return True

    def get_dict(self) -> Dict[str, Any]:
        """Get dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "is_sub_section": self.is_sub_section,
            "original_video": str(self.original_video),
            "width": self.width,
            "height": self.height,
            "fps": str(self.fps),
            "duration": self.duration,
            "project_name": self.project_name,
            "in_project_video": str(self.in_project_video),
            "in_project_thumbnail": str(self.in_project_thumbnail),
            "in_project_id": self.in_project_id,
            "parent_id": self.parent_id,
        }


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
    last_modified
        seconds since the epoch of last modification of index file
    sections
        list of sections in scene
    """

    def __init__(self, id: int, name: str, path: Path, last_modified: float, sections: List[Section]):
        self.id = id
        self.name = name
        self.path = path
        self.last_modified = last_modified
        self.sections = sections

    def get_last_modified(self) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.last_modified))

    def get_rel_dir_path(self) -> Path:
        """Used to display location in frontend."""
        parent_path = self.path.parent.absolute()
        return parent_path.relative_to(os.getcwd())
