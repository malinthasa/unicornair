
CREATE STREAM engine_temperature_stream (
    temperature_celsius DOUBLE,
    timestamp STRING,
    aircraft_id STRING,
    flight_number STRING,
    altitude_ft INT,
    status STRING
) WITH (
    KAFKA_TOPIC = 'engine_temperature_data',
    VALUE_FORMAT = 'JSON'
);

SET 'auto.offset.reset' = 'latest';
SELECT * FROM engine_temperature_stream EMIT CHANGES;

-- AVG temp
SELECT aircraft_id, AVG(temperature_celsius) AS avg_temp
FROM engine_temperature_stream
GROUP BY aircraft_id
EMIT CHANGES;

-- Count messages
SELECT aircraft_id, COUNT(*) AS event_count
FROM engine_temperature_stream
GROUP BY aircraft_id
EMIT CHANGES;

-- Over window
SELECT aircraft_id, 
       WINDOWSTART AS start_time, 
       WINDOWEND AS end_time, 
       AVG(temperature_celsius) AS avg_temp
FROM engine_temperature_stream
WINDOW TUMBLING (SIZE 5 MINUTES)
GROUP BY aircraft_id
EMIT CHANGES;


CREATE TABLE avg_engine_temperature_table AS
>SELECT 
>    aircraft_id,
>    TIMESTAMPTOSTRING(WINDOWSTART, 'yyyy-MM-dd HH:mm:ss', 'UTC') AS window_start,
>    TIMESTAMPTOSTRING(WINDOWEND, 'yyyy-MM-dd HH:mm:ss', 'UTC') AS window_end,
>    AVG(temperature_celsius) AS avg_temp
>FROM engine_temperature_stream
>WINDOW TUMBLING (SIZE 1 MINUTE)
>GROUP BY aircraft_id
>EMIT CHANGES;

