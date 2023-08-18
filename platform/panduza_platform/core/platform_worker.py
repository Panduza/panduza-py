import abc
import asyncio

class PlatformWorker(metaclass=abc.ABCMeta):
    """Mother class for all the python drivers
    """

    def __init__(self) -> None:
        self.__alive = True
        self.__thread = None
        self.reset_work_time()

    def set_thread(self, thread):
        self.__thread = thread

    def reset_work_time(self):
        self.work_time = 0

    def worker_panic(self):
        self.__thread.handle_worker_panic(self.PZA_WORKER_name())

    def stop(self):
        self.__alive = False

    async def task(self, loop):
        """
        """
        while(self.__alive):
            await asyncio.sleep(0.1)
            await self.PZA_WORKER_task(loop)

        self.PZA_WORKER_log().info("stopped")

    # =============================================================================
    # OVERRIDE REQUESTED FUNCTIONS

    # ---

    @abc.abstractmethod
    def PZA_WORKER_name(self):
        """
        """
        pass

    # ---

    @abc.abstractmethod
    def PZA_WORKER_log(self):
        """
        """
        pass

    # ---

    @abc.abstractmethod
    def PZA_WORKER_status(self):
        """Return a state report of the worker
        To be able to indicate to administrator why the platform stopped
        """
        pass

    # ---

    @abc.abstractmethod
    async def PZA_WORKER_task(self, loop):
        """
        """
        pass


