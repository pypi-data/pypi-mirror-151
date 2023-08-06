from pathlib import Path
from time import perf_counter
from datetime import timedelta

import numpy as np
from mkr_format import open_combined_file


__mkr_file__ = Path("/media/groups/machine_learning/temp/mx.mkr")


class Read:

    @profile
    def __init__(self, read, meta=False):

        self.meta = meta
        self.read_id = read.read_id
        self.run_info = read.run_info
        self.sample_id = self.run_info.sample_id
        self.run_id = self.run_info.acquisition_id

        self.acquisition_start_time = self.run_info.acquisition_start_time
        self.exp_start_time = self.acquisition_start_time.isoformat().replace('Z', '')

        self.flow_cell_id = self.run_info.flow_cell_id
        self.device_id = self.run_info.sequencer_position

        if self.meta:
            return

        self.pore = read.pore
        self.mux = self.pore.well
        self.channel = self.pore.channel
        self.read_number = read.read_number
        
        self.context_tags = dict(self.run_info.context_tags)
        self.sample_rate = int(self.context_tags['sample_frequency'])

        self.raw = read.signal
        self.num_samples = len(self.raw)

        self.start = read.start_sample / self.sample_rate
        self.duration = self.num_samples / self.sample_rate

        start_time = self.acquisition_start_time + timedelta(seconds=self.start)
        self.start_time = start_time.replace(microsecond=0).isoformat()

        self.calibration = read.calibration
        self.scaling = self.calibration.scale
        self.offset = self.calibration.offset

        scaled = self.scaling * (self.raw.astype(np.float32) + self.offset)

        # expensive normalisation would come here..o
        # ...


def get_reads(meta=False):
    for read in open_combined_file(__mkr_file__).reads():    
        yield Read(read, meta)


if __name__ == "__main__":

    samples = 0
    
    t0 = perf_counter()
    for read in get_reads(meta=False):
        samples += read.num_samples
    duration = perf_counter() - t0    
    
    print("> full read duration: %s" % timedelta(seconds=np.round(duration)))
    print("> samples per second %.1E" % (samples / duration))
    

    t0 = perf_counter()
    for read in get_reads(meta=True):
        ...
    duration = perf_counter() - t0    
    
    print("> just meta data duration: %s" % timedelta(seconds=np.round(duration)))
    print("> samples per second %.1E" % (samples / duration))
