import re
import json

from bs4 import BeautifulSoup
from requests import get
import requests
from userbot.modules import register
from userbot.modules.helper_funcs.args import get_args
from userbot.modules.helper_funcs.downloads import download_file
import yaml
from userbot import LOGGER
import os

GITHUB = 'https://github.com'

class DeviceObject():
    vendor = ""
    model = ""
    cpu = ""
    cores = 0
    cpu_freq = ""
    lineage = ""
    android = ""
    gpu = ""
    height = ""
    width = ""
    kernel = ""
    network = ""
    peripherals = ""
    ram = ""
    recovery_boot = ""
    download_boot = ""
    soc = ""
    storage = ""
    device_type = ""
    wifi = ""

@register(outgoing=True, pattern="^.magisk$")
async def magisk(request):
    """ magisk latest releases """
    await request.edit("`Downloading latest Magisk release...`")
    url = 'https://raw.githubusercontent.com/topjohnwu/magisk-files/master/stable.json'
    data = get(url).json()
    version = data["magisk"]["version"]
    link = data["magisk"]["link"]
    filename = await download_file(link)
    await request.client.send_file(request.chat_id, filename)
    await request.edit("Here is Magisk `{}`!".format(version))
    os.remove(filename) 

@register(outgoing=True, pattern=r"^.device(?: |$)(\S*)")
async def device_info(update):
    args = get_args(update)
    if len(args) < 1:
        await update.edit("`Usage: .device <codename>`")
        return
    codename = args[0]
    filename = await download_file("https://raw.githubusercontent.com/LineageOS/lineage_wiki/master/_data/devices/{}.yml".format(codename))
    device = DeviceObject()
    with open(filename, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
            if "vendor" in data:
                device.vendor = data["vendor"]
            if "name" in data:
                device.model = data["name"]
            if "soc" in data:
                device.soc = data["soc"]
            if "cpu" in data:
                device.cpu = data["cpu"]
            if "cpu_cores" in data:
                device.cores = int(data["cpu_cores"])
            if "cpu_freq" in data:
                device.cpu_freq = data["cpu_freq"]
            if "current_branch" in data:
                device.lineage = data["current_branch"]
            # TODO
            device.android = "This is not yet done!"
            if "gpu" in data:
                device.gpu = data["gpu"]
            if "height" in data:
                device.height = data["height"]
            else:
                device.height = "Unknown"
            if "width" in data:
                device.width = data["width"]
            else:
                device.height = "Unknown"
            if "kernel" in data:
                device.kernel = data["kernel"]
            if "network" in data:
                device.network = str(data["network"]).replace("[", "").replace("]", "").replace("'", "")
            if "peripherals" in data:
                device.peripherals = str(data["peripherals"]).replace("[", "").replace("]", "").replace("'", "")
            if "ram" in data:
                device.ram = data["ram"]
            if "recovery_boot" in data:
                device.recovery_boot = data["recovery_boot"].replace("<kbd>", "").replace("</kbd>", "")
            if "download_boot" in data:
                device.download_boot = data["download_boot"].replace("<kbd>", "").replace("</kbd>", "")
            if "storage" in data:
                device.storage = data["storage"]
            if "type" in data:
                device.device_type = data["type"]
            if "wifi" in data:
                device.wifi = data["wifi"]
        except:
            pass
    os.remove(filename)
    text = f"Device information for {device.vendor} {device.model}:\n\n" \
            f"**Vendor**: `{device.vendor}`\n" \
            f"**Model**: `{device.model}`\n" \
            f"**SOC**: `{device.soc}`\n" \
            f"**CPU**: `{device.cpu}`\n" \
            f"**CPU Cores**: `{device.cores}`\n" \
            f"**CPU Frequency**: `{device.cpu_freq}`\n" \
            f"**LineageOS**: `{device.lineage}`\n" \
            f"**Android**: `{device.android}`\n" \
            f"**GPU**: `{device.gpu}`\n" \
            f"**Height**: `{device.height}`\n" \
            f"**Width**: `{device.width}`\n" \
            f"**Kernel**: `{device.kernel}`\n" \
            f"**Network**: `{device.network}`\n" \
            f"**Peripherals**: `{device.peripherals}`\n" \
            f"**RAM**: `{device.ram}`\n" \
            f"**Recovery**: `{device.recovery_boot}`\n" \
            f"**Fastboot**: `{device.download_boot}`\n" \
            f"**Storage**: `{device.storage}`\n" \
            f"**Device Type**: `{device.device_type}`\n" \
            f"**WIFI**: `{device.wifi}`\n"
    await update.edit(text)

__help__ = " - `.magisk`: Get the latest Magisk releases.\n" \
        " - `.device <codename>`: Get info about an Android device.\n"

__mod_name__ = "Android"
