import requests

# ESP32 Camera IP and endpoint
esp32_ip = "192.168.141.88"
image_url = f"http://{esp32_ip}/image"

# Path to save the downloaded image
save_path = r'N:\Shop\scb_data_collection\fj_destructive_test_results\test_images\captured_image.jpg'

try:
    # Send a GET request to the ESP32 to get the image
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the image data to the specified file path
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {save_path}")
    else:
        print(f"Failed to retrieve image, status code: {response.status_code}")
        print(f"Response Content: {response.content.decode('utf-8')}")

except requests.exceptions.RequestException as e:
    print(f"Request Exception: {e}")
