"""
    Registry for task queue.
"""
import cPickle as pickle
from cytisas.tqueue.task import Task


class Registry(object):
    """A registry for task queue."""

    def __init__(self):
        self._registry = {}

    def get_task_string(self, task):
        """Generate a string of a task.

        :params: task: an instance of task.
        """
        return '{}.{}'.format(task.module_name, task.func_name)

    def register(self, task):
        """Register a task.

        :params: task: an instance of task.
        :returns: a dictionary for redis.
        """
        task_name = self.get_task_string(task)
        if task_name not in self._registry:
            redis_dict = {}
            data = pickle.dumps(task.func_data)
            self._registry[task_name] = task
            redis_dict['func_data'] = data
            # this feature is not implemented now.
            redis_dict['timeout'] = 10
            return redis_dict

    def unregister(self, redis_data):
        """Unregister a task.

        :params: redis_data: the data get from redis.
        :returns: the unregistered task.
        """
        task = Task()
        func_data = redis_data[0]
        time_out = redis_data[1]
        if not func_data:
            return None
        try:
            (task._module_name,
             task._func_name,
             task._args,
             task._kwargs) = pickle.loads(func_data)
        except Exception as exc:
            raise exc
        task_name = self.get_task_string(task)
        if task_name not in self._registry:
            return None
        del self._registry[task_name]
        return task

registry = Registry()
