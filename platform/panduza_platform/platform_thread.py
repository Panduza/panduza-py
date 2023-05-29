import time
import asyncio
import threading

from .log.thread import thread_logger

class PlatformThread:

    ID_COUNT = 0

    PERF_CYCLE_TIME = 2

    # ---

    def __init__(self) -> None:
        self.id = PlatformThread.ID_COUNT
        PlatformThread.ID_COUNT += 1

        self.__log = thread_logger("_T_" + str(self.id))

        self.__alive = True

        self.__mutex = threading.Lock()

        # List of managed worker 
        self.__workers = []

        self.evloop = asyncio.new_event_loop()

    # ---

    def attach_worker(self, worker):
        self.__mutex.acquire()
        worker.PZA_WORKER_on_thread_attach(self.evloop)
        self.__workers.append(worker)
        self.__mutex.release()

    # ---

    def start(self):
        self.__thread = threading.Thread(target=self.exec, name="T" + str(self.id))
        self.__thread.start()

    # ---

    #   def stop(self):
    #        self.__alive = False

    # ---

    def join(self):
        self.__thread.join()

    # ---

    def exec(self):
        # Create an event loop and start the driver

        self.evloop.run_until_complete(self.__async_exec())

    # ---

    async def __control_loop_load(self):
        while(self.__alive):
            await asyncio.sleep(3)
            # Compute work time
            work_time = 0
            for w in self.__workers:
                work_time += w.work_time
                w.reset_work_time()

            # Compute loop time
            # loop_time = time.perf_counter() - loop_t0

            # 
            # self.__log.info(f"{work_time} - {loop_time}")
            self.__log.info(f"{(work_time/PlatformThread.PERF_CYCLE_TIME) * 100.0} %")

    # ---

    async def __async_exec(self):
        """Main execution function of the thread

        This function runs the worker and compute there load on the thread
        """

        self.evloop.create_task(self.__control_loop_load())

        # Continue the thread while the thread is alive
        while(self.__alive):

            # Lock the worker mutex
            self.__mutex.acquire()

            # Run works during 1 time cycle
            loop_t0 = time.perf_counter()
            while(time.perf_counter() - loop_t0 < PlatformThread.PERF_CYCLE_TIME):
                for w in self.__workers:
                    await w.work(self.evloop)
                await asyncio.sleep(0.01)

            # 
            self.__mutex.release()


    #     def detach_worker(self, worker):
