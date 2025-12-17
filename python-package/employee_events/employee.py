# Import the QueryBase class
#### YOUR CODE HERE
from .query_base import QueryBase

# Import dependencies needed for sql execution
# from the `sql_execution` module
#### YOUR CODE HERE
from .sql_execution import query

# Define a subclass of QueryBase
# called Employee
#### YOUR CODE HERE
class Employee(QueryBase):

    # Set the class attribute `name`
    # to the string "employee"
    #### YOUR CODE HERE
    name: str = "Employee"

    # Define a method called `names`
    # that receives no arguments
    # This method should return a list of tuples
    # from an sql execution
    #### YOUR CODE HERE
    @query
    def names(self):
        """
        Return a list of (employee_full_name, employee_id) tuples for all employees.

        Returns
        -------
        list[tuple]
            (full_name, employee_id) for all employees in the database.

        Notes
        -----
        The schema stores names as `first_name` and `last_name`, so the full name is
        constructed in SQL.
        """
        
        # Query 3
        # Write an SQL query
        # that selects two columns 
        # 1. The employee's full name
        # 2. The employee's id
        # This query should return the data
        # for all employees in the database
        #### YOUR CODE HERE
        return f"""
            SELECT
                first_name || ' ' || last_name AS employee_name,
                employee_id
            FROM {self.name}
            ORDER BY last_name, first_name, employee_id;
        """
    

    # Define a method called `username`
    # that receives an `id` argument
    # This method should return a list of tuples
    # from an sql execution
    #### YOUR CODE HERE
    @query
    def username(self, id):
        """
        Return the full name for a single employee id.

        Parameters
        ----------
        id : int
            Employee identifier (employee_id).

        Returns
        -------
        list[tuple]
            A list with one tuple: (employee_full_name,), or an empty list if not found.

        Raises
        ------
        TypeError
            If id is None.
        ValueError
            If id cannot be cast to an integer.
        """
        if id is None:
            raise TypeError("id cannot be None")
        try:
            employee_id = int(id)
        except (TypeError, ValueError) as exc:
            raise ValueError("id must be an integer-like value") from exc
        
        # Query 4
        # Write an SQL query
        # that selects an employees full name
        # Use f-string formatting and a WHERE filter
        # to only return the full name of the employee
        # with an id equal to the id argument
        #### YOUR CODE HERE
        return f"""
            SELECT
                first_name || ' ' || last_name AS employee_name
            FROM {self.name}
            WHERE employee_id = {employee_id};
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
        Execute the provided model SQL and return a pandas DataFrame.

        Parameters
        ----------
        id : int
            Employee identifier (employee_id).

        Returns
        -------
        pandas.DataFrame
            DataFrame containing the model aggregation results.

        Raises
        ------
        TypeError
            If id is None.
        ValueError
            If id cannot be cast to integer.
        RuntimeError
            If query execution fails.
        """
        if id is None:
            raise TypeError("id cannot be None")
        try:
            int(id)
        except (TypeError, ValueError) as exc:
            raise ValueError("id must be an integer-like value") from exc

        return self.pandas_query(
            f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                """
        )