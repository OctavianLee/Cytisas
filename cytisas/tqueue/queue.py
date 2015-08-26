"""
    A task queue prototype.
"""
from bauhinia.queues import Queue
from cytisas.tqueue.registry import registry


class TaskQueue(Queue):

    """Task queue is a redis queue."""

    def __init__(self, connection, name='default'):
        super(TaskQueue, self).__init__()
        self.name = name
        self.connection = connection

    def head(self):
        """Not Implemented"""
        raise NotImplementedError

    def purge(self):
        """Not Implemented"""
        raise NotImplementedError

    def enqueue(self, task):
        """Enqueue a task.

        :params: task: an instance of task.
        :returns: the operation is okay or not.
        """

        redis_dict = registry.register(task)
        if redis_dict:
            self.connection.hmset(task.id, redis_dict)
            self.connection.rpush(self.name, task.id)
            return True
        return False

    def dequeue(self):
        """Dequeue a task."""

        key = self.connection.lpop(self.name)
        if not key:
            return None
        redis_data = self.connection.hmget(key, ['func_data', 'timeout'])
        if not redis_data:
            return None
        task = registry.unregister(redis_data)
        return task
