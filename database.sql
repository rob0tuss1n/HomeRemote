CREATE TABLE `accounts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` TEXT,
  `username` TEXT,
  `password` TEXT,
  `lastlogin` DATE,
  PRIMARY KEY  (`id`)
);

CREATE TABLE `events` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` TEXT,
  `action` TEXT,
  `who` TEXT,
  `trigger` TEXT,
  `trigger_args` TEXT,
  `timeout` INT,
  PRIMARY KEY  (`id`)
);

CREATE TABLE `helper_processes` (
  `pid` INT NOT NULL AUTO_INCREMENT,
  `type` TEXT,
  `info` TEXT,
  PRIMARY KEY  (`pid`)
);

CREATE TABLE `inputs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` TEXT,
  `pin` INT,
  `type` TEXT,
  PRIMARY KEY  (`id`)
);

CREATE TABLE `outputs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` TEXT,
  `pin` INT,
  PRIMARY KEY  (`id`)
);

CREATE TABLE `pins` (
  `pin` INT NOT NULL AUTO_INCREMENT,
  `used` INT,
  `direction` TEXT,
  PRIMARY KEY  (`pin`)
);

CREATE TABLE `security_zones` (
  `pin` INT NOT NULL AUTO_INCREMENT,
  `name` TEXT,
  PRIMARY KEY  (`pin`)
);

CREATE TABLE `settings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `field` TEXT,
  `value` TEXT,
  PRIMARY KEY  (`id`)
);