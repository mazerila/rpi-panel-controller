#!/usr/bin/env python3
#
# The Raspberry Pi panel controller is the client part of IoT panel advertising project.
# This is the main file of the project which could communicate with the Azure server to send 
# telemetry and receive commands and execute them using PanelDisplay.
# git commit -m "Add setLogger to common, tiny modif in deviceConfig"

import os
import sys
import json
import random
import asyncio
import logging
import datetime
from time import time
from pathlib import Path
from threading import Thread

from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
from azure.iot.device import Message

from matrix_config import MatrixConfig
from device_config import DeviceConfig
from panel import PanelDisplay
import common

#--------------------------------------------------------------
# todo: 
# 1. receive commands from server
# 2. apply received commands
#--------------------------------------------------------------

 
## Register the device and connect it to your IoT Central application. 
## Registration uses the Azure Device Provisioning Service.
async def register_device(deviceConf):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=deviceConf.provisioningHost,
        registration_id=deviceConf.registrationId,
        id_scope=deviceConf.idScope,
        symmetric_key=deviceConf.symmetricKey,
    )

    registration_result = await provisioning_device_client.register()

    print(f'Registration result: {registration_result.status}')

    return registration_result

async def connect_device(deviceConf):
    device_client = None
    try:
        registration_result = await register_device(deviceConf)
        if registration_result.status == 'assigned':
            device_client = IoTHubDeviceClient.create_from_symmetric_key(
                symmetric_key=deviceConf.symmetricKey,
                hostname=registration_result.registration_state.assigned_hub,
                device_id=registration_result.registration_state.device_id,
            )
            # Connect the client.
            await device_client.connect()
            print('Device connected successfully')
    finally:
        return device_client
    
    
## Send telemetry to your IoT Central application
async def send_telemetry(device_client, deviceConf):
    lat = random.randrange(39000, 42000) / 1000
    lon = random.randrange(43000, 46000) / 1000
    print(f'Sending telemetry from the provisioned device every {deviceConf.syncInterval} seconds')
    while True:
        lat = lat + (random.randrange(-100, 100) / 10000)
        lon = lon + (random.randrange(-100, 100) / 10000)
        payload = json.dumps({'latitude': lat, 'longitude': lon})
        msg = Message(payload)
        await device_client.send_message(msg, )
        print(f'Sent message: {msg}')
        await asyncio.sleep(deviceConf.syncInterval)


## Handle commands called from your IoT Central application
async def diagnostics_command(request):
    print('Starting asynchronous diagnostics run...')
    response = MethodResponse.create_from_method_request(
        request, status = 202
    )
    await device_client.send_method_response(response)    # send response
    print('Generating diagnostics...')
    await asyncio.sleep(2)
    print('Generating diagnostics...')
    await asyncio.sleep(2)
    print('Generating diagnostics...')
    await asyncio.sleep(2)
    print('Sending property update to confirm command completion')
    await device_client.patch_twin_reported_properties({'rundiagnostics': {'value': f'Diagnostics run complete at {datetime.datetime.today()}.'}})

async def turnOff_command(request):
    print('Turning off the device')
    response = MethodResponse.create_from_method_request(
        request, status = 200
    )
    await device_client.send_method_response(response)    # send response

async def restartDevice_command(request):
    print('Restarting the device')
    response = MethodResponse.create_from_method_request(
        request, status = 200
    )
    await device_client.send_method_response(response)    # send response

async def display_command(request):
    print('Received synchronous call to display')
    response = MethodResponse.create_from_method_request(
        request, status = 200, payload = {'description': f'Displaying image on panel for {request.payload} seconds'}
    )
    await device_client.send_method_response(response)    # send response
    th_panel.play(th_panel.contentType)

async def stop_command(request):
    print('Stopping the viewer')
    response = MethodResponse.create_from_method_request(
        request, status = 200
    )
    await device_client.send_method_response(response)    # send response
    th_panel.terminate()
    
async def restartViewer_command(request):
    print('Restarting the viewer')
    response = MethodResponse.create_from_method_request(
        request, status = 200
    )
    await device_client.send_method_response(response)    # send response
    th_panel.restart()
    
async def setFileName_command(request):
    print('Set the file name')
    response = MethodResponse.create_from_method_request(
        request, status = 200
    )
    await device_client.send_method_response(response)    # send response
    print(request.payload)
    th_panel.filename = request.payload
    print("file= ", th_panel.filename)
    
async def setContentType_command(request):
    print('Set te content type to be displayed')
    response = MethodResponse.create_from_method_request(
        request, status = 200
    )
    await device_client.send_method_response(response)    # send response
    th_panel.contentType = request.payload
    
# Define behavior for handling commands
async def command_listener():
    while True:
        method_request = await device_client.receive_method_request()    # Wait for commands
        await commands[method_request.name](method_request)


## Handle property updates sent from your IoT Central application. 
## The message the device sends in response to the writeable property update must include the av and ac fields. The ad field is optional
async def customerName_setting(value, version):
    await asyncio.sleep(1)
    print(f'Setting customerName value {value} - {version}')
    await device_client.patch_twin_reported_properties({'customerName' : {'value': value, 'ad': 'completed', 'ac': 200, 'av': version}})

async def brightness_setting(value, version):
    await asyncio.sleep(5)
    print(f'Setting brightness value {value} - {version}')
    await device_client.patch_twin_reported_properties({'brightness' : {'value': value, 'ad': 'completed', 'ac': 200, 'av': version}})
 
async def state_setting(value, version):
    await asyncio.sleep(5)
    print(f'Setting state value {value} - {version}')
    await device_client.patch_twin_reported_properties({'state' : {'value': value, 'ad': 'completed', 'ac': 200, 'av': version}})

        
# define behavior for receiving a twin patch
async def twin_patch_listener():
    while True:
        patch = await device_client.receive_twin_desired_properties_patch() # blocking
        to_update = patch.keys() & settings.keys()
        await asyncio.gather(
            *[settings[setting](patch[setting], patch['$version']) for setting in to_update]
        )
        

## Control the application
# Define behavior for halting the application
def stdin_listener():
    while True:
        selection = input('Press Q to quit\n')
        if selection == 'Q' or selection == 'q':
            print('Quitting...')
            killed = common.killAll()
            if killed > 0:
                logging.info(str(killed)+" running viewer(s) already exist..")
            break

#--------------------------------------------------------------
# Global vriables


#--------------------------------------------------------------
# Main thread

async def main():
    common.setLogger()
    logging.info('<< Started >>')
    ts = time()
    
    try:
        global th_panel
        th_panel = PanelDisplay(1, "Th-display")
    except:
        logging.info("Error: unable to create thread")
        
    # load connection information.
    global deviceConf
    deviceConf = DeviceConfig()

    global commands
    commands = {
        'turnOff': turnOff_command,
        'restartDevice': restartDevice_command,
        'display': display_command,
        'stop': stop_command,
        'restartViewer': restartViewer_command,
        'setFileName': setFileName_command,
        'setContentType': setContentType_command,
    }
     
    global settings
    settings = {
        'customerName': customerName_setting,
        'brightness': brightness_setting,
        'state': state_setting
    }

    global device_client
    device_client = await connect_device(deviceConf)

    if device_client is not None and device_client.connected:
        print('Send reported properties on startup')
        await device_client.patch_twin_reported_properties({'state': 'true', 'processorArchitecture': 'ARM', 'swVersion': '1.0.0'})
        tasks = asyncio.gather(
            send_telemetry(device_client, deviceConf),
            command_listener(),
            twin_patch_listener(),
        )

        # Run the stdin listener in the event loop
        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)
        
        # Wait for user to indicate they are done listening for method calls
        await user_finished

        # Cancel tasks
        tasks.add_done_callback(lambda r: r.exception())
        tasks.cancel()
        await device_client.disconnect()

    else:
        print('Device could not connect')


    logging.info('Exiting Main Thread : Took %s', time() - ts)
    logging.info('<< Exited >>')
        
if __name__ == '__main__':
    asyncio.run(main())



#--------------------------------------------------------------
