CREATE DATABASE militarydb;

-- Use the database
USE militarydb;

-- Create tables
CREATE TABLE Firearm (
    SerialNumber INT PRIMARY KEY AUTO_INCREMENT,
    Make VARCHAR(50),
    Model VARCHAR(50),
    Caliber VARCHAR(10),
    Weight DECIMAL(10, 2),
    Status VARCHAR(20)
);

CREATE TABLE Soldier (
    SoldierID INT PRIMARY KEY AUTO_INCREMENT,
    SoldierRank VARCHAR(20),
    Name VARCHAR(100),
    DateOfBirth DATE,
    Unit VARCHAR(50),
    DutyStatus VARCHAR(20)
);

CREATE TABLE MaintenanceRecord (
    MaintenanceRecordID INT PRIMARY KEY AUTO_INCREMENT,
    FirearmSerialNumber INT,
    DateOfMaintenance DATE,
    Type VARCHAR(50),
    Description TEXT,
    MaintenanceCost DECIMAL(10, 2),
    FOREIGN KEY (FirearmSerialNumber) REFERENCES Firearm(SerialNumber)
);

CREATE TABLE FirearmUsageRecord (
    RecordID INT PRIMARY KEY AUTO_INCREMENT,
    FirearmSerialNumber INT,
    SoldierID INT,
    DateOfUsage DATE,
    Purpose VARCHAR(100),
    Location VARCHAR(100),
    TemperatureDuringUsage DECIMAL(5, 2),
    WeatherConditions VARCHAR(100),
    FOREIGN KEY (FirearmSerialNumber) REFERENCES Firearm(SerialNumber),
    FOREIGN KEY (SoldierID) REFERENCES Soldier(SoldierID)
);

-- Create the Ammunition table
CREATE TABLE Ammunition (
    AmmunitionID INT PRIMARY KEY AUTO_INCREMENT,
    Caliber VARCHAR(10),
    QuantityInStock INT,
    Manufacturer VARCHAR(50),
    DateOfAcquisition DATE,
    Type VARCHAR(50)
);

-- Create the MaintenanceItem table
CREATE TABLE MaintenanceItem (
    MaintenanceItemID INT PRIMARY KEY AUTO_INCREMENT,
    DateOfItem DATE,
    Description TEXT,
    Cost DECIMAL(10, 2),
    MaintenanceRecordID INT,
    FOREIGN KEY (MaintenanceRecordID) REFERENCES MaintenanceRecord(MaintenanceRecordID)
);

-- Create the AmmunitionLot table
CREATE TABLE AmmunitionLot (
    AmmunitionLotID INT PRIMARY KEY AUTO_INCREMENT,
    LotNumber VARCHAR(20),
    QuantityInStock INT,
    DateOfManufacture DATE,
    AmmunitionID INT,
    FOREIGN KEY (AmmunitionID) REFERENCES Ammunition(AmmunitionID)
);


-- Create the FirearmAccessories table
CREATE TABLE FirearmAccessories (
    AccessoryID INT PRIMARY KEY AUTO_INCREMENT,
    FirearmSerialNumber INT,
    AccessoryType VARCHAR(50),
    Manufacturer VARCHAR(50),
    Model VARCHAR(50),
    Compatibility VARCHAR(100),
    QuantityInStock INT,
    FOREIGN KEY (FirearmSerialNumber) REFERENCES Firearm(SerialNumber)
);

-- Create the Armory table
CREATE TABLE Armory (
    ArmoryID INT PRIMARY KEY AUTO_INCREMENT,
    Location VARCHAR(100),
    Capacity INT,
    ArmorerInCharge VARCHAR(100),
    SecurityLevel VARCHAR(50),
    SurveillanceCameras INT
);

-- Create the TrainingExercise table
CREATE TABLE TrainingExercise (
    ExerciseID INT PRIMARY KEY AUTO_INCREMENT,
    ExerciseName VARCHAR(100),
    Date DATE,
    Description TEXT,
    Duration INT,
    WeatherConditions VARCHAR(100),
    TrainingType VARCHAR(50)
);

-- Create other tables (Ammunition, MaintenanceItem, AmmunitionLot, Soldier, FirearmAccessories, Armory, TrainingExercise) similarly

-- Create foreign key relationships for other tables
-- FirearmAccessories
ALTER TABLE FirearmAccessories
ADD CONSTRAINT FK_FirearmAccessories_Firearm
FOREIGN KEY (FirearmSerialNumber)
REFERENCES Firearm(SerialNumber);

-- MaintenanceRecord
ALTER TABLE MaintenanceRecord
ADD CONSTRAINT FK_MaintenanceRecord_Firearm
FOREIGN KEY (FirearmSerialNumber)
REFERENCES Firearm(SerialNumber);

-- FirearmUsageRecord
ALTER TABLE FirearmUsageRecord
ADD CONSTRAINT FK_FirearmUsageRecord_Firearm
FOREIGN KEY (FirearmSerialNumber)
REFERENCES Firearm(SerialNumber);

ALTER TABLE FirearmUsageRecord
ADD CONSTRAINT FK_FirearmUsageRecord_Soldier
FOREIGN KEY (SoldierID)
REFERENCES Soldier(SoldierID);

-- MaintenanceItem
ALTER TABLE MaintenanceItem
ADD CONSTRAINT FK_MaintenanceItem_MaintenanceRecord
FOREIGN KEY (MaintenanceRecordID)
REFERENCES MaintenanceRecord(MaintenanceRecordID);

-- AmmunitionLot
ALTER TABLE AmmunitionLot
ADD CONSTRAINT FK_AmmunitionLot_Ammunition
FOREIGN KEY (AmmunitionID)
REFERENCES Ammunition(AmmunitionID);


-- Create procedures and functions as needed
DELIMITER $$

CREATE PROCEDURE AddFirearm(
    IN p_Make VARCHAR(50),
    IN p_Model VARCHAR(50),
    IN p_Caliber VARCHAR(10),
    IN p_Weight DECIMAL(10, 2),
    IN p_Status VARCHAR(20)
)
BEGIN
    INSERT INTO Firearm (Make, Model, Caliber, Weight, Status)
    VALUES (p_Make, p_Model, p_Caliber, p_Weight, p_Status);
END$$

DELIMITER ;

-- Add more procedures and functions as needed

DELIMITER $$

CREATE PROCEDURE UpdateMaintenanceRecord(
    IN p_MaintenanceRecordID INT,
    IN p_Type VARCHAR(50),
    IN p_Description TEXT,
    IN p_MaintenanceCost DECIMAL(10, 2)
)
BEGIN
    UPDATE MaintenanceRecord
    SET Type = p_Type, Description = p_Description, MaintenanceCost = p_MaintenanceCost
    WHERE MaintenanceRecordID = p_MaintenanceRecordID;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE GetSoldierInformation(
    IN p_SoldierID INT
)
BEGIN
    SELECT * FROM Soldier
    WHERE SoldierID = p_SoldierID;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE AddMaintenanceItem(
    IN p_DateOfItem DATE,
    IN p_Description TEXT,
    IN p_Cost DECIMAL(10, 2),
    IN p_MaintenanceRecordID INT
)
BEGIN
    INSERT INTO MaintenanceItem (DateOfItem, Description, Cost, MaintenanceRecordID)
    VALUES (p_DateOfItem, p_Description, p_Cost, p_MaintenanceRecordID);
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE UpdateAmmunition(
    IN p_AmmunitionID INT,
    IN p_QuantityInStock INT
)
BEGIN
    UPDATE Ammunition
    SET QuantityInStock = p_QuantityInStock
    WHERE AmmunitionID = p_AmmunitionID;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE GetAmmunitionLotInformation(
    IN p_AmmunitionLotID INT
)
BEGIN
    SELECT * FROM AmmunitionLot
    WHERE AmmunitionLotID = p_AmmunitionLotID;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE AddArmory(
    IN p_Location VARCHAR(100),
    IN p_Capacity INT,
    IN p_ArmorerInCharge VARCHAR(100),
    IN p_SecurityLevel VARCHAR(50),
    IN p_SurveillanceCameras INT
)
BEGIN
    INSERT INTO Armory (Location, Capacity, ArmorerInCharge, SecurityLevel, SurveillanceCameras)
    VALUES (p_Location, p_Capacity, p_ArmorerInCharge, p_SecurityLevel, p_SurveillanceCameras);
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER TrainingExerciseNotification
BEFORE INSERT ON TrainingExercise
FOR EACH ROW
BEGIN
    DECLARE max_duration INT;
    SET max_duration = 120; -- Set the maximum duration threshold in minutes

    IF NEW.Duration > max_duration THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Training exercise duration exceeds the maximum allowed duration.';
    END IF;
END$$

DELIMITER ;
