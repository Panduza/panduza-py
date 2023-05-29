import abc
import time

class PlatformWorker(metaclass=abc.ABCMeta):
    """Mother class for all the python drivers
    """

    def __init__(self) -> None:
        self.reset_work_time()

    def reset_work_time(self):
        self.work_time = 0


    async def work(self, loop):
        """
        """
        work_t0 = time.perf_counter()
        await self._PZA_WORKER_task(loop)
        self.work_time += (time.perf_counter() - work_t0)

    # ---

    def PZA_WORKER_on_thread_attach(self, loop):
        """Triggered when a thread is attached to this worker
        """
        pass

    # ---

    @abc.abstractmethod
    async def _PZA_WORKER_task(self, loop):
        """
        """
        pass


