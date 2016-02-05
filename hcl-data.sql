-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (i386)
--
-- Host: localhost    Database: hcl
-- ------------------------------------------------------
-- Server version       5.1.73

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
-- Table structure for table `dev-to-validation`
--

DROP TABLE IF EXISTS `dev-to-validation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dev-to-validation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `validation_id` int(11) NOT NULL,
  `device_id` int(11) NOT NULL,
  `driver_name` char(128) CHARACTER SET latin1 NOT NULL,
  `driver_ver` char(64) CHARACTER SET latin1 DEFAULT NULL,
  `is_work` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`,`validation_id`,`device_id`),
  KEY `validation_id` (`validation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dev-to-validation`
--

LOCK TABLES `dev-to-validation` WRITE;
/*!40000 ALTER TABLE `dev-to-validation` DISABLE KEYS */;
INSERT INTO `dev-to-validation` VALUES (1,1,1,'megaraid_sas','6.705.06.00-1',1),(2,2,25,'mpt2sas','unknown',1),(3,3,26,'megaraid_sas','06.803.01.00',1),(4,4,26,'megaraid_sas','06.803.01.00',1),(5,5,27,'megaraid_sas','06.803.01.00',1),(6,6,2,'mpt2sas','02.00.00.00',1),(7,7,3,'megaraid_sas','06.902.01.00',1),(8,8,28,'megaraid_sas','06.803.01.00',1),(9,9,29,'hpsa','3.4.2-4',1),(10,10,7,'hpsa','3.4.8-140',1),(11,11,7,'hpsa','3.4.8-140',1),(12,12,30,'hpvsa','1.2.12-110',1),(13,13,30,'hpvsa','1.2.12-110',1),(14,14,30,'hpvsa','1.2.12-110',1),(15,15,10,'hpsa','unknown',1),(16,16,12,'igb','unknown',1),(17,16,5,'ixgbe','unknown',1),(18,16,14,'mpt2sas','unknown',1),(19,17,12,'igb','unknown',1),(20,17,5,'ixgbe','unknown',1),(21,17,14,'mpt2sas','unknown',1),(22,18,18,'igb','unknown',1),(23,19,5,'ixgbe','3.15.1-k',1),(24,20,31,'igb','unknown',1),(25,21,31,'igb','unknown',1),(26,22,31,'igb','unknown',1),(27,23,6,'igb','5.0.5-k',1),(28,23,5,'ixgbe','3.15.1-k',1),(29,24,6,'igb','5.0.5-k',1),(30,24,5,'ixgbe','3.15.1-k',1),(31,24,32,'megaraid_sas','06.803.01.00-rh1',1),(32,25,22,'ixgbe','unknown',1),(33,25,23,'megaraid_sas','3.4.8-140',1),(34,26,22,'ixgbe','unknown',1),(35,26,23,'megaraid_sas','3.4.8-140',1),(36,27,18,'igb','unknown',1),(37,27,19,'unknown','unknown',1),(38,28,18,'igb','unknown',1),(39,28,19,'unknown','unknown',1);
/*!40000 ALTER TABLE `dev-to-validation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--
DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(128) CHARACTER SET latin1 NOT NULL,
  `type` char(64) CHARACTER SET latin1 NOT NULL DEFAULT '',
  `description` mediumtext CHARACTER SET latin1,
  `device_maker_id` int(11) NOT NULL,
  PRIMARY KEY (`device_maker_id`,`id`),
  UNIQUE KEY `name` (`name`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` VALUES (5,'Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection','nic',NULL,1),(6,'Intel Corporation I350 Gigabit Network Connection','nic',NULL,1),(12,'Intel Corporation I210 Gigabit Network Connection','nic',NULL,1),(15,'82599ES 10-Gigabit SFI/SFP+ Network','nic',NULL,1),(16,'I350 Gigabit Network Connection','nic',NULL,1),(18,'Intel i350 Dual port','nic',NULL,1),(22,'Ethernet Controller 10-Gigabit Intel X540-T1','nic',NULL,1),(31,'Intel 82580','nic',NULL,1),(1,'LSI 9260-8i SAS','raid',NULL,2),(2,'PERC RAID H200','raid',NULL,2),(3,'PERC RAID H330','raid',NULL,2),(4,'MegaRAID SAS-3 3108 [Invader]','raid',NULL,2),(7,'H224BR','raid',NULL,2),(14,'SAS2308 PCI-Express Fusion-MPT SAS-2','raid',NULL,2),(19,'LSI 2108 SAS2','raid',NULL,2),(20,'LSI Logic / Symbios Logic MegaRAID SAS 2108 [Liberator]','raid',NULL,2),(21,'LSI Logic / Symbios Logic MegaRAID SAS 2208 [Thunderbolt]','raid',NULL,2),(23,'LSI 3108 SAS','raid',NULL,2),(25,'LSI 9210-8i SAS','raid',NULL,2),(26,'LSI 9265-8i','raid',NULL,2),(27,'PERC RAID H310','raid',NULL,2),(28,'PERC RAID H710','raid',NULL,2),(32,'LSI Logic / Symbios Logic MegaRAID SAS3008 PCI-Express Fusion-MPT SAS-3','raid',NULL,2),(9,'Smart Array P400','raid',NULL,3),(10,'Smart Array P420i','raid',NULL,3),(11,'HP Smart Array P600','raid',NULL,3),(29,'HP Smart Array P220i','raid',NULL,3),(30,'HP Dynamic Smart Array B120i/B320 Controller','raid',NULL,3),(8,'Dual NC373i Multifunction Gigabit Network Adapters','nic',NULL,4);
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_maker`
--

DROP TABLE IF EXISTS `device_maker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_maker` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(128) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_maker`
--

LOCK TABLES `device_maker` WRITE;
/*!40000 ALTER TABLE `device_maker` DISABLE KEYS */;
INSERT INTO `device_maker` VALUES (1,'Intel'),(2,'LSI Logic / Symbios Logic'),(3,'HP'),(4,'Broadcom Corporation');
/*!40000 ALTER TABLE `device_maker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `releases`
--

DROP TABLE IF EXISTS `releases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `releases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(64) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `releases`
--

LOCK TABLES `releases` WRITE;
/*!40000 ALTER TABLE `releases` DISABLE KEYS */;
INSERT INTO `releases` VALUES (1,'MOS 7.0'),(2,'MOS 8.0'),(3,'MOS 6.1');
/*!40000 ALTER TABLE `releases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server`
--

DROP TABLE IF EXISTS `server`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_vendor_id` int(11) NOT NULL,
  `name` char(128) CHARACTER SET latin1 NOT NULL,
  `notes` mediumtext CHARACTER SET latin1,
  PRIMARY KEY (`id`,`server_vendor_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server`
--

LOCK TABLES `server` WRITE;
/*!40000 ALTER TABLE `server` DISABLE KEYS */;
INSERT INTO `server` VALUES (1,3,'c6105',NULL),(2,3,'c6220',NULL),(3,3,'c8220',NULL),(4,3,'m620',NULL),(5,3,'r210',NULL),(6,3,'r430',NULL),(7,3,'r720xd',NULL),(8,4,'bl460c-g8',NULL),(9,4,'bl460c-g9',NULL),(10,4,'dl320e-g8',NULL),(11,4,'dl360e-g8',NULL),(13,4,'ml350-g6',NULL),(14,2,'SuperServer-1018D-73MTF',NULL),(15,2,'SuperServer-5017R-MTF',NULL),(16,2,'SuperServer-5018R-WR',NULL),(17,2,'SuperServer-5037MR-H8TRF',NULL),(18,2,'SuperServer-6018R-WTR',NULL),(19,2,'SuperServer-6018U-TR4+',NULL),(20,2,'SuperServer-6048R-E1CR36N',NULL),(21,2,'X9DR3-F',NULL),(22,2,'X9DRW',NULL),(23,100,'fake server',NULL);
/*!40000 ALTER TABLE `server` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_vendor`
--

DROP TABLE IF EXISTS `server_vendor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_vendor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(128) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_vendor`
--

LOCK TABLES `server_vendor` WRITE;
/*!40000 ALTER TABLE `server_vendor` DISABLE KEYS */;
INSERT INTO `server_vendor` VALUES (3,'Dell'),(4,'HP'),(1,'Intel'),(5,'Noname'),(2,'Supermicro');
/*!40000 ALTER TABLE `server_vendor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `validation`
--

DROP TABLE IF EXISTS `validation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `validation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_id` int(11) NOT NULL,
  `release_id` int(11) NOT NULL,
  `val_date` datetime NOT NULL,
  `customized-bootstrap` int(11) NOT NULL,
  `notes` mediumtext CHARACTER SET latin1,
  PRIMARY KEY (`id`,`server_id`,`release_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `validation`
--

LOCK TABLES `validation` WRITE;
/*!40000 ALTER TABLE `validation` DISABLE KEYS */;
INSERT INTO `validation` VALUES (1,1,3,'2015-06-18 17:44:52',0,NULL),(2,2,3,'2014-10-01 17:44:52',0,NULL),(3,3,3,'2015-06-18 17:44:52',0,NULL),(4,3,1,'2015-11-25 19:24:12',0,NULL),(5,4,3,'2015-06-18 17:44:52',0,NULL),(6,5,1,'2015-10-01 17:44:52',0,NULL),(7,6,1,'2015-06-18 17:44:52',0,NULL),(8,7,1,'2015-03-01 17:44:52',0,NULL),(9,8,1,'2014-10-01 17:44:52',0,NULL),(10,9,1,'2015-06-18 17:44:52',0,NULL),(11,9,3,'2015-12-18 12:14:55',0,NULL),(12,10,1,'2015-06-18 17:44:52',0,NULL),(13,10,3,'2015-08-25 20:17:52',0,NULL),(14,11,1,'2015-06-18 17:44:52',0,NULL),(15,13,1,'2014-10-01 17:44:52',0,NULL),(16,14,1,'2015-07-01 11:24:52',0,NULL),(17,14,3,'2015-07-01 11:24:52',0,NULL),(18,15,1,'2015-07-01 11:24:52',0,NULL),(19,16,1,'2015-07-01 11:24:52',0,NULL),(20,17,1,'2015-07-01 11:24:52',0,NULL),(21,17,3,'2015-07-01 11:24:52',0,NULL),(22,17,2,'2015-07-01 11:24:52',0,NULL),(23,18,3,'2015-07-01 11:24:52',0,NULL),(24,19,1,'2015-07-01 11:24:52',0,NULL),(25,20,1,'2015-07-01 11:24:52',0,NULL),(26,20,3,'2015-07-01 11:24:52',0,NULL),(27,21,2,'2015-07-01 11:24:52',0,NULL),(28,22,3,'2015-07-01 11:24:52',0,NULL);
/*!40000 ALTER TABLE `validation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `vsr_id`
--

DROP TABLE IF EXISTS `vsr_id`;
/*!50001 DROP VIEW IF EXISTS `vsr_id`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `vsr_id` (
 `server_vendor_id` tinyint NOT NULL,
  `server_id` tinyint NOT NULL,
  `release_id` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `vsr_tex`
--

DROP TABLE IF EXISTS `vsr_tex`;
/*!50001 DROP VIEW IF EXISTS `vsr_tex`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `vsr_tex` (
 `vendor_name` tinyint NOT NULL,
  `server_name` tinyint NOT NULL,
  `release_name` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vsr_id`
--
/*!50001 DROP TABLE IF EXISTS `vsr_id`*/;
/*!50001 DROP VIEW IF EXISTS `vsr_id`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vsr_id` AS select `server`.`server_vendor_id` AS `server_vendor_id`,`validation`.`server_id` AS `server_id`,`validation`.`release_id` AS `release_id` from (`server` left join `validation` on((`validation`.`server_id` = `server`.`id`))) where ((`validation`.`server_id` is not null) or (`validation`.`release_id` is not null)) group by `validation`.`server_id`,`validation`.`release_id` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vsr_tex`
--

/*!50001 DROP TABLE IF EXISTS `vsr_tex`*/;
/*!50001 DROP VIEW IF EXISTS `vsr_tex`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vsr_tex` AS select `server_vendor`.`name` AS `vendor_name`,`server`.`name` AS `server_name`,`releases`.`name` AS `release_name` from (((`releases` join `server`) join `server_vendor`) join `vsr_id` on(((`vsr_id`.`server_vendor_id` = `server_vendor`.`id`) and (`vsr_id`.`server_id` = `server`.`id`) and (`vsr_id`.`release_id` = `releases`.`id`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-02-05 19:57:50
