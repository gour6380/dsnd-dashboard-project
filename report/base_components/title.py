# base_components/title.py

from .base_component import BaseComponent
from fasthtml.common import H1


class DashboardTitle(BaseComponent):
    """
    Dashboard title that switches between Employee Performance / Team Performance
    based on the current filter settings (model.name).
    """

    def build_component(self, entity_id, model):
        selected = (getattr(model, "name", "") or "").strip().lower()

        if selected == "team":
            title = "Team Performance"
        else:
            # default (also covers "employee")
            title = "Employee Performance"

        return H1(title)