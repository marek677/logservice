import sqlite3
from sqlite3 import Error
import json
import yaml
import datetime
import os
import re

conn = sqlite3.connect("logs.db")
c = conn.cursor()
sql_csources = """ CREATE TABLE IF NOT EXISTS log_sources (
									id integer PRIMARY KEY,
									name text NOT NULL
								); """
								
c.execute(sql_csources)
sql_clogs = """ CREATE TABLE IF NOT EXISTS logs (
									source_id integer,
									time text,
									level text,
									log text NOT NULL
								); """					
c.execute(sql_clogs)
c.execute("INSERT INTO log_sources VALUES (0,'test')")
c.execute("INSERT INTO log_sources VALUES (1,'ESIpuller')")
c.execute("INSERT INTO logs VALUES (0,'','DEBUG','TEST_DEBUG')")
c.execute("INSERT INTO logs VALUES (0,'','INFO','TEST_INFO')")
c.execute("INSERT INTO logs VALUES (0,'','WARNING','TEST_WARNING')")
c.execute("INSERT INTO logs VALUES (0,'','ERROR','TEST_ERROR')")
conn.commit()
conn.close()