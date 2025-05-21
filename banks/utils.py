import requests

def send_bulk_bill_to_api(file_path):
    url = "http://196.189.53.130:28080/enterpriseApi/BillIntegrationResource/bulkBillUpload"
    api_key = "7264CBE3CED649E6BAA0D47669932E2B.ED1E0A2606AB4DA1B5E93AE779BFAD9C"

    params = {'API_KEY': api_key}
    headers = {'API_KEY': api_key}

    with open(file_path, 'rb') as f:
        files = {'uploadedFile': (f.name, f, 'text/csv')}
        response = requests.post(url, headers=headers, params=params, files=files)

    return response.status_code, response.text.strip()
