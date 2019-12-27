-- -----------------------------------------------------------
-- recursive query that traverses edges looking for paths
-- that complete cycles. reverse engineered from something
-- I found in the postgres docs.
-- https://www.postgresql.org/docs/11/queries-with.html
-- -----------------------------------------------------------

WITH RECURSIVE search_graph(from_node, to_node, steps, path, cycle)
AS (
    SELECT e.from_node, e.to_node, 0, ARRAY[e.to_node], false
    FROM edges e
    UNION ALL
    SELECT e.from_node, e.to_node, sg.steps + 1,
           path || e.to_node, e.to_node = ANY(path)
    FROM edges e, search_graph sg
    WHERE e.from_node = sg.to_node AND NOT cycle
)
SELECT path, steps, cycle FROM search_graph WHERE cycle;
