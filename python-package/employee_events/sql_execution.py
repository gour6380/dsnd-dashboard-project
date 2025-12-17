from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
#### YOUR CODE HERE
try:
    # Resolve the path to the database file relative to this file
    db_path = (Path(__file__).resolve().parent / "employee_events.db").resolve()
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found at expected location: {db_path}")
except Exception as exc:
    # Fail fast with a clear error message; downstream DB calls depend on this
    raise RuntimeError("Failed to resolve database path for employee_events.db") from exc

# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    #### YOUR CODE HERE
    def pandas_query(self, sql_query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return the results as a pandas DataFrame.

        Parameters
        ----------
        sql_query : str
            A valid SQL query string.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the query results.

        Raises
        ------
        TypeError
            If sql_query is not a string.
        ValueError
            If sql_query is empty or only whitespace.
        RuntimeError
            If there is an error executing the SQL query.
        """
        if not isinstance(sql_query, str):
            raise TypeError("sql_query must be a string")
        if not sql_query.strip():
            raise ValueError("sql_query cannot be empty")

        try:
            with connect(db_path) as connection:
                # pandas handles cursor management internally
                df = pd.read_sql_query(sql_query, connection)
                return df
        except Exception as exc:
            raise RuntimeError("Failed to execute SQL query and return pandas DataFrame") from exc

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    #### YOUR CODE HERE
    def query(self, sql_query: str):
        """
        Execute a SQL query and return the results as a list of tuples.

        Parameters
        ----------
        sql_query : str
            A valid SQL query string.

        Returns
        -------
        list[tuple]
            Query results returned by sqlite3 cursor.

        Raises
        ------
        TypeError
            If sql_query is not a string.
        ValueError
            If sql_query is empty or only whitespace.
        RuntimeError
            If there is an error executing the SQL query.
        """
        if not isinstance(sql_query, str):
            raise TypeError("sql_query must be a string")
        if not sql_query.strip():
            raise ValueError("sql_query cannot be empty")

        try:
            with connect(db_path) as connection:
                cursor = connection.cursor()
                result = cursor.execute(sql_query).fetchall()
                return result
        except Exception as exc:
            raise RuntimeError("Failed to execute SQL query and return raw results") from exc
    

 
 # Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query
