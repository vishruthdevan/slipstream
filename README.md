# slipstream

Formula 1 Database Visualizer  

Made by:

| Name            | UNI      |
|-----------------|----------|
| Vishesh Arora   | vpa2112  |
| Vishruth Devan  | vd2461   |

## PostgreSQL Information

Account Name: vpa2112

## Application URL

<http://34.148.99.119:8111/>


## Feature details
### Features of original proposal
* Users can view information on races, driver, teams and results.
* Users can search for past races by selecting a year, and then clicking on a venue, and can access details like race winners and podium finishers.
*  Users can look up driver and teams stats, including season points and rankings.


## New features for F1 db
* Overlay of circuits on the world map based on their coordinates.
* Position distribution of drivers, showing how often drivers finish in each position across all races (how many times they finished 1st, 2nd, etc.). This shows their overall consistency. 

### Features not implemented
* Lap analysis feature - Since there are over 500 thousand rows of lap data, creating plots for all of them did not seem scalable. Instead, we let users search for a driver's lap data given a year and circuit.
* User personalisation - Since users can already search for their favourite drivers and teams conveniently, we feel this feature doesn't add a lot of value.


## Interesting Queries

### 1. Driver Detail Page (`/drivers/<driver_id>`)

The **Driver Detail Page**, which showcases detailed information and statistics about a specific Formula 1 driver. This page demonstrates an interaction between user input (the driver's ID in the URL as a query paramerter) and multiple SQL queries that collectively provide a comprehensive profile of the driver.

#### Page Purpose and Use

The page is designed to give fans or analysts a full snapshot of a driver's career, including personal details (name, nationality, number), performance stats (wins, podiums, total points), and a dynamic visualization (the D3.js-powered position distribution chart). It supports data-driven storytelling by pulling from several relational tables, making it engaging.

#### Relation to Database Operations

When a user navigates to `/drivers/<driver_id>/`, the `<driver_id>` is passed into several SQL queries to extract a wide range of data:

- **Driver Basics:** A simple lookup returns basic personal information.
- **Podium & Points Stats:** Aggregate functions (`COUNT`, `SUM`) gather how often the driver finished on the podium and total points scored.
- **Wins:** Another aggregate counts how many times the driver finished 1st.
- **Race Performance:** A detailed list of all races participated in by the driver, showing position and points per race.
- **Laps Driven:** Uses `SUM(lapid)` to calculate total laps driven.
- **Best Performance:** A particularly interesting query that combines `MIN(position)` with `ORDER BY points DESC` to extract a nuanced "best performance" by both place and race importance.
- **Position Distribution:** Prepares grouped data for a histogram, enabling the D3.js chart on the frontend.

#### Why It’s Interesting

This page stands out due to how it weaves together multiple types of data operations: aggregation, filtering, grouping, and ordering — all personalized dynamically based on the `driver_id`. It showcases how a single route can query different aspects of a normalized schema and compile the results into a cohesive, interactive experience.  

The use of the D3.js chart driven by SQL data is also notable — it bridges backend and frontend cleanly, turning raw data into a visual story.

---

### 2. Circuits & Circuit Detail Pages

The **Circuits Page** and **Circuit Detail Page** are two connected parts of the F1 application that together provide an immersive way to explore circuits across the world and analyze the historical performance data tied to each track.

### Circuits Page (`/circuits/`)

#### Page Purpose and Use

This page presents a **fullscreen interactive world map** displaying all F1 circuits using red dots, with tooltips and labels. Users can **hover, zoom, and click** on any circuit to be redirected to its detail page. It's an entry point for visually exploring circuits by location.

#### Relation to Database Operations

When the circuits page is loaded, a query fetches all circuits from the `circuit` table:

- Retrieves each circuit’s `circuitid`, `name`, `city`, `country`, `latitude`, and `longitude`.
- The data is converted to JSON format and passed to the frontend to be used with D3.js.
- No joins or aggregations are needed—just a full scan of the `circuit` table to populate the map.

This provides the geospatial basis for plotting each circuit on the world map with accurate coordinates.

#### Why It’s Interesting

- Uses geographic visualization to turn raw location data into an engaging UI.
- Introduces a spatial dimension to circuit data, allowing users to explore by geography instead of a static list.
- Builds a bridge between backend data and frontend interaction with D3-powered zoom, pan, and click-to-navigate functionality.

### Circuit Detail Page (`/circuits/<circuit_id>/`)

#### Page Purpose and Use

This page displays a comprehensive profile of a selected circuit. It includes:

- Basic location info (city, country, coordinates)
- Top 3 constructors and drivers by number of wins at that circuit
- A list of all races ever held there, sorted by year

Users can click on constructors, drivers, or races to explore further details.

#### Relation to Database Operations

When a user navigates to `/circuits/<circuit_id>/`, the `<circuit_id>` is injected into multiple SQL queries that extract both static and dynamic information:

- **Circuit Basics**: A straightforward lookup in the `circuit` table returns the name, city, country, and coordinates.
  
- **Top Constructors**: A join between `raceresults`, `race`, and `constructor` identifies constructors who won (position = 1) races at this circuit. Uses:
  - `COUNT(res.raceid)` to tally wins.
  - `GROUP BY` on constructor ID and name.
  - `ORDER BY wins DESC` with a `LIMIT 3` to show the most dominant teams.

- **Top Drivers**: Similar logic joins `raceresults`, `race`, and `driver`, counting how many times each driver won at the circuit. Uses:
  - `CONCAT` to display full driver names.
  - `GROUP BY` across first/last names and IDs.
  - `ORDER BY` and `LIMIT` to isolate top 3 performers.

- **Races at Circuit**: A query on the `race` table fetches all races held at this circuit, returning `raceid`, `year`, and `name`, sorted descending by year for recency.

Each of these queries uses the `circuitid` as a filter to target results to the selected track.

#### Why It’s Interesting

- Uses data aggregation and filtering to turn race history into insights.
- Provides meaningful context by showing which teams and drivers have historically dominated each track.
- Enables further exploration through clickable rows that link to driver, constructor, or race pages.
- Offers a **layered experience**—from high-level map clicks to in-depth analytics.
- Supports **interactive data storytelling**: a user can move from global (world map) to local (circuit) to individual (race or driver) in just a few clicks.

### Connection Between the Pages

These two pages form a natural and intuitive flow:

1. **Start on the world map**, exploring circuits visually.
2. **Click a circuit marker** to dive into its rich performance history.
3. **Discover dominant drivers, constructors, and specific races**, all filtered to that location.

This blend of **interactive design**, **database-driven insights**, and **seamless navigation** makes the circuit experience not only functional but compelling for users interested in the sport’s legacy and geography.

---

## Changes in the Database after 2nd Meeting

### Relaxed Constraints

To accommodate real-world data scenarios, we had to relax two constraints:

1. **Position INT CHECK (Position BETWEEN 1 AND 20)**  
   - **Change:** Removed the `NOT NULL` constraint on the `Position` attribute.  
   - **Reason:** There are instances where a driver might not finish the race. Allowing `NULL` values ensures that such situations do not interfere with statistical collection.

2. **Grid INT NOT NULL CHECK (Grid BETWEEN 0 AND 20)**  
   - **Change:** Updated the allowed range to include `0`.  
   - **Reason:** In rare cases, a driver may start from the pit lane. For such cases, the `Grid` value is set to `0`.

### Trigger to Prevent Driver Number Conflicts

To ensure unique driver numbers within the same season, we added the following trigger and function:

#### PostgreSQL Function

```sql
CREATE FUNCTION check_driver_number_conflict()
RETURNS TRIGGER AS $$
DECLARE
    new_driver_number INT;
BEGIN
    -- Get the number of the driver being added/updated
    SELECT Number INTO new_driver_number
    FROM Driver
    WHERE DriverID = NEW.DriverID;

    -- Check for any other driver in the same season with the same number
    IF EXISTS (
        SELECT 1
        FROM SeasonStandings ss
        JOIN Driver d ON ss.DriverID = d.DriverID
        WHERE ss.Year = NEW.Year
          AND d.Number = new_driver_number
          AND ss.DriverID != NEW.DriverID
    ) THEN
        RAISE EXCEPTION 'Driver number conflict: Another driver already has number % in season %', new_driver_number, NEW.Year;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

#### Trigger Definition

```sql
CREATE TRIGGER trg_check_driver_number_conflict
BEFORE INSERT OR UPDATE ON SeasonStandings
FOR EACH ROW
EXECUTE FUNCTION check_driver_number_conflict();
```
