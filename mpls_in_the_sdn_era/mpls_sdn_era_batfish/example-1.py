import pandas as pd
from pybatfish.client.commands import *
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *
from pybatfish.question import *
from pybatfish.question import bfq

bf_session.host = "localhost"

bf_set_network("mplsinthesdnera")

SNAPSHOT_DIR = "snapshots/mplsinthesdnera/"

bf_init_snapshot(SNAPSHOT_DIR, name="snapshot-2021-03-22", overwrite=True)
