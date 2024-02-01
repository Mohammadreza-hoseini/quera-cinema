use unruffled_lalande;
CREATE TABLE `Comment` (
  `id` CHAR(36) PRIMARY KEY,
  `user_id` CHAR(36) NOT NULL ,
  `comment` text NOT NULL
);


CREATE TABLE `Movie` (
  `id` CHAR(36) PRIMARY KEY ,
  `name` varchar(255) UNIQUE NOT NULL,
  `average_rate` float DEFAULT -1, #-1: average not calculated
  `on_screen_count` int NOT NULL,
  `age_limit` int NOT NULL

);

CREATE TABLE `User` (
  `id` CHAR(36) PRIMARY KEY,
  `avatar` varchar(255) NOT NULL ,
  `username` varchar(255) UNIQUE NOT NULL ,
  `birth_date` timestamp NOT NULL,
  `phone_number` varchar(255) UNIQUE NOT NULL,
  `email` Varchar(255) UNIQUE NOT NULL,
  `password` varchar(255) DEFAULT 'None',
  `register_date` timestamp,
  `last_login` timestamp,
  `subscription` Enum('2', '3', '4') DEFAULT '2', # 2: bronze | 3: silver | 4: gold
  `bought_subscription_date` timestamp,
  `role` Enum('admin', 'user') NOT NULL
);

CREATE TABLE `MovieRateTable` (
  `movie_id` CHAR(36) NOT NULL ,
  `user_id` CHAR(36) NOT NULL ,
  `rate` Enum('1', '2', '3', '4', '5') NOT NULL,
   PRIMARY KEY (movie_id, user_id)
);

CREATE TABLE `TheaterRateTable` (
  `user_id` CHAR(36) NOT NULL ,
  `theater_id` CHAR(36) NOT NULL ,
  `rate` Enum('1', '2', '3', '4', '5') NOT NULL,
   PRIMARY KEY (theater_id, user_id)
);

CREATE TABLE `BackAccount` (
  `id` char(36) PRIMARY KEY,
  `user_id` CHAR(36) NOT NULL,
  `amount` int NOT NULL,
  `cvv2` int NOT NULL ,
  `password` varchar(255) NOT NULL
);

CREATE TABLE `Wallet` (
  `id` CHAR(36) PRIMARY KEY,
  `user_id` CHAR(36) NOT NULL ,
  `amount` int NOT NULL
);

CREATE TABLE `Theater` (
  `id` CHAR(36) PRIMARY KEY,
  `capacity` int NOT NULL ,
  `average_rate` float DEFAULT -1 #-1: average not calculated
);

CREATE TABLE `Sit` (
  `id` char(36) PRIMARY KEY,
  `theater_id` CHAR(36) NOT NULL ,
  `status` ENUM('0', '1') DEFAULT '0' # 0: empty | 1: full
);

CREATE TABLE `Schedule` (
  `id` CHAR(36) PRIMARY KEY,
  `movie_id` CHAR(36) NOT NULL ,
  `theater_id` CHAR(36) NOT NULL ,
  `on_screen_time` timestamp NOT NULL
);

CREATE TABLE `ticket` (
  `id` CHAR(36) PRIMARY KEY,
  `user_id` CHAR(36) NOT NULL,
  `schedule_id` CHAR(36) NOT NULL ,
  `sit_id` char(36) NOT NULL ,
  `price` int NOT NULL ,
  `bought_time` timestamp NOT NULL
);

ALTER TABLE `Comment` ADD CONSTRAINT fk_user_comment FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ;

ALTER TABLE `MovieRateTable` ADD CONSTRAINT  fk_Mrate_movie FOREIGN KEY (`movie_id`) REFERENCES `Movie` (`id`) ON DELETE CASCADE ;

ALTER TABLE `MovieRateTable` ADD CONSTRAINT  fk_Mrate_user FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ;

ALTER TABLE `TheaterRateTable` ADD CONSTRAINT fk_Trate_user FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ;

ALTER TABLE `TheaterRateTable` ADD CONSTRAINT fk_Trate_theater FOREIGN KEY (`theater_id`) REFERENCES `Theater` (`id`) ON DELETE CASCADE ;

ALTER TABLE `BackAccount` ADD CONSTRAINT fk_bank_user FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ;

ALTER TABLE `Wallet` ADD CONSTRAINT fk_wallet_user FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ;

ALTER TABLE `Sit` ADD CONSTRAINT fk_sit_theater FOREIGN KEY (`theater_id`) REFERENCES `Theater` (`id`) ON DELETE CASCADE ;

ALTER TABLE `Schedule` ADD CONSTRAINT fk_schedule_movie FOREIGN KEY (`movie_id`) REFERENCES `Movie` (`id`) ON DELETE CASCADE ;

ALTER TABLE `Schedule` ADD CONSTRAINT fk_schedule_theater FOREIGN KEY (`theater_id`) REFERENCES `Theater` (`id`) ON DELETE CASCADE ;

ALTER TABLE `ticket` ADD CONSTRAINT fk_ticket_user FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE ;

ALTER TABLE `ticket` ADD CONSTRAINT fk_ticket_schedule FOREIGN KEY (`schedule_id`) REFERENCES `Schedule` (`id`) ON DELETE CASCADE ;

ALTER TABLE `ticket` ADD CONSTRAINT fk_ticket_sit FOREIGN KEY (`sit_id`) REFERENCES `Sit` (`id`) ON DELETE CASCADE ;
