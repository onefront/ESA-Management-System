-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: esa_db
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('aeca6b1659c3');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `message` text NOT NULL,
  `is_pinned` tinyint(1) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `attachment` varchar(255) DEFAULT NULL,
  `attachment_name` varchar(255) DEFAULT NULL,
  `attachment_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attachments`
--

DROP TABLE IF EXISTS `attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attachments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message_id` int NOT NULL,
  `filename` varchar(255) NOT NULL,
  `filepath` varchar(500) NOT NULL,
  `filetype` varchar(255) DEFAULT NULL,
  `filesize` int DEFAULT NULL,
  `uploaded_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `message_id` (`message_id`),
  CONSTRAINT `attachments_ibfk_1` FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attachments`
--

LOCK TABLES `attachments` WRITE;
/*!40000 ALTER TABLE `attachments` DISABLE KEYS */;
INSERT INTO `attachments` VALUES (1,11,'20260719_094629.jpg','uploads/messages/20260719_094629.jpg','image/jpeg',3466933,'2026-07-23 09:12:54'),(2,13,'20260719_094629.jpg','uploads/messages/20260719_094629.jpg','image/jpeg',3466933,'2026-07-23 09:19:41'),(3,15,'ite_level_300_weekend.xlsx','uploads/messages/ite_level_300_weekend.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',9745,'2026-07-23 09:26:12'),(4,16,'WhatsApp_Installer_14.exe','uploads/messages/WhatsApp_Installer_14.exe','application/x-msdownload',1438752,'2026-07-23 10:29:43');
/*!40000 ALTER TABLE `attachments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `attendance_code` varchar(20) DEFAULT NULL,
  `member_id` int NOT NULL,
  `event_id` int NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `attendance_date` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `attendance_code` (`attendance_code`),
  KEY `member_id` (`member_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`),
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(100) NOT NULL,
  `action` varchar(255) NOT NULL,
  `action_time` datetime DEFAULT NULL,
  `module` varchar(100) NOT NULL DEFAULT 'System',
  `description` text,
  `ip_address` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
INSERT INTO `audit_logs` VALUES (1,'System Administrator','Opened Voting','2026-07-14 19:39:54','System',NULL,NULL),(2,'System Administrator','Paused Voting','2026-07-14 19:39:56','System',NULL,NULL),(3,'System Administrator','Closed Voting','2026-07-14 19:39:58','System',NULL,NULL),(4,'System Administrator','Published Results','2026-07-14 19:45:53','System',NULL,NULL),(5,'System Administrator','Opened Voting','2026-07-14 19:46:02','System',NULL,NULL),(6,'System Administrator','Opened Voting','2026-07-14 19:46:04','System',NULL,NULL),(7,'System Administrator','Opened Voting','2026-07-14 19:53:22','System',NULL,NULL),(8,'System Administrator','Paused Voting','2026-07-14 19:53:25','System',NULL,NULL),(9,'System Administrator','Closed Voting','2026-07-14 19:53:27','System',NULL,NULL),(10,'System Administrator','Opened Voting','2026-07-15 21:50:44','System',NULL,NULL),(11,'System Administrator','Published Results','2026-07-15 23:01:40','System',NULL,NULL),(12,'System Administrator','Added Member','2026-07-16 19:07:33','Members','ESA-2026-0019','127.0.0.1'),(13,'System Administrator','Created Event','2026-07-16 21:21:41','Events','playing','127.0.0.1'),(14,'System Administrator','Added Lecturer','2026-07-16 21:48:48','Lecturer Directory','Dr. Samuel  Akpatsa','127.0.0.1'),(15,'System Administrator','Updated Lecturer','2026-07-16 22:28:51','Lecturer Directory','Dr. Samuel  Akpatsa','127.0.0.1'),(16,'System Administrator','Updated Lecturer','2026-07-16 22:41:32','Lecturer Directory','Dr. Samuel  Akpatsa','127.0.0.1'),(17,'System Administrator','Added Lecturer','2026-07-16 22:45:16','Lecturer Directory','manu','127.0.0.1'),(18,'System Administrator','Appointed Assistant Course Rep','2026-07-17 09:02:37','Course Representatives','freda abu','127.0.0.1'),(19,'System Administrator','Removed Course Representative','2026-07-17 09:02:51','Course Representatives','freda abu','127.0.0.1'),(20,'System Administrator','Added Member','2026-07-17 09:43:16','Members','ESA-2026-0020','127.0.0.1'),(21,'System Administrator','Reset Password','2026-07-17 11:51:36','Members','ESA-2026-0020','127.0.0.1'),(22,'System Administrator','Published Results','2026-07-17 11:59:10','System',NULL,NULL),(23,'System Administrator','Added Member','2026-07-17 12:44:59','Members','ESA-2026-0021','127.0.0.1'),(24,'System Administrator','Appointed Assistant Course Rep','2026-07-17 12:53:33','Course Representatives','ametus yaw','127.0.0.1'),(25,'System Administrator','Removed Course Representative','2026-07-17 13:04:12','Course Representatives','Owusu Issah','127.0.0.1'),(26,'System Administrator','Removed Course Representative','2026-07-17 13:04:16','Course Representatives','ametus yaw','127.0.0.1'),(27,'System Administrator','Appointed Assistant Course Rep','2026-07-17 13:43:57','Course Representatives','ametus yaw','127.0.0.1'),(28,'System Administrator','Created Notice','2026-07-18 09:04:41','Notice Board','SRC week','127.0.0.1'),(29,'System Administrator','Created Notice','2026-07-18 09:30:16','Notice Board','SRC','127.0.0.1'),(30,'System Administrator','Added Member','2026-07-19 09:52:14','Members','ESA-2026-0022','127.0.0.1'),(31,'System Administrator','Removed Course Representative','2026-07-19 09:55:40','Course Representatives','ametus yaw','127.0.0.1'),(32,'System Administrator','Appointed Assistant Course Rep','2026-07-19 09:56:06','Course Representatives','Aayere Yaw Ametus','127.0.0.1'),(33,'System Administrator','Added Member','2026-07-19 10:00:10','Members','ESA-2026-0024','127.0.0.1'),(34,'System Administrator','Deleted Lecturer','2026-07-20 09:52:17','Lecturer Directory','manu','127.0.0.1'),(35,'System Administrator','Removed Course Representative','2026-07-20 12:36:02','Course Representatives','Aayere Yaw Ametus','127.0.0.1'),(36,'System Administrator','Appointed Assistant Course Rep','2026-07-20 12:42:53','Course Representatives','Aayere Yaw Ametus','127.0.0.1'),(37,'System Administrator','Appointed Course Rep','2026-07-20 13:07:06','Course Representatives','Owusu Issah','127.0.0.1'),(38,'System Administrator','Removed Course Representative','2026-07-20 13:34:54','Course Representatives','Aayere Yaw Ametus','127.0.0.1'),(39,'System Administrator','Appointed Assistant Course Rep','2026-07-20 17:14:20','Course Representatives','Yaw Ametus','127.0.0.1'),(40,'System Administrator','Removed Course Representative','2026-07-21 00:15:08','Course Representatives','Yaw Ametus','127.0.0.1'),(41,'System Administrator','Removed Course Representative','2026-07-21 00:15:18','Course Representatives','Owusu Issah','127.0.0.1'),(42,'System Administrator','Appointed Course Rep','2026-07-21 00:15:28','Course Representatives','Owusu Issah','127.0.0.1'),(43,'System Administrator','Appointed Assistant Course Rep','2026-07-21 00:15:39','Course Representatives','Yaw Ametus','127.0.0.1'),(44,'System Administrator','Removed Course Representative','2026-07-21 07:53:30','Course Representatives','Yaw Ametus','127.0.0.1'),(45,'System Administrator','Appointed Assistant Course Rep','2026-07-21 07:53:40','Course Representatives','Yaw Ametus','127.0.0.1'),(46,'System Administrator','Removed Course Representative','2026-07-21 11:22:23','Course Representatives','Owusu Issah','127.0.0.1'),(47,'System Administrator','Appointed Course Rep','2026-07-21 11:22:38','Course Representatives','ass rep','127.0.0.1'),(48,'System Administrator','Opened Voting','2026-07-21 19:56:24','System',NULL,NULL),(49,'System Administrator','Published Results','2026-07-21 19:56:27','System',NULL,NULL),(50,'System Administrator','Closed Voting','2026-07-21 23:33:49','System',NULL,NULL),(51,'System Administrator','Opened Voting','2026-07-22 18:16:54','System',NULL,NULL),(52,'System Administrator','Published Results','2026-07-22 18:16:56','System',NULL,NULL),(53,'System Administrator','Opened Voting','2026-07-22 18:25:03','System',NULL,NULL),(54,'System Administrator','Reset Election','2026-07-22 18:46:30','System',NULL,NULL),(55,'System Administrator','Opened Voting','2026-07-22 18:48:10','System',NULL,NULL),(56,'System Administrator','Published Results','2026-07-22 18:48:13','System',NULL,NULL),(57,'System Administrator','Closed Voting','2026-07-22 19:37:33','System',NULL,NULL),(58,'System Administrator','Reset Election','2026-07-22 19:37:37','System',NULL,NULL),(59,'System Administrator','Reset Election','2026-07-22 19:39:00','System',NULL,NULL),(60,'System Administrator','Updated Course Representative','2026-07-22 19:49:00','Course Representatives','ass rep','127.0.0.1'),(61,'System Administrator','Removed Course Representative','2026-07-22 19:49:05','Course Representatives','ass rep','127.0.0.1'),(62,'System Administrator','Appointed Course Rep','2026-07-22 20:53:13','Course Representatives','Solomon Fosu','127.0.0.1'),(63,'System Administrator','Created Notice','2026-07-23 16:17:20','Notice Board','ESA verting','127.0.0.1'),(64,'System Administrator','Deleted Notice','2026-07-23 22:11:30','Notice Board','SRC week','127.0.0.1'),(65,'System Administrator','Updated Notice','2026-07-24 15:51:24','Notice Board','ESA GENERAL ASSEMBLY','127.0.0.1'),(66,'System Administrator','Deleted Notice','2026-07-24 17:01:40','Notice Board','SRC','127.0.0.1'),(67,'System Administrator','Deleted Notice','2026-07-24 17:01:52','Notice Board','ESA GENERAL ASSEMBLY','127.0.0.1'),(68,'System Administrator','Created Notice','2026-07-24 17:23:21','Notice Board','esa elections','127.0.0.1'),(69,'System Administrator','Added Member','2026-07-24 22:15:44','Members','ESA-2026-0036','127.0.0.1'),(70,'System Administrator','Added Member','2026-07-24 22:21:09','Members','ESA-2026-0036','127.0.0.1'),(71,'System Administrator','Reset Password','2026-07-24 22:22:49','Members','ESA-2026-0036','127.0.0.1'),(72,'System Administrator','Added Member','2026-07-24 23:14:45','Members','ESA-2026-0037','127.0.0.1'),(73,'System Administrator','Added Member','2026-07-24 23:53:28','Members','ESA-2026-0036','127.0.0.1'),(74,'System Administrator','Reset Password','2026-07-24 23:58:10','Members','ESA-2026-0036','127.0.0.1'),(75,'System Administrator','Created Event','2026-07-25 08:03:21','Events','verting','127.0.0.1'),(76,'System Administrator','Created Notice','2026-07-25 08:10:18','Notice Board','class work','127.0.0.1'),(77,'System Administrator','Updated Notice','2026-07-25 08:10:32','Notice Board','class work more','127.0.0.1'),(78,'System Administrator','Deleted Notice','2026-07-25 08:10:35','Notice Board','class work more','127.0.0.1');
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidates`
--

DROP TABLE IF EXISTS `candidates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `election_id` int NOT NULL,
  `portfolio_id` int NOT NULL,
  `member_id` int NOT NULL,
  `slogan` varchar(255) DEFAULT NULL,
  `manifesto` text,
  `status` varchar(20) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `election_id` (`election_id`),
  KEY `portfolio_id` (`portfolio_id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `candidates_ibfk_1` FOREIGN KEY (`election_id`) REFERENCES `elections` (`id`),
  CONSTRAINT `candidates_ibfk_2` FOREIGN KEY (`portfolio_id`) REFERENCES `portfolios` (`id`),
  CONSTRAINT `candidates_ibfk_3` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidates`
--

LOCK TABLES `candidates` WRITE;
/*!40000 ALTER TABLE `candidates` DISABLE KEYS */;
/*!40000 ALTER TABLE `candidates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_blocks`
--

DROP TABLE IF EXISTS `chat_blocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_blocks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `blocked_by` int NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `blocked_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `blocked_by` (`blocked_by`),
  CONSTRAINT `chat_blocks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `chat_blocks_ibfk_2` FOREIGN KEY (`blocked_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_blocks`
--

LOCK TABLES `chat_blocks` WRITE;
/*!40000 ALTER TABLE `chat_blocks` DISABLE KEYS */;
/*!40000 ALTER TABLE `chat_blocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_settings`
--

DROP TABLE IF EXISTS `chat_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_enabled` tinyint(1) NOT NULL,
  `maintenance_mode` tinyint(1) NOT NULL,
  `member_to_member` tinyint(1) NOT NULL,
  `member_to_admin` tinyint(1) NOT NULL,
  `allow_attachments` tinyint(1) NOT NULL,
  `max_upload_mb` int NOT NULL,
  `max_message_length` int NOT NULL,
  `allow_edit` tinyint(1) NOT NULL,
  `allow_delete` tinyint(1) NOT NULL,
  `welcome_message` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_settings`
--

LOCK TABLES `chat_settings` WRITE;
/*!40000 ALTER TABLE `chat_settings` DISABLE KEYS */;
INSERT INTO `chat_settings` VALUES (1,1,1,1,1,1,10,5000,1,1,'Welcome to ESA VIBES.     together we build ','2026-07-23 23:17:58','2026-07-24 00:06:23');
/*!40000 ALTER TABLE `chat_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_announcements`
--

DROP TABLE IF EXISTS `class_announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_announcements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `class_group_id` int NOT NULL,
  `created_by` int NOT NULL,
  `title` varchar(200) NOT NULL,
  `message` text NOT NULL,
  `is_pinned` tinyint(1) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `event_date` date DEFAULT NULL,
  `event_time` time DEFAULT NULL,
  `venue` varchar(200) DEFAULT NULL,
  `attachment` varchar(255) DEFAULT NULL,
  `attachment_name` varchar(255) DEFAULT NULL,
  `attachment_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `class_group_id` (`class_group_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `class_announcements_ibfk_1` FOREIGN KEY (`class_group_id`) REFERENCES `class_groups` (`id`),
  CONSTRAINT `class_announcements_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `members` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_announcements`
--

LOCK TABLES `class_announcements` WRITE;
/*!40000 ALTER TABLE `class_announcements` DISABLE KEYS */;
/*!40000 ALTER TABLE `class_announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_groups`
--

DROP TABLE IF EXISTS `class_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `programme_id` int NOT NULL,
  `level` varchar(20) NOT NULL,
  `admission_year` varchar(10) DEFAULT NULL,
  `graduation_year` varchar(10) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `course_rep_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `session` varchar(20) NOT NULL DEFAULT 'Weekend',
  `assistant_course_rep_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `programme_id` (`programme_id`),
  KEY `course_rep_id` (`course_rep_id`),
  KEY `fk_assistant_course_rep` (`assistant_course_rep_id`),
  CONSTRAINT `class_groups_ibfk_1` FOREIGN KEY (`programme_id`) REFERENCES `programmes` (`id`),
  CONSTRAINT `class_groups_ibfk_2` FOREIGN KEY (`course_rep_id`) REFERENCES `members` (`id`),
  CONSTRAINT `fk_assistant_course_rep` FOREIGN KEY (`assistant_course_rep_id`) REFERENCES `members` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_groups`
--

LOCK TABLES `class_groups` WRITE;
/*!40000 ALTER TABLE `class_groups` DISABLE KEYS */;
INSERT INTO `class_groups` VALUES (2,'ITE-W300-2023',14,'300','2023/2024','2026/2027','Active',NULL,'2026-07-19 21:32:49','Weekend',NULL),(3,'IT-W100-2025',17,'100','2025/2026','2028/2029','Active',NULL,'2026-07-19 22:25:15','Weekend',NULL),(4,'ITE-W200-2024',14,'200','2024/2025','2027/2028','Active',NULL,'2026-07-19 22:25:56','Weekend',NULL),(5,'A-W100-2025',32,'100','2025/2026','2028/2029','Active',NULL,'2026-07-19 22:31:16','Weekend',NULL),(6,'A-W200-2024',32,'200','2024/2025','2027/2028','Active',NULL,'2026-07-19 22:31:40','Weekend',NULL),(7,'A-W300-2023',32,'300','2023/2024','2026/2027','Active',NULL,'2026-07-19 22:31:56','Weekend',NULL),(8,'PASCM-W100-2025',43,'100','2025/2026','2028/2029','Active',NULL,'2026-07-19 22:32:34','Weekend',NULL),(9,'PASCM-W200-2024',43,'200','2024/2025','2027/2028','Active',NULL,'2026-07-19 22:32:49','Weekend',NULL),(10,'PASCM-W300-2023',43,'300','2023/2024','2026/2027','Active',NULL,'2026-07-19 22:33:02','Weekend',NULL),(11,'BEOAASE-W100-2025',38,'100','2025/2026','2028/2029','Active',NULL,'2026-07-19 22:34:03','Weekend',NULL),(12,'BEOAASE-W200-2024',38,'200','2024/2025','2027/2028','Active',NULL,'2026-07-19 22:34:14','Weekend',NULL),(13,'BEOAASE-W300-2023',38,'300','2023/2024','2026/2027','Active',NULL,'2026-07-19 22:34:24','Weekend',NULL),(14,'HRM-W100-2025',41,'100','2025/2026','2028/2029','Active',NULL,'2026-07-19 22:34:59','Weekend',NULL),(15,'HRM-W200-2024',41,'200','2024/2025','2027/2028','Active',NULL,'2026-07-19 22:35:44','Weekend',NULL),(16,'HRM-W300-2023',41,'300','2023/2024','2026/2027','Active',NULL,'2026-07-19 22:36:08','Weekend',NULL);
/*!40000 ALTER TABLE `class_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversation_members`
--

DROP TABLE IF EXISTS `conversation_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conversation_members` (
  `id` int NOT NULL AUTO_INCREMENT,
  `conversation_id` int NOT NULL,
  `user_id` int NOT NULL,
  `joined_at` datetime DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `is_muted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `conversation_id` (`conversation_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `conversation_members_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`),
  CONSTRAINT `conversation_members_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversation_members`
--

LOCK TABLES `conversation_members` WRITE;
/*!40000 ALTER TABLE `conversation_members` DISABLE KEYS */;
INSERT INTO `conversation_members` VALUES (1,1,1,'2026-07-23 07:32:41',0,0),(2,1,29,'2026-07-23 07:32:41',0,0);
/*!40000 ALTER TABLE `conversation_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversations`
--

DROP TABLE IF EXISTS `conversations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conversations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `conversation_type` varchar(20) NOT NULL,
  `title` varchar(150) DEFAULT NULL,
  `created_by` int NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `conversations_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversations`
--

LOCK TABLES `conversations` WRITE;
/*!40000 ALTER TABLE `conversations` DISABLE KEYS */;
INSERT INTO `conversations` VALUES (1,'private',NULL,1,'2026-07-23 07:32:41','2026-07-23 07:32:41');
/*!40000 ALTER TABLE `conversations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course_reps`
--

DROP TABLE IF EXISTS `course_reps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course_reps` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `class_group_id` int NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `appointed_date` datetime DEFAULT NULL,
  `position` varchar(30) NOT NULL DEFAULT 'Course Rep',
  PRIMARY KEY (`id`),
  UNIQUE KEY `member_id` (`member_id`),
  KEY `fk_course_reps_class_group` (`class_group_id`),
  CONSTRAINT `course_reps_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`),
  CONSTRAINT `fk_course_reps_class_group` FOREIGN KEY (`class_group_id`) REFERENCES `class_groups` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_reps`
--

LOCK TABLES `course_reps` WRITE;
/*!40000 ALTER TABLE `course_reps` DISABLE KEYS */;
/*!40000 ALTER TABLE `course_reps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `department_name` varchar(150) NOT NULL,
  `programme_id` int NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `programme_id` (`programme_id`),
  CONSTRAINT `departments_ibfk_1` FOREIGN KEY (`programme_id`) REFERENCES `programmes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (48,'Department of Information Technology',13,'Active'),(49,'Department of Information Technology Education',14,'Active'),(50,'Department of Mathematics Education',15,'Active'),(51,'Department of Cyber Security',16,'Active'),(52,'Department of Information Technology Education',17,'Active'),(53,'Department of Mathematics',18,'Active'),(54,'Department of Computing and Artificial Intelligence',19,'Active'),(55,'Department of Computing and Internet of Things',20,'Active'),(56,'Department of Information Technology',21,'Active'),(57,'Department of Cyber Security',22,'Active'),(58,'Department of General Science',23,'Active'),(59,'Department of Biology',24,'Active'),(60,'Department of Chemistry',25,'Active'),(61,'Department of Physics',26,'Active'),(62,'Department of Nutrition and Dietetics',27,'Active'),(63,'Department of Public Health',28,'Active'),(64,'Department of Environmental Health',29,'Active'),(65,'Department of Occupational Health and Safety',30,'Active'),(66,'Department of Agribusiness Management',31,'Active'),(67,'Department of Accounting',32,'Active'),(68,'Department of Accounting Education',33,'Active'),(69,'Department of Business Administration',34,'Active'),(70,'Department of Banking and Finance',35,'Active'),(71,'Department of Business Information Systems',36,'Active'),(72,'Department of Procurement',37,'Active'),(73,'Department of Executive Office Administration',38,'Active'),(74,'Department of Management Education and Marketing',39,'Active'),(75,'Department of Marketing Entrepreneurship',40,'Active'),(76,'Department of Human Resource Management',41,'Active'),(77,'Department of Marketing',42,'Active'),(78,'Department of Procurement and Supply Chain Management',43,'Active'),(79,'Department of Automotive Engineering',44,'Active'),(80,'Department of Mechanical Engineering',45,'Active'),(81,'Department of Electrical and Electronics Engineering',46,'Active'),(82,'Department of Civil Engineering',47,'Active'),(83,'Department of Plumbing, Gas and Sanitary Technology',48,'Active'),(84,'Department of Construction Technology and Management',49,'Active'),(85,'Department of Wood Technology',50,'Active'),(86,'Department of Welding and Fabrication Engineering',51,'Active'),(87,'Department of Early Grade Education',52,'Active'),(88,'Department of Upper Primary Education',53,'Active'),(89,'Department of Junior High Education',54,'Active'),(90,'Department of English',55,'Active'),(91,'Department of Ghanaian Language (Asante Twi)',56,'Active'),(92,'Department of French',57,'Active'),(93,'Department of Arabic',58,'Active'),(94,'Department of Physical Education and Health',59,'Active');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `election_settings`
--

DROP TABLE IF EXISTS `election_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `election_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `active_election_id` int DEFAULT NULL,
  `voting_status` varchar(20) DEFAULT NULL,
  `results_visible` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `active_election_id` (`active_election_id`),
  CONSTRAINT `election_settings_ibfk_1` FOREIGN KEY (`active_election_id`) REFERENCES `elections` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `election_settings`
--

LOCK TABLES `election_settings` WRITE;
/*!40000 ALTER TABLE `election_settings` DISABLE KEYS */;
INSERT INTO `election_settings` VALUES (1,NULL,'Closed',1);
/*!40000 ALTER TABLE `election_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `elections`
--

DROP TABLE IF EXISTS `elections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `elections` (
  `id` int NOT NULL AUTO_INCREMENT,
  `election_name` varchar(200) NOT NULL,
  `description` text,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `elections`
--

LOCK TABLES `elections` WRITE;
/*!40000 ALTER TABLE `elections` DISABLE KEYS */;
/*!40000 ALTER TABLE `elections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `event_code` varchar(20) DEFAULT NULL,
  `title` varchar(200) NOT NULL,
  `venue` varchar(200) NOT NULL,
  `event_date` date NOT NULL,
  `event_time` varchar(20) NOT NULL,
  `description` text,
  `banner` varchar(200) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `event_code` (`event_code`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (5,'ESA-EVT-002','verting','ESA PAVILION','2026-07-25','11:02','there will be a verting','logo.jpg','Upcoming','2026-07-25 08:03:20');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `executives`
--

DROP TABLE IF EXISTS `executives`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `executives` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int DEFAULT NULL,
  `executive_id` varchar(20) DEFAULT NULL,
  `full_name` varchar(150) NOT NULL,
  `position` varchar(100) NOT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  `year` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  UNIQUE KEY `executive_id` (`executive_id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `executives_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `executives`
--

LOCK TABLES `executives` WRITE;
/*!40000 ALTER TABLE `executives` DISABLE KEYS */;
INSERT INTO `executives` VALUES (1,NULL,'ESA-EX-001','Owusu Issah','CEO','0244680211','owusuissah@gmail.com','front.jpeg','2026/2027','2026-07-16 19:36:58');
/*!40000 ALTER TABLE `executives` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculties`
--

DROP TABLE IF EXISTS `faculties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculties` (
  `id` int NOT NULL AUTO_INCREMENT,
  `faculty_name` varchar(150) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `faculty_name` (`faculty_name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculties`
--

LOCK TABLES `faculties` WRITE;
/*!40000 ALTER TABLE `faculties` DISABLE KEYS */;
INSERT INTO `faculties` VALUES (1,'Faculty of Applied Sciences and Mathematics Education (FASME)','Active'),(2,'Faculty of Business Education (FBE)','Active'),(3,'Faculty of Technical Education (FTE)','Active'),(4,'Faculty of Vocational Education (FVE)','Active'),(5,'Faculty of Education and Communication Sciences (FECS)','Active');
/*!40000 ALTER TABLE `faculties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lecturers`
--

DROP TABLE IF EXISTS `lecturers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lecturers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lecturer_name` varchar(150) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lecturers`
--

LOCK TABLES `lecturers` WRITE;
/*!40000 ALTER TABLE `lecturers` DISABLE KEYS */;
INSERT INTO `lecturers` VALUES (1,'Dr. Samuel  Akpatsa','0594815658','Department of Cyber Security','2026-07-16 21:48:48');
/*!40000 ALTER TABLE `lecturers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_applications`
--

DROP TABLE IF EXISTS `member_applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(30) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(120) NOT NULL,
  `faculty_id` int DEFAULT NULL,
  `programme` varchar(150) DEFAULT NULL,
  `department` varchar(150) DEFAULT NULL,
  `level` varchar(20) DEFAULT NULL,
  `session` varchar(20) DEFAULT NULL,
  `academic_year` varchar(20) DEFAULT NULL,
  `passport` varchar(255) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `date_applied` datetime DEFAULT NULL,
  `class_group_id` int DEFAULT NULL,
  `reviewed_by` int DEFAULT NULL,
  `reviewed_at` datetime DEFAULT NULL,
  `rejection_reason` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`student_id`),
  UNIQUE KEY `email` (`email`),
  KEY `faculty_id` (`faculty_id`),
  KEY `fk_application_class_group` (`class_group_id`),
  KEY `fk_application_reviewer` (`reviewed_by`),
  CONSTRAINT `fk_application_class_group` FOREIGN KEY (`class_group_id`) REFERENCES `class_groups` (`id`),
  CONSTRAINT `fk_application_reviewer` FOREIGN KEY (`reviewed_by`) REFERENCES `users` (`id`),
  CONSTRAINT `member_applications_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculties` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_applications`
--

LOCK TABLES `member_applications` WRITE;
/*!40000 ALTER TABLE `member_applications` DISABLE KEYS */;
/*!40000 ALTER TABLE `member_applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_indexes`
--

DROP TABLE IF EXISTS `member_indexes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member_indexes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(30) NOT NULL,
  `used` tinyint(1) DEFAULT '0',
  `used_by` int DEFAULT NULL,
  `used_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`student_id`),
  KEY `fk_member_indexes_user` (`used_by`),
  CONSTRAINT `fk_member_indexes_user` FOREIGN KEY (`used_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1018 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_indexes`
--

LOCK TABLES `member_indexes` WRITE;
/*!40000 ALTER TABLE `member_indexes` DISABLE KEYS */;
INSERT INTO `member_indexes` VALUES (1,'5230210065',0,NULL,NULL,'2026-07-20 02:51:58'),(859,'5230210098',1,29,'2026-07-23 05:02:12','2026-07-23 04:58:23'),(860,'5230210002',0,NULL,NULL,'2026-07-23 05:53:18'),(861,'5230210003',0,NULL,NULL,'2026-07-23 05:53:18'),(862,'5230210004',0,NULL,NULL,'2026-07-23 05:53:18'),(863,'5230210005',0,NULL,NULL,'2026-07-23 05:53:18'),(864,'5230210006',0,NULL,NULL,'2026-07-23 05:53:18'),(865,'5230210007',0,NULL,NULL,'2026-07-23 05:53:18'),(866,'5230210008',0,NULL,NULL,'2026-07-23 05:53:18'),(867,'5230210009',0,NULL,NULL,'2026-07-23 05:53:18'),(869,'5230210011',0,NULL,NULL,'2026-07-23 05:53:18'),(870,'5230210012',0,NULL,NULL,'2026-07-23 05:53:18'),(871,'5230210013',0,NULL,NULL,'2026-07-23 05:53:18'),(872,'5230210014',0,NULL,NULL,'2026-07-23 05:53:18'),(873,'5230210015',0,NULL,NULL,'2026-07-23 05:53:18'),(874,'5230210016',0,NULL,NULL,'2026-07-23 05:53:18'),(875,'5230210017',0,NULL,NULL,'2026-07-23 05:53:18'),(876,'5230210018',0,NULL,NULL,'2026-07-23 05:53:18'),(877,'5230210019',0,NULL,NULL,'2026-07-23 05:53:18'),(878,'5230210020',0,NULL,NULL,'2026-07-23 05:53:18'),(879,'5230210021',0,NULL,NULL,'2026-07-23 05:53:18'),(880,'5230210022',0,NULL,NULL,'2026-07-23 05:53:18'),(881,'5230210023',0,NULL,NULL,'2026-07-23 05:53:18'),(882,'5230210024',0,NULL,NULL,'2026-07-23 05:53:18'),(883,'5230210025',0,NULL,NULL,'2026-07-23 05:53:18'),(884,'5230210026',0,NULL,NULL,'2026-07-23 05:53:18'),(885,'5230210027',0,NULL,NULL,'2026-07-23 05:53:18'),(886,'5230210028',0,NULL,NULL,'2026-07-23 05:53:18'),(887,'5230210029',0,NULL,NULL,'2026-07-23 05:53:18'),(888,'5230210030',0,NULL,NULL,'2026-07-23 05:53:18'),(889,'5230210031',0,NULL,NULL,'2026-07-23 05:53:18'),(890,'5230210032',0,NULL,NULL,'2026-07-23 05:53:18'),(891,'5230210033',0,NULL,NULL,'2026-07-23 05:53:18'),(892,'5230210034',0,NULL,NULL,'2026-07-23 05:53:18'),(893,'5230210035',0,NULL,NULL,'2026-07-23 05:53:18'),(894,'5230210036',0,NULL,NULL,'2026-07-23 05:53:18'),(895,'5230210037',0,NULL,NULL,'2026-07-23 05:53:18'),(896,'5230210038',0,NULL,NULL,'2026-07-23 05:53:18'),(897,'5230210039',0,NULL,NULL,'2026-07-23 05:53:18'),(898,'5230210040',0,NULL,NULL,'2026-07-23 05:53:18'),(899,'5230210041',0,NULL,NULL,'2026-07-23 05:53:18'),(900,'5230210042',0,NULL,NULL,'2026-07-23 05:53:18'),(901,'5230210043',0,NULL,NULL,'2026-07-23 05:53:18'),(902,'5230210044',0,NULL,NULL,'2026-07-23 05:53:18'),(903,'5230210045',0,NULL,NULL,'2026-07-23 05:53:18'),(904,'5230210046',0,NULL,NULL,'2026-07-23 05:53:18'),(905,'5230210047',0,NULL,NULL,'2026-07-23 05:53:18'),(906,'5230210048',0,NULL,NULL,'2026-07-23 05:53:18'),(907,'5230210049',0,NULL,NULL,'2026-07-23 05:53:18'),(908,'5230210050',0,NULL,NULL,'2026-07-23 05:53:18'),(909,'5230210051',0,NULL,NULL,'2026-07-23 05:53:18'),(910,'5230210052',0,NULL,NULL,'2026-07-23 05:53:18'),(911,'5230210053',0,NULL,NULL,'2026-07-23 05:53:18'),(912,'5230210054',0,NULL,NULL,'2026-07-23 05:53:18'),(914,'5230210056',0,NULL,NULL,'2026-07-23 05:53:18'),(915,'5230210057',0,NULL,NULL,'2026-07-23 05:53:18'),(916,'5230210058',0,NULL,NULL,'2026-07-23 05:53:18'),(917,'5230210059',0,NULL,NULL,'2026-07-23 05:53:18'),(918,'5230210060',0,NULL,NULL,'2026-07-23 05:53:18'),(919,'5230210061',0,NULL,NULL,'2026-07-23 05:53:18'),(920,'5230210062',0,NULL,NULL,'2026-07-23 05:53:18'),(921,'5230210063',0,NULL,NULL,'2026-07-23 05:53:18'),(922,'5230210064',0,NULL,NULL,'2026-07-23 05:53:18'),(923,'5230210066',0,NULL,NULL,'2026-07-23 05:53:18'),(924,'5230210067',0,NULL,NULL,'2026-07-23 05:53:18'),(925,'5230210068',0,NULL,NULL,'2026-07-23 05:53:18'),(926,'5230210069',0,NULL,NULL,'2026-07-23 05:53:18'),(927,'5230210070',0,NULL,NULL,'2026-07-23 05:53:18'),(928,'5230210071',0,NULL,NULL,'2026-07-23 05:53:18'),(929,'5230210072',0,NULL,NULL,'2026-07-23 05:53:18'),(930,'5230210073',0,NULL,NULL,'2026-07-23 05:53:18'),(931,'5230210074',0,NULL,NULL,'2026-07-23 05:53:18'),(932,'5230210075',0,NULL,NULL,'2026-07-23 05:53:18'),(933,'5230210076',0,NULL,NULL,'2026-07-23 05:53:18'),(935,'5230210078',0,NULL,NULL,'2026-07-23 05:53:18'),(936,'5230210079',0,NULL,NULL,'2026-07-23 05:53:18'),(937,'5230210080',0,NULL,NULL,'2026-07-23 05:53:18'),(938,'5230210081',0,NULL,NULL,'2026-07-23 05:53:18'),(939,'5230210082',0,NULL,NULL,'2026-07-23 05:53:18'),(940,'5230210083',0,NULL,NULL,'2026-07-23 05:53:18'),(941,'5230210084',0,NULL,NULL,'2026-07-23 05:53:18'),(942,'5230210085',0,NULL,NULL,'2026-07-23 05:53:18'),(943,'5230210086',0,NULL,NULL,'2026-07-23 05:53:18'),(944,'5230210087',0,NULL,NULL,'2026-07-23 05:53:18'),(945,'5230210088',0,NULL,NULL,'2026-07-23 05:53:18'),(946,'5230210089',0,NULL,NULL,'2026-07-23 05:53:18'),(947,'5230210090',0,NULL,NULL,'2026-07-23 05:53:18'),(948,'5230210091',0,NULL,NULL,'2026-07-23 05:53:18'),(949,'5230210092',0,NULL,NULL,'2026-07-23 05:53:18'),(950,'5230210093',0,NULL,NULL,'2026-07-23 05:53:18'),(951,'5230210094',0,NULL,NULL,'2026-07-23 05:53:18'),(952,'5230210095',0,NULL,NULL,'2026-07-23 05:53:18'),(953,'5230210096',0,NULL,NULL,'2026-07-23 05:53:18'),(954,'5230210097',0,NULL,NULL,'2026-07-23 05:53:18'),(955,'5230210099',0,NULL,NULL,'2026-07-23 05:53:18'),(956,'5230210100',0,NULL,NULL,'2026-07-23 05:53:18'),(957,'5230210101',0,NULL,NULL,'2026-07-23 05:53:18'),(958,'5230210102',0,NULL,NULL,'2026-07-23 05:53:18'),(959,'5230210103',0,NULL,NULL,'2026-07-23 05:53:18'),(960,'5230210104',0,NULL,NULL,'2026-07-23 05:53:18'),(961,'5230210105',0,NULL,NULL,'2026-07-23 05:53:18'),(962,'5230210106',0,NULL,NULL,'2026-07-23 05:53:18'),(963,'5230210107',0,NULL,NULL,'2026-07-23 05:53:18'),(964,'5230210108',0,NULL,NULL,'2026-07-23 05:53:18'),(965,'5230210109',0,NULL,NULL,'2026-07-23 05:53:18'),(966,'5230210110',0,NULL,NULL,'2026-07-23 05:53:18'),(967,'5230210111',0,NULL,NULL,'2026-07-23 05:53:18'),(968,'5230210112',0,NULL,NULL,'2026-07-23 05:53:18'),(969,'5230210113',0,NULL,NULL,'2026-07-23 05:53:18'),(970,'5230210114',0,NULL,NULL,'2026-07-23 05:53:18'),(971,'5230210115',0,NULL,NULL,'2026-07-23 05:53:18'),(972,'5230210116',0,NULL,NULL,'2026-07-23 05:53:18'),(973,'5230210117',0,NULL,NULL,'2026-07-23 05:53:18'),(974,'5230210118',0,NULL,NULL,'2026-07-23 05:53:18'),(975,'5230210119',0,NULL,NULL,'2026-07-23 05:53:18'),(976,'5230210120',0,NULL,NULL,'2026-07-23 05:53:18'),(977,'5230210121',0,NULL,NULL,'2026-07-23 05:53:18'),(978,'5230210122',0,NULL,NULL,'2026-07-23 05:53:18'),(979,'5230210123',0,NULL,NULL,'2026-07-23 05:53:18'),(980,'5230210124',0,NULL,NULL,'2026-07-23 05:53:18'),(981,'5230210125',0,NULL,NULL,'2026-07-23 05:53:18'),(982,'5230210126',0,NULL,NULL,'2026-07-23 05:53:18'),(983,'5230210127',0,NULL,NULL,'2026-07-23 05:53:18'),(984,'5230210128',0,NULL,NULL,'2026-07-23 05:53:18'),(985,'5230210129',0,NULL,NULL,'2026-07-23 05:53:18'),(986,'5230210130',0,NULL,NULL,'2026-07-23 05:53:18'),(987,'5230210131',0,NULL,NULL,'2026-07-23 05:53:18'),(988,'5230210132',0,NULL,NULL,'2026-07-23 05:53:18'),(989,'5230210133',0,NULL,NULL,'2026-07-23 05:53:18'),(990,'5230210134',0,NULL,NULL,'2026-07-23 05:53:18'),(991,'5230210135',0,NULL,NULL,'2026-07-23 05:53:18'),(992,'5230210136',0,NULL,NULL,'2026-07-23 05:53:18'),(993,'5230210137',0,NULL,NULL,'2026-07-23 05:53:18'),(994,'5230210138',0,NULL,NULL,'2026-07-23 05:53:18'),(995,'5230210139',0,NULL,NULL,'2026-07-23 05:53:18'),(996,'5230210140',0,NULL,NULL,'2026-07-23 05:53:18'),(997,'5230210141',0,NULL,NULL,'2026-07-23 05:53:18'),(998,'5230210142',0,NULL,NULL,'2026-07-23 05:53:18'),(999,'5230210143',0,NULL,NULL,'2026-07-23 05:53:18'),(1000,'5230210144',0,NULL,NULL,'2026-07-23 05:53:18'),(1001,'5230210145',0,NULL,NULL,'2026-07-23 05:53:18'),(1002,'5230210146',0,NULL,NULL,'2026-07-23 05:53:18'),(1003,'5230210147',0,NULL,NULL,'2026-07-23 05:53:18'),(1004,'5230210148',0,NULL,NULL,'2026-07-23 05:53:18'),(1005,'5230210149',0,NULL,NULL,'2026-07-23 05:53:18'),(1006,'5230210150',0,NULL,NULL,'2026-07-23 05:53:18'),(1007,'5230210151',0,NULL,NULL,'2026-07-23 05:53:18'),(1008,'5230210152',0,NULL,NULL,'2026-07-23 05:53:18'),(1009,'5230210153',0,NULL,NULL,'2026-07-23 05:53:18'),(1010,'5230210154',0,NULL,NULL,'2026-07-23 05:53:18'),(1011,'5230210155',0,NULL,NULL,'2026-07-23 05:53:18'),(1012,'5230210156',0,NULL,NULL,'2026-07-23 05:53:18'),(1013,'5230210157',0,NULL,NULL,'2026-07-23 05:53:18'),(1014,'5230210158',0,NULL,NULL,'2026-07-23 05:53:18'),(1015,'4240210001',0,NULL,NULL,'2026-07-23 05:55:14'),(1016,'4240210002',0,NULL,NULL,'2026-07-23 05:55:23'),(1017,'4240210003',0,NULL,NULL,'2026-07-23 05:55:35');
/*!40000 ALTER TABLE `member_indexes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `members`
--

DROP TABLE IF EXISTS `members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `members` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` varchar(30) NOT NULL,
  `esa_id` varchar(20) DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `passport` varchar(255) DEFAULT NULL,
  `faculty_id` int DEFAULT NULL,
  `programme` varchar(150) DEFAULT NULL,
  `department` varchar(150) DEFAULT NULL,
  `level` varchar(20) DEFAULT NULL,
  `session` varchar(20) DEFAULT NULL,
  `academic_year` varchar(20) DEFAULT NULL,
  `guardian_name` varchar(150) DEFAULT NULL,
  `guardian_phone` varchar(20) DEFAULT NULL,
  `relationship` varchar(100) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `date_registered` datetime DEFAULT NULL,
  `has_voted` tinyint(1) NOT NULL DEFAULT '0',
  `user_id` int DEFAULT NULL,
  `expiry_date` datetime DEFAULT NULL,
  `class_group_id` int DEFAULT NULL,
  `registration_status` varchar(20) DEFAULT 'Pending',
  `approved_by` int DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `student_id` (`student_id`),
  UNIQUE KEY `esa_id` (`esa_id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `fk_members_class_group` (`class_group_id`),
  KEY `fk_member_approved_by` (`approved_by`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `fk_member_approved_by` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_member_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_members_class_group` FOREIGN KEY (`class_group_id`) REFERENCES `class_groups` (`id`),
  CONSTRAINT `members_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculties` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `members`
--

LOCK TABLES `members` WRITE;
/*!40000 ALTER TABLE `members` DISABLE KEYS */;
INSERT INTO `members` VALUES (6,'5230210065','ESA-2026-0002','Owusu','Issah','Male','1986-02-10','0244680211',NULL,'Postal address P.O.BOX ST 245 KUMASI STADIUM','WhatsApp_Image_2026-07-15_at_10.20.49_PM.jpeg',1,'B.Sc. Information Technology Education','','300','Weekend','2026/2027','aasamoah','0244680211','FATHER','Active','2026-07-13 01:19:42',1,NULL,NULL,2,'Pending',NULL,NULL),(35,'5230210098','ESA-2026-0007','Yaw','Ametus','Male',NULL,'0541125950',NULL,NULL,'20260719_094629.jpg',1,'B.Sc. Information Technology Education','','300','Weekend','2023/2024',NULL,NULL,NULL,'Active','2026-07-23 05:02:12',0,29,'2027-07-23 05:02:12',2,'Approved',NULL,'2026-07-23 05:02:12');
/*!40000 ALTER TABLE `members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message_reads`
--

DROP TABLE IF EXISTS `message_reads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message_reads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message_id` int NOT NULL,
  `user_id` int NOT NULL,
  `read_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `message_id` (`message_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `message_reads_ibfk_1` FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`),
  CONSTRAINT `message_reads_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message_reads`
--

LOCK TABLES `message_reads` WRITE;
/*!40000 ALTER TABLE `message_reads` DISABLE KEYS */;
INSERT INTO `message_reads` VALUES (1,1,29,'2026-07-23 08:44:56'),(2,2,29,'2026-07-23 08:44:56'),(3,3,29,'2026-07-23 08:44:56'),(4,4,1,'2026-07-23 08:47:23'),(5,5,1,'2026-07-23 08:47:23'),(6,6,1,'2026-07-23 08:47:23'),(7,7,29,'2026-07-23 08:48:03'),(8,8,1,'2026-07-23 08:48:33'),(9,9,29,'2026-07-23 08:57:09'),(10,10,29,'2026-07-23 08:57:09'),(11,11,29,'2026-07-23 09:26:54'),(12,12,29,'2026-07-23 09:26:54'),(13,13,29,'2026-07-23 09:26:54'),(14,14,29,'2026-07-23 09:26:54'),(15,15,29,'2026-07-23 09:26:54'),(16,16,29,'2026-07-23 11:10:04'),(17,17,29,'2026-07-23 11:10:04'),(18,18,29,'2026-07-23 11:10:04'),(19,19,1,'2026-07-23 11:30:09'),(20,20,1,'2026-07-23 11:30:09'),(21,21,1,'2026-07-23 11:30:09'),(22,22,1,'2026-07-23 11:30:09'),(23,23,29,'2026-07-23 11:30:32'),(24,24,1,'2026-07-23 11:31:01'),(25,25,1,'2026-07-23 13:32:37'),(26,26,1,'2026-07-23 13:32:37'),(27,27,29,'2026-07-23 23:40:03'),(28,28,29,'2026-07-23 23:40:03'),(29,29,29,'2026-07-23 23:40:03'),(30,30,29,'2026-07-23 23:40:03'),(32,33,29,'2026-07-24 01:50:49'),(33,35,1,'2026-07-24 01:52:04'),(34,36,29,'2026-07-24 01:52:25'),(35,37,1,'2026-07-24 02:05:14'),(38,41,29,'2026-07-25 09:15:41'),(40,43,1,'2026-07-25 13:47:25'),(41,44,1,'2026-07-25 13:47:25'),(42,45,1,'2026-07-25 13:47:25');
/*!40000 ALTER TABLE `message_reads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `conversation_id` int NOT NULL,
  `sender_id` int NOT NULL,
  `message` text NOT NULL,
  `edited` tinyint(1) DEFAULT NULL,
  `edited_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `reply_to_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `conversation_id` (`conversation_id`),
  KEY `sender_id` (`sender_id`),
  KEY `reply_to_id` (`reply_to_id`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`),
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`),
  CONSTRAINT `messages_ibfk_3` FOREIGN KEY (`reply_to_id`) REFERENCES `messages` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,1,1,'hello',0,NULL,'2026-07-23 07:52:24',NULL),(2,1,1,'how are u doing today',0,NULL,'2026-07-23 07:52:36',NULL),(3,1,1,'hello',0,NULL,'2026-07-23 08:35:25',NULL),(4,1,29,'hello senior',0,NULL,'2026-07-23 08:45:03',NULL),(5,1,29,'how is your day going',0,NULL,'2026-07-23 08:45:32',NULL),(6,1,29,'is going well boss',0,NULL,'2026-07-23 08:45:49',NULL),(7,1,1,'okay',0,NULL,'2026-07-23 08:47:49',NULL),(8,1,29,'good',0,NULL,'2026-07-23 08:48:20',NULL),(9,1,1,'will u be able to come class weekend',0,NULL,'2026-07-23 08:53:30',NULL),(10,1,1,'lets meet n talk',0,NULL,'2026-07-23 08:56:34',NULL),(11,1,1,'',0,NULL,'2026-07-23 09:12:54',NULL),(12,1,1,'',0,NULL,'2026-07-23 09:19:18',NULL),(13,1,1,'',0,NULL,'2026-07-23 09:19:41',NULL),(14,1,1,'',0,NULL,'2026-07-23 09:20:29',NULL),(15,1,1,'',0,NULL,'2026-07-23 09:26:12',NULL),(16,1,1,'',0,NULL,'2026-07-23 10:29:43',NULL),(17,1,1,'hi',0,NULL,'2026-07-23 10:45:47',NULL),(18,1,1,'hg',0,NULL,'2026-07-23 11:09:35',NULL),(19,1,29,'hello',0,NULL,'2026-07-23 11:10:16',NULL),(20,1,29,'hi',0,NULL,'2026-07-23 11:10:38',NULL),(21,1,29,'he',0,NULL,'2026-07-23 11:29:02',NULL),(22,1,29,'hi',0,NULL,'2026-07-23 11:29:26',NULL),(23,1,1,'kkkkkk',0,NULL,'2026-07-23 11:30:14',NULL),(24,1,29,'255456',0,NULL,'2026-07-23 11:30:37',NULL),(25,1,29,'hello',0,NULL,'2026-07-23 12:01:34',NULL),(26,1,29,'hi',0,NULL,'2026-07-23 12:01:48',NULL),(27,1,1,'hi',0,NULL,'2026-07-23 13:49:36',NULL),(28,1,1,'how are u doing',0,NULL,'2026-07-23 13:49:45',NULL),(29,1,1,'hi',0,NULL,'2026-07-23 14:00:52',NULL),(30,1,1,'will u be on campus today',0,NULL,'2026-07-23 14:06:42',NULL),(33,1,1,'hi',0,NULL,'2026-07-24 00:49:14',NULL),(35,1,29,'hello',0,NULL,'2026-07-24 01:51:07',NULL),(36,1,1,'hello',0,NULL,'2026-07-24 01:52:09',NULL),(37,1,29,'hello',0,NULL,'2026-07-24 02:00:30',NULL),(41,1,1,'are u okat',1,'2026-07-25 09:58:32','2026-07-25 08:40:58',NULL),(43,1,29,'hello',0,NULL,'2026-07-25 10:00:41',NULL),(44,1,29,'hello sir',0,NULL,'2026-07-25 13:42:22',NULL),(45,1,29,'how are u doing today',0,NULL,'2026-07-25 13:42:40',NULL),(46,1,1,'hello',0,NULL,'2026-07-25 13:47:32',NULL);
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notices`
--

DROP TABLE IF EXISTS `notices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `message` text NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `is_pinned` tinyint(1) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `attachment` varchar(255) DEFAULT NULL,
  `attachment_name` varchar(255) DEFAULT NULL,
  `attachment_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notices`
--

LOCK TABLES `notices` WRITE;
/*!40000 ALTER TABLE `notices` DISABLE KEYS */;
INSERT INTO `notices` VALUES (4,'esa elections','general Elections','General',0,'Published',NULL,'2026-07-24 17:23:21',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `notices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_settings`
--

DROP TABLE IF EXISTS `payment_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `momo_network` varchar(30) NOT NULL,
  `momo_number` varchar(30) NOT NULL,
  `account_name` varchar(120) NOT NULL,
  `payment_instruction` text,
  `qr_code` varchar(255) DEFAULT NULL,
  `online_payment_enabled` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_settings`
--

LOCK TABLES `payment_settings` WRITE;
/*!40000 ALTER TABLE `payment_settings` DISABLE KEYS */;
INSERT INTO `payment_settings` VALUES (1,'MTN Mobile Money','0246154632','OWUSU ISSAH','PAY  YOUR REGISTRATION DUES ',NULL,1);
/*!40000 ALTER TABLE `payment_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` int NOT NULL,
  `payment_type` varchar(50) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_method` varchar(30) DEFAULT NULL,
  `reference` varchar(100) DEFAULT NULL,
  `date_paid` datetime DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `proof_image` varchar(255) DEFAULT NULL,
  `approved_by` int DEFAULT NULL,
  `approved_at` datetime DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  KEY `approved_by` (`approved_by`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`id`),
  CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`approved_by`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (16,35,'Registration Fee',200.00,'Cash','ESA-REC-2026-000016','2026-07-24 22:38:56','Approved',NULL,1,'2026-07-24 22:40:17',''),(17,35,'Year Dues',50.00,'Cash','ESA-REC-2026-000017','2026-07-24 22:39:00','Approved',NULL,1,'2026-07-24 22:40:13',''),(18,35,'ESA Cloth',100.00,'Cash','ESA-REC-2026-000018','2026-07-24 22:39:12','Approved',NULL,1,'2026-07-24 22:40:10','');
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `portfolios`
--

DROP TABLE IF EXISTS `portfolios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `portfolios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `portfolio_name` varchar(100) NOT NULL,
  `description` text,
  `display_order` int DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `portfolio_name` (`portfolio_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `portfolios`
--

LOCK TABLES `portfolios` WRITE;
/*!40000 ALTER TABLE `portfolios` DISABLE KEYS */;
INSERT INTO `portfolios` VALUES (1,'CEO','in charge of esa activities',1,'Active'),(2,'DEPT.CEO','',1,'Active'),(3,'FINANCIAL SECRETARY','',1,'Active'),(4,'GENERAL SECRETARY','',1,'Active'),(5,'TREASURER','',1,'Active'),(6,'WOCOM','',1,'Active');
/*!40000 ALTER TABLE `portfolios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programmes`
--

DROP TABLE IF EXISTS `programmes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `programmes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `programme_name` varchar(150) NOT NULL,
  `faculty_id` int NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `programme_name` (`programme_name`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `programmes_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculties` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programmes`
--

LOCK TABLES `programmes` WRITE;
/*!40000 ALTER TABLE `programmes` DISABLE KEYS */;
INSERT INTO `programmes` VALUES (13,'B.Sc. Information Technology',1,'Active'),(14,'B.Sc. Information Technology Education',1,'Active'),(15,'B.Sc. Mathematics Education',1,'Active'),(16,'B.Sc. Cyber Security and Digital Forensics',1,'Active'),(17,'B.Ed. Information Technology',1,'Active'),(18,'B.Ed. Mathematics',1,'Active'),(19,'B.Ed. Computing with Artificial Intelligence (AI)',1,'Active'),(20,'B.Ed. Computing with Internet of Things (IoT)',1,'Active'),(21,'Diploma in Information Technology',1,'Active'),(22,'Diploma in Cyber Security',1,'Active'),(23,'B.Ed. General Science',1,'Active'),(24,'B.Ed. Biology',1,'Active'),(25,'B.Ed. Chemistry',1,'Active'),(26,'B.Ed. Physics',1,'Active'),(27,'B.Sc. Nutrition and Dietetics',1,'Active'),(28,'B.Sc. Public Health',1,'Active'),(29,'B.Sc. Environmental Health and Sanitation Education',1,'Active'),(30,'B.Sc. Occupational Health and Safety',1,'Active'),(31,'B.Sc. Agribusiness Management',1,'Active'),(32,'B.Sc. Accounting',2,'Active'),(33,'B.Sc. Accounting Education',2,'Active'),(34,'B.Sc. Administration (Accounting)',2,'Active'),(35,'B.Sc. Administration (Banking & Finance)',2,'Active'),(36,'B.Sc. Administration (Business Information Systems)',2,'Active'),(37,'B.Sc. Administration (Procurement)',2,'Active'),(38,'B.B.A. Executive Office Administration and Secretarial Education',2,'Active'),(39,'B.Sc. Management Education and Marketing',2,'Active'),(40,'B.Sc. Marketing Entrepreneurship',2,'Active'),(41,'B.Sc. Human Resource Management',2,'Active'),(42,'B.Sc. Marketing',2,'Active'),(43,'B.Sc. Procurement and Supply Chain Management',2,'Active'),(44,'B.Sc. Automotive Engineering Technology with Education',3,'Active'),(45,'B.Sc. Mechanical Engineering Technology with Education',3,'Active'),(46,'B.Sc. Electrical and Electronics Engineering Technology with Education',3,'Active'),(47,'B.Sc. Civil Engineering Technology',3,'Active'),(48,'B.Sc. Plumbing, Gas and Sanitary Technology',3,'Active'),(49,'B.Sc. Construction Technology and Management',3,'Active'),(50,'B.Sc. Wood Technology with Education',3,'Active'),(51,'B.Sc. Welding and Fabrication Engineering Technology with Education',3,'Active'),(52,'B.Ed. Early Grade Education',5,'Active'),(53,'B.Ed. Upper Primary Education',5,'Active'),(54,'B.Ed. Junior High Education',5,'Active'),(55,'B.A./B.Ed. English',5,'Active'),(56,'B.A./B.Ed. Ghanaian Language (Asante Twi)',5,'Active'),(57,'B.A./B.Ed. French',5,'Active'),(58,'B.A./B.Ed. Arabic',5,'Active'),(59,'B.Ed. Physical Education and Health',5,'Active');
/*!40000 ALTER TABLE `programmes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sliders`
--

DROP TABLE IF EXISTS `sliders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sliders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `subtitle` varchar(500) DEFAULT NULL,
  `image` varchar(255) NOT NULL,
  `button_text` varchar(100) DEFAULT NULL,
  `button_link` varchar(255) DEFAULT NULL,
  `display_order` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sliders`
--

LOCK TABLES `sliders` WRITE;
/*!40000 ALTER TABLE `sliders` DISABLE KEYS */;
INSERT INTO `sliders` VALUES (3,'ESA ELECTIONS 2026','ESA EXECUTIVE ELECTIONS ','uploads/slides/dc4e4d6ef9db45a89baed69dcb1a2b08_logo.png','ESA DECIDES ','#',3,1,'2026-07-22 14:21:29'),(4,'ESA CEO ','ONEFRONT','uploads/slides/ccbf07a81b114d1ab4c19aad5a430d87_front.jpeg','TOGETHER WE BUILD ','#',2,1,'2026-07-22 14:22:29');
/*!40000 ALTER TABLE `sliders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_settings`
--

DROP TABLE IF EXISTS `system_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `system_name` varchar(200) DEFAULT NULL,
  `short_name` varchar(50) DEFAULT NULL,
  `slogan` varchar(200) DEFAULT NULL,
  `university_name` varchar(255) DEFAULT NULL,
  `campus` varchar(100) DEFAULT NULL,
  `membership_validity` int DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `ceo_signature` varchar(255) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `website` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_settings`
--

LOCK TABLES `system_settings` WRITE;
/*!40000 ALTER TABLE `system_settings` DISABLE KEYS */;
INSERT INTO `system_settings` VALUES (1,'Executive Student Association','ESA','Together We Build','University of Skills Training and Entrepreneurial Development','Kumasi Campus',2,'logo.jpg','ceo_signature.png.png',NULL,NULL,NULL);
/*!40000 ALTER TABLE `system_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(30) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime DEFAULT NULL,
  `username` varchar(30) NOT NULL,
  `must_change_password` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'System Administrator','admin@usted.edu.gh','scrypt:32768:8:1$ULATtA6eAkXo3ZkI$c95a029559ed1408a4fc451cbcd4b1b7b186660536fb749d413051123bc1eaff23cc363b2765df55cdfc8c22c184a0c842d03ed0c1d4ab16288191f392c997e2','Administrator',1,'2026-07-11 09:31:17','admin',0),(29,'Yaw Ametus',NULL,'scrypt:32768:8:1$Tk2txM63oGwe2Q7R$84e61df4442d226f889103c9eb1c64d3e20ab05198a80932207f56a4c7996f0f1d31066f14700d5cdcd5468dc6e1ff2e92823a7111b537d76f2ed3bd22cb26e9','Member',1,'2026-07-23 05:02:12','yaw123',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `votes`
--

DROP TABLE IF EXISTS `votes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `votes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `election_id` int NOT NULL,
  `portfolio_id` int NOT NULL,
  `candidate_id` int NOT NULL,
  `member_index_id` int NOT NULL,
  `vote_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_member_vote` (`election_id`,`portfolio_id`,`member_index_id`),
  KEY `portfolio_id` (`portfolio_id`),
  KEY `candidate_id` (`candidate_id`),
  KEY `member_index_id` (`member_index_id`),
  CONSTRAINT `votes_ibfk_1` FOREIGN KEY (`election_id`) REFERENCES `elections` (`id`),
  CONSTRAINT `votes_ibfk_2` FOREIGN KEY (`portfolio_id`) REFERENCES `portfolios` (`id`),
  CONSTRAINT `votes_ibfk_3` FOREIGN KEY (`candidate_id`) REFERENCES `candidates` (`id`),
  CONSTRAINT `votes_ibfk_4` FOREIGN KEY (`member_index_id`) REFERENCES `member_indexes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `votes`
--

LOCK TABLES `votes` WRITE;
/*!40000 ALTER TABLE `votes` DISABLE KEYS */;
/*!40000 ALTER TABLE `votes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-25 16:21:49
