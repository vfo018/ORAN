import requests

def send_scenario_request(scenario):
    url = "http://localhost:8000/scenario"
    data = {'scenario': scenario}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"Scenario {scenario} successfully sent to E2node.")
    else:
        print(f"Failed to send scenario {scenario}. Status code: {response.status_code}")

def main():
    while True:
        print("Choose a scenario:")
        print("1: CU Addition")
        print("2: CU Removal")
        print("3: DU Addition")
        print("4: DU Removal")

        scenario = input("Enter the number of the scenario you want to run: ")
        if scenario in ['1', '2', '3', '4']:
            send_scenario_request(scenario)
        else:
            print("Invalid scenario number")

if __name__ == "__main__":
    main()
