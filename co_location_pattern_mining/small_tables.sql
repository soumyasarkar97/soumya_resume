CREATE TABLE IF NOT EXISTS "TiAI_Assignment1_InputData_Small"."small_A"
(
    id character varying NOT NULL,
    lat_long geography NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "TiAI_Assignment1_InputData_Small"."small_B"
(
    id character varying NOT NULL,
    lat_long geography NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS "TiAI_Assignment1_InputData_Small"."small_C"
(
    id character varying NOT NULL,
    lat_long geography NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS "TiAI_Assignment1_InputData_Small"."small_A" OWNER to postgres;
ALTER TABLE IF EXISTS "TiAI_Assignment1_InputData_Small"."small_B" OWNER to postgres;
ALTER TABLE IF EXISTS "TiAI_Assignment1_InputData_Small"."small_C" OWNER to postgres;