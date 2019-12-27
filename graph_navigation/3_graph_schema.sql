-- -----------------------------------------------------------
-- clean up previous schema ----------------------------------
-- -----------------------------------------------------------
DROP TABLE IF EXISTS edges;
DROP TABLE IF EXISTS nodes;
DROP TABLE IF EXISTS graphs;
DROP SEQUENCE IF EXISTS graphs_pkid_seq;

-- -----------------------------------------------------------
-- create new schema -----------------------------------------
-- -----------------------------------------------------------
CREATE SEQUENCE graphs_pkid_seq;

-- I chose to add another pkid column here (in addition to id)
-- as I felt uncomfortable making a varchar primary key on a
-- table that I anticipated was going to have a lot of joins.
-- It could be removed, but there's no reason to at this point,
-- though the id column is relatively useless now.
CREATE TABLE graphs(
    pkid INTEGER DEFAULT nextval('graphs_pkid_seq') PRIMARY KEY,
    id VARCHAR NOT NULL,
    name VARCHAR NOT NULL
);

-- composite primary key here so that different graphs can have
-- nodes with equal ids without conflict.
CREATE TABLE nodes(
    graph_pkid INTEGER REFERENCES graphs(pkid),
    id VARCHAR,
    name VARCHAR NOT NULL,
    PRIMARY KEY (graph_pkid, id)
);

-- multiple foreign keys to ensure linked nodes cannot be deleted
-- without breaking the constraints, and no meaningless edges can
-- be added. Arguably this should be handled by the business logic,
-- but since we don't have a backend, this will do here.
CREATE TABLE edges(
    graph_pkid INTEGER,
    id VARCHAR,
    from_node VARCHAR,
    to_node VARCHAR,
    cost FLOAT NOT NULL DEFAULT 0,
    FOREIGN KEY (graph_pkid, from_node) REFERENCES nodes(graph_pkid, id),
    FOREIGN KEY (graph_pkid, to_node) REFERENCES nodes(graph_pkid, id),
    PRIMARY KEY (graph_pkid, id)
);

-- -----------------------------------------------------------
-- insert sample data ----------------------------------------
-- -----------------------------------------------------------
INSERT INTO graphs(id, name) VALUES
    ('g1', 'graph001'), ('g2', 'graph002');

-- second graph included to test constraints
INSERT INTO nodes(graph_pkid, id, name) VALUES
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'a', 'A name'),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'b', 'B name'),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'c', 'C name'),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'd', 'D name'),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'e', 'E name'),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'f', 'F name'),
    ((SELECT pkid FROM graphs WHERE id = 'g2'), 'b', 'B name'),
    ((SELECT pkid FROM graphs WHERE id = 'g2'), 'c', 'C name'),
    ((SELECT pkid FROM graphs WHERE id = 'g2'), 'z', 'Z name');

INSERT INTO edges(graph_pkid, id, from_node, to_node, cost) VALUES
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'a1', 'a', 'b', 0),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'a2', 'a', 'c', 2),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'b1', 'b', 'c', 1),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'd1', 'd', 'a', 0),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'd2', 'd', 'e', 2),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'e1', 'e', 'f', 1),
    ((SELECT pkid FROM graphs WHERE id = 'g1'), 'f1', 'f', 'd', 2);