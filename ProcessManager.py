from multiprocessing import Process
import time


class ProcessManager:

    def run(self, proc_attrs, check_interval):
        proc_objects = []
        for key, value in proc_attrs.items():
            p = Process(target=value['func'], name=key, args=(value['arg'],))
            p.start()
            proc_objects.append(p)

        while True:
            for proc_object in proc_objects:
                print(str(proc_object) + ' - - ' + str(proc_object.is_alive()))
                if not proc_object.is_alive():
                    p = Process(target=proc_attrs[proc_object.name]['func'], name=proc_object.name
                                , args=(proc_attrs[proc_object.name]['arg'],))
                    p.start()
                    proc_object.terminate()
                    proc_objects.append(p)
                    proc_objects.remove(proc_object)

            time.sleep(check_interval)