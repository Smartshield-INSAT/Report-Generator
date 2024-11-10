import asyncio
import httpx
import time
import matplotlib.pyplot as plt

URL = "http://localhost:8002/generator/generate-report"  

async def make_request(client, data):
    """Makes an asynchronous HTTP POST request to a predefined URL.
    
    Args:
        client: An asynchronous HTTP client object capable of making POST requests.
        data (dict): The JSON data to be sent in the request body.
    
    Returns:
        float or None: The time taken for the request in seconds if successful, or None if the request fails.
    
    Raises:
        Exception: If the request fails for any reason. The error is printed to console.
    """
    try:
        response = await client.post(URL, json=data)
        response.raise_for_status()
        return response.elapsed.total_seconds()  
    except Exception as e:
        print(f"Request failed: {e}")
        return None

async def stress_test_wave(wave_num, num_clients, request_data):
    """Perform a stress test for a specific wave of client requests.
    
    Args:
        wave_num (int): The wave number for this stress test.
        num_clients (int): The number of simultaneous client requests to simulate.
        request_data (dict): The data to be sent in each client request.
    
    Returns:
        List[float]: A list of response times for successful requests.
    
    """
    async with httpx.AsyncClient() as client:
        tasks = [make_request(client, request_data) for _ in range(num_clients)]
        results = await asyncio.gather(*tasks)
        response_times = [r for r in results if r is not None]
        print(f"Wave {wave_num} - Success rate: {len(response_times)}/{num_clients}")
        return response_times

async def run_stress_test():
    """Executes a stress test with multiple waves of concurrent clients.
    
    Args:
        None
    
    Returns:
        list: A list of response times from all waves of the stress test.
    
    Raises:
        None
    
    Description:
        This asynchronous function performs a stress test by simulating multiple waves of concurrent clients
        sending requests. It uses a predefined request payload and runs a specified number of waves with
        a set number of clients per wave. The function collects response times from each wave and returns
        the combined results.
    
        The stress test parameters are:
        - Number of clients per wave: 10
        - Number of waves: 4
        - Request payload: A dictionary containing 'threat' and 'threat_data'
    
        Between each wave, there is a short pause of 1 second to allow for system cooldown.
    
    Note:
        This function depends on an external 'stress_test_wave' coroutine, which is not shown in the
        provided code snippet. Ensure that this dependency is properly implemented and available.
    """
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
