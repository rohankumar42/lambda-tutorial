
class LambdaJob(object):
    '''Represents a job with its args and kwargs.'''

    def __init__(self, f, job_id, *args, **kwargs):
        self.f = f
        self.job_id = job_id
        self.args = args
        self.kwargs = kwargs

    def run(self):
        return self.f(*self.args, **self.kwargs)
