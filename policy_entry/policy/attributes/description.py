"""
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>.
"""

import re


class Description:
    def __init__(self, description:str, language:str="stand"):
        self.validateLanguage(language)
        self.description = description
        self.language = language

    def validateLanguage(self, language):
        if language != "stand":
            regex = re.compile(r"^([a-z]{2})_([A-Z]{2})$")
            match = regex.match(language)
            if not match:
                raise ValueError(
                    f"The description language is not in accordance with rfc4646: {language}"
                )


    @classmethod
    def from_dict(cls, data: dict):
        return cls(description=data.get("description"), language=data.get("language"))

    def to_dict(self):
        if self.language == "stand":
            return {f'description': self.description}
        else:
            return {f"description#{self.language}": self.description}
