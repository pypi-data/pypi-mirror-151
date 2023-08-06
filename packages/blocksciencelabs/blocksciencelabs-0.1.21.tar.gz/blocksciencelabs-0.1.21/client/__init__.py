import common
import csv, functools, json, operator, os, pickle, requests, subprocess, sys

LABS_API = "https://api.blocksciencelabs.com"
WHEEL_BASE_URL = "https://models-private.s3.us-east-2.amazonaws.com"
WHEEL_NAME = "pkg-0.0.0-py3-none-any.whl"

Config = dict[str, str]

maxInt = sys.maxsize

while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10) # Reduce by factor of 10 until overflow ends
    
class Client:
    def __init__(self, config: Config = {}):
        email = ""
        password = ""
        
        # Check both env variables and config for auth information
        if "LABS_EMAIL" in os.environ:
            email = os.environ["LABS_EMAIL"]
            
        if "LABS_PASS" in os.environ:
            password = os.environ["LABS_PASS"]
        
        if "LABS_EMAIL" in config:
            email = config["LABS_EMAIL"]
        
        if "LABS_PASS" in config:
            password = config["LABS_PASS"]
        
        if (email == "" or password == "") and "LABS_TOKEN" not in os.environ:
            raise Exception(common.ERROR_MISSING_PARAMETERS)
        elif email != "" and password != "":
            response = requests.post(f'{LABS_API}/login', {"email": email, "password": password})
            if response.status_code == 400:
                raise Exception(response.text)
            elif response.status_code == 401:
                raise Exception(json.loads(response.text)["message"])
            else:
                self.token = json.loads(response.text)["payload"]["token"]
        else:
            self.token = os.environ["LABS_TOKEN"]
                
    def authenticated_request(self, method: str = "GET", endpoint: str = "ping", data: any = None):
        response = None;
        url = f'{LABS_API}/{endpoint}'
        headers = {"Authorization": f'Bearer {self.token}'}
        
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = request.post(url, headers=headers, data=data)
        else:
            response = request.get(url, headers=headers)
            
        return response

    def fetch_results(self, simulation_id):
        response = self.authenticated_request("GET", f'fetch-results?simulationId={simulation_id}')

        unserialized = []
        
        if response.status_code == 200:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--ignore-installed", "--no-warn-script-location", get_wheel_url(simulation_id)])
            for record in json.loads(response.text)["payload"]:
                unserialized.append(pickle.loads(bytes.fromhex(record["data"])))

            return functools.reduce(operator.iconcat, unserialized, [])    
        else:
            return []
        
    def import_results(self, file_name, simulation_id):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--ignore-installed", "--no-warn-script-location", get_wheel_url(simulation_id)])
        
        unserialized = []
        
        with open(file_name, 'r') as fd:
            csv_reader = csv.reader(fd)
            header = next(csv_reader)
            if header != None:
                for row in csv_reader:
                    unserialized.append(pickle.loads(bytes.fromhex(row[5])))
                
        return functools.reduce(operator.iconcat, unserialized, [])
    
def get_wheel_url(simulation_id):
        return f'{WHEEL_BASE_URL}/{simulation_id}/{WHEEL_NAME}'