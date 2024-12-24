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
-- Table structure for table `easymanagement_eeuser`
--

DROP TABLE IF EXISTS `easymanagement_eeuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `easymanagement_eeuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `is_manager` tinyint(1) NOT NULL,
  `is_desk` tinyint(1) NOT NULL,
  `business_id` bigint DEFAULT NULL,
  `token` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `easymanagement_eeuse_business_id_368b7a63_fk_easymanag` (`business_id`),
  CONSTRAINT `easymanagement_eeuse_business_id_368b7a63_fk_easymanag` FOREIGN KEY (`business_id`) REFERENCES `easymanagement_business` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `easymanagement_eeuser`
--

LOCK TABLES `easymanagement_eeuser` WRITE;
/*!40000 ALTER TABLE `easymanagement_eeuser` DISABLE KEYS */;
INSERT INTO `easymanagement_eeuser` VALUES (1,'pbkdf2_sha256$870000$9v7UuUW1ofzswyygTyeu6x$1bsiINmn1l6mBrvJGmuj8mh1nel3UeGU1S5BkmiDrsg=','2024-12-08 11:47:15.541374',1,'easy_admin','','','mserhata@gmail.com',1,1,'2024-12-08 11:43:43.774412','',0,0,NULL,NULL),(2,'pbkdf2_sha256$870000$9v7UuUW1ofzswyygTyeu6x$1bsiINmn1l6mBrvJGmuj8mh1nel3UeGU1S5BkmiDrsg=','2024-12-18 13:47:44.219136',1,'admin','','','msakkaya06@gmail.com',1,1,'2024-12-08 11:45:36.528359','',0,0,NULL,NULL),(3,'pbkdf2_sha256$870000$sNng0Gm0oA1dYpyokKRPOi$umjIlv07vqVU3ktGPO5dsTmY46V8r/8EXVr6Uh/XzEo=','2024-12-18 13:43:22.651930',0,'rosemarin_pizza','Rosemarin','Pizza','rosemarin@gmail.com',0,1,'2024-12-08 11:50:57.000000','img/rosemarin.jpg',1,0,1,NULL),(4,'pbkdf2_sha256$870000$U5C8YhPk9TBfaz9FydvBph$ti+cWU/D+q3Ap0I10ORs3z4GVTf5z+8bcAA/0cRxEak=','2024-12-19 09:02:46.136251',0,'rosemarin-pizza-masa-1','','','',0,1,'2024-12-08 12:11:22.000000','img/none_oTCF8aT.jpeg',0,1,1,'cm9zZW1hcmluLXBpenphLW1hc2EtMTo4NWYxZGNjNC0yMDY3LTRjOGUtOGZiMC0yOWJlYTc4YWI3NzE='),(5,'pbkdf2_sha256$870000$xpk9IuQITyvmxMlbXp2bk2$8cMh2SGVbfVtRKuetKokna0s/CUh4Af44uhQLadGBGA=','2024-12-12 09:50:08.718611',0,'rosemarin-pizza-masa-2','','','',0,1,'2024-12-08 12:11:32.469970','',0,1,1,'cm9zZW1hcmluLXBpenphLW1hc2EtMjo2NmE3ZDZjMi1jMGRkLTRhOTQtOTg1ZC02NDljZWEzMDEyZWY='),(6,'pbkdf2_sha256$870000$T0I8gRvq1TU8mVXMPeJ7ux$ZSXENyLV6hkSEkOf71gzc2ykC61tQn3Yl2ygzNb5N0g=','2024-12-08 16:01:01.934477',0,'rosemarin-pizza-masa-3','','','',0,1,'2024-12-08 12:11:39.296104','',0,1,1,'cm9zZW1hcmluLXBpenphLW1hc2EtMzo3ZWYzNjFmYi01YmIzLTQzNmQtYTQ3YS05ZDVjOWM3MmMxYmM='),(7,'pbkdf2_sha256$870000$HcQFhWkbX0c5HHlOLRg5og$wUWDfYRHBecC+j2n2rjobE7aeuR5kDrenrzCFy03jlk=','2024-12-16 09:47:52.215190',0,'rosemarin-pizza-masa-4','','','',0,1,'2024-12-08 12:17:16.645762','',0,1,1,'cm9zZW1hcmluLXBpenphLW1hc2EtNDo4NjRlZTY1Yy1jYzMwLTQ1NmQtOTY2Mi0yMDQ4NzJkYTVmNGE='),(8,'pbkdf2_sha256$870000$WzrXgwP9N2PoYk55Is7V59$fV8t6NDnGUtkTaQbCSGXbYD+3ULYQnYZ3yVA9i5i6H0=','2024-12-12 12:19:16.577627',0,'rosemarin-pizza-masa-5','','','',0,1,'2024-12-08 12:17:24.686909','',0,1,1,'cm9zZW1hcmluLXBpenphLW1hc2EtNTozMTJlNmExYi1kYzc4LTRjM2UtOWVhOS04NWIyOGU1ZGY4ZmQ='),(9,'pbkdf2_sha256$870000$R2ws23F4Y0u4B6FFkdwxvu$edH/idOh0/HfQqwrxBBpmaYRYg4nl5KYj6vOnkRQDuA=','2024-12-16 09:51:12.737300',0,'rosemarin-pizza-bahce-masa-1','','','',0,1,'2024-12-08 12:17:35.786719','',0,1,1,'cm9zZW1hcmluLXBpenphLWJhaGNlLW1hc2EtMToxMDA4Y2U2Ni1hODkwLTQwOGMtYWJkZC00ZGY1YjQ4M2Y0YmQ='),(10,'pbkdf2_sha256$870000$gHrNjD1vl4KkaHULK6tzHI$nbxWfo8k9gQUA2G3bkeq6nx/6jWLf3Cw2r7R7OuBoqU=',NULL,0,'rosemarin-pizza-bahce-masa-2','','','',0,1,'2024-12-08 12:17:44.701104','',0,1,1,'cm9zZW1hcmluLXBpenphLWJhaGNlLW1hc2EtMjpiODM0YjAzYy0xMmY5LTRmZmEtOGEyZC0zYTEzZWMwMDNlNGY='),(11,'pbkdf2_sha256$870000$To6qdK6SaQTaPqTAdBUqyx$YTp5RkSmGmE9BoJBeBDBRAo/e1vU2dnnIChwD9ZOFGk=','2024-12-08 18:00:12.169390',0,'rosemarin-pizza-bahce-masa-3','','','',0,1,'2024-12-08 12:17:52.995980','',0,1,1,'cm9zZW1hcmluLXBpenphLWJhaGNlLW1hc2EtMzplNzRjYzg0Yi1iNmZjLTRjMTYtODc0Yi03ZmUyMmRjOWI3ZGI='),(12,'pbkdf2_sha256$870000$zLTj0Umfqv0dvJPMw7IpW8$heTxU8F3qSWFcmDrsmYZPJ8M2I45WZXkQ9dV7rvQ0uM=',NULL,0,'rosemarin-pizza-masa-6','','','',0,1,'2024-12-10 17:59:22.450050','',0,1,1,'cm9zZW1hcmluLXBpenphLW1hc2EtNjo4NzFlOTVkYi1lNGI4LTQ3YjQtYjAyMS0xY2EyNjRkMmZhODc='),(13,'pbkdf2_sha256$870000$PFsBvKSj8xLTGC2raymhfY$R+ii5ROGs5DCtk/Q9I8vGCMvaB5k65aW5AttMeREock=',NULL,0,'rosemarin-pizza-masa-7','','','',0,1,'2024-12-10 18:06:46.687801','',0,1,1,'cm9zZW1hcmluLXBpenphLW1hc2EtNzpmNmY3NTAxMy01YTY0LTRiYTQtOWIxNi1jMTQ1YmZkODExMjA='),(14,'pbkdf2_sha256$870000$ck24b4VpuFDwTA8uAioO2I$UCqrtCeDDITfxvJGw4LUXx44P21z8ky/nxiRt/XAkgU=','2024-12-16 13:28:01.961365',0,'rosemarin-pizza-masa-8','','','',0,1,'2024-12-16 09:53:28.717385','',0,1,1,'cm9zZW1hcmluLXBpenphLW1hc2EtODo4MWJhMjAxYS0zZmRlLTRkZWQtOWZmMi03NzYyZGRlYjczNDA='),(15,'pbkdf2_sha256$870000$i9Wvl8Qz5Bg6nW7nfOP5Vr$kwdPUfE6u+hf0dJBCnLWcV5yIVoLgtUxT5cSRvEj2VQ=','2024-12-19 08:24:49.447516',0,'ekin-kebap','Ekin','Kebap','ekin62@gmail.com',0,1,'2024-12-17 09:00:08.000000','img/ekin-kebap.jpg',1,0,2,NULL),(16,'pbkdf2_sha256$870000$4Xu8YA7O5At4PHHgaGL5Uv$mYz+RsYhWovAOESRZ+0t/PjBDgR9IQ5CI8LDZbrL3Io=','2024-12-19 08:57:29.075259',0,'ekin-kebap-masa-1','','','',0,1,'2024-12-17 09:02:04.693086','',0,1,2,'ZWtpbi1rZWJhcC1tYXNhLTE6MWI4NmE3YmUtMWI1OC00NDE2LTg0OTktY2Y5MjM2MTY4MDVk'),(17,'pbkdf2_sha256$870000$BIAaw0biFe5dAxfQuxhhly$+8CTpBbvm4Oe3xtKKImOhElnvaOIV9HrPHqE+X79hkA=','2024-12-19 08:30:59.959902',0,'ekin-kebap-masa-2','','','',0,1,'2024-12-17 09:02:09.779265','',0,1,2,'ZWtpbi1rZWJhcC1tYXNhLTI6YWJjMmYyNTktOWNhNC00NjEwLTg5OGItNzc3ZWU2ZGRhMmQ2'),(18,'pbkdf2_sha256$870000$ZiL1vsvQUk1hE2aKMNRczx$EbkJc/t+gVQ2yIpSDLt/ZVmyMQeod8GqzcmXD9K6qD4=','2024-12-17 12:05:13.792967',0,'ekin-kebap-masa-3','','','',0,1,'2024-12-17 09:02:14.594086','',0,1,2,'ZWtpbi1rZWJhcC1tYXNhLTM6MTg0NGVjY2ItZjA1Yy00YTE4LTllNDktOGU4ZGRlNjMyZjIw'),(19,'pbkdf2_sha256$870000$jKfQqqwFUrwxZxMjUX48Vc$E3ff3CyLYMktyAalwhrfHiSlJehoTyjGISRUge+O1Ek=',NULL,0,'ekin-kebap-masa-4','','','',0,1,'2024-12-17 09:02:18.972463','',0,1,2,'ZWtpbi1rZWJhcC1tYXNhLTQ6MjIzZWZkZjItOWE1Zi00M2Q5LWI3ZjEtOTlkMTI3ZDEyZWY5'),(20,'pbkdf2_sha256$870000$lwg1SDI2rVRBfQ6eHmTGn6$pBMKHd8dFfX7w6+P5RqfAyXRkyQ0e9aqe6YmsKBts9I=','2024-12-17 12:06:38.485810',0,'ekin-kebap-masa-5','','','',0,1,'2024-12-17 09:02:24.456192','',0,1,2,'ZWtpbi1rZWJhcC1tYXNhLTU6ZWEzNzg5MzMtMGRmNy00NjFlLTg5MmEtYTZhODUyNmMwYWZm'),(21,'pbkdf2_sha256$870000$bNxpbungCaVNIdrtbk8Vae$j9ujuVaGhvTmwGnodArUqmZ+hz/eG/TZ6tQcDz6ceoA=','2024-12-17 12:07:18.493102',0,'ekin-kebap-masa-6','','','',0,1,'2024-12-17 09:02:28.574006','',0,1,2,'ZWtpbi1rZWJhcC1tYXNhLTY6NzkxMjIyZjYtMWNmNC00ZGJiLTljZWQtOTg2ODgyYWNlOTk4'),(22,'pbkdf2_sha256$870000$p8txLDkN0DnbfSMzUcHwfQ$0tgTk0w9fo346J4seJlk6JC2koc2WABtJw+JrLEY0KM=',NULL,0,'ekin-kebap-masa-7','','','',0,1,'2024-12-17 09:02:33.675871','',0,1,2,'ZWtpbi1rZWJhcC1tYXNhLTc6NzUwYjEwNTctOTU3OC00ZDc5LWE1NWUtNTA2ZGVjMTExMWZm'),(23,'pbkdf2_sha256$870000$juNH2gs28sPa4CcCp7RN4t$v9Rh2FaUpSp2sACdgKDdHCW9LiT2O7mNaRYTyhd3/aE=',NULL,0,'ekin-kebap-masa-8','','','',0,1,'2024-12-17 09:02:38.092634','',0,1,2,'ZWtpbi1rZWJhcC1tYXNhLTg6YjMxY2VlNjQtN2FhMC00ZGNmLWE4NTUtZWU4NGQ2OGFlNTAy'),(24,'pbkdf2_sha256$870000$L2oEBWI8EfEz3jZ5FZQXG8$wkRiWaP0HxH1S35/XxyRq9jyzix54BpTVQMaOE5WrpY=',NULL,0,'ekin-kebap-masa-9','','','',0,1,'2024-12-17 09:02:42.624093','',0,1,2,'ZWtpbi1rZWJhcC1tYXNhLTk6ZjRiNDIwN2EtZjQ4Ny00MGUwLThkYTAtNWEwODljOWY4ZTYx'),(25,'pbkdf2_sha256$870000$9VyjjWoWR4kMvORzAudSrG$L0BMkhtlxQgwU3HU/c0LxGu6rnBdvheV7oc3qzqP0Ag=',NULL,0,'ekin-kebap-masa-10','','','',0,1,'2024-12-17 09:02:51.369085','',0,1,2,'ZWtpbi1rZWJhcC1tYXNhLTEwOjE3ZmFhYTRiLTkwMWEtNDdhNC05YzU2LTk4Y2NhY2JjMjg0OA==');
/*!40000 ALTER TABLE `easymanagement_eeuser` ENABLE KEYS */;
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
