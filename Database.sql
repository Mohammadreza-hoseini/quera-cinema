CREATE TABLE Movie (
    id              CHAR(36)         NOT NULL PRIMARY KEY,
    name            VARCHAR(255)     NOT NULL,
    average_rate    FLOAT DEFAULT -1 NULL,
    on_screen_count INT              NOT NULL,
    age_limit       INT              NOT NULL,
    price           FLOAT          NOT NULL,

    CONSTRAINT name UNIQUE (name)
);

CREATE TABLE Theater
(
    id           CHAR(36)         NOT NULL PRIMARY KEY,
    capacity     INT              NOT NULL,
    average_rate FLOAT DEFAULT -1 NULL
);

CREATE TABLE Schedule
(
    id             CHAR(36)  NOT NULL PRIMARY KEY,
    movie_id       CHAR(36)  NOT NULL,
    theater_id     CHAR(36)  NOT NULL,
    on_screen_time TIMESTAMP NOT NULL,

    CONSTRAINT fk_schedule_movie
        FOREIGN KEY (movie_id) REFERENCES Movie (id)
            ON DELETE CASCADE,

    CONSTRAINT fk_schedule_theater
        FOREIGN KEY (theater_id) REFERENCES Theater (id)
            ON DELETE CASCADE
);

CREATE TABLE Sit
(
    id         CHAR(36)                    NOT NULL PRIMARY KEY,
    theater_id CHAR(36)                    NOT NULL,
    status     ENUM ('0', '1') DEFAULT '0' NULL,

    CONSTRAINT fk_sit_theater
        FOREIGN KEY (theater_id) REFERENCES Theater (id)
            ON DELETE CASCADE
);

CREATE TABLE User
(
    id                       CHAR(36)                            NOT NULL PRIMARY KEY,
    avatar                   VARCHAR(255)                        NOT NULL,
    username                 VARCHAR(255)                        NOT NULL,
    birth_date               TIMESTAMP                           NOT NULL,
    phone_number             VARCHAR(255)                        NOT NULL,
    email                    VARCHAR(255)                        NOT NULL,
    password                 VARCHAR(255)         DEFAULT 'None' NULL,
    register_date            TIMESTAMP                           NULL,
    last_login               TIMESTAMP                           NULL,
    subscription             ENUM ('2', '3', '4') DEFAULT '2'    NULL,
    bought_subscription_date TIMESTAMP                           NULL,
    role                     ENUM ('admin', 'user')              NOT NULL,
    logged_in                TINYINT(1)           DEFAULT 0      NOT NULL,

    CONSTRAINT email UNIQUE (email),
    CONSTRAINT phone_number UNIQUE (phone_number),
    CONSTRAINT username UNIQUE (username)
);

CREATE TABLE BankAccount
(
    id          CHAR(36)                            NOT NULL PRIMARY KEY,
    user_id     CHAR(36)                            NOT NULL,
    amount      DECIMAL                             NOT NULL,
    cvv2        INT                                 NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    password    VARCHAR(255)                        NOT NULL,
    card_number BIGINT                              NOT NULL,

    CONSTRAINT fk_bank_user
        FOREIGN KEY (user_id) REFERENCES User (id)
            ON DELETE CASCADE
);

CREATE TABLE Comment
(
    id         CHAR(36)                            NOT NULL PRIMARY KEY,
    user_id    CHAR(36)                            NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    comment    TEXT                                NOT NULL,
    CONSTRAINT fk_user_comment
        FOREIGN KEY (user_id) REFERENCES User (id)
            ON DELETE CASCADE
);

CREATE TABLE MovieRateTable
(
    movie_id CHAR(36)                       NOT NULL,
    user_id  CHAR(36)                       NOT NULL,
    rate     ENUM ('1', '2', '3', '4', '5') NOT NULL,

    PRIMARY KEY (movie_id, user_id),

    CONSTRAINT fk_Mrate_movie
        FOREIGN KEY (movie_id) REFERENCES Movie (id)
            ON DELETE CASCADE,

    CONSTRAINT fk_Mrate_user
        FOREIGN KEY (user_id) REFERENCES User (id)
            ON DELETE CASCADE
);

CREATE TABLE TheaterRateTable
(
    user_id    CHAR(36)                       NOT NULL,
    theater_id CHAR(36)                       NOT NULL,
    rate       ENUM ('1', '2', '3', '4', '5') NOT NULL,
    PRIMARY KEY (theater_id, user_id),

    CONSTRAINT fk_Trate_theater
        FOREIGN KEY (theater_id) REFERENCES Theater (id)
            ON DELETE CASCADE,

    CONSTRAINT fk_Trate_user
        FOREIGN KEY (user_id) REFERENCES User (id)
            ON DELETE CASCADE
);

CREATE TABLE Wallet
(
    id         CHAR(36)                            NOT NULL PRIMARY KEY,
    user_id    CHAR(36)                            NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,
    amount     DECIMAL                             NOT NULL,

    CONSTRAINT fk_wallet_user
        FOREIGN KEY (user_id) REFERENCES User (id)
            ON DELETE CASCADE
);

CREATE TABLE ticket
(
    id          CHAR(36)                            NOT NULL PRIMARY KEY,
    user_id     CHAR(36)                            NOT NULL,
    schedule_id CHAR(36)                            NOT NULL,
    sit_id      CHAR(36)                            NOT NULL,
    price       FLOAT                               NOT NULL,
    bought_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL,

    CONSTRAINT fk_ticket_schedule
        FOREIGN KEY (schedule_id) REFERENCES Schedule (id)
            ON DELETE CASCADE,

    CONSTRAINT fk_ticket_sit
        FOREIGN KEY (sit_id) REFERENCES Sit (id)
            ON DELETE CASCADE,

    CONSTRAINT fk_ticket_user
        FOREIGN KEY (user_id) REFERENCES User (id)
            ON DELETE CASCADE
);

