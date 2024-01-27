import requests
import subprocess
import re

def get_kernel_version():
    """Function to get a simplified current Linux kernel version."""
    try:
        full_version = subprocess.check_output(['uname', '-r']).strip().decode()
        # Extracting major and minor version (e.g., '5.15' from '5.15.90.1-microsoft-standard-WSL2')
        match = re.search(r'(\d+\.\d+)', full_version)
        if match:
            return match.group(1)
        else:
            print("Unable to extract a simplified kernel version.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while getting kernel version: {e}")
        return None

def query_nvd_api(kernel_version):
    """Query the NVD API for vulnerabilities related to the given kernel version."""
    api_endpoint = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    params = {
        'keyword': f"Linux {kernel_version}",
        'resultsPerPage': '10'
    }

    try:
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            print(f"Invalid JSON response: {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Error occurred while accessing the NVD API: {e}")
        return None

def main():
    kernel_version = get_kernel_version()
    if kernel_version:
        print(f"Checking vulnerabilities for Kernel Version: {kernel_version}")
        vulnerabilities = query_nvd_api(kernel_version)
        if vulnerabilities:
            for item in vulnerabilities.get('result', {}).get('CVE_Items', []):
                cve_id = item.get('cve', {}).get('CVE_data_meta', {}).get('ID', 'N/A')
                description = item.get('cve', {}).get('description', {}).get('description_data', [{}])[0].get('value', 'No description available')
                print(f"CVE ID: {cve_id}, Description: {description}")
    else:
        print("Unable to determine the kernel version.")

if __name__ == "__main__":
    main()