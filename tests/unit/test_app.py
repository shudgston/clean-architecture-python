"""
This test module should help to demonstrate how the app is wired together.

If the delivery mechanism was Flask or Django, the controllers, presenters, and
views would most likely be implemented in that project (assuming a separate
project). The important thing is that this project, the core application, has
no idea and does not care how input data will be delivered to it.
"""

import json
import unittest

from links.usecases import bookmarks
from links.usecases.interfaces import Controller, OutputBoundary, View
from tests.unit.helpers import setup_testing_data
from tests.unit.usecases.spies import ViewSpy


class TestBookmarkDetailsController(Controller):
    """
    A generic controller implementation. A concrete controller implementation
    would be implemented on most likely exist in the UI.
    """

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, request):
        """The overridden ABC/interface method"""
        self.usecase.bookmark_details(request['user_id'], request['bookmark_id'], self.presenter)
        view_model = self.presenter.get_view_model()
        return self.view.generate_view(view_model)


class TestPresenter(OutputBoundary):
    """
    A generic presenter/output boundary implementation.
    Concrete implementations would most likely exist in the UI.
    """

    def __init__(self):
        self.view_model = {}

    def present(self, response_model):
        """The overridden ABC/interface method"""
        self.view_model['bookmark_id'] = response_model.bookmark_id
        self.view_model['name'] = response_model.name
        self.view_model['url'] = response_model.url
        self.view_model['date_created_iso'] = response_model.date_created.isoformat()
        self.view_model['added_by_presenter'] = True

    def get_view_model(self):
        """The overridden ABC/interface method"""
        return self.view_model


class JSONView(View):
    """
    A generic view to show how a view model might be rendered.
    """

    def generate_view(self, view_model):
        return json.dumps(view_model, indent=2)


class AppTest(unittest.TestCase):

    def setUp(self):
        setup_testing_data()

    def test_bookmark_details_presentation(self):
        """
        The presenter should assemble a view model that we expect.
        Also shows the flow of the controller > usecase > presenter > view
        request.
        """
        usecase = bookmarks.BookmarkDetailsUseCase()
        presenter = TestPresenter()
        view = ViewSpy()

        request = {'user_id': 'hodor', 'bookmark_id': 'hodorID1'}
        controller = TestBookmarkDetailsController(usecase, presenter, view)
        controller.handle(request)

        self.assertEqual('hodorID1', view.view_model['bookmark_id'])
        self.assertEqual('google', view.view_model['name'])
        self.assertEqual('web://google.com', view.view_model['url'])
        self.assertTrue(isinstance(view.view_model['date_created_iso'], str))
        self.assertTrue(view.view_model['added_by_presenter'], True)

    def test_bookmark_details_rendered_view(self):
        """
        A test to demonstrate a fully rendered view return. The view
        implementation in this case returns a JSON blob.
        """
        usecase = bookmarks.BookmarkDetailsUseCase()
        presenter = TestPresenter()
        view = JSONView()

        request = {'user_id': 'hodor', 'bookmark_id': 'hodorID1'}
        controller = TestBookmarkDetailsController(usecase, presenter, view)
        rendered_view = controller.handle(request)
        jsondict = json.loads(rendered_view)
        self.assertIn('bookmark_id', jsondict)
        self.assertIn('name', jsondict)
        self.assertIn('url', jsondict)
        self.assertIn('date_created_iso', jsondict)
        self.assertIn('added_by_presenter', jsondict)
