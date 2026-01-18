import requests

def test_timestamps():
    url = "http://localhost:5555/messages"
    
    # Create message
    print("Creating message...")
    response = requests.post(url, json={"body": "Test timestamp", "username": "Tester"})
    if response.status_code != 201:
        print(f"Failed to create message: {response.text}")
        return
    
    data = response.json()
    print(f"Created message: {data}")
    
    if 'created_at' not in data or data['created_at'] is None:
        print("FAIL: created_at is missing or None")
    else:
        print("PASS: created_at is present")

    if 'updated_at' not in data or data['updated_at'] is None:
        print("FAIL: updated_at is missing or None")
    else:
        print("PASS: updated_at is present")

    # Clean up
    msg_id = data.get('id')
    if msg_id:
        requests.delete(f"{url}/{msg_id}")
        print("Cleaned up test message.")

if __name__ == "__main__":
    test_timestamps()
