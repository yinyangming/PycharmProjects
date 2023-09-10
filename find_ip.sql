/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 80031
Source Host           : localhost:3306
Source Database       : find_ip

Target Server Type    : MYSQL
Target Server Version : 80031
File Encoding         : 65001

Date: 2023-07-15 23:03:05
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ip_list
-- ----------------------------
DROP TABLE IF EXISTS `ip_list`;
CREATE TABLE `ip_list` (
  `ip` char(17) COLLATE utf8mb3_croatian_ci NOT NULL,
  `number` char(8) COLLATE utf8mb3_croatian_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_croatian_ci;

-- ----------------------------
-- Records of ip_list
-- ----------------------------
INSERT INTO `ip_list` VALUES ('180.101.50.188', '12');
INSERT INTO `ip_list` VALUES ('59.82.122.115', '13');
INSERT INTO `ip_list` VALUES ('111.255.55.244', '14');
INSERT INTO `ip_list` VALUES ('12.16.35.5', '15');
