import time
import threading


class PlatformThread:
    
    ID_COUNT = 0

    # ---

    def __init__(self) -> None:
        self.id = PlatformThread.ID_COUNT
        PlatformThread.ID_COUNT += 1

        self.__alive = True

        # List of managed worker 
        self.__workers = []


    # ---

    def attach_worker(self, worker):
        self.__workers.append(worker)

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
        
                
        while(self.__alive):

            loop_t0 = time.perf_counter()
            work_time = 0

            while(time.perf_counter() - loop_t0 < 1):

                work_t0 = time.perf_counter()
                print("pif")
                # time.sleep(0.0001)
                work_time += (time.perf_counter() - work_t0)

                time.sleep(0.0001)

    #             For w in self.__workers:
    #                    w.exec()


    #              If (tnow - t_start > 1):
    #                     Compute stats

            loop_time = time.perf_counter() - loop_t0

            print(f"{work_time} - {loop_time}")
            print(f"pok {(work_time/loop_time) * 100.0} %")



    #     def detach_worker(self, worker):
