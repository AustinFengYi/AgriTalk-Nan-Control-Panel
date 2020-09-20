import logging

class EnvironmentConfig(): 
    host = '0.0.0.0'
    port = 7789
    df_his_record_len = 200
    max_thresholds = 5 
    server_ip = 'https://demo.iottalk.tw'
    mac_addr = 'Customized_button__NanLinTriggers'
    ctlboard_profile = {
        'd_name': 'NanLinTriggers',
        'dm_name': 'FiveToggle',
        'u_name': 'yb',
        'is_sim': False,
        'df_list': ['5Toggle-I1','5Toggle-I2','5Toggle-I3','5Toggle-I4','5Toggle-I5'],
    } 

env_config = EnvironmentConfig() 