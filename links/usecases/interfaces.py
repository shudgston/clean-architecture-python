from abc import ABCMeta, abstractmethod

# TODO: Make a single InputBoundary ABC


class IUseCase(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, request, presenter):
        pass


class UseCase(metaclass=ABCMeta):

    @abstractmethod
    def execute(self, presenter):
        pass


class IPresenter(metaclass=ABCMeta):
    """
    This interface decouples a use cases's output from the view and is
    implemented by "presenter" objects to construct a view model.

    A presenter should be given raw output data by a use case, and then
    translate that data into a presentable format for a "view" object to
    render.
    """

    @abstractmethod
    def present(self, response_model):
        pass

    @abstractmethod
    def get_view_model(self):
        # TODO: remove this and just use the attribute?
        pass


class OutputBoundary(metaclass=ABCMeta):
    """
    This interface decouples a use cases's output from the view and is
    implemented by "presenter" objects to construct a view model.

    A presenter should be given raw output data by a use case, and then
    translate that data into a presentable format for a "view" object to
    render.
    """

    @abstractmethod
    def present(self, response_model):
        pass

    @abstractmethod
    def get_view_model(self):
        # TODO: remove this and just use the attribute?
        pass


class View(metaclass=ABCMeta):

    @abstractmethod
    def generate_view(self, view_model):
        """
        Create a view from the view_model object. The specific view type is
        unknown at the interface level, but some examples could be a string of
        HTML, a string of JSON, or some other object required by another means
        of output.

        :param view_model: a presentable data structure that can be converted
          into a viewable format.
        :return:
        """
        pass


class Controller(metaclass=ABCMeta):
    """Controller interface"""

    @abstractmethod
    def handle(self, request):
        pass

