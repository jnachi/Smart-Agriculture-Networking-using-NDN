#Author for Udp Global & local Broadcast, Tcp Request and response - Nachiketh and Pradyumn
#Author for sensor data generation, evaluation, Data Encryption and sending request- Madhumati and Ramya

import asyncio
import json
import socket
from asyncio import DatagramTransport
import threading
from typing import Tuple
import random
import argparse
import re
import rsa

#Author for sensor data generation, evaluation- Madhumati and Ramya

async def generate_data(sensorType,udp):
    while True:
        for i in sensorType:
            sensor_data_generation(udp, i)
        await asyncio.sleep(5)

def sensor_data_generation(udp, sensor_type):
    if udp.vehicle_name not in udp.sensor:
        udp.sensor[udp.vehicle_name] = {}

    if sensor_type == 'temperature':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(-10, 40)), 5]
    elif sensor_type == 'humidity':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 100)), 5]
    elif sensor_type == 'pressure':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(900, 1100)), 5]
    elif sensor_type == 'ph':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 14)), 5]
    elif sensor_type == 'nitrogen':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 100)), 5]
    elif sensor_type == 'nutrients':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 100)), 5]
    elif sensor_type == 'potassium':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 100)), 5]
    elif sensor_type == 'moisture':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 100)), 5]
    elif sensor_type == 'speed':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(80), 5]
    elif sensor_type == 'direction':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 360)), 5]
    elif sensor_type == 'uv':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 10)), 5]
    elif sensor_type == 'co2':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 1000)), 5]
    elif sensor_type == 'rainfall':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 50)), 5]
    elif sensor_type == 'position':
        udp.sensor[udp.vehicle_name][sensor_type] = [[str(random.uniform(-180, 180)), str(random.uniform(-90, 90))], 5]
    elif sensor_type == 'rgb':
        udp.sensor[udp.vehicle_name][sensor_type] = [[str(random.randint(0, 255)), str(random.randint(0, 255)), str(random.randint(0, 255))], 5]
    elif sensor_type == 'infrared':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 100)), 5]
    elif sensor_type == 'altitude':
         udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 5000)), 5]
    elif sensor_type == 'dissolvedo2':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 20)), 5]
    elif sensor_type == 'acidic':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 14)), 5]
    elif sensor_type == 'hydration':
        udp.sensor[udp.vehicle_name][sensor_type] = [str(random.uniform(0, 100)), 5]
    elif sensor_type == 'health':
        udp.sensor[udp.vehicle_name][sensor_type] = {
        'temperature': [str(random.uniform(20, 35)), 5],
        'humidity': [str(random.uniform(40, 80)), 5],
        'nutrient_levels': [str(random.uniform(0, 100)), 5],
        'pest_infestation': [str(random.uniform(0, 10)), 5],
        'water_availability': [str(random.uniform(30, 70)), 5],
        'growth_stage': [random.choice(['germination', 'vegetative', 'flowering', 'harvest']), 5],
    }
        pass
    else:
        print(f"Unknown sensor type: {sensor_type}")

def evaluate_data(sensor_type, data):
    if sensor_type == 'temperature':
        if float(data) > 30:
            print("Temperature is too high. Take necessary actions.")
        else:
            print("Temperature is Optimal.")
    elif sensor_type == 'humidity':
        if float(data) > 80:
            print("High humidity detected. Take necessary actions.")
        else:
            print("Humidity is Optimal.")
    elif sensor_type == 'pressure':
        if float(data) < 950 or float(data) > 1050:
            print("Pressure is outside the optimal range. Take necessary actions.")
        else:
            print("Pressure is Optimal.")
    elif sensor_type == 'speed':
        if float(data) > 60:
            print("High speed detected. Take necessary actions.")
        else:
            print("Speed is Optimal.")
    elif sensor_type == 'co2':
        if float(data) > 500:
            print("High CO2 levels detected. Take necessary actions.")
        else:
            print("CO2 level is Optimal.")
    elif sensor_type == 'ph':
        if float(data) < 6 or float(data) > 8:
            print("pH level is outside the optimal range. Take necessary actions.")
        else:
            print("pH level is Optimal.")
    elif sensor_type == 'nutrients':
        if float(data) < 30 or float(data) > 70:
            print("Nutrient levels are outside the optimal range. Take necessary actions.")
        else:
            print("Nutrients level is Optimal.")
    elif sensor_type == 'moisture':
        if float(data) < 40 or float(data) > 80:
             print("Moisture level is outside the optimal range. Take necessary actions.")
        else:
            print("Moisture is Optimal.")
    elif sensor_type == 'position':
        if -180 <= float(data[0]) <= 180 and -90 <= float(data[1]) <= 90:
            print("Valid position data. No action required.")
        else:
            print("Invalid position data. Take necessary actions.")
    else:
        print(f"Unknown sensor type: {sensor_type}")





class _Address:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def __eq__(self, other):
        return self.host == other.host and self.port == other.port

    def __hash__(self):
        return hash((self.host, self.port))

    def __str__(self):
        return f"{self.host}:{self.port}"

#Author for Udp Global & local Broadcast - Nachiketh and Pradyumn

class Device:
    def __init__(self, network, name, port) -> None:
        self.udp_port = port
        self.udp_local_port = self.udp_port + 1
        self.tcp_port = self.udp_port + 200
        self.network = network
        self.vehicle_name = name
        self.hostname = socket.gethostbyname(socket.gethostname())
        self.fib = {}
        self.sensor = {}
        self.announcement = {
            "heartbeat": "ALIVE",
            "NEIGHBOURS": self.hostname,
            "vehicle_name": self.vehicle_name,
            "network": self.network,
            "port": self.tcp_port
        }

    async def start_GlobalUdp(self):
        # Listen for announcements
        class Protocol:
            def connection_made(_, transport: DatagramTransport):
                print(f"UDP transport established: {transport}")

            def connection_lost(_, e: Exception):
                print(f"UDP transport lost: {e}")

            def datagram_received(_, data: bytes, addr: Tuple[str, int]):
                self.on_recieve(data, _Address(*addr[0:2]))
                
            def error_received(_, e: OSError):
                print(f"UDP transport error: {e}")

        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(lambda: Protocol(),
                                                                local_addr=("0.0.0.0", self.udp_port),
                                                                allow_broadcast=True)

        # Regularly broadcast announcements
        while True:
            print("Sending peer announcement...")
            transport.sendto(json.dumps(self.announcement).encode('utf-8'), ("255.255.255.255", self.udp_port))
            await asyncio.sleep(20)

    def on_recieve(self, data: bytes, addr: _Address):
        self.update_FIB(data, addr)
        print(self.fib)

    def update_FIB(self, data: bytes, addr: _Address):
        # Decode the bytes data to string and parse it as JSON
        decoded_data = data.decode('utf-8')

        try:
            # Parsing the JSON data
            parsed_data = json.loads(decoded_data)
            vehicle_identifier = parsed_data['vehicle_name']
            communication_network = parsed_data['network']
            server_host = addr.host
            server_port = parsed_data['port']
            time_to_live = 25
            network_info = {}
            network_info[vehicle_identifier] = [server_host, server_port, time_to_live]

            # Updating the Forwarding Information Base (FIB)
            if communication_network in self.fib:
                if vehicle_identifier in self.fib[communication_network]:
                    self.fib[communication_network][vehicle_identifier][2] = time_to_live
                else:
                    self.fib[communication_network].update({vehicle_identifier: network_info[vehicle_identifier]})
            else:
                self.fib[communication_network] = {vehicle_identifier: network_info[vehicle_identifier]}
        except json.JSONDecodeError as json_error:
            import traceback
            print(traceback.format_exc())
            print(f"JSON decoding error: {json_error}")
        except KeyError as key_error:
            import traceback
            print(traceback.format_exc())
            print(f"Key error: Missing 'vehicle_name' in the data - {decoded_data}")

    async def decrement_ttl(self):
        while True:
            try:
                # Iterate through Forwarding Information Base (FIB) entries
                for network in list(self.fib.keys()):
                    print(network)
                    for vehicle in list(self.fib[network].keys()):
                        print(vehicle)
                        # Decrement the TTL for each entry
                        self.fib[network][vehicle][2] -= 1
                        # Remove the entry if the TTL reaches zero
                        if self.fib[network][vehicle][2] <= 0:
                            del self.fib[network][vehicle]

                # Iterate through sensor entries
                for sensor_network in list(self.sensor.keys()):
                    print(sensor_network)
                    for sensor_device in list(self.sensor[sensor_network].keys()):
                        print(sensor_device)
                        # Decrement the TTL for each sensor entry
                        self.sensor[sensor_network][sensor_device][1] -= 1
                        # Remove the sensor entry if the TTL reaches zero
                        if self.sensor[sensor_network][sensor_device][1] <= 0:
                            del self.sensor[sensor_network][sensor_device]
            except Exception as e:
                # Optionally log the exception details

                print(f"Error occurred during TTL decrement: {e}")
            # Wait for 1 second before decrementing again
            await asyncio.sleep(1)

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        print(f"(handle_client) Received connection from {addr}")

        while True:
            data = await reader.read(100)
            if not data:
                break

            # Decrypting the received data
            decrypted_message = rsa.decrypt(data, rsa.PrivateKey.load_pkcs1(privateKey2))
            decrypted_message = decrypted_message.decode('utf-8')
            network, name, sensor_type = decrypted_message.split('/')
            print(f"(handle_client) Received {decrypted_message} from {addr}")

            # Processing the message based on network and name
            if name not in self.sensor:
                if network == self.network and network in self.fib:
                    host = socket.gethostbyname(socket.gethostname())
                    port = self.fib[network][name][1]
                    response = await self.transmit_encrypted_request(host, port, decrypted_message)
                elif network != self.network and network in self.fib:
                    host, port = self.fib[network][list(self.fib[network].keys())[0]][:2]
                    response = await self.transmit_encrypted_request(host, port, decrypted_message)
                else:
                    break
            else:
                response = self.sensor[name][sensor_type][0]

            # Encrypting and sending the response
            response = response.encode('utf-8')
            public_key = rsa.PublicKey.load_pkcs1(publicKey2)
            encrypted_response = rsa.encrypt(response, public_key)
            writer.write(encrypted_response)
            await writer.drain()

        print(f"Closing connection with {addr}")
        writer.close()
        await writer.wait_closed()
#Author for Tcp Request and response - Nachiketh and Pradyumn

    async def start_tcp_server(self):
        server = await asyncio.start_server(self.handle_client, self.hostname, self.tcp_port)
        addr = server.sockets[0].getsockname()
        print(f'Serving (start_tcp_server) on {addr}')

        async with server:
            await server.serve_forever()



    async def transmit_encrypted_request(self, host, port, message):
        print(f"Sending request to {host}:{port}...")
        loadPublicKey = rsa.PublicKey.load_pkcs1(publicKey2)
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(rsa.encrypt(message.encode('utf-8'), loadPublicKey))
        await writer.drain()

        response = await reader.read(100)  # Read the response
        decrypted_response = rsa.decrypt(response, rsa.PrivateKey.load_pkcs1(privateKey2)).decode('utf-8')
        print(f"Received response from {host}:{port} - value: {decrypted_response}")

        writer.close()
        await writer.wait_closed()

        return decrypted_response

#Author for sending request- Madhumati and Ramya

def requestLoop(device, loop):
    while True:
        command = input("Enter command (send, quit): ").strip().lower()
        if command == "send":
            request_data = input("Enter interest package (eg. network2/bus1/temperature): ").strip().lower()
            network, vehicle_name, sensortype = request_data.split('/')

            if network == device.network and network in device.fib:
                if vehicle_name in device.fib[network]:
                    host = device.hostname
                    port = device.fib[network][vehicle_name][1]
                    response = asyncio.run_coroutine_threadsafe(device.transmit_encrypted_request(host, port, request_data), loop).result(30)
                    evaluate_data(sensortype, response)
                else:
                    print("Vehicle name doesn't exist")
                    continue

            elif network != device.network and network in device.fib:
                try:
                    first_vehicle_info = list(device.fib[network].values())[0]
                    host, port = first_vehicle_info[:2]
                    host = f'rasp-0{host.split(".")[3]}.berry.scss.tcd.ie'
                    response = asyncio.run_coroutine_threadsafe(device.transmit_encrypted_request(host, port, request_data), loop).result(30)
                    evaluate_data(sensortype, response)
                except Exception as e:
                    print(f"Error occurred: {e}")
                    continue

            else:
                print("Network doesn't exist")
                continue

        elif command == "quit":
            break
        else:
            continue


class ListenerProtocol(asyncio.DatagramProtocol):
    def __init__(self, udp_obj) -> None:
        self.udp_obj = udp_obj
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport
        print(f"ListeningProtocol on {self.transport.get_extra_info('sockname')}")

    def datagram_received(self, data, addr):
        self.udp_obj.update_FIB(data, _Address(*addr[0:2]))


async def localUdp(udp, sendports):
    loop = asyncio.get_running_loop()

    # Create one listening transport
    listen_transport, _ = await loop.create_datagram_endpoint(
        lambda: ListenerProtocol(udp_obj=udp),
        local_addr=('127.0.0.1', udp.udp_local_port))

    # Create sender transport and protocol only once
    sender_transport, sender_protocol = await loop.create_datagram_endpoint(
        lambda: asyncio.DatagramProtocol(),
        local_addr=('127.0.0.1', 0))  # A random outgoing port is fine

    try:
        print("Sending peer announcements...")
        while True:
            announcement = {
                "heartbeat": "ALIVE",
                "NEIGHBOURS": udp.hostname,
                "vehicle_name": udp.vehicle_name,
                "network": udp.network,
                "port": udp.tcp_port
            }
            for port in sendports:
                sender_transport.sendto(json.dumps(announcement).encode('utf-8'), ('127.0.0.1', port))
            await asyncio.sleep(5)

    finally:
        # Close the transports
        listen_transport.close()
        sender_transport.close()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', help='Enter Port for Global UDP broadcast', type=int)
    parser.add_argument('--name', help='Enter Name for Device', type=str)
    parser.add_argument('--network', help='Enter Name for Network', type=str)

    args = parser.parse_args()
    if args.port is None:
        print("Please specify the port UDP Broadcast")
        exit(1)
    if args.name is None:
        print("Please specify the name of the device")
        exit(1)
    if args.network is None:
        print("Please specify the network it belongs to")
        exit(1)
    device = Device(args.network, args.name, args.port)
    sensors_agri = {'weather': ['temperature', 'humidity', 'pressure', 'speed', 'direction', 'uv', 'co2', 'rainfall'],
                    'soil': ['temperature', 'humidity', 'pressure', 'ph', 'nitrogen','nutrients', 'potassium', 'moisture' ],
                    'drone': ['temperature', 'humidity', 'pressure', 'speed', 'position', 'rgb', 'infrared', 'altitude'],
                    'water': ['temperature', 'humidity', 'pressure', 'ph', 'dissolvedo2', 'nutrients', 'acidic', 'nitrogen'],
                    'health': ['temperature', 'humidity', 'pressure', 'nutrients', 'moisture', 'co2', 'hydration', 'nitrogen']}
    devicetype = re.findall('[a-zA-Z]', args.name)
    devicetype = ''.join(devicetype)
    sensor_task=asyncio.create_task(generate_data(sensors_agri[devicetype],device))
    sendports = list(range(33022, 33040, 2))
    sendports.remove(args.port + 1)

    globalUDP_task = asyncio.create_task(device.start_GlobalUdp())
    localUDP_task = asyncio.create_task(localUdp(device, sendports))
    TCPserver_task = asyncio.create_task(device.start_tcp_server())
    ttl_task = asyncio.create_task(device.decrement_ttl())

    # Get the current event loop for the main thread
    loop = asyncio.get_running_loop()

    # Start the command loop in a separate thread, passing the event loop
    command_thread = threading.Thread(target=requestLoop, args=(device, loop), daemon=True)
    command_thread.start()

    try:
        await asyncio.gather(globalUDP_task, localUDP_task, TCPserver_task, ttl_task, sensor_task)
    except asyncio.CancelledError:
        # The server task has been cancelled, meaning we're shutting down
        pass

publicKey2  = b'-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCn9eH0j8o/x4VlN5qVp6KVVs94o/7RgkmTNHAj195bVee1xoGcYmycSn1Q\n1CO3wLoFdAbJg8yyJGXkZLdJzQ7hAgMBAAE=\n-----END RSA PUBLIC KEY-----\n'
privateKey2 = b'-----BEGIN RSA PRIVATE KEY-----\nMIIBPQIBAAJBAKf14fSPyj/HhWU3mpWnopVWz3ij/tGCSZM0cCPX3ltV57XGgZxi\nbJxKfVDUI7fAugV0BsmDzLIkZeRkt0nNDuECAwEAAQJBAI5mFbLtsbAPLZZZ5RKa\ndGoelnmWuHTR/CT0oVqSKmJUaPw+xQaqSmWVTsKvtZAnbp6H5H32bFkH1oA4/uAz\nJEECIwDyXKYb6T12ta+OyfE0B2MyL2iQzEzpXtEo7LJPs3LeRuzZAh8AsWlxIg0n\nFWyQ1tTzll1Du0xSZ0D0DqzGg6+cII1JAiImTCWje3PO8l7PfXGz+wbdw0gOuXnd\n1rHOebijh4O7RBHhAh5ESbvcSYfDvVg6+RkRxbBuhcAqMlw+0c5PnebQuNECIwDu\n90XbjH44bBPIO+rzpcqytDXufJ6/R7JRidC2O4S+TBrW\n-----END RSA PRIVATE KEY-----\n'

# Run the event loop
asyncio.run(main())

# network1/weather/temperature
# network2/car1/temperature