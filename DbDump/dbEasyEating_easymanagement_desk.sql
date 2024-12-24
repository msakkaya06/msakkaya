CREATE DATABASE  IF NOT EXISTS `dbEasyEating` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dbEasyEating`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: dbEasyEating
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
-- Table structure for table `easymanagement_desk`
--

DROP TABLE IF EXISTS `easymanagement_desk`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `easymanagement_desk` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `isReserve` tinyint(1) NOT NULL,
  `isActive` tinyint(1) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `business_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `easymanagement_desk_business_id_c58b8493_fk_easymanag` (`business_id`),
  CONSTRAINT `easymanagement_desk_business_id_c58b8493_fk_easymanag` FOREIGN KEY (`business_id`) REFERENCES `easymanagement_business` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easymanagement_desk`
--

LOCK TABLES `easymanagement_desk` WRITE;
/*!40000 ALTER TABLE `easymanagement_desk` DISABLE KEYS */;
INSERT INTO `easymanagement_desk` VALUES (1,'Masa 1',0,1,'rosemarin-pizza-masa-1',1),(2,'Masa 2',0,1,'rosemarin-pizza-masa-2',1),(3,'Masa 3',0,1,'rosemarin-pizza-masa-3',1),(4,'Masa 4',0,1,'rosemarin-pizza-masa-4',1),(5,'Masa 5',0,1,'rosemarin-pizza-masa-5',1),(6,'Bahçe Masa 1',0,1,'rosemarin-pizza-bahce-masa-1',1),(7,'Bahçe Masa 2',0,1,'rosemarin-pizza-bahce-masa-2',1),(8,'Bahçe Masa 3',0,1,'rosemarin-pizza-bahce-masa-3',1),(9,'Masa 6',0,1,'rosemarin-pizza-masa-6',1),(10,'Masa 7',0,1,'rosemarin-pizza-masa-7',1),(11,'Masa 8',0,1,'rosemarin-pizza-masa-8',1),(12,'Masa 1',0,1,'ekin-kebap-masa-1',2),(13,'Masa 2',0,1,'ekin-kebap-masa-2',2),(14,'Masa 3',0,1,'ekin-kebap-masa-3',2),(15,'Masa 4',0,1,'ekin-kebap-masa-4',2),(16,'Masa 5',0,1,'ekin-kebap-masa-5',2),(17,'Masa 6',0,1,'ekin-kebap-masa-6',2),(18,'Masa 7',0,1,'ekin-kebap-masa-7',2),(19,'Masa 8',0,1,'ekin-kebap-masa-8',2),(20,'Masa 9',0,1,'ekin-kebap-masa-9',2),(21,'Masa 10',0,1,'ekin-kebap-masa-10',2);
/*!40000 ALTER TABLE `easymanagement_desk` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-24 12:37:08
