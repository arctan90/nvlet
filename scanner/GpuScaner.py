import threading
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler


class GpuScaner:
    def __init__(self):
        self.scheduler = BlockingScheduler()

    def start(self):
        self.scheduler.add_job(_job, 'interval', seconds=20)
        thread = threading.Thread(target=self.scheduler.start())
        thread.daemon = True
        thread.start()


# key-gpuId value-busy:True
gpu_busy_map_smi = {}


def _job():
    try:
        # invoke nvidia-smi
        result = subprocess.check_output(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'])

        # decode
        gpu_utilization = [float(utilization) for utilization in result.decode('utf-8').strip().split('\n')]

        for gpu_id, utilization in enumerate(gpu_utilization):
            gpu_busy_map_smi[gpu_id] = utilization > 10.0

        print(gpu_busy_map_smi)

    except Exception as e:
        print(f"Error: {e}")
