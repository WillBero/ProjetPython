CREATE DATABASE IF NOT EXISTS `promeo` ;
USE `promeo`;


CREATE TABLE IF NOT EXISTS `centres` (
  `id_centre` int NOT NULL AUTO_INCREMENT,
  `ville` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_centre`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DELETE FROM `centres`;
INSERT INTO `centres` (`id_centre`, `ville`) VALUES
	(1, 'Compiègne'),
	(2, 'Beauvais');

CREATE TABLE IF NOT EXISTS `formateurs` (
  `id_formateur` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `prenom` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mdp` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telephone` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_formateur`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DELETE FROM `formateurs`;
INSERT INTO `formateurs` (`id_formateur`, `nom`, `prenom`, `email`, `mdp`, `telephone`) VALUES
	(1, 'Berhault', 'William', 'berowilliam60@gmail.com', '$2y$10$ZQe2PES6/XkKqydm7C16MeKu9e29dfCo/7ZGZYGXhtOzPqOHoPZU6', '0786883088'),
	(2, 'Douillet', 'Killian', 'kdouillet@gmail.com', '$2y$10$ZQe2PES6/XkKqydm7C16MeKu9e29dfCo/7ZGZYGXhtOzPqOHoPZU6', '0786683089');

CREATE TABLE IF NOT EXISTS `contacts` (
  `id_contact` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(25) COLLATE utf8mb4_general_ci NOT NULL,
  `date` datetime NOT NULL,
  `id_formateur` int DEFAULT NULL,
  `prenom` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `message` text COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id_contact`),
  KEY `fk_formateur` (`id_formateur`),
  CONSTRAINT `fk_formateur` FOREIGN KEY (`id_formateur`) REFERENCES `formateurs` (`id_formateur`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `formateurs_centres` (
  `id_formateur` int NOT NULL,
  `id_centre` int NOT NULL,
  PRIMARY KEY (`id_formateur`,`id_centre`),
  KEY `id_centre` (`id_centre`),
  CONSTRAINT `formateurs_centres_ibfk_1` FOREIGN KEY (`id_formateur`) REFERENCES `formateurs` (`id_formateur`),
  CONSTRAINT `formateurs_centres_ibfk_2` FOREIGN KEY (`id_centre`) REFERENCES `centres` (`id_centre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DELETE FROM `formateurs_centres`;
INSERT INTO `formateurs_centres` (`id_formateur`, `id_centre`) VALUES
	(1, 1),
	(1, 2),
	(2, 2);

CREATE TABLE IF NOT EXISTS `formations` (
  `id_formation` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(15) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id_formation`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

DELETE FROM `formations`;
INSERT INTO `formations` (`id_formation`, `nom`) VALUES
	(1, 'LP RGI');

CREATE TABLE IF NOT EXISTS `rdv` (
  `id_rdv` int NOT NULL AUTO_INCREMENT,
  `debut` datetime DEFAULT NULL,
  `fin` datetime DEFAULT NULL,
  `nom` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `prenom` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `email` varchar(25) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `telephone` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `id_formation` int DEFAULT NULL,
  `id_formateur` int NOT NULL,
  PRIMARY KEY (`id_rdv`),
  KEY `id_formation` (`id_formation`),
  KEY `id_formateur` (`id_formateur`),
  CONSTRAINT `rdv_ibfk_1` FOREIGN KEY (`id_formation`) REFERENCES `formations` (`id_formation`),
  CONSTRAINT `rdv_ibfk_2` FOREIGN KEY (`id_formateur`) REFERENCES `formateurs` (`id_formateur`)
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


