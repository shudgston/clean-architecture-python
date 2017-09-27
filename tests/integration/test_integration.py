import json
import unittest

from links.context import context, init_context
from links import entities
from links.usecases import create_bookmark
from links.settings import Settings
from links.usecases import interfaces


class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        Settings.DATABASE_PLUGIN = 'inmemory'
        init_context(Settings)

    def test_integration(self):
        """
        Show a simple wiring of the system using a custom controller,
        presenter, and view.
        """
        user = entities.User('hodor')
        context.user_repo.save(user)

        # a dict of data gathered from a web form or some other means of input
        request = {
            'user_id': 'hodor',
            'name': 'test',
            'url': 'http://www.example.com',
        }

        usecase = create_bookmark.CreateBookmarkUseCase()
        presenter = TestJSONPresenter()
        view = TestJSONView()
        controller = TestController(usecase, presenter, view)

        rendered_view = controller.handle(request)
        self.assertDictEqual(
            json.loads(rendered_view),
            {'success': True, 'errors': {}}
        )


class TestController(interfaces.Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        self.usecase.user_id = request['user_id']
        self.usecase.name = request['name']
        self.usecase.url = request['url']
        self.usecase.execute(self.presenter)
        return self.view.generate_view(self.presenter.get_view_model())


class TestJSONPresenter(interfaces.OutputBoundary):

    def __init__(self):
        self._view_model = {}

    def present(self, response_model):
        # if any date formatting was needed, it would happen here
        self._view_model['success'] = response_model.errors == {}
        self._view_model['errors'] = response_model.errors

    def get_view_model(self):
        return self._view_model


class TestJSONView(interfaces.View):

    def generate_view(self, view_model):
        return json.dumps(view_model)