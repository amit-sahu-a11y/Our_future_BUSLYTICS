import requests

def fetch_camera_image(camera_url: str) -> bytes:
    """
    camera_url example:
    http://192.168.1.5:8080/shot.jpg
    """
    response = requests.get(camera_url, timeout=5)

    if response.status_code != 200:
        raise Exception("Failed to fetch camera image")

    return response.content
