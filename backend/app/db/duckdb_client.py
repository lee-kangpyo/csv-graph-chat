import duckdb
import os
from typing import Optional


class DuckDBConnection:
    _instance: Optional[duckdb.DuckDBPyConnection] = None

    @classmethod
    def get_connection(cls) -> duckdb.DuckDBPyConnection:
        if cls._instance is None:
            cls._instance = duckdb.connect(database=":memory:")
        return cls._instance

    @classmethod
    def close(cls):
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None


def read_csv_file(file_path: str, table_name: str = "csv_data") -> dict:
    conn = DuckDBConnection.get_connection()
    conn.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM read_csv_auto('{file_path}')"
    )

    columns = [desc[0] for desc in conn.execute(f"DESCRIBE {table_name}").fetchall()]
    row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    return {"table_name": table_name, "columns": columns, "row_count": row_count}


def execute_query(query: str, params: list = None):
    conn = DuckDBConnection.get_connection()
    if params:
        result = conn.execute(query, params).fetchall()
    else:
        result = conn.execute(query).fetchall()
    return result


def get_table_info(table_name: str = "csv_data") -> dict:
    conn = DuckDBConnection.get_connection()
    columns = [desc[0] for desc in conn.execute(f"DESCRIBE {table_name}").fetchall()]
    row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    sample_data = conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchall()

    return {
        "table_name": table_name,
        "columns": columns,
        "row_count": row_count,
        "sample_data": sample_data,
    }
