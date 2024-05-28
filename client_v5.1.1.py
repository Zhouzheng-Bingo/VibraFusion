import asyncio
import nidaqmx
import websockets

async def getdatalist(num):
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(f"Dev1/ai0:4")
        task.timing.cfg_samp_clk_timing(
            rate=800,
            sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
            samps_per_chan=40000
        )

        datalist = task.read(number_of_samples_per_channel=num)
        return datalist

# 读五条 ai0, ai1, ai2, ai3, ai4 的值
async def send_msg(websocket):
    i = 0
    while True:
        try:
            datalist = await getdatalist(800)
            print(f"-------start!! {i} !!send data to server!----")
            for i in range(100):
                await websocket.send(
                    f"{datalist[0][i]}|{datalist[1][i]}|{datalist[2][i]}|{datalist[3][i]}|{datalist[4][i]}"
                )
                rec_str = await websocket.recv()
                print(f"***** 通道的数据已发送 : {rec_str}")

            print("-------send finished!----\n\n")
            i += 1
            await asyncio.sleep(2)
        except websockets.ConnectionClosedError:
            print("服务器已关闭")
            return True

async def main_logic():
    async with websockets.connect('ws://localhost:8765') as websocket:
        await send_msg(websocket)

asyncio.get_event_loop().run_until_complete(main_logic())
