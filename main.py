from configparser import ConfigParser

import subprocess
import time

from pypresence import Presence

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)

client_id = config['Client']['ClientID']
if config['Client']['Program'] != '[Optional]' or not config['Client']['Program']:
    program = config['Client']['Program']
else:
    program = None

if config['States']['State'] != '<Required>' or not config['States']['State']:
    state = config['States']['State']
else:
    state = 'Left unchanged'

if config['States']['Details'] != '[Optional]' or not config['States']['Details']:
    details = config['States']['Details']
else:
    details = None

if config['States']['ElapsedTime'] == 'True':
    start = time.time()
else:
    start = None

if config['Images']['LargeImage'] != '[Optional]' or not config['Images']['LargeImage']:
    large_image = config['Images']['LargeImage']
else:
    large_image = None

if config['Images']['SmallImage'] != '[Optional]' or not config['Images']['SmallImage']:
    small_image = config['Images']['SmallImage']
else:
    small_image = None

if config['Images']['LargeTooltip'] != '[Optional]' or not config['Images']['LargeTooltip']:
    large_tooltip = config['Images']['LargeTooltip']
else:
    large_tooltip = None

if config['Images']['SmallTooltip'] != '[Optional]' or not config['Images']['SmallTooltip']:
    small_tooltip = config['Images']['SmallTooltip']
else:
    small_tooltip = None

rpc = Presence(client_id)

print(f'Application ID: {client_id}')
print(f'Program: {program}')
print(f'State: {state}')
print(f'Details: {details if details else "None (Optional)"}')
print(f'Elapsed Time: {"On" if start else "Off"}')
print(
    f'Large Image: {large_image}{" with tooltip/text" if large_tooltip else ""}')
print(
    f'Small Image: {small_image}{" with tooltip/text" if small_tooltip else ""}\n')

print('Connecting presence...')

connected = 0

try:
    while True:
        subprocesses = subprocess.check_output('tasklist', shell=True)

        if program:
            if program.encode('utf-8') in subprocesses and not connected:
                rpc.connect()
                print(f'{program} detected!')
                print('Presence connected!\n')
                rpc.update(state=state, details=details, start=start, large_image=large_image,
                           small_image=small_image, large_text=large_tooltip, small_text=small_tooltip)
                connected = 1

            if program.encode('utf-8') not in subprocesses and connected:
                rpc.close()
                print(f'{program} not detected anymore.')
                print('Presence disconnected...\n')
                connected = 0
        else:
            try:
                print('Connection may take awhile...')
                rpc.connect()
                if not connected:
                    rpc.update(state=state, details=details, start=start, large_image=large_image,
                               small_image=small_image, large_text=large_tooltip, small_text=small_tooltip)
                    print('Presence connected!\n')
                    connected = 1
            except KeyboardInterrupt:
                if connected:
                    rpc.close()
                print('Disconnecting presence...')
                print('Exiting program...')
                time.sleep(2)
                break
            except:
                print('Presence failed to connect...')
                print('Exiting program...')
                time.sleep(2)
                break

        time.sleep(1)

except KeyboardInterrupt:
    if connected:
        rpc.close()
    print('Disconnecting presence...')
    print('Exiting program...')
    time.sleep(2)
