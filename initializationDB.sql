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
'Xenon biggrid',
'REPLACE_BASE_FOR_ID/getPolicy/https%3A%2F%2Foperations-portal.egi.eu%2Fvo%2Fview%2Fvoname%2Fxenon.biggrid.nl',
'Thilde.Soerensen@xenon.nl'),
('urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815',
'Nikhef',
'REPLACE_BASE_FOR_ID/getPolicy/urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815',
'Nikolas.Hefner@Nikhef.nl'),
('https://some-community.org',
'Some community',
'REPLACE_BASE_FOR_ID/getPolicy/https%3A%2F%2Fsome-community.org',
'Jeff.winger@community.org'),
('https://another-community.org',
'Another community',
'REPLACE_BASE_FOR_ID/getPolicy/https%3A%2F%2Fanother-community.org',
'Beff.Linger@cummonity.gor'),
('urn:idk:123456',
'The community',
'REPLACE_BASE_FOR_ID/getPolicy/urn:idk:123456',
'Tove.ditlevsen@dane.dk'),
('urn:som:654321',
'Minimum info policy',
'REPLACE_BASE_FOR_ID/getPolicy/urn:som:654321',
'Max.richter@classic.de'
)
;


INSERT INTO authorities(auth_id,uri)
VALUES ('1','https://www.nikhef.nl/'), 
('2','https://xenonexperiment.org/'),
('3','https://cern.ch'),
('4', NULL),
('5', NULL)
;

INSERT INTO authority_names(auth_id,auth_name,language)
VALUES ('1','Nikhef','stand'),
('2','Xenon-nT collaboration','stand'),
('2','Xenon-nT samarbejde', 'dk_DK'),
('3','CERN','dk_DK'),
('3','CERN','stand'),
('4','Auto sikkerhed','dk_DK'),
('5','Sicherheit fur dich', 'stand')
;

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

INSERT INTO policy(policy_url,auth_id, valid_from, ttl, policy_class, notice_refresh_period, id)
VALUES(
  'https://some-community.org',
  '2',
  '2025-10-17 09:00:00',
  '21817600',
  'privacy',
  '41212301',
  'https://some-community.org'
);

INSERT INTO policy(policy_url,auth_id, valid_from, ttl, policy_class, notice_refresh_period, id)
VALUES(
  'https://another-community.org',
  '3',
  '2019-06-10 23:59:59',
  '31104300',
  'sla',
  NULL,
  'https://another-community.org'
);

INSERT INTO policy(policy_url, auth_id, valid_from, ttl, policy_class, notice_refresh_period, id)
VALUES(
  'https://the-community.org',
  '4',
  '2025-05-01 18:00:00',
  '604800',
  'conditions',
  '259200',
  'urn:idk:123456'
);

INSERT INTO policy(policy_url, auth_id, valid_from, ttl, policy_class, notice_refresh_period, id)
VALUES(
  NULL,
  '5',
  NULL,
  NULL,
  'privacy',
  NULL,
  'urn:som:654321'
);

INSERT INTO descriptions(id,description, language)
VALUES ('urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815','This Acceptable Use Policy governs the use of the Nikhef networking and computer services; all users of these services are expected to understand and comply to these rules.','stand'),
('https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl','detector construction and experiment analysis for the search of dark matter using Xenon detectors','stand'),
('urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815','Deze Gebruiksvoorwaarden betreffen het gebruik van netwerk en computers bij Nikhef. Iedere gebruiker van deze middelen of diensten wordt geacht op hoogte te zijn van deze voorwaarden en deze na te leven.','nl_NL'),
('https://some-community.org','A community somwhere researching for the betterment of mankind (hopefully)', 'stand'),
('https://some-community.org','Et samarbejde et eller andet sted som forsker til fordel for menneskeheden (forhaabentlig)','dk_DK'),
('https://another-community.org','A research community beyond suspicion.','stand'),
('https://another-community.org','Et trovaerdigt forsknings institut.','dk_DK')
;

INSERT INTO contacts(type, email, id)
VALUES ('standard', 'grid.support@nikhef.nl', 'https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl'),
('security', 'vo-xenon-admins@biggrid.nl', 'https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl'),
('security', 'abuse@nikhef.nl', 'urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815'),
('standard', 'helpdesk@nikhef.nl', 'urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815'),
('standard', 'information-security@nikhef.nl', 'urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815'),
('privacy', 'privacy@nikhef.nl', 'urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815'),
('standard', 'research.support@somewhere.org', 'https://some-community.org'),
('security', 'secure@somewhere.org', 'https://some-community.org'),
('privacy', 'safe@somewhere.org','https://some-community.org'),
('standard','notSupicious@mikrosoft.xyz','https://another-community.org'),
('standard','friend@gov.org','urn:idk:123456'),
('standard','Max.Jurgen@hochschule.de','urn:som:654321')
;


INSERT INTO implicit_policy_uris(id, implicit_uri)
VALUES ('urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815', 'https://documents.egi.eu/document/2623'),
('https://some-community.org','urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815'),
('https://some-community.org','urn:idk:123456'),
('https://another-community.org','https://some-community.org'),
('https://another-community.org','https://wise-community.org/wise-baseline-aup/v1/'),
('urn:idk:123456','https://another-community.org')
;

INSERT INTO augment_policy_uris(id, augment_uri)
VALUES ('https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl', 'https://wise-community.org/wise-baseline-aup/v1/'),
('https://another-community.org','https://documents.egi.eu/document/2623'),
('urn:idk:123456','urn:doi:10.60953/68611c23-ccc7-4199-96fe-74a7e6021815'),
('https://some-community.org','https://operations-portal.egi.eu/vo/view/voname/xenon.biggrid.nl')
;

INSERT INTO privacy_policies(id,jurisdiction)
VALUES ('https://some-community.org', 'eu')
