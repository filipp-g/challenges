# Graph Challenge
### Instructions
- install `python 3.7`
- create a virtualenv to not pollute system packages
  - `python3 -m venv env`
  - active env: `source env/bin/activate`
- `pip install psycopg2-binary` (regular `psycopg` package will work, but gives warnings about upcoming changes.)
- update `settings.conf` with postgres server details
- run files:
  1. 1_2_xml_parser.py
  2. 3_graph_schema.sql
  3. 4_cycle_detection.sql
  4. 5_json_backend.py
