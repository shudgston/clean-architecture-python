from datetime import datetime
from unittest import TestCase

from web.app.main import presentation

from links.usecases.bookmarks import BookmarkDetails, CreateBookmarkResponse


class BookmarkDetailsPresenterTest(TestCase):

    def test_presenter_creates_view_model(self):
        dt = datetime(year=2017, month=1, day=1)
        response = BookmarkDetails('id1', 'test', 'web://test.com', dt)
        presenter = presentation.BookmarkDetailsPresenter()
        presenter.present(response)
        view_model = presenter.get_view_model()
        expected = {
            'bookmark_id': 'id1',
            'name': 'test',
            'url': 'web://test.com',
            'date_created': 'Jan 1, 2017',
            'date_created_iso': '2017-01-01T00:00:00',
            'host': 'test.com'
        }
        self.assertDictEqual(expected, view_model)


class BookmarkListPresentationTest(TestCase):

    def test_presenter_creates_view_model(self):
        dt = datetime(year=2017, month=1, day=1)
        response = [
            BookmarkDetails('id1', 'test1', 'web://test.com', dt),
            BookmarkDetails('id2', 'test2', 'web://test.com', dt),
        ]
        presenter = presentation.BookmarkListPresenter()
        presenter.present(response)
        view_model = presenter.get_view_model()
        expected = {
            'bookmark_id': 'id1',
            'name': 'test1',
            'url': 'web://test.com',
            'date_created': 'Jan 1, 2017',
            'date_created_iso': '2017-01-01T00:00:00',
            'host': 'test.com'
        }
        self.assertEqual(2, len(view_model))
        self.assertDictEqual(expected, view_model[0])


class CreateBookmarkPresentationTest(TestCase):

    def test_presenter_creates_view_model(self):
        response = CreateBookmarkResponse('id1', {})
        presenter = presentation.CreateBookmarkPresenter()
        presenter.present(response)
        view_model = presenter.get_view_model()
        expected = {'bookmark_id': 'id1', 'errors': {}}
        self.assertDictEqual(expected, view_model)
