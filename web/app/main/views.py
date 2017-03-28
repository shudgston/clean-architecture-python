from flask import render_template, jsonify
from flask_login import current_user

from links.usecases.bookmarks import BookmarkDetailsUseCase, CreateBookmarkUseCase, \
    ListBookmarksUseCase
from . import forms
from . import main
from . import presentation


@main.route('/bookmarks')
def index():
    print(current_user.get_id())
    controller = presentation.BookmarkListController(
        ListBookmarksUseCase(),
        presentation.BookmarkListPresenter(),
        presentation.BookmarkListView())
    return controller.handle({'user_id': current_user.get_id()})


@main.route('/bookmarks/<string:bookmark_id>')
def bookmark_details(bookmark_id):
    uc = BookmarkDetailsUseCase()
    presenter = presentation.BookmarkDetailsPresenter()
    view = presentation.BookmarkDetailsView()
    controller = presentation.BookmarkDetailsController(uc, presenter, view)
    return controller.handle({'user_id': current_user.get_id(), 'bookmark_id': bookmark_id})


@main.route('/bookmarks.json')
def json_index():
    uc = ListBookmarksUseCase()
    presenter = presentation.BookmarkListPresenter()
    view = presentation.BookmarkListJSONView()
    controller = presentation.BookmarkListController(uc, presenter, view)
    try:
        return controller.handle({'user_id': current_user.get_id()})
    except Exception:
        return jsonify({'error': 'Something bad happened'})


@main.route('/create', methods=['GET', 'POST'])
def create():
    form = forms.CreateBookmarkForm()

    if form.validate_on_submit():
        uc = CreateBookmarkUseCase()
        presenter = presentation.CreateBookmarkPresenter()
        view = presentation.CreateBookmarkView(form)
        controller = presentation.CreateBookmarkController(uc, presenter, view)
        # View will redirect or regenerate form.
        request = {'user_id': current_user.get_id(), 'form': form}
        return controller.handle(request)

    return render_template('create_bookmark.html', form=form)
