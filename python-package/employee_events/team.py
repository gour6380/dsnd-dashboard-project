# Import the QueryBase class
# YOUR CODE HERE
from .query_base import QueryBase

# Import dependencies for sql execution
#### YOUR CODE HERE
from .sql_execution import query

# Create a subclass of QueryBase
# called  `Team`
#### YOUR CODE HERE
class Team(QueryBase):

    # Set the class attribute `name`
    # to the string "team"
    #### YOUR CODE HERE
    name: str = "Team"

    # Define a `names` method
    # that receives no arguments
    # This method should return
    # a list of tuples from an sql execution
    #### YOUR CODE HERE
    @query
    def names(self):
        """
        Return all teams (team_name, team_id).

        Returns
        -------
        list[tuple]
            A list of (team_name, team_id) tuples for all teams.

        Raises
        ------
        RuntimeError
            If SQL execution fails.
        """
        
        # Query 5
        # Write an SQL query that selects
        # the team_name and team_id columns
        # from the team table for all teams
        # in the database
        #### YOUR CODE HERE
        return f"""
            SELECT
                team_name,
                team_id
            FROM {self.name};
        """
    

    # Define a `username` method
    # that receives an ID argument
    # This method should return
    # a list of tuples from an sql execution
    #### YOUR CODE HERE
    @query
    def username(self, id):
        """
        Return the team_name for a given team_id.

        Parameters
        ----------
        id : int
            Team identifier (team_id).

        Returns
        -------
        list[tuple]
            A single-row result containing the team's name.

        Raises
        ------
        TypeError
            If id is None.
        RuntimeError
            If SQL execution fails.
        """
        if id is None:
            raise TypeError("id cannot be None")

        # Query 6
        # Write an SQL query
        # that selects the team_name column
        # Use f-string formatting and a WHERE filter
        # to only return the team name related to
        # the ID argument
        #### YOUR CODE HERE
        return f"""
            SELECT
                team_name
            FROM {self.name}
            WHERE team_id = {int(id)};
        """


    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    #### YOUR CODE HERE
    def model_data(self, id):
        """
        Return per-employee aggregated event counts for a given team as a pandas DataFrame.

        Parameters
        ----------
        id : int
            Team identifier (team_id).

        Returns
        -------
        pandas.DataFrame
            DataFrame with columns: employee_id, positive_events, negative_events.

        Raises
        ------
        TypeError
            If id is None.
        RuntimeError
            If SQL execution fails.
        """
        if id is None:
            raise TypeError("id cannot be None")

        return self.pandas_query(
            f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """
        )