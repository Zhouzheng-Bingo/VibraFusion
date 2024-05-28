import asyncio
import websockets
import csv

async def startServer(websocket, path):
    print('-------- server start ------')
    i = 0

    with open('data.csv', 'a', newline='') as csvfile:
        fieldnames = ['vol_ch1', 'vol_ch2', 'vol_ch3']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write header only once

        while True:
            try:
                rec_data = await websocket.recv()
                split_data = rec_data.split("|")
                i += 1

                vol_ch1 = float(split_data[0])
                vol_ch2 = float(split_data[1])
                vol_ch3 = float(split_data[2])

                writer.writerow({'vol_ch1': vol_ch1, 'vol_ch2': vol_ch2, 'vol_ch3': vol_ch3})

                greeting = f'server get ch1: {vol_ch1}, ch2: {vol_ch2}, ch3: {vol_ch3}'
                print(greeting)
                await websocket.send(greeting)
            except websockets.ConnectionClosedError:
                print("客户已断开")
                print(f"已经保存{i}条数据")
                return True

start_server = websockets.serve(startServer, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(asyncio.shield(start_server))
asyncio.get_event_loop().run_forever()
