from db import base, engine

# script to create db
base.metadata.create_all(engine)