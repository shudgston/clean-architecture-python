"""

"""
import argparse
import dateutil.parser
import json
import sys

from links.usecases.interfaces import View
from links.usecases import create_bookmark
from links.usecases.create_user import CreateUserUseCase, CreateUserController, CreateUserPresenter
from links.usecases import list_bookmarks
from links.logger import get_logger
from links.context import init_context

LOGGER = get_logger(__name__)
USUCCESS = "\u2713"
UFAILURE = "\u2717"


class CreateUserConsoleView(View):

    def generate_view(self, view_model):
        super().generate_view(view_model)
        usuccess = "\n\u2713 Created user '{}'"
        ufailure = "\n\u2717 Failed to create user '{}'"

        if view_model['user_created']:
            return usuccess.format(view_model['username'])

        return ufailure.format(view_model['username'])


class ListBookmarksConsoleView(View):

    def generate_view(self, view_model):
        return json.dumps(view_model, indent=True)


def create_user(args):
    controller = CreateUserController(
        CreateUserUseCase(),
        CreateUserPresenter(),
        CreateUserConsoleView()
    )
    print(controller.handle({'username': args.username, 'password': args.password}))


def export_bookmarks(args):
    controller = list_bookmarks.ListBookmarksController(
        list_bookmarks.ListBookmarksUseCase(),
        list_bookmarks.ListBookmarksPresenter(),
        ListBookmarksConsoleView()
    )
    # rv = uc.list_bookmarks(args.user, filterkey='everything')
    # print(rv)
    print(controller.handle({'user_id': args.user, 'filterkey': 'everything'}))


def import_bookmarks(args):
    LOGGER.info("Creating temp user %s", args.user)
    rv = CreateUserUseCase().create_user(args.user, 'password')
    LOGGER.info(rv)

    for x in import_from_json(args.source):
        date_created = dateutil.parser.parse(x['date_created_iso'])
        uc = create_bookmark.CreateBookmarkUseCase()
        rv = uc.create_bookmark(args.user, x['name'], x['url'], date_created)
        presenter = create_bookmark.CreateBookmarkPresenter()
        presenter.present(rv)
        LOGGER.info(presenter.get_view_model())


def import_from_json(path):
    importdata = []
    with open(path, 'r') as fh:
        importdata = json.load(fh)

    return importdata


def main():

    def main_help(args):
        parser.print_help(sys.stderr)

    parser = argparse.ArgumentParser(
        description='CLI Tools',
        prog='tools.py')

    parser_user_parent = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_export_links = subparsers.add_parser(
        'export',
        description='Export as JSON'
    )
    parser_export_links.add_argument(
        '-u', '--user', type=str, required=True
    )
    parser_export_links.set_defaults(func=export_bookmarks)

    parser_import_links = subparsers.add_parser(
        'import',
        description='Import links from external sources')
    parser_import_links.add_argument(
        '-u', '--user', type=str, required=True)
    parser_import_links.add_argument('source', type=str)
    parser_import_links.set_defaults(func=import_bookmarks)

    create_user_parser = subparsers.add_parser('create_user', description='Create a user')
    create_user_parser.add_argument('-u', '--username', type=str, required=True)
    create_user_parser.add_argument('-p', '--password', type=str, required=True)
    create_user_parser.set_defaults(func=create_user)

    parser.set_defaults(func=main_help)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    init_context()
    main()
