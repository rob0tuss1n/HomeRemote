/*
Navicat MySQL Data Transfer

Source Server         : RPi Automation
Source Server Version : 50531
Source Host           : 192.168.1.68:3306
Source Database       : automation

Target Server Type    : MYSQL
Target Server Version : 50531
File Encoding         : 65001

Date: 2013-07-14 13:37:27
*/
CREATE DATABASE automation;
GRANT ALL PRIVILEGES ON automation.* TO 'automation'@'127.0.0.1' IDENTIFIED BY '6bc878bfcefbf5cdf88db13c76901135';
GRANT ALL PRIVILEGES ON automation.* TO 'automation'@'localhost' IDENTIFIED BY '6bc878bfcefbf5cdf88db13c76901135';
USE automation;

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `accounts`
-- ----------------------------
DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `name` text,
  `username` text,
  `password` text,
  `sid` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for `events`
-- ----------------------------
DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `action` text,
  `who` text,
  `trigger` text,
  `trigger_args` text,
  `timeout` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of events
-- ----------------------------

-- ----------------------------
-- Table structure for `helper_processes`
-- ----------------------------
DROP TABLE IF EXISTS `helper_processes`;
CREATE TABLE `helper_processes` (
  `pid` int(11) NOT NULL,
  `type` text,
  `info` text,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of helper_processes
-- ----------------------------

-- ----------------------------
-- Table structure for `inputs`
-- ----------------------------
DROP TABLE IF EXISTS `inputs`;
CREATE TABLE `inputs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `pin` int(11) DEFAULT NULL,
  `type` text NOT NULL,
  `type_args` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of inputs
-- ----------------------------

-- ----------------------------
-- Table structure for `outputs`
-- ----------------------------
DROP TABLE IF EXISTS `outputs`;
CREATE TABLE `outputs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `pin` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of outputs
-- ----------------------------

-- ----------------------------
-- Table structure for `pins`
-- ----------------------------
DROP TABLE IF EXISTS `pins`;
CREATE TABLE `pins` (
  `pin` int(11) NOT NULL DEFAULT '0',
  `used` int(11) DEFAULT NULL,
  `direction` text,
  PRIMARY KEY (`pin`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of pins
-- ----------------------------
INSERT INTO `pins` VALUES ('9', '1', 'out');
INSERT INTO `pins` VALUES ('14', '1', 'out');
INSERT INTO `pins` VALUES ('15', '1', 'out');
INSERT INTO `pins` VALUES ('17', '1', 'out');
INSERT INTO `pins` VALUES ('18', '1', 'in');
INSERT INTO `pins` VALUES ('22', '1', 'out');
INSERT INTO `pins` VALUES ('23', '1', 'out');
INSERT INTO `pins` VALUES ('24', '1', 'out');
INSERT INTO `pins` VALUES ('25', '1', 'out');

-- ----------------------------
-- Table structure for `security_cameras`
-- ----------------------------
DROP TABLE IF EXISTS `security_cameras`;
CREATE TABLE `security_cameras` (
  `video_device` int(11) NOT NULL,
  `name` text,
  `server_address` text,
  `type` text,
  `address` text,
  `username` text,
  `password` text,
  PRIMARY KEY (`video_device`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of security_cameras
-- ----------------------------

-- ----------------------------
-- Table structure for `security_zones`
-- ----------------------------
DROP TABLE IF EXISTS `security_zones`;
CREATE TABLE `security_zones` (
  `pin` int(11) NOT NULL,
  `name` text,
  PRIMARY KEY (`pin`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of security_zones
-- ----------------------------

-- ----------------------------
-- Table structure for `settings`
-- ----------------------------
DROP TABLE IF EXISTS `settings`;
CREATE TABLE `settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field` text,
  `value` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of settings
-- ----------------------------
INSERT INTO `settings` VALUES ('1', 'city_id', null);
INSERT INTO `settings` VALUES ('2', 'alarm timeout', '30');
INSERT INTO `settings` VALUES ('3', 'motion_server', null);
INSERT INTO `settings` VALUES ('6', 'temp_interval', '60');

-- ----------------------------
-- Table structure for `system_slaves`
-- ----------------------------
DROP TABLE IF EXISTS `system_slaves`;
CREATE TABLE `system_slaves` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `function` text,
  `address` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of system_slaves
-- ----------------------------

-- ----------------------------
-- Table structure for `temperature_records`
-- ----------------------------
DROP TABLE IF EXISTS `temperature_records`;
CREATE TABLE `temperature_records` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pin` int(11) DEFAULT NULL,
  `temp` int(11) DEFAULT NULL,
  `date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of temperature_records
-- ----------------------------
