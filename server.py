import atexit
import logging
import time 
import threading
import json

from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask import render_template, url_for
from flask import request
from flask import jsonify

import DAN 

from config import env_config

app = Flask(__name__)
back_data = None

scheduler = BackgroundScheduler()  
scheduler.start()

job_dict = {'toggle1': {'turn_off_time': None, 'job': None, 'toggle_value': None, 'trigger_status': None},
            'toggle2': {'turn_off_time': None, 'job': None, 'toggle_value': None, 'trigger_status': None},
            'toggle3': {'turn_off_time': None, 'job': None, 'toggle_value': None, 'trigger_status': None},
            'toggle4': {'turn_off_time': None, 'job': None, 'toggle_value': None, 'trigger_status': None}, }

def turn_off_job(toggle_id):
    #print(datetime.now())
    DAN.push('5Toggle-I{}'.format(toggle_id), 0)
    print ('5Toggle-I{} push 0'.format(toggle_id))
    job_dict['toggle{}'.format(toggle_id)]['trigger_status'] = 0
    get_turn_off_data = {'id': toggle_id, 'turn_off_time': job_dict['toggle{}'.format(toggle_id)]['turn_off_time'].strftime('%H:%M'), 'toggle_value': job_dict['toggle{}'.format(toggle_id)]['toggle_value'], 'trigger_status': job_dict['toggle{}'.format(toggle_id)]['trigger_status']}
    print(get_turn_off_data)  

def on_exit():
    # DAN.deregister()
    return

@app.route('/')
def main_page():
    return render_template('index.html', data=job_dict)

@app.route('/<df>', methods=['POST'])
def get_push(df):
    data = request.json
    back_data = schedule_job(data)
    print(back_data)
    return jsonify(back_data), 200

def schedule_job(data):
    toggle_id = data['toggle_id']
    toggle_value = data['value']
    turn_off_time = None
    trigger_status = None

    if toggle_value in (0, 1):
        DAN.push('5Toggle-I{}'.format(toggle_id), toggle_value)
        print('5Toggle-I{} push {}'.format(toggle_id, toggle_value))
        job_dict['toggle{}'.format(toggle_id)]['toggle_value'] = toggle_value
        job_dict['toggle{}'.format(toggle_id)]['trigger_status'] = toggle_value
        trigger_status = toggle_value
        if job_dict['toggle{}'.format(toggle_id)]['turn_off_time'] is not None and \
            datetime.now() < job_dict['toggle{}'.format(toggle_id)]['turn_off_time']:
            job3 = job_dict['toggle{}'.format(toggle_id)]['job']
            job3.remove()
            job_dict['toggle{}'.format(toggle_id)]['turn_off_time'] = None
        elif job_dict['toggle{}'.format(toggle_id)]['turn_off_time'] is not None and \
            datetime.now() > job_dict['toggle{}'.format(toggle_id)]['turn_off_time']:
            job_dict['toggle{}'.format(toggle_id)]['turn_off_time'] = None
        return {'id': toggle_id, 'turn_off_time': '', 'toggle_value': toggle_value, 'trigger_status': trigger_status}
    elif toggle_value == 2:
        DAN.push('5Toggle-I{}'.format(toggle_id), 1)
        print ('5Toggle-I{} push 1'.format(toggle_id))
        turn_off_time = datetime.now() + timedelta(minutes=1) 
    elif toggle_value == 3:  
        DAN.push('5Toggle-I{}'.format(toggle_id), 1)
        print ('5Toggle-I{} push 1'.format(toggle_id))
        turn_off_time = datetime.now() + timedelta(minutes=2)
    elif toggle_value == 4:  
        DAN.push('5Toggle-I{}'.format(toggle_id), 1)
        print ('5Toggle-I{} push 1'.format(toggle_id))
        turn_off_time = datetime.now() + timedelta(minutes=3) 

    trigger_status = 1  

    if job_dict['toggle{}'.format(toggle_id)]['turn_off_time'] is None or \
       datetime.now() > job_dict['toggle{}'.format(toggle_id)]['turn_off_time']:
        job1 = scheduler.add_job(turn_off_job, 'date', args=[toggle_id],
                                 next_run_time=turn_off_time) 
        job_dict['toggle{}'.format(toggle_id)]['job'] = job1
    else:
        job2 = job_dict['toggle{}'.format(toggle_id)]['job']
        job2.reschedule(trigger='date', run_date=turn_off_time)
    

    if turn_off_time is not None:
        job_dict['toggle{}'.format(toggle_id)]['turn_off_time'] = turn_off_time
    if toggle_value is not None:
        job_dict['toggle{}'.format(toggle_id)]['toggle_value'] = toggle_value 
    if trigger_status is not None:
        job_dict['toggle{}'.format(toggle_id)]['trigger_status'] = trigger_status
    

    back_data = {'id': toggle_id, 'turn_off_time': turn_off_time.strftime('%H:%M'), 'toggle_value': toggle_value, 'trigger_status': trigger_status  }
    
    return back_data

@app.route('/list_all', methods=['GET'])
def list_all():
    new_dict = {'toggle1': {},
                'toggle2': {},
                'toggle3': {},
                'toggle4': {}, }

    for i in range(1, 5):
        new_dict['toggle{}'.format(i)]['turn_off_time'] = job_dict['toggle{}'.format(i)]['turn_off_time']
        new_dict['toggle{}'.format(i)]['toggle_value'] = job_dict['toggle{}'.format(i)]['toggle_value']
        new_dict['toggle{}'.format(i)]['trigger_status'] = job_dict['toggle{}'.format(i)]['trigger_status']
    
    return jsonify(new_dict), 200


if '__main__' == __name__:
    DAN.profile = env_config.ctlboard_profile
    DAN.device_registration_with_retry(env_config.server_ip, env_config.mac_addr)

    atexit.register(on_exit)

    app.run(
        host=env_config.host,
        port=env_config.port,
        threaded=True,
        debug=True
    )
