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
-- Table structure for table `tunbisapp_unit`
--

DROP TABLE IF EXISTS `tunbisapp_unit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tunbisapp_unit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` longtext NOT NULL,
  `parent_unit` int DEFAULT NULL,
  `super_unit` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tunbisapp_unit`
--

LOCK TABLES `tunbisapp_unit` WRITE;
/*!40000 ALTER TABLE `tunbisapp_unit` DISABLE KEYS */;
INSERT INTO `tunbisapp_unit` VALUES (1,'TUNCELİ',1,1,1),(2,'Özel Kalem Büro Amirliği',1,1,1),(3,'Trafik Tescil ve Denetleme Şube Müdürlüğü',1,1,1),(4,'Bilgi Teknolojileri ve Haberleşme Şube Müdürlüğü',1,1,1),(5,'Personel Şube Müdürlüğü',1,1,1),(6,'Asayiş Şube Müdürlüğü',1,1,1),(7,'Çevik Kuvvet Şube Müdürlüğü',1,1,1),(8,'TUNCELİ-PERTEK',1,1,1),(9,'Güvenlik Şube Müdürlüğü',1,1,1),(10,'İstihbarat Şube Müdürlüğü',1,1,1),(11,'Sosyal Hizmetler ve Sağlık Şube Müdürlüğü',1,1,1),(12,'Koruma Şube Müdürlüğü',1,1,1),(13,'TUNCELİ-OVACIK',1,1,1),(14,'Özel Harekat Şube Müdürlüğü',1,1,1),(15,'Bölge Trafik Denetleme Şube Müdürlüğü',1,1,1),(16,'TUNCELİ-NAZIMİYE',1,1,1),(17,'Kaçakçılık ve Organize Suçlarla Mücadele Şube Müdürlüğü',1,1,1),(18,'Belge Yönetimi ve Koordinasyon Şube Müdürlüğü',1,1,1),(19,'Çocuk Şube Müdürlüğü',1,1,1),(20,'TUNCELİ-ÇEMİŞGEZEK',1,1,1),(21,'Narkotik Suçlarla Mücadele Şube Müdürlüğü',1,1,1),(22,'Destek Hizmetleri ve İnşaat Emlak Şube Müdürlüğü',1,1,1),(23,'Tanık Koruma Büro Amirliği',1,1,1),(24,'Olay Yeri İnceleme Şube Müdürlüğü',1,1,1),(25,'TUNCELİ-PÜLÜMÜR',1,1,1),(26,'Siber Suçlarla Mücadele Şube Müdürlüğü',1,1,1),(27,'Polisevi Şube Müdürlüğü',1,1,1),(28,'Eğitim Şube Müdürlüğü',1,1,1),(29,'Hukuk İşleri ve Soruşturma Şube Müdürlüğü',1,1,1),(30,'Merkez Şehit Nahit Bulut Polis Merkezi Amirliği',1,1,1),(31,'TUNCELİ-HOZAT',1,1,1),(32,'Terörle Mücadele Şube Müdürlüğü',1,1,1),(33,'Silah ve Patlayıcı Maddeler Şube Müdürlüğü',1,1,1),(34,'TUNCELİ-MAZGİRT',1,1,1),(35,'Toplum Destekli Polislik Şube Müdürlüğü',1,1,1),(36,'Özel Güvenlik Şube Müdürlüğü',1,1,1),(37,'Göçmen Kaçakçılığıyla Mücadele ve Hudut Kapıları Şube Müdürlüğü',1,1,1),(38,'Spor Güvenliği Şube Müdürlüğü',1,1,1),(39,'Kolluk Gözetim Komisyonu İşlemleri Büro Amirliği',1,1,1),(40,'Medya - Halkla İlişkiler ve Protokol Şube Müdürlüğü',1,1,1),(41,'İnsansız Hava Araçları Büro Amirliği',1,1,1),(42,'Personel Emrinde',1,1,1);
/*!40000 ALTER TABLE `tunbisapp_unit` ENABLE KEYS */;
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
