import abc
import time

class PlatformWorker(metaclass=abc.ABCMeta):
    """Mother class for all the python drivers
    """

    def __init__(self) -> None:
        self.reset_work_time()

    def reset_work_time(self):
        self.work_time = 0

    async def work(self):
        """
        """
        work_t0 = time.perf_counter()
        await self._PZA_WORKER_task()
        self.work_time += (time.perf_counter() - work_t0)

    @abc.abstractmethod
    async def _PZA_WORKER_task(self):
        """
        """
        pass


