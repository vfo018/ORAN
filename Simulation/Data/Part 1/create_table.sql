-- LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\output_handover_scenario_training1.csv' INTO TABLE training_set 
-- FIELDS TERMINATED BY ',' 
-- IGNORE 1 ROWS;

-- LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\output_handover_scenario_test1.csv' INTO TABLE testing_set 
-- FIELDS TERMINATED BY ',' 
-- IGNORE 1 ROWS;

CREATE TABLE training_set_cleaned
SELECT * FROM training_set GROUP BY t, cell_id ORDER BY t, cell_id;