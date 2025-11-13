"""
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>.
"""
import re
from enum import Enum


class ContactTypes(Enum):
    STANDARD = "standard"
    SECURITY = "security"
    PRIVACY = "privacy"


class Contact:
    def __init__(self, contact_type:str, email:str):
        self.validateEmail(email)
        self.validateType(contact_type)
        self.email = email
        self.contact_type = contact_type

    def validateEmail(self, email):
        """Veryfying the email. Simple validation, not in depth"""
        regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(regex, email):
            raise ValueError(f"The email: {email}, is not a valid email for a contact")


    def validateType(self, contact_type):
        """Veryifying the type is within the restricted enums"""
        if contact_type not in ContactTypes:
            raise ValueError(
                f"The type: {contact_type}, is not a valid enum type. Only standard, security or privacy is allowed"
            )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            contact_type=data.get("type"),
            email=data.get("email")
        )
    
    def to_dict(self):
        return{"email": self.email, "type": self.contact_type}
