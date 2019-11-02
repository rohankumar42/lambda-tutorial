import logging
import queue

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(message)s')

QUEUE_TIMEOUT = 10 ** -2


class LambdaWorker(object):
    '''Simple worker that waits for jobs, runs them, and returns results.'''

    def __init__(self, job_queue, result_dict, worker_id):
        self.functions = {}
        self._job_queue = job_queue
        self._result_dict = result_dict
        self._id = worker_id
        self.await_jobs()

    def await_jobs(self):
        '''Waits for new jobs to come in via the job queue, runs the job, and
        puts the result into the results dict.'''

        logger.info('[WORKER {}] Ready!'.format(self._id))

        while True:
            try:
                job = self._job_queue.get(timeout=QUEUE_TIMEOUT)
            except queue.Empty:
                logger.debug('[WORKER {}] found empty queue'.format(self._id))
                continue

            logger.debug('[WORKER {}] Running job {}'
                         .format(self._id, job.job_id))
            result = job.run()

            logger.debug('[WORKER {}] Returning result {}'
                         .format(self._id, job.job_id))
            self._result_dict[job.job_id] = result
