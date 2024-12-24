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
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_easymanagement_eeuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_easymanagement_eeuser_id` FOREIGN KEY (`user_id`) REFERENCES `easymanagement_eeuser` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2024-12-08 11:50:51.751646','1','Rosemarin Pizza',1,'[{\"added\": {}}]',6,1),(2,'2024-12-08 11:51:29.019156','3','rosemarin_pizza',1,'[{\"added\": {}}]',8,1),(3,'2024-12-08 12:18:13.067525','1','Menüler',1,'[{\"added\": {}}]',16,1),(4,'2024-12-08 12:18:20.994868','2','Orta Boy Pizzalar',1,'[{\"added\": {}}]',16,1),(5,'2024-12-08 12:18:24.849972','3','Büyük Boy Pizzalar',1,'[{\"added\": {}}]',16,1),(6,'2024-12-08 12:18:28.080885','4','Yan Ürünler',1,'[{\"added\": {}}]',16,1),(7,'2024-12-08 12:18:32.063222','5','Salatalar',1,'[{\"added\": {}}]',16,1),(8,'2024-12-08 12:18:51.635231','6','Tatlılar',1,'[{\"added\": {}}]',16,1),(9,'2024-12-17 08:59:53.178135','2','Ekin Kebap',1,'[{\"added\": {}}]',6,2),(10,'2024-12-17 09:01:24.583974','15','ekin-kebap',1,'[{\"added\": {}}]',8,2),(11,'2024-12-17 11:39:22.901226','7','Çorba',1,'[{\"added\": {}}]',16,2),(12,'2024-12-17 11:39:29.753316','7','Çorbalar',2,'[{\"changed\": {\"fields\": [\"Name\"]}}]',16,2),(13,'2024-12-17 11:39:44.851879','8','Izgaralar',1,'[{\"added\": {}}]',16,2),(14,'2024-12-17 11:39:58.653066','9','Sulu Yemekler',1,'[{\"added\": {}}]',16,2),(15,'2024-12-17 11:40:20.066790','10','Kebap/Döner',1,'[{\"added\": {}}]',16,2),(16,'2024-12-17 11:40:49.653219','11','Pide/Lahmacun',1,'[{\"added\": {}}]',16,2),(17,'2024-12-17 11:40:52.371368','10','Kebap/Döner',2,'[]',16,2),(18,'2024-12-17 11:40:54.360943','11','Pide/Lahmacun',2,'[]',16,2),(19,'2024-12-17 11:40:56.527455','10','Kebap/Döner',2,'[]',16,2),(20,'2024-12-17 11:43:45.015495','12','İçecekler',1,'[{\"added\": {}}]',16,2),(21,'2024-12-18 13:48:24.693604','4','rosemarin-pizza-masa-1',2,'[{\"changed\": {\"fields\": [\"Password\", \"Image\"]}}]',8,2);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
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
