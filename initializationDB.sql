CREATE TABLE IF NOT EXISTS policy_entries (
  name VARCHAR(256) NOT NULL,
  informational_url VARCHAR(256) NOT NULL,
  owner VARCHAR(256) DEFAULT NULL,
  id VARCHAR(256) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY name (name)
);

CREATE TABLE IF NOT EXISTS `authorities` (
  `auth_id` int NOT NULL AUTO_INCREMENT,
  `uri` VARCHAR(256) DEFAULT NULL,
  PRIMARY KEY (`auth_id`)
);

CREATE TABLE IF NOT EXISTS `authority_names` (
  `auth_id` int NOT NULL,
  `auth_name` varchar(50) NOT NULL,
  `language` char(5) NOT NULL,
  PRIMARY KEY (`auth_id`, `language`),
  FOREIGN KEY (`auth_id`) REFERENCES `authorities` (`auth_id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `policy` (
  `policy_url` varchar(256) DEFAULT NULL,
  `valid_from` timestamp NULL DEFAULT NULL,
  `ttl` int DEFAULT NULL,
  `policy_class` enum('purpose','acceptable-use','conditions','sla','privacy') NOT NULL,
  `notice_refresh_period` int DEFAULT NULL,
  `id` varchar(256) NOT NULL,
  `auth_id` int NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `policy_ibfk_3` FOREIGN KEY (`auth_id`) REFERENCES `authorities` (`auth_id`),
  CONSTRAINT `policy_ibfk_4` FOREIGN KEY (`id`) REFERENCES `policy_entries` (`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `descriptions` (
  `id` varchar(256) NOT NULL,
  `description` text,
  `language` char(5),
  PRIMARY KEY (`id`,`language`),
  CONSTRAINT `description_id` FOREIGN KEY (`id`) REFERENCES `policy` (`id`) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `privacy_policies` (
  `id` varchar(256) NOT NULL,
  `jurisdiction` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `priv_id` FOREIGN KEY (`id`) REFERENCES `policy` (`id`) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS `contacts` (
  `type` enum('standard','security','privacy') NOT NULL,
  `email` varchar(255) NOT NULL,
  `id` varchar(256) NOT NULL,
  PRIMARY KEY (`type`,`email`,`id`),
  KEY `id` (`id`),
  CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`id`) REFERENCES `policy` (`id`) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS `implicit_policy_uris` (
  `id` varchar(256) NOT NULL,
  `implicit_uri` varchar(256) NOT NULL,
  PRIMARY KEY (`id`,`implicit_uri`),
  CONSTRAINT `implicit_policy_uris_ibfk_1` FOREIGN KEY (`id`) REFERENCES `policy` (`id`) ON DELETE CASCADE
); 


CREATE TABLE IF NOT EXISTS `augment_policy_uris` (
  `augment_uri` varchar(256) NOT NULL,
  `id` varchar(256) NOT NULL,
  PRIMARY KEY (`id`,`augment_uri`),
  CONSTRAINT `augment_policy_uris_ibfk_1` FOREIGN KEY (`id`) REFERENCES `policy` (`id`) ON DELETE CASCADE
);

INSERT INTO policy_entries(id,name,informational_url,owner)
VALUES('https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl',
'AARC documentation example2',
'REPLACE_BASE_FOR_ID/getPolicy/https%3A%2F%2Foperations-portal.egi.eu%2Fvo%2Fview%2Fvoname%2Fxenon.biggrid.nl',
'Owner is later to be decided'),
('urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815',
'AARC documentation example',
'REPLACE_BASE_FOR_ID/getPolicy/urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815',
'Owner is later to be decided');


INSERT INTO authorities(auth_id,uri)
VALUES ('1','https://www.nikhef.nl/'), 
('2','https://xenonexperiment.org/');

INSERT INTO authority_names(auth_id,auth_name,language)
VALUES ('1','Nikhef','stand'),
('2','Xenon-nT collaboration','stand');

INSERT INTO policy(policy_url, auth_id, valid_from, ttl, policy_class, notice_refresh_period, id)
VALUES (
'https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl',
'2',
'2011-07-29 00:00:00',
'31557600',
'purpose',
NULL,
'https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl');

INSERT INTO policy(policy_url, auth_id, valid_from, ttl, policy_class, notice_refresh_period, id)
VALUES (
'https://www.nikhef.nl/aup/',
'1',
'2022-04-04 00:00:00',
'604800',
'acceptable-use',
'34214400',
'urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815');

INSERT INTO descriptions(id,description, language)
VALUES ('urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815','This Acceptable Use Policy governs the use of the Nikhef networking and computer services; all users of these services are expected to understand and comply to these rules.','stand'),
('https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl','detector construction and experiment analysis for the search of dark matter using Xenon detectors','stand');

INSERT INTO contacts(type, email, id)
VALUES ('standard', 'grid.support@nikhef.nl', 'https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl'),
('security', 'vo-xenon-admins@biggrid.nl', 'https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl'),
('security', 'abuse@nikhef.nl', 'urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815'),
('standard', 'helpdesk@nikhef.nl', 'urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815'),
('standard', 'information-security@nikhef.nl', 'urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815'),
('privacy', 'privacy@nikhef.nl', 'urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815');


INSERT INTO implicit_policy_uris(id, implicit_uri)
VALUES ('urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815', 'https://documents.egi.eu/document/2623');

INSERT INTO augment_policy_uris(id, augment_uri)
VALUES ('https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl', 'https://wise-community.org/wise-baseline-aup/v1/');
