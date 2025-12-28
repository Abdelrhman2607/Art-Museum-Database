DROP DATABASE IF EXISTS MUSEUM;
CREATE DATABASE MUSEUM;
USE MUSEUM;

DROP TABLE IF EXISTS ARTIST;
CREATE TABLE ARTIST (
    Name VARCHAR(255) PRIMARY KEY,
    MainStyle VARCHAR(255),
    DateBorn DATE,
    DateDied DATE,
    Description VARCHAR(255),
    Epoch VARCHAR(255),
    CountryCulture VARCHAR(255)
);

INSERT INTO ARTIST (Name, MainStyle, DateBorn, DateDied, Description, Epoch, CountryCulture) 
VALUES 
('Leonard da Vinci', 'Renaissance', '1452-04-15', '1519-05-02', 'Polymath of the High Renaissance', 'Renaissance', 'Italy'),
('Vincent van Gogh', 'Post-Impressionism', '1853-03-30', '1890-07-29', 'Dutch Post-Impressionist painter', 'Modern', 'Netherlands'),
('Michelangelo', 'Renaissance', '1475-03-06', '1564-02-18', 'Sculptor, painter, architect, and poet', 'Renaissance', 'Italy'),
('Auguste Rodin', 'Impressionism', '1840-11-12', '1917-11-17', 'French sculptor, founder of modern sculpture', 'Modern', 'France'),
('Pablo Picasso', 'Cubism', '1881-10-25', '1973-04-08', 'Spanish painter, sculptor, printmaker', 'Modern', 'Spain');

DROP TABLE IF EXISTS ART_OBJECT;
CREATE TABLE ART_OBJECT (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Year INT,
    Description VARCHAR(255),
    Style VARCHAR(255),
    Artist VARCHAR(255),
    FOREIGN KEY (Artist) 
        REFERENCES ARTIST(Name) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

INSERT INTO ART_OBJECT (ID, Title, Year, Description, Style, Artist) 
VALUES
(1, 'Mona Lisa', 1503, 'Portrait of Lisa Gherardini', 'Renaissance', 'Leonard da Vinci'),
(2, 'Starry Night', 1889, 'View from the east-facing window of his asylum room', 'Post-Impressionism', 'Vincent van Gogh'),
(3, 'David', 1504, 'Marble statue of a standing male nude', 'Renaissance', 'Michelangelo'),
(4, 'The Thinker', 1904, 'Bronze sculpture on a stone pedestal', 'Impressionism', 'Auguste Rodin'),
(5, 'Guernica', 1937, 'Large oil painting on canvas', 'Cubism', 'Pablo Picasso'),
(6, 'Vitruvian Man', 1490, 'Drawing accompanied by notes', 'Renaissance', 'Leonard da Vinci');

DROP TABLE IF EXISTS PAINTING;
CREATE TABLE PAINTING (
    ID INT PRIMARY KEY,
    DrawnOn VARCHAR(255),
    PaintType VARCHAR(255),
    FOREIGN KEY (ID) 
        REFERENCES ART_OBJECT(ID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

INSERT INTO PAINTING (ID, DrawnOn, PaintType) 
VALUES
(1, 'Poplar panel', 'Oil'),
(2, 'Canvas', 'Oil'),
(5, 'Canvas', 'Oil');

DROP TABLE IF EXISTS OTHER;
CREATE TABLE OTHER (
    ID INT PRIMARY KEY,
    Type VARCHAR(255) NOT NULL,
    FOREIGN KEY (ID) 
        REFERENCES ART_OBJECT(ID) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);

INSERT INTO OTHER (ID, Type) 
VALUES
(6, 'Drawing');

DROP TABLE IF EXISTS STATUE_SCULPTURE;
CREATE TABLE STATUE_SCULPTURE (
    ID INT PRIMARY KEY,
    Material VARCHAR(255),
    Height DECIMAL(6, 2),
    Weight DECIMAL(8, 2),
    Type VARCHAR(255) NOT NULL,
    FOREIGN KEY (ID) 
        REFERENCES ART_OBJECT(ID) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);

INSERT INTO STATUE_SCULPTURE (ID, Material, Height, Weight, Type) 
VALUES
(3, 'Marble', 517.00, 5660.00, 'Statue'),
(4, 'Bronze', 189.00, 700.00, 'Sculpture');

DROP TABLE IF EXISTS COLLECTION;
CREATE TABLE COLLECTION (
    Name VARCHAR(255) PRIMARY KEY,
    Type VARCHAR(255),
    Description VARCHAR(255),
    Phone VARCHAR(255),
    Contact VARCHAR(255),
    Address VARCHAR(255)
);

INSERT INTO COLLECTION (Name, Type, Description, Phone, Contact, Address) 
VALUES
('Louvre Museum', 'Museum', 'World''s largest art museum', '+33 1 40 20 53 17', 'Jean-Luc Martinez', 'Rue de Rivoli, 75001 Paris, France'),
('The Museum of Modern Art', 'Museum', 'Influential modern art museum', '+1 212 708 9400', 'Glenn D. Lowry', '11 W 53rd St, New York, NY 10019'),
('Museo Nacional del Prado', 'Museum', 'Main Spanish national art museum', '+34 913 30 28 00', 'Miguel Falomir', 'C. de Ruiz de Alarcón, 23, 28014 Madrid, Spain'),
('Galleria dell''Accademia', 'Museum', 'Art museum in Florence', '+39 055 238 8609', 'Cecilie Hollberg', 'Via Ricasoli, 58/60, 50122 Firenze FI, Italy');

DROP TABLE IF EXISTS ON_DISPLAY;
CREATE TABLE ON_DISPLAY (
    Object INT,
    ExhibitionName VARCHAR(255),
    StartDate DATE,
    EndDate DATE,
    PRIMARY KEY (Object, ExhibitionName),
    FOREIGN KEY (Object) 
        REFERENCES ART_OBJECT(ID) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);

INSERT INTO ON_DISPLAY (Object, ExhibitionName, StartDate, EndDate) 
VALUES
(1, 'Renaissance Masterpieces', '2023-01-01', '2023-12-31'),
(3, 'Renaissance Masterpieces', '2023-01-01', '2023-12-31'),
(2, 'Modern Art Revolution', '2024-01-15', '2024-06-15'),
(4, 'Modern Art Revolution', '2024-01-15', '2024-06-15'),
(5, 'Cubism & Beyond', '2024-07-01', '2024-12-31');

DROP TABLE IF EXISTS BORROWED;
CREATE TABLE BORROWED (
    Collection VARCHAR(255),
    Object INT NOT NULL,
    DateBorrowed DATE NOT NULL,
    DateReturned DATE,
    PRIMARY KEY (Collection, Object),
    FOREIGN KEY (Collection) 
        REFERENCES COLLECTION(Name) 
            ON DELETE RESTRICT 
            ON UPDATE CASCADE,
    FOREIGN KEY (Object) 
        REFERENCES ART_OBJECT(ID) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);

INSERT INTO BORROWED (Collection, Object, DateBorrowed, DateReturned) 
VALUES
('Museo Nacional del Prado', 5, '2023-06-01', '2023-09-01'),
('The Museum of Modern Art', 4, '2024-01-01', '2024-06-30');

DROP TABLE IF EXISTS PERMANENT;
CREATE TABLE PERMANENT (
    Object INT PRIMARY KEY,
    Status VARCHAR(255),
    Cost DECIMAL(12, 2),
    DateAcquired DATE,
    FOREIGN KEY (Object) 
        REFERENCES ART_OBJECT(ID) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE
);

INSERT INTO PERMANENT (Object, Status, Cost, DateAcquired) 
VALUES
(1, 'On Display', 850000000.00, '1797-01-01'),
(2, 'On Display', 100000000.00, '1941-01-01'),
(3, 'On Display', 0.00, '1873-01-01'),
(6, 'In Storage', 0.00, '1822-01-01');
