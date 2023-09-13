CREATE TABLE IF NOT EXISTS "TiAI_Assignment1_InputData_Large"."large_A"
(
    id character varying NOT NULL,
    lat_long geography NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "TiAI_Assignment1_InputData_Large"."large_B"
(
    id character varying NOT NULL,
    lat_long geography NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "TiAI_Assignment1_InputData_Large"."large_C"
(
    id character varying NOT NULL,
    lat_long geography NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "TiAI_Assignment1_InputData_Large"."large_D"
(
    id character varying NOT NULL,
    lat_long geography NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "TiAI_Assignment1_InputData_Large"."large_E" 
(
    id character varying NOT NULL,
    lat_long geography NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS "TiAI_Assignment1_InputData_Large"."large_A" OWNER to postgres;
ALTER TABLE IF EXISTS "TiAI_Assignment1_InputData_Large"."large_B" OWNER to postgres;
ALTER TABLE IF EXISTS "TiAI_Assignment1_InputData_Large"."large_C" OWNER to postgres;
ALTER TABLE IF EXISTS "TiAI_Assignment1_InputData_Large"."large_D" OWNER to postgres;
ALTER TABLE IF EXISTS "TiAI_Assignment1_InputData_Large"."large_E" OWNER to postgres;