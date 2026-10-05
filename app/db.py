"""Database connection. register_vector teaches psycopg to send/receive pgvector values."""

import psycopg
from pgvector.psycopg import register_vector

from app import config


def connect() -> psycopg.Connection:
    conn = psycopg.connect(config.DATABASE_URL)
    register_vector(conn)
    return conn
