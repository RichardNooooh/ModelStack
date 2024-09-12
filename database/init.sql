CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS models
(
    pk          SERIAL PRIMARY KEY,
    id          UUID DEFAULT uuid_generate_v4() NOT NULL,
    model       JSONB,          -- useful for GET requests
    is_trained  BOOLEAN DEFAULT FALSE NOT NULL,
    file_path   VARCHAR(128) NOT NULL
);

INSERT INTO models (model, file_path) VALUES 
--     ('{
--         "name":"fake_model1", 
--         "input_shape": [28, 28], 
--         "layers": [{"layer_type": "Linear", "size": 3}],
--         "output_shape": 10
--     }', '/fake_model_path_1/'),
--     ('{
--         "name":"fake_model2", 
--         "input_shape": [64, 64], 
--         "layers": [{"layer_type": "Conv2d", "num_channels": 3, "kernel": 2}],
--         "output_shape": 10
--     }', '/fake_model_path_2/'),
--     ('{
--         "name":"fake_model3", 
--         "input_shape": [23, 23], 
--         "layers": [{"layer_type": "Linear", "size": 3},
--                     {"layer_type": "Conv2d", "num_channels": 4}],
--         "output_shape": 10
--     }', '/fake_model_path_3/');
;

CREATE TABLE IF NOT EXISTS datasets
(
    pk              SERIAL PRIMARY KEY,
    id              UUID DEFAULT uuid_generate_v4() NOT NULL,
    name            VARCHAR(64) NOT NULL
    -- dataset_path    VARCHAR(128) NOT NULL
);

INSERT INTO datasets (name) VALUES ('mnist');

CREATE TYPE JOB_STATUS AS ENUM ('pending', 'running', 'cancelled', 'done', 'error');

CREATE TABLE IF NOT EXISTS jobs
(
    pk              serial PRIMARY KEY,
    id              UUID DEFAULT uuid_generate_v4() NOT NULL,
    model_id        UUID NOT NULL,
    dataset_name    VARCHAR(64) NOT NULL,
    parameters      JSONB NOT NULL,
    job_status      JOB_STATUS DEFAULT 'pending' NOT NULL,
    start_time      timestamp DEFAULT (NOW() AT TIME ZONE 'utc') NOT NULL
);

-- CREATE TABLE IF NOT EXISTS metrics
-- (
--     pk          serial PRIMARY KEY,
--     job_id      uuid DEFAULT uuid_generate_v4(),
-- );
;

-- 
-- {
--   "name": "test_model1",
--   "input_shape": [
--     28,
--     28
--   ],
--   "output_shape": 10,
--   "layers": [
--     {
--       "layer_type": "Flatten"
--     },
--     {
--       "layer_type": "Linear",
--       "size": 512
--     },
--     {
--       "layer_type": "Activation",
--       "activation": "ReLU"
--     },
--     {
--       "layer_type": "Linear",
--       "size": 512
--     },
--     {
--       "layer_type": "Activation",
--       "activation": "ReLU"
--     }
--   ]
-- }
;