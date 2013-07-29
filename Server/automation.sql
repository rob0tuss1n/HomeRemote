-- ----------------------------
-- Table structure for `accounts`
-- ----------------------------
CREATE TABLE `accounts` (
`id`  int(11) NOT NULL ,
`name`  text NULL ,
`username`  text NULL ,
`password`  text NULL ,
`sid`  text NULL ,
PRIMARY KEY (`id`)
)

;

-- ----------------------------
-- Table structure for `events`
-- ----------------------------
CREATE TABLE `events` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  text NULL ,
`action`  text NULL ,
`who`  text NULL ,
`trigger`  text NULL ,
`trigger_args`  text NULL ,
`timeout`  text NULL ,
PRIMARY KEY (`id`)
)
AUTO_INCREMENT=1

;

-- ----------------------------
-- Table structure for `helper_processes`
-- ----------------------------
CREATE TABLE `helper_processes` (
`pid`  int(11) NOT NULL ,
`type`  text NULL ,
`info`  text NULL ,
PRIMARY KEY (`pid`)
)

;

-- ----------------------------
-- Table structure for `inputs`
-- ----------------------------
CREATE TABLE `inputs` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  text NULL ,
`pin`  int(11) NULL DEFAULT NULL ,
`type`  text NOT NULL ,
`type_args`  text NULL ,
PRIMARY KEY (`id`)
)
AUTO_INCREMENT=2

;

-- ----------------------------
-- Table structure for `outputs`
-- ----------------------------
CREATE TABLE `outputs` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  text NULL ,
`pin`  text NULL ,
PRIMARY KEY (`id`)
)
AUTO_INCREMENT=2

;

-- ----------------------------
-- Table structure for `pins`
-- ----------------------------
CREATE TABLE `pins` (
`pin`  int(11) NOT NULL DEFAULT 0 ,
`used`  int(11) NULL DEFAULT NULL ,
`direction`  text NULL ,
PRIMARY KEY (`pin`)
)

;

-- ----------------------------
-- Table structure for `security_cameras`
-- ----------------------------
CREATE TABLE `security_cameras` (
`video_device`  int(11) NOT NULL ,
`name`  text NULL ,
`server_address`  text NULL ,
`type`  text NULL ,
`address`  text NULL ,
`username`  text NULL ,
`password`  text NULL ,
PRIMARY KEY (`video_device`)
)

;

-- ----------------------------
-- Table structure for `security_zones`
-- ----------------------------
CREATE TABLE `security_zones` (
`pin`  int(11) NOT NULL ,
`name`  text NULL ,
PRIMARY KEY (`pin`)
)

;

-- ----------------------------
-- Table structure for `settings`
-- ----------------------------
CREATE TABLE `settings` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`field`  text NULL ,
`value`  text NULL ,
PRIMARY KEY (`id`)
)
AUTO_INCREMENT=7

;

-- ----------------------------
-- Table structure for `system_slaves`
-- ----------------------------
CREATE TABLE `system_slaves` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`name`  text NULL ,
`function`  text NULL ,
`address`  text NULL ,
PRIMARY KEY (`id`)
)
AUTO_INCREMENT=1

;

-- ----------------------------
-- Table structure for `temperature_records`
-- ----------------------------
CREATE TABLE `temperature_records` (
`id`  int(11) NOT NULL AUTO_INCREMENT ,
`pin`  int(11) NULL DEFAULT NULL ,
`temp`  int(11) NULL DEFAULT NULL ,
`date`  timestamp NULL DEFAULT NULL ,
PRIMARY KEY (`id`)
)
AUTO_INCREMENT=1

;

-- ----------------------------
-- Auto increment value for `events`
-- ----------------------------
ALTER TABLE `events` AUTO_INCREMENT=1;

-- ----------------------------
-- Auto increment value for `inputs`
-- ----------------------------
ALTER TABLE `inputs` AUTO_INCREMENT=2;

-- ----------------------------
-- Auto increment value for `outputs`
-- ----------------------------
ALTER TABLE `outputs` AUTO_INCREMENT=2;

-- ----------------------------
-- Auto increment value for `settings`
-- ----------------------------
ALTER TABLE `settings` AUTO_INCREMENT=7;

-- ----------------------------
-- Auto increment value for `system_slaves`
-- ----------------------------
ALTER TABLE `system_slaves` AUTO_INCREMENT=1;

-- ----------------------------
-- Auto increment value for `temperature_records`
-- ----------------------------
ALTER TABLE `temperature_records` AUTO_INCREMENT=1;
