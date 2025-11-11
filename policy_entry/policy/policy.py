"""
Copyright (c) European Organization for Nuclear Research (CERN). 2025
This file is part of AARC3-WP4-Policy-Registration-API.
AARC3-WP4-Policy-Registration-API is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
AARC3-WP4-Policy-Registration-API is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with AARC3-WP4-Policy-Registration-API. If not, see <https://www.gnu.org/licenses/>.
"""
import json

from policy_entry.policy.attributes.authority import Authority, AuthorityNames
from policy_entry.policy.attributes.contact import Contact
from policy_entry.policy.attributes.description import Description

from enum import Enum
from typing import List

class PolicyTypes(Enum):
    PURPOSE = "purpose"
    ACCEPTABLE_USE = "acceptable-use"
    CONDITIONS = "conditions"
    SLA = "sla"
    PRIVACY = "privacy"



class Policy:
    def __init__(
        self,
        name: str,
        owner: str,
        policyId: str,
        policy_class: str,
        authority: Authority,
        contacts: List[Contact],
        valid_from: str = None,
        policy_url:str = None,
        augment_policy_uris: List[str] = None,
        implicit_policy_uris: List[str] = None,
        descriptions: List[Description] = None, 
        notice_refresh_period:int = None,
        ttl: int = None,
        policy_jurisdiction:str = None
    ):
        self.validatePolicyClass(policy_class)
        self.validatePolicyJurisdiction(policy_jurisdiction, policy_class)
        self.name = name
        self.owner = owner
        self.policyId = policyId
        self.policy_class = policy_class
        self.authority = authority
        self.contacts = contacts
        self.valid_from = valid_from
        self.policy_url = policy_url
        self.augment_policy_uris = augment_policy_uris
        self.implicit_policy_uris = implicit_policy_uris
        self.descriptions = descriptions
        self.notice_refresh_period = notice_refresh_period
        self.ttl = ttl
        self.policy_jurisdiction = policy_jurisdiction

    def validatePolicyClass(self, policy_class:str):
        if policy_class is not None and policy_class not in PolicyTypes:
            raise ValueError(f'Not a valid policy class type:{policy_class}')
        
    def validatePolicyJurisdiction(self,policy_jurisdiction:str, policy_class:str):
        if policy_jurisdiction is not None and policy_class is not PolicyTypes.PRIVACY:
            raise ValueError(f'Jurisdiction is only valid with Privacy policy not: {policy_class}')


    @classmethod
    def from_dict(cls, data: dict):
        """Deserialize a dictionary into a Policy object"""
        
        # Build Authority from 'aut' and 'auth_languages'
        aut_url = data.get("aut")
        auth_names_data = data.get("auth_languages", [])
        authority = None
        if aut_url or auth_names_data:
            authority_names = [AuthorityNames.from_dict(a) for a in auth_names_data]
            authority = Authority(aut=aut_url, names=authority_names)

        # Create Contacts
        contacts_data = data.get("contacts", [])
        contacts = [Contact.from_dict(c) for c in contacts_data]

        # Create Descriptions
        descriptions_data = data.get("descriptions", [])
        descriptions = [Description.from_dict(d) for d in descriptions_data]

        return cls(
            name=data["name"],
            owner=data["owner"],
            policyId=data["id"],
            policy_class=data["policy_class"],
            authority=authority,
            contacts=contacts,
            augment_policy_uris=data.get("augment_policy_uris"),
            implicit_policy_uris=data.get("includes_policy_uris"),
            descriptions=descriptions,
            notice_refresh_period=data.get("notice_refresh_period"),
            ttl=data.get("ttl"),
            policy_jurisdiction=data.get("policy_jurisdiction"),
            valid_from=data["valid_from"],
            policy_url=data["policy_url"]
        )

    @classmethod
    def from_json(cls, json_str: str):
        """Deserialize a JSON string into a Policy object"""
        data = json.loads(json_str)
        return cls.from_dict(data)



