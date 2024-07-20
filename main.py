import asyncio
import datetime
import telnetlib

from gpiozero import Button

from settings import IP_ADDRESS, PORT, TIMEOUT_SECONDS, PIN_FOR_CHANGE_TO_CAMERA, PIN_FOR_CHANGE_TO_HDMI, ROUTING


tn = telnetlib.Telnet(IP_ADDRESS, PORT, TIMEOUT_SECONDS)

signal_to_switch_to_camera = Button(PIN_FOR_CHANGE_TO_CAMERA, pull_up=False)
signal_to_switch_to_hdmi = Button(PIN_FOR_CHANGE_TO_HDMI, pull_up=False)

is_camera_out = True

camera_output = ROUTING["camera"]
hdmi_output = ROUTING["hdmi"]

async def switch_channel(output_channel: int, input_channels: int):
        tn.write((f"video output routing:\n{output_channel} {input_channels}\n\n").encode('ascii'))
        tn.read_until(b"ACK", TIMEOUT_SECONDS)
        print(f"{datetime.datetime.now()} __ Switched channels, output:{output_channel}, input:{input_channels}")

async def main():
    print(f"\n{datetime.datetime.now()} __ Start auto switching.\n")
    while True:
        if signal_to_switch_to_camera.is_pressed and is_camera_out:
            await asyncio.run(
                switch_channel(camera_output["OUTPUT_CHANNELS"], camera_output["INPUT_CHANNELS"]),
            )
        elif signal_to_switch_to_hdmi.is_pressed and not is_camera_out:
             await asyncio.run(
                switch_channel(hdmi_output["OUTPUT_CHANNELS"], hdmi_output["INPUT_CHANNELS"]),
            )
    print(f"\n{datetime.datetime.now()} __ Finished auto switching.")

if __name__ == "__main__":
    asyncio.run(main())
