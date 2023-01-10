import httpx


def extract_data(link: str):
    return httpx.get(link).text
