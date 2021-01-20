CREATE TABLE `Entry` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `concept` TEXT NOT NUll,
    `entry` TEXT NOT NULL,
    `date` DATE,
    `mood_id` INTEGER,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Mood` (
    `id` INTEGER,
    `label` TEXT NOT NULL
)

INSERT INTO `Entry` VALUES (null, 'Hooks', 'confusing', '1598458543321', 1);
INSERT INTO `Entry` VALUES (null, 'GET', 'get data', '1598458548239', 2);
INSERT INTO `Entry` VALUES (null, 'POST', 'post data', '1598458548249', 1);

INSERT INTO `Mood` VALUES (null, "sad");
INSERT INTO `Mood` VALUES (null, "happy");

