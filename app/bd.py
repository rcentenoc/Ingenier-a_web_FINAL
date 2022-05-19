from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:@localhost/flaskmysql')

conn = engine.connect()

