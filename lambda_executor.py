import logging
from multiprocessing import Process, Queue, Manager
from lambda_job import LambdaJob
from lambda_worker import LambdaWorker

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')


class Lambda(object):
    '''A simple job-executor that uses multiprocessing processes as workers.'''

    def __init__(self, num_workers=4):
        self._n = num_workers
        self._workers = []
        self._manager = Manager()

        # Queue to send tasks to workers
        self._job_queue = Queue()

        # Dictionary to receive results from workers
        self._result_dict = self._manager.dict()

        # Count of number of jobs sent out
        self._num_jobs = 0

        # Initialize workers
        for i in range(self._n):
            new_worker = Process(target=LambdaWorker, name=i, daemon=True,
                                 kwargs={
                                     'job_queue': self._job_queue,
                                     'result_dict': self._result_dict,
                                     'worker_id': i
                                 })
            self._workers.append(new_worker)
            new_worker.start()

    def run(self, f, *args, **kwargs):
        '''Run a function and return the result. All args and kwargs provided
        are passed to the function.'''

        assert callable(f), 'f must be callable'
        job_id = self._num_jobs
        self._num_jobs += 1

        logger.debug('[EXECUTOR] Sending job {}'.format(job_id))
        new_job = LambdaJob(f, job_id, *args, **kwargs)
        self._job_queue.put(new_job)

        # Wait until result has been put in the dict
        while job_id not in self._result_dict:
            continue

        # Get result and delete it from the results dictionary
        result = self._result_dict[job_id]
        logger.debug('[EXECUTOR] Got result {}'.format(job_id))
        del self._result_dict[job_id]
        return result

    def stop(self):
        '''Stop all worker processes.'''
        for worker in self._workers:
            worker.kill()
