-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           8.0.30 - MySQL Community Server - GPL
-- SE du serveur:                Win64
-- HeidiSQL Version:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour promeo
CREATE DATABASE IF NOT EXISTS `promeo` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `promeo`;

-- Listage de la structure de table promeo. centres
CREATE TABLE IF NOT EXISTS `centres` (
  `id_centre` int NOT NULL AUTO_INCREMENT,
  `ville` varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_centre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Listage des données de la table promeo.centres : ~2 rows (environ)
DELETE FROM `centres`;
INSERT INTO `centres` (`id_centre`, `ville`) VALUES
	(1, 'Compiègne'),
	(2, 'Beauvais');

-- Listage de la structure de table promeo. contacts
CREATE TABLE IF NOT EXISTS `contacts` (
  `id_contact` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `date` datetime NOT NULL,
  `id_formateur` int DEFAULT NULL,
  `prenom` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `message` text COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id_contact`),
  KEY `fk_formateur` (`id_formateur`),
  CONSTRAINT `fk_formateur` FOREIGN KEY (`id_formateur`) REFERENCES `formateurs` (`id_formateur`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Listage des données de la table promeo.contacts : ~3 rows (environ)
DELETE FROM `contacts`;
INSERT INTO `contacts` (`id_contact`, `nom`, `email`, `date`, `id_formateur`, `prenom`, `message`) VALUES
	(5, 'Berhault', 'berowilliam60@gmail.com', '2024-02-01 14:27:07', 2, 'William', 'COUCOU COUCOU'),
	(6, 'Berhault', 'Ber', '2024-02-01 14:33:11', 2, 'WIlliam', 'dzqdk^plm'),
	(7, 'Berhault', 'berowilliam60@gmail.com', '2024-06-03 14:57:36', 1, 'dzq', 'test');

-- Listage de la structure de table promeo. formateurs
CREATE TABLE IF NOT EXISTS `formateurs` (
  `id_formateur` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `prenom` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mdp` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telephone` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_formateur`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Listage des données de la table promeo.formateurs : ~2 rows (environ)
DELETE FROM `formateurs`;
INSERT INTO `formateurs` (`id_formateur`, `nom`, `prenom`, `email`, `mdp`, `telephone`) VALUES
	(1, 'Berhault', 'William', 'berowilliam60@gmail.com', '$2y$10$ZQe2PES6/XkKqydm7C16MeKu9e29dfCo/7ZGZYGXhtOzPqOHoPZU6', '0786883088'),
	(2, 'Douillet', 'Killian', 'kdouillet@gmail.com', '$2y$10$ZQe2PES6/XkKqydm7C16MeKu9e29dfCo/7ZGZYGXhtOzPqOHoPZU6', '0786683089');

-- Listage de la structure de table promeo. formateurs_centres
CREATE TABLE IF NOT EXISTS `formateurs_centres` (
  `id_formateur` int NOT NULL AUTO_INCREMENT,
  `id_centre` int NOT NULL,
  PRIMARY KEY (`id_formateur`,`id_centre`),
  KEY `id_centre` (`id_centre`),
  CONSTRAINT `formateurs_centres_ibfk_1` FOREIGN KEY (`id_formateur`) REFERENCES `formateurs` (`id_formateur`),
  CONSTRAINT `formateurs_centres_ibfk_2` FOREIGN KEY (`id_centre`) REFERENCES `centres` (`id_centre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Listage des données de la table promeo.formateurs_centres : ~3 rows (environ)
DELETE FROM `formateurs_centres`;
INSERT INTO `formateurs_centres` (`id_formateur`, `id_centre`) VALUES
	(1, 1),
	(1, 2),
	(2, 2);

-- Listage de la structure de table promeo. formations
CREATE TABLE IF NOT EXISTS `formations` (
  `id_formation` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(15) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_formation`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Listage des données de la table promeo.formations : ~1 rows (environ)
DELETE FROM `formations`;
INSERT INTO `formations` (`id_formation`, `nom`) VALUES
	(1, 'LP RGI');

-- Listage de la structure de table promeo. rdv
CREATE TABLE IF NOT EXISTS `rdv` (
  `id_rdv` int NOT NULL AUTO_INCREMENT,
  `debut` datetime DEFAULT NULL,
  `fin` datetime DEFAULT NULL,
  `nom` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `prenom` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telephone` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `id_formation` int DEFAULT NULL,
  `id_formateur` int NOT NULL,
  PRIMARY KEY (`id_rdv`),
  KEY `id_formation` (`id_formation`),
  KEY `id_formateur` (`id_formateur`),
  CONSTRAINT `rdv_ibfk_1` FOREIGN KEY (`id_formation`) REFERENCES `formations` (`id_formation`),
  CONSTRAINT `rdv_ibfk_2` FOREIGN KEY (`id_formateur`) REFERENCES `formateurs` (`id_formateur`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Listage des données de la table promeo.rdv : ~8 rows (environ)
DELETE FROM `rdv`;
INSERT INTO `rdv` (`id_rdv`, `debut`, `fin`, `nom`, `prenom`, `email`, `telephone`, `id_formation`, `id_formateur`) VALUES
	(79, '2024-05-07 10:00:00', '2024-05-07 10:30:00', 'Durand', 'Kevin', 'Kdurant@gmail.com', '0786883088', NULL, 1),
	(80, '2024-05-07 13:00:00', '2024-05-07 15:00:00', NULL, NULL, NULL, NULL, NULL, 1),
	(81, '2024-05-07 10:30:00', '2024-05-07 12:00:00', NULL, NULL, NULL, NULL, NULL, 1),
	(82, '2024-05-07 08:00:00', '2024-05-07 10:00:00', NULL, NULL, NULL, NULL, NULL, 1),
	(84, '2024-05-17 08:00:00', '2024-05-17 10:00:00', NULL, NULL, NULL, NULL, NULL, 1),
	(85, '2024-05-17 11:00:00', '2024-05-17 17:00:00', NULL, NULL, NULL, NULL, NULL, 1),
	(88, '2024-06-05 09:00:00', '2024-06-05 10:00:00', 'Kevin', 'Durand', 'Kdurant@gmail.com', '0786883088', NULL, 1),
	(89, '2024-06-05 10:00:00', '2024-06-05 13:00:00', NULL, NULL, NULL, NULL, NULL, 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
