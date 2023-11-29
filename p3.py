import requests

def connect_to_api(url):
    response = requests.get(url)
    return response.json()

def main():
    url = "https://api.github.com/users/defunkt"
    data = connect_to_api(url)
    print(data)

if __name__ == "__main__":
    main()