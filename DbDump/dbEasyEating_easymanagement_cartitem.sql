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
-- Table structure for table `easymanagement_cartitem`
--

DROP TABLE IF EXISTS `easymanagement_cartitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `easymanagement_cartitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int NOT NULL,
  `isConfirm` tinyint(1) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `cart_id` bigint NOT NULL,
  `produce_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `easymanagement_carti_cart_id_9e2a2d29_fk_easymanag` (`cart_id`),
  KEY `easymanagement_carti_produce_id_4013a43b_fk_easymanag` (`produce_id`),
  CONSTRAINT `easymanagement_carti_cart_id_9e2a2d29_fk_easymanag` FOREIGN KEY (`cart_id`) REFERENCES `easymanagement_cart` (`id`),
  CONSTRAINT `easymanagement_carti_produce_id_4013a43b_fk_easymanag` FOREIGN KEY (`produce_id`) REFERENCES `easymanagement_produce` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easymanagement_cartitem`
--

LOCK TABLES `easymanagement_cartitem` WRITE;
/*!40000 ALTER TABLE `easymanagement_cartitem` DISABLE KEYS */;
INSERT INTO `easymanagement_cartitem` VALUES (1,1,1,309.00,1,1),(2,1,1,314.00,1,2),(3,1,1,259.00,2,4),(4,1,1,309.00,4,1),(5,1,1,259.00,4,4),(6,1,1,125.00,5,10),(7,1,1,325.00,5,7),(8,1,1,314.00,6,2),(9,2,1,314.00,7,2),(10,1,1,309.00,8,1),(11,1,1,259.00,8,4),(12,1,1,314.00,8,2),(13,1,1,309.00,8,1),(14,1,1,314.00,8,2),(15,1,1,309.00,8,1),(16,1,1,309.00,8,3),(17,1,1,309.00,8,1),(18,1,1,309.00,9,1),(19,1,1,314.00,9,2),(20,1,1,309.00,10,1),(21,1,1,314.00,10,2),(22,1,1,309.00,10,1),(23,1,1,314.00,10,2),(24,1,1,309.00,11,1),(25,1,1,309.00,12,1),(26,1,1,314.00,12,2),(27,1,1,199.00,13,5),(28,1,1,309.00,15,1),(29,1,1,314.00,15,2),(30,1,1,309.00,15,1),(31,1,1,314.00,15,2),(32,1,1,249.00,15,6),(33,1,1,325.00,15,7),(34,1,1,309.00,16,1),(35,1,1,259.00,16,4),(36,1,1,125.00,16,10),(37,1,1,314.00,17,2),(38,1,1,199.00,17,5),(39,1,1,325.00,18,7),(40,1,1,129.90,18,11),(41,1,1,314.00,19,2),(42,1,1,129.90,19,11),(43,1,1,309.00,20,1),(44,1,1,314.00,20,2),(45,1,1,309.00,21,1),(46,1,1,314.00,21,2),(47,1,1,325.00,22,14),(48,1,1,240.00,22,16),(49,2,1,160.00,22,12),(50,1,1,160.00,25,12),(51,1,1,250.00,25,15),(52,1,1,325.00,23,14),(53,1,1,80.00,23,13),(54,1,1,160.00,24,12),(55,1,1,220.00,24,21),(56,1,1,160.00,26,12),(57,2,1,325.00,26,14),(58,1,1,240.00,26,16),(59,1,1,220.00,26,21),(60,1,1,160.00,27,12),(61,1,1,150.00,27,17),(62,2,1,80.00,27,18),(63,1,1,160.00,36,12),(64,1,1,220.00,36,21),(65,1,1,309.00,39,3);
/*!40000 ALTER TABLE `easymanagement_cartitem` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-24 12:37:09
