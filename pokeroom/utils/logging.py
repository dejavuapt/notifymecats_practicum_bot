import logging
from typing import Optional

def get_logger(file_name: str, class_name: Optional[str] = None) -> logging.Logger:
    parts = file_name.split("_")
    if parts[1].startswith("utils") and class_name is None:
        name = parts[0].rstrip(".")
    else:
        name = "%s%s" % (parts[0], class_name or parts[1].capitalize())
    return logging.getLogger(name)