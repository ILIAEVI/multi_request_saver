import os
import time
import aiohttp
import asyncio
import json


base_url = "https://jsonplaceholder.typicode.com/posts/"

output_file = "async_responses.json"


async def fetch(session, post_id):
    try:
        url = f"{base_url}{post_id}"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch post {post_id}: Status code {response.status_code}")
    except Exception as e:
        print(f"Failed to fetch post {post_id}: {e}")


async def main():

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 78):
            tasks.append(fetch(session, i))

        responses = await asyncio.gather(*tasks)

        with open(output_file, "w") as f:
            json.dump(responses, f, indent=4)

if __name__ == "__main__":
    if os.path.exists(output_file):
        os.remove(output_file)
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
