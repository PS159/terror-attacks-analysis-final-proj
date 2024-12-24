from sqlalchemy import create_engine



CONN_URI = 'postgresql://postgres:LightAndMic!@localhost:5432/trror_attacks_anlayze'

engine = create_engine(CONN_URI)

