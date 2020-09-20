import time, requests ,threading, csmapi, DAN
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

ServerURL = 'https://demo.iottalk.tw' #with non-secure connection
Reg_addr='Countdown-I1-Default' # if None, Reg_addr = MAC address

DAN.profile['dm_name']='Countdown'
DAN.profile['df_list']=['Threshold-O1', 'Trigger-I1', 'Threshold-O2', 'Trigger-I2',
                    'Threshold-O3', 'Trigger-I3', 'Threshold-O4', 'Trigger-I4',
                    'Threshold-O5', 'Trigger-I5']
DAN.profile['d_name']= 'FarmLin' # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)
print('Register Countdown device.')
#DAN.deregister()  #if you want to deregister this device, uncomment this line
#exit()            #if you want to deregister this device, uncomment this line                                

def turn_off_job(toggle_id):
    print(datetime.now())
    DAN.push('Trigger-I{}'.format(toggle_id), 0)
    print ('Trigger-I{} push 0'.format(toggle_id))


scheduler = BackgroundScheduler()  
scheduler.start()

job_dict = {'toggle1': {'trigger_time': None, 'job': None},
            'toggle2': {'trigger_time': None, 'job': None},
            'toggle3': {'trigger_time': None, 'job': None},
            'toggle4': {'trigger_time': None, 'job': None}, }

while True:
    try:
        for toggle_id in range(1, 5):
            data = DAN.pull('Threshold-O{}'.format(toggle_id))
            
            if data is not None:
                data = data[0]
                trigger_time = None

                if data in (0, 1):
                    DAN.push('Trigger-I{}'.format(toggle_id), data)
                    print('Trigger-I{} push {}'.format(toggle_id, data))
                    print(job_dict['toggle{}'.format(toggle_id)]['trigger_time'])
                    if job_dict['toggle{}'.format(toggle_id)]['trigger_time'] is not None and \
                        datetime.now() < job_dict['toggle{}'.format(toggle_id)]['trigger_time']:
                        job3 = job_dict['toggle{}'.format(toggle_id)]['job']
                        job3.remove()
                        job_dict['toggle{}'.format(toggle_id)]['trigger_time'] = None
                    continue
                elif data == 2:
                    DAN.push('Trigger-I{}'.format(toggle_id), 1)
                    print ('Trigger-I{} push 1'.format(toggle_id))
                    trigger_time = datetime.now() + timedelta(minutes=1)
                elif data == 3:  
                    DAN.push('Trigger-I{}'.format(toggle_id), 1)
                    print ('Trigger-I{} push 1'.format(toggle_id))
                    trigger_time = datetime.now() + timedelta(minutes=2)
                elif data == 4:  
                    DAN.push('Trigger-I{}'.format(toggle_id), 1)
                    print ('Trigger-I{} push 1'.format(toggle_id))
                    trigger_time = datetime.now() + timedelta(minutes=3)

                if job_dict['toggle{}'.format(toggle_id)]['trigger_time'] is None or \
                   datetime.now() > job_dict['toggle{}'.format(toggle_id)]['trigger_time']:
                    job1 = scheduler.add_job(turn_off_job, 'date', args=[toggle_id],
                                             next_run_time=trigger_time)
                    job_dict['toggle{}'.format(toggle_id)]['job'] = job1
                else:
                    job2 = job_dict['toggle{}'.format(toggle_id)]['job']
                    job2.reschedule(trigger='date', run_date=trigger_time)

                if trigger_time is not None:
                    job_dict['toggle{}'.format(toggle_id)]['trigger_time'] = trigger_time

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)

    time.sleep(0.2)
