from time import time
import os
import pandas as pd
from datetime import datetime
import csv
from potentiostat import Potentiostat


def read_pots():
    devlist = os.listdir('/dev')

    coms = [c for c in devlist if c.startswith('ttyACM')]

    pots = {}
    for c in coms:
        p = Potentiostat('/dev/{}'.format(c))
        _id = p.get_device_id()
        if p not in pots:
            pots['pot{}'.format(_id)] = p
    return pots

#pots = read_pots()

def chronoamperometry(p, print_values=True, **params):

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
    p.set_param(test_name, param)
    p.set_curr_range(curr_range)
    p.set_sample_rate(sample_rate)

### Getting Parameters ###
    out_volt_range = p.get_volt_range()
### Total Duration Time ###
    step_duration = step1_duration + step2_duration
    time_all = []
    volt_all = []
    current_all = []
    start_time = datetime.now()
     
    while run_duration != 0:

        time, volt, current = p.run_test(test_name, display='pbar')
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
        'potentio_id': p.get_device_id(),
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
        

def cyclic_voltammetry(p, **params):
    # getting Parameters
    quietValue = params.get('quietValue', 0)
    quietTime = params.get('quietTime', 0)
    minVolt = params.get('minVolt', -0.2)
    maxVolt = params.get('maxVolt', 1)
    scanRate = params.get('scanRate', 0.1)
    numCycles = params.get('numCycles', 10)
    shift = params.get('shift', 0.0)
    curr_range = params.get('curr_range', '100uA')
    test_name = params.get('test_name', 'cyclic')
  
    amplitude = 0.5 * ((maxVolt) - (minVolt))
    offset = 0.5 * ((maxVolt) + (minVolt))
    period = int(
        4* params.get('periodfactor', 1000) * amplitude / scanRate)

    param = {
        'quietValue': quietValue,
        'quietTime': quietTime,
        'amplitude': amplitude,
        'offset': offset,
        'period': period,
        'numCycles': numCycles,
        'shift': shift
        }

    # setting parameters
    p.set_param(test_name, param)
    p.set_curr_range(curr_range)
    p.set_sample_rate(10)
    # running
    t, v, c = p.run_test(test_name)
    print('Time {0}, Voltage {1}, Current {2}'
          .format(t, v, c)) 
    d = {
        'time': t,
        'voltage': v,
        'current': c,
        'quietValue': quietValue,
        'quietTime': quietTime,
        'amplitude': amplitude,
        'offset': offset,
        'period': period,
        'numCycles': numCycles,
        'shift': shift,
        'test_name': test_name,
        'potentio_id': p.get_device_id(),
        'electrode': params.get('electrode', None)
         }
    df = pd.DataFrame(d)
    try:
        df.to_csv('{}'.format(params.get('filename', './data_cv.csv')),
            mode='a', header=False)
    except:
        df.to_csv('./data_cv.csv')


#def export_data()
