#!/usr/bin/env python
"""
A backend that receives JSON, queries the database for any or cheapest
paths, and sends back response.
"""

import json
import sys
import uuid
import psycopg2
from pg_conn_wrapper import connect

# reversed the query from 4_cycle_detection.py in order to get all paths that
# where not cycles, and then added the cost column to save another trip to
# the database when looking for cheapest trips.
all_paths_query = \
    """
        WITH RECURSIVE
            search_graph(from_node, to_node, steps, path, cycle, cost)
        AS (
            SELECT
                e.from_node, e.to_node, 0, ARRAY[e.to_node],
                false, ARRAY[0::FLOAT]
            FROM edges e
            UNION ALL
            SELECT e.from_node, e.to_node, sg.steps + 1,
                path || e.to_node, e.to_node = ANY(path), sg.cost || e.cost
            FROM edges e, search_graph sg
            WHERE e.from_node = sg.to_node AND NOT cycle
        )
        SELECT DISTINCT path, cost
        FROM search_graph
        WHERE NOT cycle AND steps > 0;
    """


# After pasting in complete JSON into stdin, send EOF by ctrl-d on Mac
# or ctl-z on Windows
def get_input_queries():
    """
    I took the liberty to preprocess the incoming JS object to make it valid
    JSON. Ideally the frontend would send standardized JSON so backend can
    focus on business logic.
    """
    processed_json = ''
    unprocessed_json = sys.stdin.readlines()
    for line in unprocessed_json:
        line = line.replace('[', '{').replace(']', '}')
        line = line.replace('paths', f'paths_{str(uuid.uuid4())[:4]}')
        line = line.replace('cheapest', f'cheapest_{str(uuid.uuid4())[:4]}')
        processed_json += line
    return json.loads(processed_json)['queries']


# def get_input_queries():
# """ helper method to load json from file instead of stdin """
#     with open('sample.json') as json_data:
#         processed_json = ''
#         for ln in json_data:
#             ln = ln.replace('[', '{').replace(']', '}')
#             ln = ln.replace('paths', f'paths_{str(uuid.uuid4())[:4]}')
#             ln = ln.replace('cheapest', f'cheapest_{str(uuid.uuid4())[:4]}')
#             processed_json += ln
#         return json.loads(processed_json)['queries']


def get_all_paths(cursor):
    cursor.execute(all_paths_query)
    return cursor.fetchall()


def items_match(list, a, b):
    return a in list and b in list and list.index(a) == 0


def get_filtered_paths(paths, start, end):
    """ filters matching paths plus sums up their cost """
    return [(x[0], sum(x[1])) for x in paths if items_match(x[0], start, end)]


def get_cheapest_path(paths):
    """ looks for cheapest path. if multiple match, takes quickest """
    lowest_val = min([x[1] for x in paths])
    cheapest = [x[0] for x in paths if x[1] == lowest_val]
    if len(cheapest) == 0:
        return False
    elif len(cheapest) > 1:
        quickest = min([len(x) for x in cheapest])
        return [x for x in cheapest if len(x) == quickest][0]
    else:
        return cheapest[0]


def process_queries(queries, paths):
    response = {'paths': [], 'cheapest': []}
    for key in queries.keys():
        start = queries[key]['start']
        end = queries[key]['end']
        filtered_paths = get_filtered_paths(paths, start, end)
        if key.startswith('paths'):
            result_paths = [x[0] for x in filtered_paths]
            path = {'from': start, 'to': end, 'paths': result_paths}
            response['paths'].append(path)
        elif key.startswith('cheapest'):
            result_cheapest = get_cheapest_path(filtered_paths)
            path = {'from': start, 'to': end, 'path': result_cheapest}
            response['cheapest'].append(path)
    return response


def send_json(response):
    json_response = json.dumps(response)
    print(json_response)


def main():
    conn = connect()
    cursor = conn.cursor()

    input_queries = get_input_queries()
    paths = get_all_paths(cursor)
    response = process_queries(input_queries, paths)
    send_json(response)

    cursor.close()
    conn.close()


main()
