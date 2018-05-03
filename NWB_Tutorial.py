
from datetime import datetime
from pynwb import NWBFile, TimeSeries
from pynwb import NWBHDF5IO
from pynwb.ecephys import LFP

"""
-Code used from the NWB Tutorial found here: http://pynwb.readthedocs.io/en/latest/tutorials/index.html
-Contains a simple function to write an NWB Test File and a random data generator to create the data
used for the test NWB File
-Contains comments to describe each class type
"""

# Function to create a test NWBfile
# parameters are filename and data
def write_test_file(filename, data):
    """
    Simple helper function to write an NWBFile with a single timeseries containing data
    :param filename: String with the name of the output file
    :param data: The data of the timeseries
    """

    # datetime is a combination of date and time
    # datetime(year, month, day, hour, minute, second)
    start_time = datetime(2017, 4, 3, 11, 0, 0)
    create_date = datetime(2017, 4, 15, 12, 0, 0)

    # create a test NWBFile
    # NWBFile(source, description, identifier, session_start_time, file_create_date)
    # there are many more inputs that can be added, however by default
    # they are none
    # use the tutorial as the source for now
    nwbfile = NWBFile('PyNWB tutorial',
                      'demonstrate NWBFile basics',
                      'NWB123',
                      start_time,
                      file_create_date=create_date)

    # create a time series
    # TimeSeries(name, source, data, unit, rate, starting time)
    # rate is the sampling rate in Hz
    # starting_time is the timestamp of the first sample
    test_ts = TimeSeries(name='synthetic_timeseries',
                         source='PyNWB tutorial',
                         data=data,
                         unit='SIunit',
                         rate=1.0,
                         starting_time=0.0)
    # add a new NWBDataInterface to this NWBFile
    nwbfile.add_acquisition(test_ts)

    # ElectricalSeries(name,source,data,electrodes)

    """
    elec_series= ElectricalSeries('test_electricalseries',
                                  'PyNWB tutorial',
                                  test_ts,
                                  )
    """

    # electrodes are an ElectrodeTableRegion type
    # ElectrodeTableRegion(table,region,description,name)
    # need more information about what to include for the ElectricalSeries

    # Write the data to file
    # NWBHDF5IO(path, mode='a')
    io = NWBHDF5IO(filename, 'w')
    io.write(nwbfile)
    io.close()

# Step 1: Define the data generator

from math import sin, pi
from random import random
import numpy as np


def iter_sin(chunk_length=10, max_chunks=100):
    """
    Generator creating a random number of chunks (but at most max_chunks) of length chunk_length containing
    random samples of sin([0, 2pi]).
    """
    x = 0
    num_chunks = 0
    while(x < 0.5 and num_chunks < max_chunks):
        val = np.asarray([sin(random() * 2 * pi) for i in range(chunk_length)])
        x = random()
        num_chunks += 1
        yield val
    return

# Step 2: Wrap the generator in a DataChunkIterator

from pynwb.form.data_utils import DataChunkIterator

data = DataChunkIterator(data=iter_sin(10))

# Step 3: Write the data as usual
# Here we use our wrapped generator to create the data for a synthetic time series.

write_test_file(filename='NWB_Tutorial_Trial.nwb',
                data=data)

print("maxshape=%s, recommended_data_shape=%s, dtype=%s" % (str(data.maxshape),
                                                            str(data.recommended_data_shape()),
                                                            str(data.dtype)))

