DROP DATABASE IF EXISTS `mem2`;
CREATE DATABASE `mem2` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `mem2`;

DROP TABLE IF EXISTS `family`;
CREATE TABLE `family` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fam_id` int(11) NOT NULL,
  `mem_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `member`;
CREATE TABLE `member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `street` varchar(150) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(3) NOT NULL,
  `zip` varchar(10) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(150) NOT NULL,
  `dob` date NOT NULL,
  `level` varchar(20) NOT NULL,
  `reg_date` date NOT NULL,
  `exp_date` date NOT NULL,
  `fam` int(11) DEFAULT NULL,
  `benefactor` tinyint(4) NOT NULL DEFAULT '0',
  `email_code` varchar(50) DEFAULT NULL,
  `status` varchar(20) DEFAULT 'new',
  `pay_code` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `payment_log`;
CREATE TABLE `payment_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `members` varchar(45) DEFAULT NULL,
  `checkout_created_time` datetime DEFAULT NULL,
  `checkout_id` varchar(45) DEFAULT NULL,
  `order_id` varchar(45) DEFAULT NULL,
  `order_create_time` datetime DEFAULT NULL,
  `location_id` varchar(45) DEFAULT NULL,
  `state` varchar(20) DEFAULT NULL,
  `total_money` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `joad_registration`;
CREATE TABLE `joad_registration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mem_id` int(11) NOT NULL,
  `bow` varchar(20) DEFAULT NULL,
  `joad_indoor` int(11) DEFAULT 0,
  `joad_outdoor` int(11) DEFAULT 0,
  `usaa_member` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `mem_id_UNIQUE` (`mem_id` ASC)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `joad_session_registration`;
CREATE TABLE `mem2`.`joad_session_registration` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `mem_id` int(11) NOT NULL,
  `pay_status` varchar(20) DEFAULT NULL,
  `pay_code` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `joad_sessions`;
CREATE TABLE `mem2`.`joad_sessions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `start_date` DATE NULL,
  `state` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `start_date_UNIQUE` (`start_date` ASC));


DROP TABLE IF EXISTS `pin_shoot`;
CREATE TABLE `pin_shoot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `club` varchar(45) DEFAULT NULL,
  `category` varchar(20) DEFAULT NULL,
  `bow` varchar(45) DEFAULT NULL,
  `shoot_date` date DEFAULT NULL,
  `distance` int(11) DEFAULT NULL,
  `target` int(11) DEFAULT NULL,
  `star_achievement` int(11) DEFAULT NULL,
  `wpa_membership_number` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
