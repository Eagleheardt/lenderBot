CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE Media (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, MediaType INTEGER NOT NULL DEFAULT 1, MediaCategory INTEGER NOT NULL DEFAULT 1, OwnerID TEXT NOT NULL, FullName TEXT NOT NULL, LongGame BIT NOT NULL DEFAULT 1, FOREIGN KEY (MediaType) REFERENCES MediaType(ID), FOREIGN KEY (MediaCategory) REFERENCES MediaCategory(ID), FOREIGN KEY (OwnerID) REFERENCES Users(SlackID));
CREATE TABLE IF NOT EXISTS "MediaCategory" (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`Name`	TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "MediaType" (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`Description`	TEXT NOT NULL UNIQUE
);
CREATE TABLE `Users` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`userName`	TEXT NOT NULL,
	`slackID`	TEXT NOT NULL UNIQUE,
	`directID`	TEXT NOT NULL,
	`IsAdmin`	BIT NOT NULL DEFAULT 0
);
CREATE TABLE `Insults` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`Line`	TEXT NOT NULL UNIQUE
);
CREATE TABLE `Facts` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`Line`	TEXT NOT NULL UNIQUE
);
CREATE TABLE Transactions (
'ID' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
'MediaID' INTEGER NOT NULL, 
'SlackID' TEXT NOT NULL, 
'CheckIN' DATE,
'CheckOUT' DATE,

FOREIGN KEY (MediaID) REFERENCES Media(ID),
FOREIGN KEY (SlackID) REFERENCES Users(SlackID)
);
