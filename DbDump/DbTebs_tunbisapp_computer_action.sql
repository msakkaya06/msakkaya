CREATE DATABASE  IF NOT EXISTS `DbTebs` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `DbTebs`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: DbTebs
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tunbisapp_computer_action`
--

DROP TABLE IF EXISTS `tunbisapp_computer_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tunbisapp_computer_action` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `part_installed` tinyint(1) NOT NULL,
  `os_installed` tinyint(1) NOT NULL,
  `other` tinyint(1) NOT NULL,
  `requester_date` datetime(6) NOT NULL,
  `completed_date` datetime(6) DEFAULT NULL,
  `action_notes` longtext NOT NULL,
  `computer_id` bigint NOT NULL,
  `performer_id` bigint DEFAULT NULL,
  `requester_id` bigint DEFAULT NULL,
  `requester_notes` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tunbisapp_computerac_computer_id_2f09ef07_fk_tunbisapp` (`computer_id`),
  KEY `tunbisapp_computerac_performer_id_8e828f8b_fk_tunbisapp` (`performer_id`),
  KEY `tunbisapp_computerac_requester_id_1361f99b_fk_tunbisapp` (`requester_id`),
  CONSTRAINT `tunbisapp_computerac_computer_id_2f09ef07_fk_tunbisapp` FOREIGN KEY (`computer_id`) REFERENCES `tunbisapp_computer_informations` (`id`),
  CONSTRAINT `tunbisapp_computerac_performer_id_8e828f8b_fk_tunbisapp` FOREIGN KEY (`performer_id`) REFERENCES `tunbisapp_tebsuser` (`id`),
  CONSTRAINT `tunbisapp_computerac_requester_id_1361f99b_fk_tunbisapp` FOREIGN KEY (`requester_id`) REFERENCES `tunbisapp_tebsuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tunbisapp_computer_action`
--

LOCK TABLES `tunbisapp_computer_action` WRITE;
/*!40000 ALTER TABLE `tunbisapp_computer_action` DISABLE KEYS */;
INSERT INTO `tunbisapp_computer_action` VALUES (1,0,1,0,'2024-12-20 12:30:53.700830','2024-12-20 12:31:11.768399','Format attık efem.',495,814,41,'Güncelleme aldım bilgisayar bir daha açılmadı.',0),(2,0,0,1,'2024-12-20 12:34:42.504346','2024-12-20 12:35:16.356625','Tabi yavaş olur efem kaç kere söyledim değiştirelim diye',343,814,23,'Bilgisayarım çok yavaş',0);
/*!40000 ALTER TABLE `tunbisapp_computer_action` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-24 12:37:10
