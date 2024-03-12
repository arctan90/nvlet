import threading

from apscheduler.schedulers.blocking import BlockingScheduler
import torch


class GpuScaner:
    def __init__(self):
        self.scheduler = BlockingScheduler()

    def start(self):
        self.scheduler.add_job(_job, 'interval', seconds=20)

        thread = threading.Thread(target=self.scheduler.start())
        thread.daemon = True
        thread.start()


# key-gpuId value-busy:True
gpu_busy_map = {}


def _job():
    global gpu_busy_map
    print("Getting GPU information...")
    try:
        gpu_ids = torch.cuda.device_count()

        for gpu_id in range(gpu_ids):
            current_stream = torch.cuda.current_stream(gpu_id)
            gpu_busy_map[gpu_id] = not current_stream.is_waiting()
        print(gpu_busy_map)
    except Exception as e:
        print(f"Error: {e}")
