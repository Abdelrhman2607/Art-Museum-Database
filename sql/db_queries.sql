-- @block
USE MUSEUM;

-- @block
-- 1) Show all tables and explain how they are related to one another (keys, triggers, etc.)
SHOW TABLES;

-- @block
-- Show all foreign keys and their relationships
SELECT 
    TABLE_NAME AS TableName, 
    COLUMN_NAME AS ColumnName, 
    REFERENCED_TABLE_NAME AS ReferencedTableName, 
    REFERENCED_COLUMN_NAME AS ReferencedColumnName
FROM 
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE 
WHERE 
    TABLE_SCHEMA = 'MUSEUM' 
    AND REFERENCED_TABLE_NAME IS NOT NULL;

-- @block
-- 2) A basic retrieval query
SELECT * FROM ARTIST;

-- @block
-- 3) A retrieval query with ordered results
SELECT Title, Year, Style, Artist 
FROM ART_OBJECT 
ORDER BY Year ASC;

-- @block
-- 4) A nested retrieval query
SELECT Title, Description 
FROM ART_OBJECT 
WHERE Artist IN (
    SELECT Name 
    FROM ARTIST 
    WHERE CountryCulture = 'Italy'
);

-- @block
-- 5) A retrieval query using joined tables
SELECT 
    ART_OBJECT.Title, 
    ART_OBJECT.Year, 
    ARTIST.Name AS ArtistName, 
    ARTIST.MainStyle AS ArtistStyle
FROM 
    ART_OBJECT
JOIN 
    ARTIST ON ART_OBJECT.Artist = ARTIST.Name;

-- @block
-- 6) An update operation with any necessary triggers
-- Correct the artist name
UPDATE ARTIST
SET Name = 'Leonardo da Vinci'
WHERE Name = 'Leonard da Vinci';
-- @block
-- Verify the update cascaded by checking the ART_OBJECT table
SELECT ART_OBJECT.Title, ART_OBJECT.Year, ART_OBJECT.Artist
FROM ART_OBJECT
WHERE ART_OBJECT.Artist = 'Leonardo da Vinci';

-- @block
-- 7) A deletion operation with any necessary triggers
-- Delete the ART_OBJECT with ID 1
DELETE FROM ART_OBJECT
WHERE ART_OBJECT.ID = 1;
-- @block
-- Verify the deletion. There should be no painting with ID 1 since it was deleted when the ART_OBJECT was deleted.
SELECT * FROM PAINTING 
WHERE ID = 1;
