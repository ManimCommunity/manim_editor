from .editor import set_config
from .config import Config

from .editor import IconNormal, IconSkip, IconLoop, IconCompleteLoop, EditorLogo, EditorBanner
from .editor import PresentationSectionType, get_config, set_config

set_config(Config)


# NORMAL = PresentationSectionType.NORMAL
# SKIP = PresentationSectionType.SKIP
# LOOP = PresentationSectionType.LOOP
# COMPLETE_LOOP = PresentationSectionType.COMPLETE_LOOP
