import importlib
import uuid


class Task(object):

    """Task means a job to do ,it stores a function as a task."""

    @classmethod
    def create(cls, func, *args, **kwargs):
        """Create a task.

        :params: func: the function which will be added as a task.
        :params: args: the args of a function.
        :params: kwargs: the key-value args of a function.
        :returns: an instance of task.
        """
        task = Task()
        task._module_name = func.__module__
        task._func_name = func.__name__
        task._args = args
        task._kwargs = kwargs
        return task

    def __init__(self):
        self._id = None
        self._module_name = None
        self._func_name = None
        self._args = None
        self._kwargs = None

    @property
    def id(self):
        if self._id:
            self._id = str(uuid.uuid1())
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def module_name(self):
        return self._module_name

    @property
    def module_name(self):
        return self._module_name

    @property
    def func_name(self):
        return self._func_name

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def func(self):
        if not (self.module_name and self.func_name):
            return
        module = importlib.import_module(self.module_name)
        return getattr(module, self.func_name)

    @property
    def func_data(self):
        return (
            self.module_name, self.func_name,
            self.args, self.kwargs
        )
