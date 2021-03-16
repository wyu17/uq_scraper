-- MySQL dump 10.13  Distrib 5.7.33, for Linux (x86_64)
--
-- Host: localhost    Database: classes
-- ------------------------------------------------------
-- Server version	5.7.33-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `constraints`
--

DROP TABLE IF EXISTS `constraints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `constraints` (
  `dcode` varchar(255) NOT NULL,
  `constraintColumn` varchar(255) NOT NULL,
  PRIMARY KEY (`dcode`,`constraintColumn`),
  CONSTRAINT `constraints_ibfk_1` FOREIGN KEY (`dcode`) REFERENCES `degrees` (`dcode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses` (
  `code` varchar(8) NOT NULL,
  `title` varchar(255) NOT NULL,
  `units` int(2) NOT NULL,
  `sem1` tinyint(1) NOT NULL,
  `sem2` tinyint(1) NOT NULL,
  `summer` tinyint(1) NOT NULL,
  `prereq` text,
  `incomp` text,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `degreeopts`
--

DROP TABLE IF EXISTS `degreeopts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `degreeopts` (
  `dcode` varchar(255) NOT NULL,
  `majors` int(11) NOT NULL,
  `minors` int(11) NOT NULL,
  `emaj` int(11) NOT NULL,
  PRIMARY KEY (`dcode`,`majors`,`minors`,`emaj`),
  CONSTRAINT `degreeopts_ibfk_1` FOREIGN KEY (`dcode`) REFERENCES `degrees` (`dcode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `degrees`
--

DROP TABLE IF EXISTS `degrees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `degrees` (
  `dcode` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `unit` int(11) NOT NULL,
  `YEAR` int(4) DEFAULT '2021',
  `level` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`dcode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `includedDegrees`
--

DROP TABLE IF EXISTS `includedDegrees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `includedDegrees` (
  `dcode` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `unit` int(11) NOT NULL,
  `YEAR` int(4) DEFAULT '2021',
  `level` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`dcode`),
  CONSTRAINT `includedDegrees_ibfk_1` FOREIGN KEY (`dcode`) REFERENCES `degrees` (`dcode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `interX`
--

DROP TABLE IF EXISTS `interX`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interX` (
  `optionCode` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  PRIMARY KEY (`optionCode`,`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `majors`
--

DROP TABLE IF EXISTS `majors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `majors` (
  `dcode` varchar(255) NOT NULL,
  `mcode` varchar(255) NOT NULL,
  `type` enum('main','major','minor','eMajor') DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `units` int(11) DEFAULT '0',
  PRIMARY KEY (`dcode`,`mcode`),
  CONSTRAINT `majors_ibfk_1` FOREIGN KEY (`dcode`) REFERENCES `degrees` (`dcode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sectionCodes`
--

DROP TABLE IF EXISTS `sectionCodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sectionCodes` (
  `section` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `dcode` varchar(255) NOT NULL,
  `mcode` varchar(255) NOT NULL,
  `options` int(1) DEFAULT '0',
  PRIMARY KEY (`code`,`dcode`,`mcode`,`section`),
  KEY `dcode` (`dcode`,`mcode`,`section`),
  CONSTRAINT `sectionCodes_ibfk_1` FOREIGN KEY (`dcode`, `mcode`, `section`) REFERENCES `sections` (`dcode`, `mcode`, `section`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sections`
--

DROP TABLE IF EXISTS `sections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sections` (
  `dcode` varchar(255) NOT NULL,
  `mcode` varchar(255) NOT NULL,
  `section` varchar(255) NOT NULL,
  `min` int(11) NOT NULL,
  `max` int(11) NOT NULL,
  PRIMARY KEY (`dcode`,`mcode`,`section`),
  CONSTRAINT `sections_ibfk_1` FOREIGN KEY (`dcode`, `mcode`) REFERENCES `majors` (`dcode`, `mcode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
