#!/usr/bin/env python3
"""
IoT Egg Incubator - Raspberry Pi Serial Telemetry Gateway
Author: Kevin Andrey Herrera Silva <kahs_kevin@hotmail.com>

Bridges the Arduino Mega 2560 embedded controller to the web monitoring dashboard
via serial communication (USB ACM/UART) and HTTP POST telemetry transmission.
"""

import sys
import time
import argparse
import logging
import random
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("IncubatorGateway")

DEFAULT_URL = "http://localhost:8096/Service.php"
DEFAULT_PORT = "/dev/ttyACM0"
DEFAULT_BAUD = 9600


class IncubatorGateway:
    def __init__(self, target_url=DEFAULT_URL, serial_port=DEFAULT_PORT, baud_rate=DEFAULT_BAUD, mock=False):
        self.target_url = target_url
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.mock = mock
        self.serial_conn = None

    def connect_serial(self):
        """Attempts connection to the Arduino serial port."""
        if self.mock:
            logger.info("Running in MOCK mode. Physical serial connection bypassed.")
            return True

        try:
            import serial
            self.serial_conn = serial.Serial(self.serial_port, self.baud_rate, timeout=3)
            time.sleep(2)  # Wait for Arduino reset on serial connection
            logger.info(f"Connected to Arduino Mega on {self.serial_port} @ {self.baud_rate} baud")
            return True
        except ImportError:
            logger.warning("pyserial module not installed. Falling back to MOCK telemetry generation.")
            self.mock = True
            return True
        except Exception as e:
            logger.error(f"Failed to connect to {self.serial_port}: {e}")
            return False

    def generate_mock_telemetry(self):
        """Generates realistic avian embryonic incubation telemetry."""
        # Chicken embryo setpoint: ~37.55 C, 60% RH, ~58.5g egg weight, ~22cm water reservoir
        t1 = round(37.50 + random.uniform(-0.15, 0.15), 2)
        t2 = round(37.55 + random.uniform(-0.15, 0.15), 2)
        tp = round((t1 + t2) / 2.0, 2)

        h1 = round(60.0 + random.uniform(-0.5, 0.5), 2)
        h2 = round(59.8 + random.uniform(-0.5, 0.5), 2)
        hp = round((h1 + h2) / 2.0, 2)

        water_level = round(22.0 + random.uniform(-0.2, 0.2), 2)
        p1 = round(58.40 + random.uniform(-0.1, 0.1), 2)
        p2 = round(59.00 + random.uniform(-0.1, 0.1), 2)
        pp = round((p1 + p2) / 2.0, 2)

        return f"{t1},{t2},{tp},{h1},{h2},{hp},{water_level},{p1},{p2},{pp}"

    def send_telemetry(self, raw_data):
        """Dispatches telemetry data payload to the web monitoring endpoint."""
        cleaned_data = raw_data.strip()
        logger.info(f"Dispatching telemetry: {cleaned_data}")

        post_fields = {"Dato": cleaned_data}
        encoded_data = urlencode(post_fields).encode("utf-8")
        req = Request(self.target_url, data=encoded_data, headers={"User-Agent": "IncubatorGateway/2.0"})

        try:
            with urlopen(req, timeout=5) as response:
                result = response.read().decode("utf-8")
                logger.info(f"Web service response: {result}")
                return True
        except HTTPError as e:
            logger.error(f"HTTP error {e.code}: {e.reason}")
            return False
        except URLError as e:
            logger.error(f"Network / connection error: {e.reason}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending telemetry: {e}")
            return False

    def run(self, interval=10):
        """Main continuous operational loop."""
        logger.info(f"Starting Incubator Gateway. Target URL: {self.target_url}")
        self.connect_serial()

        while True:
            try:
                if self.mock:
                    telemetry = self.generate_mock_telemetry()
                    self.send_telemetry(telemetry)
                    time.sleep(interval)
                else:
                    if self.serial_conn and self.serial_conn.is_open:
                        line = self.serial_conn.readline().decode("utf-8", errors="ignore").strip()
                        if line and "," in line:
                            self.send_telemetry(line)
                    else:
                        logger.warning("Serial connection lost. Reconnecting...")
                        time.sleep(5)
                        self.connect_serial()
            except KeyboardInterrupt:
                logger.info("Gateway stopped by user. Shutting down gracefully.")
                break
            except Exception as e:
                logger.error(f"Loop exception: {e}")
                time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="IoT Egg Incubator Serial Telemetry Gateway")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"Target web service URL (default: {DEFAULT_URL})")
    parser.add_argument("--port", default=DEFAULT_PORT, help=f"Serial port device (default: {DEFAULT_PORT})")
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD, help=f"Baud rate (default: {DEFAULT_BAUD})")
    parser.add_argument("--interval", type=int, default=10, help="Transmission interval in seconds (default: 10)")
    parser.add_argument("--mock", action="store_true", help="Run with simulated telemetry without physical hardware")
    args = parser.parse_args()

    gateway = IncubatorGateway(
        target_url=args.url,
        serial_port=args.port,
        baud_rate=args.baud,
        mock=args.mock
    )
    gateway.run(interval=args.interval)


if __name__ == "__main__":
    main()
