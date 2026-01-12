from scapy.all import IP, ICMP, sr1
import asyncio
import argparse
import time

def blocking_ping(target_ip, payload_size, timeout):
    """Send one ICMP ping using Scapy (blocking).

    This function performs the actual packet send/receive using Scapy's
    sr1(), which is a blocking call. It is intentionally kept synchronous
    and must NOT be executed directly inside an asyncio event loop."""
    packet = IP(dst=target_ip) / ICMP() / ("X" * payload_size)
    start = time.time()
    reply = sr1(packet, timeout=timeout, verbose=False)
    end = time.time()

    if reply:
        rtt = (end - start) * 1000
        return f"Reply from {reply.src}: bytes={len(reply)} time={rtt:.2f}ms"
    else:
        return f"Request timed out for {target_ip}"

async def send_ping(target_ip, payload_size, timeout):
    """Run a blocking ping in a background thread."""
    return await asyncio.to_thread(
        blocking_ping,
        target_ip,
        payload_size,
        timeout
    )

async def icmp_pinger(target_ip, payload_size, count, interval, timeout, sequential=False):
    """Send multiple ICMP pings asynchronously or sequentially."""
    if sequential:
        # Classic ping behavior: one at a time
        for _ in range(count):
            print(await send_ping(target_ip, payload_size, timeout))
            await asyncio.sleep(interval)
    else:
        # Concurrent mode
        tasks = []
        for _ in range(count):
            tasks.append(asyncio.create_task(send_ping(target_ip, payload_size, timeout)))
            await asyncio.sleep(interval)
        for task in asyncio.as_completed(tasks):
            print(await task)

if __name__ == "__main__":
    """CLI entry point"""
    parser = argparse.ArgumentParser(description="Async ICMP Pinger")
    parser.add_argument("target_ip", type=str, help="Target IP Address")
    parser.add_argument("--payload_size", type=int, default=32, help="Size of ICMP load")
    parser.add_argument("--count", type=int, default=4, help="Number of pings")
    parser.add_argument("--interval", type=float, default=1, help="Interval between pings in seconds")
    parser.add_argument("--timeout", type=float, default=1, help="Timeout for each ping in seconds")
    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Run pings one after another instead of concurrently"
    )
    args = parser.parse_args()

    asyncio.run(icmp_pinger(args.target_ip, args.payload_size, args.count, args.interval, args.timeout, sequential=args.sequential))
