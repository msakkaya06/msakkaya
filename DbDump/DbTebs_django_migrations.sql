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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-12-19 11:29:09.323954'),(2,'contenttypes','0002_remove_content_type_name','2024-12-19 11:29:09.683761'),(3,'auth','0001_initial','2024-12-19 11:29:11.203559'),(4,'auth','0002_alter_permission_name_max_length','2024-12-19 11:29:11.534947'),(5,'auth','0003_alter_user_email_max_length','2024-12-19 11:29:11.559611'),(6,'auth','0004_alter_user_username_opts','2024-12-19 11:29:11.579183'),(7,'auth','0005_alter_user_last_login_null','2024-12-19 11:29:11.599149'),(8,'auth','0006_require_contenttypes_0002','2024-12-19 11:29:11.626882'),(9,'auth','0007_alter_validators_add_error_messages','2024-12-19 11:29:11.648388'),(10,'auth','0008_alter_user_username_max_length','2024-12-19 11:29:11.665039'),(11,'auth','0009_alter_user_last_name_max_length','2024-12-19 11:29:11.680386'),(12,'auth','0010_alter_group_name_max_length','2024-12-19 11:29:11.720134'),(13,'auth','0011_update_proxy_permissions','2024-12-19 11:29:11.739176'),(14,'auth','0012_alter_user_first_name_max_length','2024-12-19 11:29:11.758321'),(15,'tunbisapp','0001_initial','2024-12-19 11:29:14.046666'),(16,'admin','0001_initial','2024-12-19 11:29:14.754163'),(17,'admin','0002_logentry_remove_auto_add','2024-12-19 11:29:14.781013'),(18,'admin','0003_logentry_add_action_flag_choices','2024-12-19 11:29:14.802377'),(19,'sessions','0001_initial','2024-12-19 11:29:14.982148'),(20,'tunbisapp','0002_computerinformations','2024-12-19 11:29:15.718711'),(21,'tunbisapp','0003_rename_computerinformations_computer_informations','2024-12-19 11:29:15.841952'),(22,'tunbisapp','0004_computer_informations_created_date_and_more','2024-12-19 11:29:16.248304'),(23,'tunbisapp','0005_computeraction','2024-12-19 11:29:17.516959'),(24,'tunbisapp','0006_rename_computeraction_computer_action','2024-12-19 11:29:17.628289'),(25,'tunbisapp','0007_rename_notes_computer_action_action_notes_and_more','2024-12-19 11:29:17.828678'),(26,'tunbisapp','0008_computer_action_is_active','2024-12-19 11:29:18.051892'),(27,'tunbisapp','0009_tebsgroup','2024-12-19 11:29:18.783179'),(28,'tunbisapp','0010_alter_tebsgroup_table','2024-12-19 11:29:18.874424'),(29,'tunbisapp','0011_tebsuser_force_password_change_and_more','2024-12-19 11:29:19.277316'),(30,'tunbisapp','0012_alter_tebsuser_security_question','2024-12-19 11:29:19.618421'),(31,'tunbisapp','0013_alter_tebsuser_last_login','2024-12-19 11:29:19.654952'),(32,'tunbisapp','0014_printerscannerinformation','2024-12-19 11:29:20.060383'),(33,'tunbisapp','0015_printerscannerinformation_connection_interface','2024-12-19 11:29:20.175871'),(34,'tunbisapp','0016_alter_printerscannerinformation_color_mode_and_more','2024-12-19 11:29:20.469276'),(35,'tunbisapp','0017_alter_tebsuser_birthday','2024-12-19 12:27:37.544135');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
