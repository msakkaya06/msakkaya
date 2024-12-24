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
-- Table structure for table `easymanagement_producetype`
--

DROP TABLE IF EXISTS `easymanagement_producetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `easymanagement_producetype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  `isActive` tinyint(1) NOT NULL,
  `slug` varchar(150) NOT NULL,
  `business_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `easymanagement_produ_business_id_61cd1795_fk_easymanag` (`business_id`),
  CONSTRAINT `easymanagement_produ_business_id_61cd1795_fk_easymanag` FOREIGN KEY (`business_id`) REFERENCES `easymanagement_business` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easymanagement_producetype`
--

LOCK TABLES `easymanagement_producetype` WRITE;
/*!40000 ALTER TABLE `easymanagement_producetype` DISABLE KEYS */;
INSERT INTO `easymanagement_producetype` VALUES (1,'Menüler',1,'rosemarin-pizza-menuler',1),(2,'Orta Boy Pizzalar',1,'rosemarin-pizza-orta-boy-pizzalar',1),(3,'Büyük Boy Pizzalar',1,'rosemarin-pizza-buyuk-boy-pizzalar',1),(4,'Yan Ürünler',1,'rosemarin-pizza-yan-urunler',1),(5,'Salatalar',1,'rosemarin-pizza-salatalar',1),(6,'Tatlılar',1,'rosemarin-pizza-tatllar',1),(7,'Çorbalar',1,'ekin-kebap-corbalar',2),(8,'Izgaralar',1,'ekin-kebap-izgaralar',2),(9,'Sulu Yemekler',1,'ekin-kebap-sulu-yemekler',2),(10,'Kebap/Döner',1,'ekin-kebap-kebapdoner',2),(11,'Pide/Lahmacun',1,'ekin-kebap-pidelahmacun',2),(12,'İçecekler',1,'ekin-kebap-icecekler',2);
/*!40000 ALTER TABLE `easymanagement_producetype` ENABLE KEYS */;
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
