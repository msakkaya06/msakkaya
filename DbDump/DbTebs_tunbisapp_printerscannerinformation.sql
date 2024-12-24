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
-- Table structure for table `tunbisapp_printerscannerinformation`
--

DROP TABLE IF EXISTS `tunbisapp_printerscannerinformation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tunbisapp_printerscannerinformation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `device_type` varchar(75) NOT NULL,
  `device_name` varchar(75) NOT NULL,
  `manufacturer` varchar(75) DEFAULT NULL,
  `model` varchar(75) DEFAULT NULL,
  `serial_number` varchar(75) DEFAULT NULL,
  `ip_address` varchar(15) DEFAULT NULL,
  `mac_address` varchar(17) DEFAULT NULL,
  `network_used` varchar(75) DEFAULT NULL,
  `color_mode` varchar(20) NOT NULL,
  `print_speed_ppm` int DEFAULT NULL,
  `scan_speed_ipm` int DEFAULT NULL,
  `max_resolution_dpi` int DEFAULT NULL,
  `duplex` tinyint(1) NOT NULL,
  `wireless_capability` tinyint(1) NOT NULL,
  `paper_capacity` int DEFAULT NULL,
  `toner_level` varchar(10) DEFAULT NULL,
  `drum_unit_life_remaining` varchar(10) DEFAULT NULL,
  `scan_unit_life_remaining` varchar(10) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_date` datetime(6) NOT NULL,
  `updated_date` datetime(6) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `unit_id` bigint DEFAULT NULL,
  `connection_interface` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tunbisapp_printersca_unit_id_c0b81046_fk_tunbisapp` (`unit_id`),
  CONSTRAINT `tunbisapp_printersca_unit_id_c0b81046_fk_tunbisapp` FOREIGN KEY (`unit_id`) REFERENCES `tunbisapp_unit` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tunbisapp_printerscannerinformation`
--

LOCK TABLES `tunbisapp_printerscannerinformation` WRITE;
/*!40000 ALTER TABLE `tunbisapp_printerscannerinformation` DISABLE KEYS */;
/*!40000 ALTER TABLE `tunbisapp_printerscannerinformation` ENABLE KEYS */;
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
