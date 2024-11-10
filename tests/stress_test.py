import asyncio
import httpx
import time
import matplotlib.pyplot as plt

URL = "http://localhost:8002/generator/generate-report"  

async def make_request(client, data):
    try:
        response = await client.post(URL, json=data)
        response.raise_for_status()
        return response.elapsed.total_seconds()  
    except Exception as e:
        print(f"Request failed: {e}")
        return None

async def stress_test_wave(wave_num, num_clients, request_data):
    async with httpx.AsyncClient() as client:
        tasks = [make_request(client, request_data) for _ in range(num_clients)]
        results = await asyncio.gather(*tasks)
        response_times = [r for r in results if r is not None]
        print(f"Wave {wave_num} - Success rate: {len(response_times)}/{num_clients}")
        return response_times

async def run_stress_test():
    request_data = {
        "threat": "Sample Threat",
        "threat_data": {"example_key": "example_value"}
    }
    num_clients = 10
    waves = 4
    all_response_times = []

    for wave_num in range(1, waves + 1):
        print(f"Starting wave {wave_num} with {num_clients} clients...")
        start_time = time.perf_counter()
        response_times = await stress_test_wave(wave_num, num_clients, request_data)
        end_time = time.perf_counter()
        wave_duration = end_time - start_time
        print(f"Wave {wave_num} completed in {wave_duration:.2f} seconds")
        all_response_times.extend(response_times)
        await asyncio.sleep(1)  # Short pause between waves

    return all_response_times

# Run the stress test
response_times = asyncio.run(run_stress_test())

# Plot the performance metrics
if response_times:
    plt.hist(response_times, bins=10, color='skyblue', edgecolor='black')
    plt.title("Distribution of Response Times")
    plt.xlabel("Response Time (seconds)")
    plt.ylabel("Frequency")
    plt.show()
