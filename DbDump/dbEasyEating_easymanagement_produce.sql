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
-- Table structure for table `easymanagement_produce`
--

DROP TABLE IF EXISTS `easymanagement_produce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `easymanagement_produce` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(75) NOT NULL,
  `price` decimal(11,2) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `description` longtext NOT NULL,
  `slug` varchar(50) NOT NULL,
  `produceType_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `easymanagement_produ_produceType_id_3a4247fc_fk_easymanag` (`produceType_id`),
  CONSTRAINT `easymanagement_produ_produceType_id_3a4247fc_fk_easymanag` FOREIGN KEY (`produceType_id`) REFERENCES `easymanagement_producetype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easymanagement_produce`
--

LOCK TABLES `easymanagement_produce` WRITE;
/*!40000 ALTER TABLE `easymanagement_produce` DISABLE KEYS */;
INSERT INTO `easymanagement_produce` VALUES (1,'Rosburger Menü',309.00,'img/rosburger.jpg','Rosburger (Ev yapımı burger ekmeğine; 120 gr. dana eti, domates, marul, özel köfte sosu) + Patates Kızartması + Kutu İçecek','rosburger-menu',1),(2,'Mantarlı Rosburger Menü',314.00,'img/mantarli_rosburger.jpg','Mantarlı Rosburger + Kutu İçecek','mantarl-rosburger-menu',1),(3,'Cheeseburger Menü',309.00,'img/cheeseburger.jpg','Cheeseburger + Patates Kızartması + Kutu İçecek','cheeseburger-menu',1),(4,'Çökertme Pizza (Orta Boy)',259.00,'img/cokertme_GkEL98g.jpg','Pizza sosu, mozzarella peyniri, dana eti, sarımsak, yoğurt, kibrit patates kızartması','cokertme-pizza-orta-boy',2),(5,'Mix Pizza (Orta Boy)',199.00,'img/miz_orta.jpg','Pizza sosu, sucuk, zeytin, mantar','mix-pizza-orta-boy',2),(6,'Ton Balıklı Pizza (Orta Boy)',249.00,'img/ton_balikli.jpg','Pizza sosu, mantar, kırmızıbiber, yeşil biber, yeşil zeytin, siyah zeytin, ton balığı, mısır','ton-balkl-pizza-orta-boy',2),(7,'Nirvana Pizza(Büyük Boy)',325.00,'img/nirvana.jpg','Sucuk, kırmızıbiber, yeşil biber, zeytin, kırmızı soğan, pizza sosu, mozzarella peyniri','nirvana-pizzabuyuk-boy',3),(8,'Beş Peynirli Pizza (Büyük Boy)',409.00,'img/bes_peynirli.jpg','5 çeşit özel Rosemarin peyniri','bes-peynirli-pizza-buyuk-boy',3),(10,'Parmak Patates Kızartması',125.00,'img/parmak_patates.jpg','Dilimlenmiş patateslerin kızartılarak servis edildiği bir atıştırmalıktır.','parmak-patates-kzartmas',4),(11,'Elma Dilim Patates Kızartması',129.90,'img/elma_dilim.jpg','Elma dilim patateslerin kızartılarak servis edildiği bir atıştırmalıktır.','elma-dilim-patates-kzartmas',4),(12,'Gerdan Çorbası',160.00,'img/gerdan.jpg','Kuzu gerdanından terbiyeli çorba','gerdan-corbas',7),(13,'Mercimek Çorbası',80.00,'img/mercimek_efllXm8.jpg','Süzülmüş mercimek çorbası','mercimek-corbas',7),(14,'Karışık Izgara',325.00,'img/karisik-kebap-1-830x604-1.jpg','Köfte, Adana, Tavuk Şiş, Tavuk Kanat, Bulgur/Pirinç Pilavı, Kuzu Pirzola, Salata','karsk-izgara',8),(15,'Et Döner',250.00,'img/et_doner.jpg','Et Döner, Pilav, Salata','et-doner',10),(16,'Et Haşlama',240.00,'img/et_haslama.jpg','Kuzu Etinden Haşlama','et-haslama',9),(17,'Kıymalı Pide',150.00,'img/kıymalı_pide.jpg','Kıymalı Pide','kymal-pide',11),(18,'Lahmacun',80.00,'img/lahmacun.jpg','Lahmacun','lahmacun',11),(19,'Kaşarlı Pide',150.00,'img/kasarlipide.jpg','Kaşarlı Pide','kasarl-pide',11),(20,'Kuşbaşılı Pide',185.00,'img/kusbasilipide.jpg','Kuşbaşılı Pide','kusbasl-pide',11),(21,'Adana Kebap',220.00,'img/adana-kebap-v2.jpg','Zırhta çekilmiş adana kebap','adana-kebap',8);
/*!40000 ALTER TABLE `easymanagement_produce` ENABLE KEYS */;
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
