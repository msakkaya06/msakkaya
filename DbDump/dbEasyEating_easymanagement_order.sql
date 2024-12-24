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
-- Table structure for table `easymanagement_order`
--

DROP TABLE IF EXISTS `easymanagement_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `easymanagement_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `isActive` tinyint(1) NOT NULL,
  `status` varchar(20) NOT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  `desk_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `easymanagement_order_desk_id_f7518f2d_fk_easymanagement_desk_id` (`desk_id`),
  CONSTRAINT `easymanagement_order_desk_id_f7518f2d_fk_easymanagement_desk_id` FOREIGN KEY (`desk_id`) REFERENCES `easymanagement_desk` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easymanagement_order`
--

LOCK TABLES `easymanagement_order` WRITE;
/*!40000 ALTER TABLE `easymanagement_order` DISABLE KEYS */;
INSERT INTO `easymanagement_order` VALUES (1,'2024-12-08 15:47:28.324010',0,'completed',623.00,3),(2,'2024-12-08 15:51:42.046114',0,'completed',259.00,1),(3,'2024-12-08 16:02:48.472727',0,'completed',568.00,3),(4,'2024-12-08 17:09:47.982612',0,'completed',450.00,8),(5,'2024-12-08 17:13:04.787143',0,'completed',314.00,6),(6,'2024-12-08 18:00:17.948891',0,'completed',628.00,8),(7,'2024-12-10 17:48:56.238893',0,'completed',2432.00,1),(8,'2024-12-10 17:53:52.491556',0,'completed',623.00,2),(9,'2024-12-10 17:57:33.448896',0,'completed',1246.00,2),(10,'2024-12-10 18:07:26.951207',0,'completed',309.00,2),(11,'2024-12-12 09:48:02.899916',0,'completed',623.00,2),(12,'2024-12-12 09:50:17.322548',0,'completed',199.00,2),(13,'2024-12-12 12:22:11.497581',0,'completed',1820.00,4),(14,'2024-12-16 08:17:07.445134',0,'completed',693.00,1),(15,'2024-12-16 09:48:01.653607',0,'completed',513.00,4),(16,'2024-12-16 09:51:23.906399',0,'completed',454.90,6),(17,'2024-12-16 10:56:23.446797',0,'completed',443.90,1),(18,'2024-12-16 11:01:42.323734',0,'completed',623.00,11),(19,'2024-12-16 13:28:11.603955',0,'completed',623.00,11),(20,'2024-12-17 12:03:15.871308',0,'completed',885.00,12),(21,'2024-12-17 12:07:42.990726',0,'completed',410.00,14),(22,'2024-12-17 12:08:12.413246',0,'completed',405.00,12),(23,'2024-12-17 12:08:30.642776',0,'completed',380.00,13),(24,'2024-12-17 12:09:15.191959',0,'completed',1270.00,16),(25,'2024-12-17 12:09:46.724489',0,'completed',470.00,17),(26,'2024-12-19 08:31:15.027869',0,'completed',380.00,13),(27,'2024-12-19 09:02:57.220217',0,'completed',309.00,1);
/*!40000 ALTER TABLE `easymanagement_order` ENABLE KEYS */;
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
