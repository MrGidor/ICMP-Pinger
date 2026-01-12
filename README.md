# ICMP-Pinger

A lightweight asynchronous ICMP ping tool built with Python and Scapy.
Supports sequential and concurrent pinging, configurable payload size, interval, timeout, and ping count.

## Features

- Send ICMP echo requests to a target host
- Sequential or concurrent ping modes (--sequential)
- Adjustable payload size, interval, timeout, and number of pings
- Cross-platform compatible with Linux (requires root)

## Usage
Install the required python libraries: ```pip install -r requirements.txt```

⚠ Note: Raw ICMP packets require root privileges on Linux. Use sudo when running the tool.

```sudo python3 main.py <target_ip> [options]```

## Options

| Option         | Default | Description                                                   |
|----------------|---------|---------------------------------------------------------------|
| --payload_size  | 32      | Size of the ICMP payload in bytes                             |
| --count         | 4       | Number of pings to send                                       |
| --interval      | 1       | Interval between pings in seconds                              |
| --timeout       | 1       | Timeout for each ping in seconds                                |
| --sequential    | False   | Run pings one after another instead of concurrently           |

## Examples:
Concurrent pings (default): `sudo python3 main.py 8.8.8.8 --count 5 --interval 0.2`

Sequential pings: `sudo python3 main.py 8.8.8.8 --count 5 --interval 1 --sequential`
