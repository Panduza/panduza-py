import time
import asyncio
import threading

from log.thread import thread_logger




class MeasuredEventLoop(asyncio.SelectorEventLoop):
    def __init__(self, log, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._total_time = 0
        self._select_time = 0

        self._before_select = None
        
        self.log = log

    # TOTAL TIME:
    def run_forever(self):
        self.ref_time = self.time()
        try:
            super().run_forever()
        finally:
            finished = self.time()
            # self._total_time = finished - started

    # SELECT TIME:
    def _run_once(self):
        # print("_run_once")
        self._before_select = self.time()
        super()._run_once()

    def _process_events(self, *args, **kwargs):
        after_select = self.time()
        self._select_time += after_select - self._before_select

        # print("_process_events", args, kwargs)
        super()._process_events(*args, **kwargs)

        cycle_time = self.time() - self.ref_time
        if cycle_time >= PlatformThread.PERF_CYCLE_TIME:

            work_time = cycle_time - self._select_time
            self.load = round((work_time/PlatformThread.PERF_CYCLE_TIME) * 100.0, 3)
            if self.load > 60:
                self.log.info(f"loop load {self.load}% !!")
            # else:
            #     self.log.info(f"{load}%")
            self._select_time = 0
            self.ref_time = self.time()


class PlatformThread:

    ID_COUNT = 0

    PERF_CYCLE_TIME = 2

    # ---

    def __init__(self, parent_platform) -> None:
        self.id = PlatformThread.ID_COUNT
        PlatformThread.ID_COUNT += 1

        self.platform = parent_platform

        self.log = thread_logger("_T_" + str(self.id))


        self.__alive = True

        self.__mutex = threading.Lock()

        # List of managed worker 
        self.__workers = []

        self.evloop = MeasuredEventLoop(log = self.log)

    # ---

    def attach_worker(self, worker):
        self.__mutex.acquire()
        worker.set_thread(self)
        self.__workers.append(worker)
        self.__mutex.release()

    # ---

    def start(self):
        self.__thread = threading.Thread(target=self.exec, name="T" + str(self.id))
        self.__thread.start()

    # ---

    def stop(self):
        for w in self.__workers:
            w.stop()

        self.__alive = False

        # self.evloop.call_soon_threadsafe(self.evloop.stop)

    # ---

    def get_worker_stats(self):
        report  = ""
        report += "=================================\n"
        report +=f"== STATS THREAD {self.id}\n"
        report += "=================================\n"
        for w in self.__workers:
            report += w.PZA_WORKER_report()
        return report

    # ---

    def handle_worker_panic(self, worker_name):
        self.platform.panic()

    # ---

    def join(self):
        self.__thread.join()

    # ---

    def exec(self):
        # Create an event loop and start the driver
        self.evloop.run_until_complete(self.__async_exec())
        self.log.info("THREAD OUT !")

    # ---

    async def __async_exec(self):
        """Main execution function of the thread

        This function runs the worker and compute there load on the thread
        """

        for w in self.__workers:
            self.evloop.create_task( w.task(self.evloop) )

        # Continue the thread while the thread is alive
        while(self.__alive):
            await asyncio.sleep(1)

        self.log.info("Task OUT !")
