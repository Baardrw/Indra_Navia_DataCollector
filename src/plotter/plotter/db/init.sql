-- CREATE TABLE wgs84 (
--     id INTEGER,
--     flight_key INTEGER NOT NULL,
--     lat REAL NOT NULL,
--     lon REAL NOT NULL,
--     alt REAL NOT NULL,
--     stamp INTEGER NOT NULL,
--     speed REAL NOT NULL,
--     bearing REAL NOT NULL,
--     PRIMARY KEY (id, flight_key)
-- );

-- INSERT INTO wgs84 (id, flight_key, lat, lon, alt, stamp, speed, bearing)
-- VALUES (1, 1234, 37.7749, -122.4194, 5000.0, 1620638620, 450.0, 180.0);

SELECT *
FROM wgs84
WHERE flight_key = 1234;