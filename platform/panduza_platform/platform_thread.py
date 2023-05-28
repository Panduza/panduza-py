import time
import asyncio
import threading


class PlatformThread:

    ID_COUNT = 0

    PERF_CYCLE_TIME = 2

    # ---

    def __init__(self) -> None:
        self.id = PlatformThread.ID_COUNT
        PlatformThread.ID_COUNT += 1

        self.__alive = True

        self.__mutex = threading.Lock()

        # List of managed worker 
        self.__workers = []


    # ---

    def attach_worker(self, worker):
        self.__mutex.acquire()
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
        self.evloop = asyncio.new_event_loop()
        self.evloop.run_until_complete(self.__async_exec())

    # ---

    async def __async_exec(self):

        while(self.__alive):
            # 
            self.__mutex.acquire()

            # Run works during 1 time cycle
            loop_t0 = time.perf_counter()
            while(time.perf_counter() - loop_t0 < PlatformThread.PERF_CYCLE_TIME):
                for w in self.__workers:
                    await w.work()
                await asyncio.sleep(0.01)

            # Compute work time
            work_time = 0
            for w in self.__workers:
                work_time += w.work_time
                w.reset_work_time()

            # Compute loop time
            loop_time = time.perf_counter() - loop_t0

            # 
            print(f"{work_time} - {loop_time}")
            print(f"pok {(work_time/loop_time) * 100.0} %")

            # 
            self.__mutex.release()


    #     def detach_worker(self, worker):
