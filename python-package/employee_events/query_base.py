# Import any dependencies needed to execute sql queries
# YOUR CODE HERE
from __future__ import annotations

from typing import Any, List

import pandas as pd

from .sql_execution import QueryMixin

# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
# YOUR CODE HERE
class QueryBase(QueryMixin):

    # Create a class attribute called `name`
    # set the attribute to an empty string
    # YOUR CODE HERE
    name: str = ""

    # Define a `names` method that receives
    # no passed arguments
    # YOUR CODE HERE
    def names(self) -> List[Any]:
        """
        Return the list of entity names for the table referenced by the `name` class attribute.

        Notes
        -----
        The base implementation intentionally returns an empty list because the schema
        for name lookup can differ across entity tables (e.g., employees, departments).
        Subclasses should override this method.

        Returns
        -------
        list
            Empty list by default.
        """
        
        # Return an empty list
        # YOUR CODE HERE
        return []


    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    # YOUR CODE HERE
    def event_counts(self, id: Any) -> pd.DataFrame:
        """
        Return per-date aggregated event counts for an entity.

        This method dynamically adapts to the subclass by using the `name`
        class attribute to determine which foreign key column to filter on
        (e.g., employee_id or team_id).

        Parameters
        ----------
        id : Any
            Identifier for the entity (employee_id or team_id).

        Returns
        -------
        pd.DataFrame
            DataFrame with columns:
            - event_date
            - positive_events
            - negative_events

        Raises
        ------
        ValueError
            If the `name` class attribute is not set.
        TypeError
            If `id` is None.
        ValueError
            If `id` cannot be cast to an integer.
        RuntimeError
            If query execution fails.
        """
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("QueryBase.name must be set to a non-empty table name in a subclass")
        if id is None:
            raise TypeError("id cannot be None")

        try:
            entity_id = int(id)
        except (TypeError, ValueError) as exc:
            raise ValueError("id must be an integer-like value") from exc

        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        # YOUR CODE HERE
        sql_query = f"""
            SELECT
                ee.event_date,
                SUM(ee.positive_events) AS positive_events,
                SUM(ee.negative_events) AS negative_events
            FROM employee_events ee
            JOIN {self.name} t
                ON ee.{self.name}_id = t.{self.name}_id
            WHERE t.{self.name}_id = {entity_id}
            GROUP BY ee.event_date
            ORDER BY ee.event_date;
        """
        return self.pandas_query(sql_query)
            
    

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    # YOUR CODE HERE
    def notes(self, id: Any) -> pd.DataFrame:
        """
        Return notes associated with an entity.

        This method works for any subclass that sets the `name` attribute.
        The correct foreign key column is inferred dynamically using
        `{name}_id`, allowing the same logic to support both employees
        and teams.

        Parameters
        ----------
        id : Any
            Identifier for the entity (employee_id or team_id).

        Returns
        -------
        pd.DataFrame
            DataFrame containing:
            - note_date
            - note

        Raises
        ------
        ValueError
            If the `name` class attribute is not set.
        TypeError
            If `id` is None.
        ValueError
            If `id` cannot be cast to an integer.
        RuntimeError
            If query execution fails.
        """
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("QueryBase.name must be set to a non-empty table name in a subclass")
        if id is None:
            raise TypeError("id cannot be None")

        try:
            entity_id = int(id)
        except (TypeError, ValueError) as exc:
            raise ValueError("id must be an integer-like value") from exc

        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        # YOUR CODE HERE
        sql_query = f"""
            SELECT
                n.note_date,
                n.note
            FROM notes n
            JOIN {self.name} t
                ON n.{self.name}_id = t.{self.name}_id
            WHERE t.{self.name}_id = {entity_id}
            ORDER BY n.note_date;
        """
        return self.pandas_query(sql_query)