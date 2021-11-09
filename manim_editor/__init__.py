from .config import Config
from .editor import (
    EditorBanner,
    EditorLogo,
    IconCompleteLoop,
    IconLoop,
    IconNormal,
    IconSkip,
    PresentationSectionType,
    get_config,
    set_config,
)

set_config(Config)


# NORMAL = PresentationSectionType.NORMAL
# SKIP = PresentationSectionType.SKIP
# LOOP = PresentationSectionType.LOOP
# COMPLETE_LOOP = PresentationSectionType.COMPLETE_LOOP
