CREATE TABLE Circuit (
    CircuitID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    City VARCHAR(100) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    Latitude DECIMAL(9,6) CHECK (Latitude BETWEEN -90 AND 90),
    Longitude DECIMAL(9,6) CHECK (Longitude BETWEEN -180 AND 180)
);

CREATE TABLE Race (
    RaceID SERIAL PRIMARY KEY,
    CircuitID INT NOT NULL REFERENCES Circuit(CircuitID) ON DELETE CASCADE,
    Year INT NOT NULL,
    Round INT NOT NULL,
    Name VARCHAR(100) NOT NULL,
    Date DATE NOT NULL,
    Time TIME,
    FP1_Date DATE,
    FP1_Time TIME,
    FP2_Date DATE,
    FP2_Time TIME,
    FP3_Date DATE,
    FP3_Time TIME,
    Qualifying_Date DATE,
    Qualifying_Time TIME,
    Sprint_Date DATE,
    Sprint_Time TIME,
    Weather VARCHAR(50),
    CONSTRAINT unique_race_year_round UNIQUE (Year, Round)
);

CREATE TABLE Constructor (
    ConstructorID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Nationality VARCHAR(50) NOT NULL
);

CREATE TABLE Driver (
    DriverID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Number INT CHECK (Number BETWEEN 1 AND 99),
    Nationality VARCHAR(50) NOT NULL,
    DOB DATE NOT NULL CHECK (DOB <= CURRENT_DATE)
);

CREATE TABLE Lap (
    LapID SERIAL PRIMARY KEY,
    RaceID INT NOT NULL REFERENCES Race(RaceID) ON DELETE CASCADE,
    DriverID INT NOT NULL REFERENCES Driver(DriverID) ON DELETE CASCADE,
    ConstructorID INT NOT NULL REFERENCES Constructor(ConstructorID) ON DELETE CASCADE,
    LapNumber INT NOT NULL CHECK (LapNumber > 0),
    Position INT NOT NULL CHECK (Position BETWEEN 1 AND 20),
    LapTime INTERVAL NOT NULL CHECK (LapTime > '00:00:00'),
    CONSTRAINT unique_lap_entry UNIQUE (RaceID, DriverID, ConstructorID, LapNumber)
);

CREATE TABLE Pitstop (
    PitstopID SERIAL PRIMARY KEY,
    LapID INT UNIQUE NOT NULL REFERENCES Lap(LapID) ON DELETE CASCADE,
    Time TIME NOT NULL,
    Duration INTERVAL NOT NULL CHECK (Duration > '00:00:00')
);

CREATE TABLE QualifyingResults (
    RaceID INT NOT NULL REFERENCES Race(RaceID) ON DELETE CASCADE,
    DriverID INT NOT NULL REFERENCES Driver(DriverID) ON DELETE CASCADE,
    ConstructorID INT NOT NULL REFERENCES Constructor(ConstructorID) ON DELETE CASCADE,
    Position INT NOT NULL CHECK (Position BETWEEN 1 AND 20),
    Q1 INTERVAL,
    Q2 INTERVAL,
    Q3 INTERVAL,
    PRIMARY KEY (RaceID, DriverID, ConstructorID),
    CONSTRAINT qualifying_sessions_order CHECK (
        (Q2 IS NULL OR Q1 IS NOT NULL) AND
        (Q3 IS NULL OR Q2 IS NOT NULL)
    )
);

CREATE TABLE SprintResults (
    RaceID INT NOT NULL REFERENCES Race(RaceID) ON DELETE CASCADE,
    DriverID INT NOT NULL REFERENCES Driver(DriverID) ON DELETE CASCADE,
    ConstructorID INT NOT NULL REFERENCES Constructor(ConstructorID) ON DELETE CASCADE,
    Duration INTERVAL CHECK (Duration > '00:00:00'),
    Grid INT NOT NULL CHECK (Grid BETWEEN 1 AND 20),
    Position INT NOT NULL CHECK (Position BETWEEN 1 AND 20),
    Points INT NOT NULL CHECK (Points >= 0),
    PRIMARY KEY (RaceID, DriverID, ConstructorID)
);

CREATE TABLE RaceResults (
    RaceID INT NOT NULL REFERENCES Race(RaceID) ON DELETE CASCADE,
    DriverID INT NOT NULL REFERENCES Driver(DriverID) ON DELETE CASCADE,
    ConstructorID INT NOT NULL REFERENCES Constructor(ConstructorID) ON DELETE CASCADE,
    Position INT NOT NULL CHECK (Position BETWEEN 1 AND 20),
    Grid INT NOT NULL CHECK (Grid BETWEEN 1 AND 20),
    Points INT NOT NULL CHECK (Points >= 0),
    PRIMARY KEY (RaceID, DriverID, ConstructorID)
);

CREATE TABLE SeasonStandings (
    DriverID INT NOT NULL REFERENCES Driver(DriverID) ON DELETE CASCADE,
    ConstructorID INT NOT NULL REFERENCES Constructor(ConstructorID) ON DELETE CASCADE,
    Year INT NOT NULL,
    Points INT NOT NULL CHECK (Points >= 0),
    Rank INT NOT NULL CHECK (Rank BETWEEN 1 AND 20),
    PRIMARY KEY (Year, DriverID, ConstructorID)
);

CREATE TABLE ConstructorStandings (
    ConstructorID INT NOT NULL REFERENCES Constructor(ConstructorID) ON DELETE CASCADE,
    Year INT NOT NULL,
    Points INT NOT NULL CHECK (Points >= 0),
    Rank INT NOT NULL CHECK (Rank BETWEEN 1 AND 20),
    PRIMARY KEY (Year, ConstructorID)
);
