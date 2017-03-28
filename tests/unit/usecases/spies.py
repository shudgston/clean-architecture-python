from links.usecases.interfaces import OutputBoundary, View


class PresenterSpy(OutputBoundary):

    def __init__(self):
        self.response_model = None
        self.present_called = False
        self.present_input_errors_called = False
        self._view_model = {}

    def present(self, response_model):
        self.response_model = response_model
        self.present_called = True

    def present_input_errors(self, response_model):
        self.response_model = response_model
        self.present_input_errors_called = True

    def get_view_model(self):
        return self._view_model


class ViewSpy(View):

    def __init__(self):
        self.view_model = None
        self.generate_view_called = False

    def generate_view(self, view_model):
        self.view_model = view_model
        self.generate_view_called = True
        return "<p>A Generated View</p>"
