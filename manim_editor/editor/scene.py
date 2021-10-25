import os
import shutil
import time
import pathlib
from fractions import Fraction
from enum import Enum
from typing import List, Dict, Any

from .commands import run_ffmpeg


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
        Unique id for this section.
    name
        Human readable, non-unique name for this section.
    type
        How should this section be played?
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

    See Also
    --------
    :class:`.PresentationSectionType`
    """

    def __init__(self,
                 id: int,
                 name: str,
                 type: PresentationSectionType,
                 original_video: str,
                 width: int,
                 height: int,
                 fps: Fraction,
                 duration: float,
                 # only to be used when loading from project file
                 project_name: str = "",
                 in_project_video: str = "",
                 in_project_thumbnail: str = "",
                 in_project_id: int = -1):
        self.id = id
        self.name = name
        self.type = type
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

    def set_project(self, project_name: str, in_project_id: int) -> None:
        self.project_name = project_name
        self.in_project_id = in_project_id
        # TODO support other filetypes as well
        self.in_project_video = f"video_{in_project_id:04}.mp4"
        self.in_project_thumbnail = f"thumb_{in_project_id:04}.jpg"

    def get_in_project_video_abs(self) -> str:
        return os.path.join(self.project_name, self.in_project_video)

    def get_in_project_thumbnail_abs(self) -> str:
        return os.path.join(self.project_name, self.in_project_thumbnail)

    def copy_video(self) -> None:
        """Copy original video to project dir."""
        shutil.copyfile(self.original_video, self.get_in_project_video_abs())

    def create_thumbnail(self) -> bool:
        """Create thumbnail for section in project dir.
        Retrun False at failure."""
        print(f"extracting '{self.in_project_thumbnail}' from '{self.original_video}'")
        if not run_ffmpeg([
            "-sseof",
            "-3",
            "-i",
            self.original_video,
            "-update",
            "1",
            "-q:v",
            "1",
            self.get_in_project_thumbnail_abs(),
            "-y",
        ]):
            print(f"Thumbnail extraction failed.")
            return False
        return True

    def get_dict(self) -> Dict[str, Any]:
        """Get dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "original_video": self.original_video,
            "width": self.width,
            "height": self.height,
            "fps": str(self.fps),
            "duration": self.duration,
            "project_name": self.project_name,
            "in_project_video": self.in_project_video,
            "in_project_thumbnail": self.in_project_thumbnail,
            "in_project_id": self.in_project_id,
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

    def __init__(self, id: int, name: str, path: str, last_modified: float, sections: List[Section]):
        self.id = id
        self.name = name
        self.path = path
        self.last_modified = last_modified
        self.sections = sections

    def get_last_modified(self) -> str:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.last_modified))

    def get_rel_dir_path(self) -> str:
        parent_path = pathlib.Path(self.path).parent.absolute()
        return os.path.relpath(parent_path)
