import os
from time import time
from datetime import datetime
from potentiostat import Potentiostat
import pandas as pd

class PotentiostatsModel:

    def __init__(self):
        pass

    def read_all(self):
        """
        searches the operating system for connected serial ports
        """
        devlist = os.listdir('/dev')

        coms = [c for c in devlist if c.startswith('ttyACM')]

        pots = {}
        for c in coms:
            p = Potentiostat('/dev/{}'.format(c))
            _id = p.get_device_id()
            if p not in pots:
                pots['pot{}'.format(_id)] = p
        return pots

class ChronoampModel:

    def __init__(self):
        pass

    def run_test(self, potentiostat, print_values=True, **params):
        """
        runs Chronoamperometry Test with the given parameters.
        Otherwise, it uses default parameters.
        """
        test_name = params.get('test_name', 'chronoamp')
        curr_range = params.get('curr_range','100uA')
        sample_rate = params.get('sample_rate', 1)

        quietValue = params.get('quietValue', 0.0)
        quietTime = params.get('quietTime', 0)
        run_duration = params.get('run_duration', 3000)
        step1_volt = params.get('step1_volt', 0.05)
        step1_duration = params.get('step1_duration', 3000)
        step2_volt = params.get('step2_volt', 0.0)
        step2_duration = params.get('step2_duration', 0)

        step = [
            (step1_duration, step1_volt),
            (step2_duration, step2_volt)]

        param = {
            'quietValue': quietValue,
            'quietTime': quietTime,
            'step': step
        }

       ### Setting Parameters ###
        potentiostat.set_param(test_name, param)
        potentiostat.set_curr_range(curr_range)
        potentiostat.set_sample_rate(sample_rate)

       ### Getting Parameters ###
        out_volt_range = potentiostat.get_volt_range()
       ### Total Duration Time ###
        step_duration = step1_duration + step2_duration
        time_all = []
        volt_all = []
        current_all = []
        start_time = datetime.now()

        while run_duration != 0:

            time, volt, current = potentiostat.run_test(test_name, display='pbar')
            time_all += time
            volt_all += volt
            current_all += current

            run_duration -= step_duration

        end_time = datetime.now()
        d = {
            'start_time': start_time,
            'end_time': end_time,
            'time': time_all,
            'voltage': volt_all,
            'current': current_all,
            'quietValue': quietValue,
            'quietTime': quietTime,
            'run_duration': run_duration,
            'step1_duration': step1_duration,
            'step1_volt': step1_volt,
            'step2_duration': step2_duration,
            'step2_volt': step2_volt,
            'sample_rate': sample_rate,
            'curr_range': curr_range,
            'out_volt_range': out_volt_range,
            'test_name': test_name,
            'potentio_id': potentiostat.get_device_id(),
            'electrode': params.get('electrode', None)
         }

        df = pd.DataFrame(d)
        filename = '{}'.format(
            params.get('filename','./data_chronoamp.csv'))
        newfile = not os.path.exists(filename)

        if newfile:
            df.to_csv(filename)
        else:
            df.to_csv(filename, mode='a', header=False)

        if print_values:
            print('Time {0}, Voltage {1}, Current {2}'
                .format(time_all, volt_all, current_all))
            print('Out_Volt_range: {}'.format(out_volt_range))
            print('Out_Curr_Range: {}'.format(curr_range))