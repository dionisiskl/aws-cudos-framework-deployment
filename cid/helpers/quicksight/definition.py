import logging
import re
from typing import Dict
from cid.helpers.quicksight.resource import CidQsResource
from cid.helpers.quicksight.version import CidVersion

logger = logging.getLogger(__name__)

class Definition:

    def __init__(self, raw: dict) -> None:
        self.raw: dict = raw
        # Resolve version from definition contents
        self._raw_version = self.resolve_version(self.raw)
    
    @property
    def cid_version(self) -> CidVersion:
        # Resolve version from "About" sheet contents
        try:
            return CidVersion(self._raw_version)
        except TypeError as e:
            logger.debug(f"Could not resolve CID version. Raw version value '{self._raw_version}' does not conform to CID version format vmajor.minor.build e.g. v.1.0.1")
        
        return None
    
    def resolve_version(self, raw: dict):
        about_content = [text_content["Content"] for sheet in raw["Sheets"] for text_content in sheet["TextBoxes"] if sheet["Name"] == "About"]
        if about_content:
            all_about_content = " | ".join(about_content)
            # find first string that looks like vx.y.z using a regular expression where x, y and z are numbers
            version_matches = re.findall(r"(v\d+?\.\d+?\.\d+?)", all_about_content)
            if version_matches:
                return version_matches[0]
            else:
                version_matches = re.findall(r"(v\d+?\.\d+?)", all_about_content)
                if version_matches:
                    return f"{version_matches[0]}.0"

        return None
        

