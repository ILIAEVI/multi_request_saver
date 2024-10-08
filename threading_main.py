import os
import requests
import threading
import json
import time


base_url = "https://jsonplaceholder.typicode.com/posts"

lock = threading.Lock()


def fetch_and_save_post(post_id, filename="responses.json"):
    url = f"{base_url}/{post_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with lock:
                with open(filename, "r+") as f:
                    existing_data = json.load(f)
                    existing_data.append(data)
                    f.seek(0)
                    json.dump(existing_data, f, indent=4)
        else:
            print(f"Failed to fetch post {post_id}: Status code {response.status_code}")
    except Exception as e:
        print(f"Failed to fetch post {post_id}: {e}")

def main():
    num_posts = 77
    threads = []
    filename = "threading_responses.json"

    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, "w") as f:
        json.dump([], f)

    for post_id in range(1, num_posts + 1):
        thread = threading.Thread(target=fetch_and_save_post, args=(post_id, filename))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Responses saved to {filename}")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
