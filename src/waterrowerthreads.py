"""
Python script to broadcast WaterRower data over BLE with FTMS protocol
RowFlo (device-neutral fork of PiRowFlo)

To begin choose an interface from where the data will be taken from.
Currently supported:
- S4 Monitor via USB

SmartRow and ANT+ support removed in favor of FTMS protocol.

Example:
python3 waterrowerthreads.py -i s4 -b
"""

"""
import logging
import logging.config
import threading
import Example:
python3 waterrowerthreads.py -i s4 -b
"""
import logging
import logging.config
import threading
import argparse
from queue import Queue
from collections import deque
import pathlib
import signal

from adapters.ble import waterrowerble
from adapters.s4 import waterrowerble as s4_ble
from adapters import ftms_rower

loggerconfigpath = str(pathlib.Path(__file__).parent.absolute()) + "/logging.conf"
logger = logging.getLogger(__name__)

Mainlock = threading.Lock()
argparse
from queue import Queue
from collections import deque
import pathlib
import signal

from adapters.ble import waterrowerble
from adapters.s4 import waterrowerble as s4_ble
from adapters import ftms_rower

loggerconfigpath = str(pathlib.Path(__file__).parent.absolute()) + "/logging.conf"
logger = logging.getLogger(__name__)

Mainlock = threading.Lock()

class Graceful:
    def __init__(self):
        self.run = True
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        with Mainlock:
            self.run = False
            logger.info("Graceful shutdown requested")

def main(args):
    logging.config.fileConfig(loggerconfigpath, disable_existing_loggers=False)
    grace = Graceful()

    def BleService(out_q, ble_in_q):
        logger.info("Starting BLE advertise and GATT server")
        ftms_rower.main(out_q, ble_in_q)

    def Waterrower(in_q, ble_out_q):
        logger.info("Starting S4 WaterRower interface")
        service = s4_ble.main(in_q, ble_out_q)
        service()

    q = Queue()
    ble_q = deque(maxlen=1)
    threads = []


    # Interface selection
    if args.interface == "s4":
        logger.info("Interface selected: S4 monitor")
        t = threading.Thread(target=Waterrower, args=(q, ble_q), daemon=True)
        t.start()
        threads.append(t)
    # SmartRow support removed

    # Bluetooth service
    if args.blue:
        logger.info("Starting BLE service")
        t = threading.Thread(target=BleService, args=(q, ble_q), daemon=True)
        t.start()
        threads.append(t)
    else:
        logger.info("BLE service not enabled")

def main(args):
    logging.config.fileConfig(loggerconfigpath, disable_existing_loggers=False)
    grace = Graceful()

    def BleService(out_q, ble_in_q):
        logger.info("Starting BLE advertise and GATT server (FTMS protocol)")
        service = ftms_rower.main(out_q, ble_in_q)

    def Waterrower(in_q, ble_out_q):
        logger.info("Starting S4 WaterRower interface")
        service = s4_ble.main(in_q, ble_out_q)
        service()

    q = Queue()
    ble_q = deque(maxlen=1)
    threads = []

    # Interface selection
    if args.interface == "s4":
        logger.info("Interface selected: S4 monitor")
        t = threading.Thread(target=Waterrower, args=(q, ble_q), daemon=True)
        t.start()
        threads.append(t)
    elif args.interface == "sr":
        logger.error("SmartRow support is disabled in RowFlo")
        return
    else:
        logger.error("No valid interface selected")
        return

    # BLE service
    if args.blue:
        t = threading.Thread(target=BleService, args=(q, ble_q), daemon=True)
        t.start()
        threads.append(t)
    else:
        logger.info("BLE service not enabled")

    # Main loop
    while grace.run:
        for thread in threads:
            thread.join(timeout=10)
            if not thread.is_alive():
                logger.error("A worker thread exited unexpectedly")
                return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--interface",
        choices=["s4"],
        default="s4",
        help="Choose interface: s4 (USB S4 monitor)",
    )
    parser.add_argument(
        "-b",
        "--blue",
        action="store_true",
        help="Broadcast WaterRower data over Bluetooth Low Energy (FTMS protocol)",
    )

    args = parser.parse_args()
    logger.info(args)
    try:
        main(args)
    except KeyboardInterrupt:
        print("RowFlo shut down by user")
