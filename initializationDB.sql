
CREATE TABLE IF NOT EXISTS policy_entries (
    uri CHAR(36) PRIMARY KEY, 
    name VARCHAR(256) NOT NULL,
    informational_url VARCHAR(256) NOT NULL,
    owner VARCHAR(256) NOT NULL
);


CREATE TABLE IF NOT EXISTS `authorities` (
  uri varchar(256) DEFAULT NULL,
  auth_name varchar(50) NOT NULL,
  PRIMARY KEY (`auth_name`)
);


CREATE TABLE IF NOT EXISTS `policy` (
  uri char(36) NOT NULL,
  description text,
  policy_url varchar(256) DEFAULT NULL,
  valid_from timestamp NULL DEFAULT NULL,
  ttl int DEFAULT NULL,
  policy_class enum('purpose','acceptable-use','conditions','sla','privacy') DEFAULT NULL,
  notice_refresh_period int DEFAULT NULL,
  id varchar(256) DEFAULT NULL,
  auth_name varchar(50) DEFAULT NULL,
  PRIMARY KEY (`uri`),
  KEY `auth_name` (`auth_name`),
  CONSTRAINT `policy_ibfk_2` FOREIGN KEY (`uri`) REFERENCES `policy_entries` (`uri`),
  CONSTRAINT `policy_ibfk_3` FOREIGN KEY (`auth_name`) REFERENCES `authorities` (`auth_name`)
);


CREATE TABLE IF NOT EXISTS `contacts` (
  type enum('standard','security','privacy') NOT NULL,
  email varchar(255) NOT NULL,
  policy_uri char(36) NOT NULL,
  PRIMARY KEY (`policy_uri`,`email`,`type`),
  CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`policy_uri`) REFERENCES `policy_entries` (`uri`)
);


CREATE TABLE IF NOT EXISTS `implicit_policy_uris` (
  uri char(36) NOT NULL,
  implicit_uri varchar(256) DEFAULT NULL,
  PRIMARY KEY (`uri`),
  CONSTRAINT `implicit_policy_uris_ibfk_1` FOREIGN KEY (`uri`) REFERENCES `policy_entries` (`uri`)
); 


CREATE TABLE IF NOT EXISTS `augment_policy_uris` (
  uri char(36) NOT NULL,
  augment_uri varchar(256) DEFAULT NULL,
  PRIMARY KEY (`uri`),
  CONSTRAINT `augment_policy_uris_ibfk_2` FOREIGN KEY (`uri`) REFERENCES `policy_entries` (`uri`)
);




INSERT IGNORE INTO authorities(uri,auth_name)
VALUES ('https://www.nikhef.nl/', 'Nikhef'), ('https://xenonexperiment.org/', 'Xenon-nT collaboration');


INSERT IGNORE INTO contacts(type, email, policy_uri)
VALUES ('standard', 'grid.support@nikhef.nl', '4a6d33b3-34c0-4d39-9c87-f39d6f932a6b'),
('security', 'vo-xenon-admins@biggrid.nl', '4a6d33b3-34c0-4d39-9c87-f39d6f932a6b'),
('security', 'abuse@nikhef.nl', '8eaa6f4e-bf42-4cb4-8048-e26864c7ec58'),
('standard', 'helpldesk@nikhef.nl', '8eaa6f4e-bf42-4cb4-8048-e26864c7ec58'),
('standard', 'information-security@nikhef.nl', '8eaa6f4e-bf42-4cb4-8048-e26864c7ec58'),
('privacy', 'privacy@nikhef.nl', '8eaa6f4e-bf42-4cb4-8048-e26864c7ec58');


INSERT IGNORE INTO implicit_policy_uris(uri, implicit_uri)
VALUES ('8eaa6f4e-bf42-4cb4-8048-e26864c7ec58', 'https://documents.egi.eu/document/2623');

INSERT IGNORE INTO augment_policy_uris(uri, augment_uri)
VALUES ('4a6d33b3-34c0-4d39-9c87-f39d6f932a6b', 'https://wise-community.org/wise-baseline-aup/v1/');

INSERT IGNORE INTO policy(uri, description, policy_url, auth_name, valid_from, ttl, policy_class, notice_refresh_period, id)
VALUES ('4a6d33b3-34c0-4d39-9c87-f39d6f932a6b', 
'detector construction and experiment analysis for the search of dark matter using Xenon detectors',
'https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl',
'Xenon-nT collaboration',
'1311890400',
'31557600',
'purpose',
NULL,
'https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl');

INSERT IGNORE INTO policy(uri, description, policy_url, auth_name, valid_from, ttl, policy_class, notice_refresh_period, id)
VALUES ('8eaa6f4e-bf42-4cb4-8048-e26864c7ec58',
'This Acceptable Use Policy governs the use of the Nikhef networking and computer services; all users of these services are expected to understand and comply to these rules.',
'https://www.nikhef.nl/aup/',
'Nikhef',
'1649023200',
'604800',
'acceptable-use',
'34214400',
'urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815');

INSERT IGNORE INTO policy_entries(uri,name,informational_url,owner)
VALUES('4a6d33b3-34c0-4d39-9c87-f39d6f932a6b',
'AARC documentation example2',
'https://base-api-notice-management-api.app.cern.ch/getPolicy/4a6d33b3-34c0-4d39-9c87-f39d6f932a6b',
'Owner is later to be decided'),
('8eaa6f4e-bf42-4cb4-8048-e26864c7ec58',
'AARC documentation example',
'https://base-api-notice-management-api.app.cern.ch/getPolicy/8eaa6f4e-bf42-4cb4-8048-e26864c7ec58',
'Owner is later to be decided');
