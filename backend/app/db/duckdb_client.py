import pandas as pd
import os
from typing import Optional


class CSVReader:
    _instance: Optional["CSVReader"] = None
    _df: Optional[pd.DataFrame] = None
    _file_path: Optional[str] = None

    @classmethod
    def load_csv(cls, file_path: str) -> dict:
        cls._file_path = file_path
        for encoding in ["utf-8", "cp949", "euc-kr"]:
            try:
                cls._df = pd.read_csv(file_path, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue

        columns = list(cls._df.columns)
        row_count = len(cls._df)

        return {"file_path": file_path, "columns": columns, "row_count": row_count}

    @classmethod
    def get_columns(cls) -> list:
        if cls._df is None:
            return []
        return list(cls._df.columns)

    @classmethod
    def get_row_count(cls) -> int:
        if cls._df is None:
            return 0
        return len(cls._df)

    @classmethod
    def execute_query(cls, query: str) -> list:
        if cls._df is None:
            return []

        try:
            result = cls._df.query(query)
            return result.to_dict("records")
        except Exception:
            return []

    @classmethod
    def get_data(cls, columns: list = None, limit: int = 100) -> list:
        if cls._df is None:
            return []

        df = cls._df if columns is None else cls._df[columns]
        if limit:
            df = df.head(limit)
        return df.to_dict("records")

    @classmethod
    def get_table_info(cls) -> dict:
        if cls._df is None:
            return {"columns": [], "row_count": 0, "sample_data": []}

        columns = list(cls._df.columns)
        row_count = len(cls._df)
        sample_data = cls._df.head(5).to_dict("records")

        return {"columns": columns, "row_count": row_count, "sample_data": sample_data}

    @classmethod
    def close(cls):
        cls._df = None
        cls._file_path = None
