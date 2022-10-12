-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema ImageDB
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `ImageDB` ;
CREATE SCHEMA IF NOT EXISTS `ImageDB` DEFAULT CHARACTER SET utf8 ;
USE `ImageDB` ;

-- -----------------------------------------------------
-- Table `ImageDB`.`Image`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ImageDB`.`Image`;

CREATE TABLE IF NOT EXISTS `ImageDB`.`Image` (
  `iid` INT NOT NULL AUTO_INCREMENT,
  `_key` VARCHAR(45) NOT NULL UNIQUE,
  `name` VARCHAR(45) NOT NULL,
  `location` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`iid`))
ENGINE = InnoDB ;

-- -----------------------------------------------------
-- Table `ImageDB`.`Stats`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ImageDB`.`Stats`;

CREATE TABLE IF NOT EXISTS `ImageDB`.`Stats` (
  `sid` INT NOT NULL AUTO_INCREMENT,
  `num_items` INT, -- number of items in chache
  `size_items` INT, -- total size of items in cache
  `num_requests` INT, -- number of requests served
  `num_hit` INT, -- number of hit
  `num_miss` INT, -- number of miss
  `_timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`sid`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `ImageDB`.`Config`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ImageDB`.`Config`;

CREATE TABLE IF NOT EXISTS `ImageDB`.`Config` (
  `cid` INT NOT NULL AUTO_INCREMENT,
  `capacity` INT NOT NULL,
  `replacement_policy` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`cid`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


-- -----------------------------------------------------
-- Data for table `ImageDB`.`Stats`
-- -----------------------------------------------------
START TRANSACTION;
USE `ImageDB`;
-- INSERT INTO `ImageDB`.`Image` (`_key`, `name`, `location`) VALUES ("key1", "img1.png", "/Users/images/img1");
INSERT INTO `ImageDB`.`Stats` (`num_items`, `size_items`, `num_requests`, `num_hit`, `num_miss`, `_timestamp`) VALUES (0, 0, 0, 0, 0, CURRENT_TIMESTAMP);
-- INSERT INTO `ImageDB`.`Config` (`capacity`, `replacement_policy`) VALUES (0, "Random");
COMMIT;