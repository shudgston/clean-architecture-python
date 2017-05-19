from flask import request, render_template
from flask_login import current_user, login_required

from . import forms
from . import main
from ..links_ext import controller_factory, Settings


@main.route('/bookmarks', defaults={'filterkey': 'recent'})
@main.route('/bookmarks/<filterkey>')
@login_required
def index(filterkey):
    controller = controller_factory('list_bookmarks')
    req = {'user_id': current_user.get_id(), 'filterkey': filterkey}
    return controller.handle(req)


@main.route('/bookmarks.json')
@login_required
def json_index():
    controller = controller_factory('list_bookmarks_json')
    req = {'user_id': current_user.get_id()}
    return controller.handle(req)


@main.route('/bookmarks/<string:bookmark_id>')
@login_required
def bookmark_details(bookmark_id):
    controller = controller_factory('get_bookmark_details')
    req = {'user_id': current_user.get_id(), 'bookmark_id': bookmark_id}
    return controller.handle(req)


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = forms.CreateBookmarkForm()

    # Bookmarklet popup window
    # optionally accept query string args
    name = request.args.get('name')
    if name is not None:
        form.name.data = name

    url = request.args.get('url')
    if url is not None:
        form.url.data = url

    if form.validate_on_submit():
        controller = controller_factory('create_bookmark')
        # inject the form into the view, for flask/wtf validation
        controller.view.form = form
        controller.view.close_bookmarklet_window = request.args.get('close') is not None
        req = {
            'user_id': current_user.get_id(),
            'name': form.name.data,
            'url': form.url.data,
        }
        return controller.handle(req)

    return render_template('create_bookmark.html', form=form)
