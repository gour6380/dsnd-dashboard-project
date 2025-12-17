from fasthtml.common import H1, Div, FastHTML, serve, Title
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
#### YOUR CODE HERE
try:
    # Preferred: package exposes these at top-level
    from employee_events import QueryBase, Employee, Team  # type: ignore
except Exception:  # pragma: no cover
    # Fallbacks for common module layouts
    raise ImportError(
        "Unable to import QueryBase, Employee, Team from employee_events. "
        "Ensure the employee_events package is installed and exposes these symbols."
    )

# import the load_model function from the utils.py file
#### YOUR CODE HERE
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable,
    DashboardTitle,
    )

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
#### YOUR CODE HERE
class ReportDropdown(Dropdown):
    
    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    #### YOUR CODE HERE
    def build_component(self, entity_id, model):
        """
        Build a dropdown selector for the current model type (employee/team).

        Parameters
        ----------
        entity_id : Any
            The currently selected entity id (string/int).
        model : Any
            An instance of Employee or Team model class.

        Returns
        -------
        Any
            A fasthtml Select component.

        Raises
        ------
        TypeError
            If model is None.
        """
        if model is None:
            raise TypeError("model cannot be None")
        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        #### YOUR CODE HERE
        self.label = getattr(model, "name", "") or ""
        
        # Return the output from the
        # parent class's build_component method
        #### YOUR CODE HERE
        return super().build_component(entity_id, model)
    
    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    #### YOUR CODE HERE
    def component_data(self, entity_id, model):
        """
        Return iterable of (display_text, value) pairs for the dropdown.

        Expected model API:
          - model.names() -> Iterable[Tuple[str, Any]]
        """
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's
        # names and ids
        if model is None:
            return []

        names_fn = getattr(model, "names", None)
        if not callable(names_fn):
            return []

        try:
            data = names_fn()
        except Exception:
            return []

        if data is None:
            return []

        return data


# Create a subclass of base_components/BaseComponent
# called `Header`
#### YOUR CODE HERE
class Header(BaseComponent):

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    #### YOUR CODE HERE
    def build_component(self, entity_id, model):
        """
        Build the dashboard title.

        The title dynamically updates based on the selected profile type:
        - "Employee Performance" when viewing employees
        - "Team Performance" when viewing teams

        Returns
        -------
        fasthtml.common.H1
            An H1 element containing the appropriate dashboard title.
        """
        if model is None:
            raise TypeError("model cannot be None")
        
        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
        #### YOUR CODE HERE
        return DashboardTitle().build_component(entity_id, model)
          

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
#### YOUR CODE HERE
class LineChart(MatplotlibViz):
    
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    #### YOUR CODE HERE
    def visualization(self, entity_id, model):
        """
        Render a cumulative event count line chart for the given entity.

        Expected model API:
          - model.event_counts(asset_id) -> pandas.DataFrame-like
        """
        asset_id = entity_id

        if model is None:
            raise TypeError("model cannot be None")

        event_counts_fn = getattr(model, "event_counts", None)
        if not callable(event_counts_fn):
            raise AttributeError("model must implement an event_counts(asset_id) method")
    

        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        #### YOUR CODE HERE
        df = event_counts_fn(asset_id)
        
        # Use the pandas .fillna method to fill nulls with 0
        #### YOUR CODE HERE
        df = df.fillna(0)
        
        # User the pandas .set_index method to set
        # the date column as the index
        #### YOUR CODE HERE
        df = df.set_index('event_date')
        
        # Sort the index
        #### YOUR CODE HERE
        df = df.sort_index()
        
        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        #### YOUR CODE HERE
        df = df.cumsum()
        
        
        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        #### YOUR CODE HERE
        df.columns = ['Positive', 'Negative']
        
        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        #### YOUR CODE HERE
        fig, ax = plt.subplots()
        
        # call the .plot method for the
        # cumulative counts dataframe
        #### YOUR CODE HERE
        df.plot(ax=ax)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        # Use keyword arguments to set 
        # the border color and font color to black. 
        # Reference the base_components/matplotlib_viz file 
        # to inspect the supported keyword arguments
        #### YOUR CODE HERE
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        
        # Set title and labels for x and y axis
        #### YOUR CODE HERE
        ax.set_title("Cumulative Event Counts")
        ax.set_xlabel("Day")
        ax.set_ylabel("Event Count")

# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
#### YOUR CODE HERE
class BarChart(MatplotlibViz):
    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    #### YOUR CODE HERE
    predictor = load_model()

    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    #### YOUR CODE HERE
    def visualization(self, entity_id, model):
        """
        Render a horizontal bar chart for predicted recruitment risk.

        Expected model API:
          - model.model_data(asset_id) -> features for ML model
        Expected predictor API:
          - predictor.predict_proba(X) -> ndarray-like (n, 2)
        """
        asset_id = entity_id

        if model is None:
            raise TypeError("model cannot be None")

        model_data_fn = getattr(model, "model_data", None)
        if not callable(model_data_fn):
            raise AttributeError("model must implement a model_data(asset_id) method")

        if self.predictor is None:
            raise RuntimeError("predictor model is not loaded")

        predict_proba_fn = getattr(self.predictor, "predict_proba", None)
        if not callable(predict_proba_fn):
            raise AttributeError("predictor must implement predict_proba(X)")

        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        #### YOUR CODE HERE
        data = model_data_fn(asset_id)
        
        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        #### YOUR CODE HERE
        proba = predict_proba_fn(data)
        
        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        #### YOUR CODE HERE
        proba = proba[:, 1:2]
        
        
        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        #### YOUR CODE HERE
        if getattr(model, "name", "") == "team":
            pred = float(proba.mean())
            
        # Otherwise set `pred` to the first value
        # of the predict_proba output
        #### YOUR CODE HERE
        else:
            pred = float(proba[0][0])
        
        # Initialize a matplotlib subplot
        #### YOUR CODE HERE
        fig, ax = plt.subplots()
        
        # Run the following code unchanged
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        #### YOUR CODE HERE
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
 
# Create a subclass of combined_components/CombinedComponent
# called Visualizations       
#### YOUR CODE HERE
class Visualizations(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    #### YOUR CODE HERE
    children = [LineChart(), BarChart()]

    # Leave this line unchanged
    outer_div_type = Div(cls='grid')
            
# Create a subclass of base_components/DataTable
# called `NotesTable`
#### YOUR CODE HERE
class NotesTable(DataTable):

    # Overwrite the `component_data` method
    # using the same parameters as the parent class
    #### YOUR CODE HERE
    def component_data(self, entity_id, model):
        """
        Return notes for the given entity_id.

        Expected model API:
          - model.notes(entity_id) -> pandas.DataFrame-like with columns
        """
        
        # Using the model and entity_id arguments
        # pass the entity_id to the model's .notes 
        # method. Return the output
        #### YOUR CODE HERE
        if model is None:
            raise TypeError("model cannot be None")

        notes_fn = getattr(model, "notes", None)
        if not callable(notes_fn):
            raise AttributeError("model must implement a notes(entity_id) method")

        return notes_fn(entity_id)
    

class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method="POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]
    
# Create a subclass of CombinedComponents
# called `Report`
#### YOUR CODE HERE
class Report(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing initialized instances 
    # of the header, dashboard filters,
    # data visualizations, and notes table
    #### YOUR CODE HERE
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


# Initialize a fasthtml app 
#### YOUR CODE HERE
app = FastHTML(title="Employee Performance")

# Initialize the `Report` class
#### YOUR CODE HERE
report = Report()

def page_title(model):
    """
    Determine the page title based on the active profile type.

    Parameters
    ----------
    model : Any
        Model instance representing the current profile type.
        Expected to expose a `name` attribute with values
        such as "employee" or "team".

    Returns
    -------
    str
        "Team Performance" if the model represents a team,
        otherwise "Employee Performance".
    """
    if (getattr(model, "name", "") or "").lower() == "team":
        return "Team Performance"
    return "Employee Performance"

def with_mode(model, mode: str):
    """
    Attach a profile mode to a model instance.

    This helper ensures consistency between routing logic,
    radio button state, dropdown contents, and page title
    by explicitly setting the model's `name` attribute.

    Parameters
    ----------
    model : Any
        An instance of an Employee or Team model.
    mode : str
        Profile type identifier. Expected values are
        "employee" or "team".

    Returns
    -------
    Any
        The same model instance with its `name` attribute set.
    """
    model.name = mode
    return model

# Create a route for a get request
# Set the route's path to the root
#### YOUR CODE HERE
@app.get('/')
def root():

    # Call the initialized report
    # pass the integer 1 and an instance
    # of the Employee class as arguments
    # Return the result
    #### YOUR CODE HERE
    model = with_mode(Employee(), "employee")
    return Title(page_title(model)), report(1, model)

# Create a route for a get request
# Set the route's path to receive a request
# for an employee ID so `/employee/2`
# will return the page for the employee with
# an ID of `2`. 
# parameterize the employee ID 
# to a string datatype
#### YOUR CODE HERE
@app.get('/employee/{id}')
def employee(id: str):

    # Call the initialized report
    # pass the ID and an instance
    # of the Employee SQL class as arguments
    # Return the result
    #### YOUR CODE HERE
    model = with_mode(Employee(), "employee")
    return Title(page_title(model)), report(id, model)

# Create a route for a get request
# Set the route's path to receive a request
# for a team ID so `/team/2`
# will return the page for the team with
# an ID of `2`. 
# parameterize the team ID 
# to a string datatype
#### YOUR CODE HERE
@app.get('/team/{id}')
def team(id: str):

    # Call the initialized report
    # pass the id and an instance
    # of the Team SQL class as arguments
    # Return the result
    #### YOUR CODE HERE
    model = with_mode(Team(), "team")
    return Title(page_title(model)), report(id, model)

# Keep the below code unchanged!
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    profile_type = r.query_params['profile_type']
    if profile_type == 'Team':
        model = with_mode(Team(), "team")
        return dropdown(None, model)
    elif profile_type == 'Employee':
        model = with_mode(Employee(), "employee")
        return dropdown(None, model)


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)
    


serve()
