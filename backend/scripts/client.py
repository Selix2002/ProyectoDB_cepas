import httpx

BASE_URL = "http://localhost:8000"
USERNAME = "sebas"
PASSWORD = "sebas"


def main():
    token = get_token()

    with httpx.Client(
        base_url="http://localhost:8000",
        headers={"Authorization": f"Bearer {token}"},
    ) as client:
        r = client.get("/cepas/get-all")
        for item in r.json():
            print(f"id={item['id']},title={item['title']}")


def get_token() -> str:
    with httpx.Client(base_url=BASE_URL) as client:
        r = client.post("/auth/login", data={"username": USERNAME, "password": PASSWORD})
        r_data = r.json()

    return r_data["access_token"]


if __name__ == "__main__":
    main()
