import requests, ast
from bs4 import BeautifulSoup

# Base URLs
TACTICS_URL = "https://attack.mitre.org/tactics/enterprise/"
TECHNIQUES_URL_TEMPLATE = "https://attack.mitre.org/tactics/{}/"

# Function to get all tactics and their codes
def fetch_tactics():
    response = requests.get(TACTICS_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    tactics = {}
    table = soup.find("table", class_="table")
    rows = table.find_all("tr")

    for row in rows[1:]:  # Skip the header row
        cells = row.find_all("td")
        if len(cells) > 0:
            tactic_code = cells[0].get_text(strip=True)
            tactic_name = cells[1].get_text(strip=True)
            tactics[tactic_code] = {
                "name": tactic_name,
                "techniques": []
            }
    return tactics

# Function to get techniques and sub-techniques for a given tactic
def fetch_techniques_for_tactic(tactic_code):
    url = TECHNIQUES_URL_TEMPLATE.format(tactic_code)
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Not able to fetch techniques for tactic: \"{tactic_code}\" with error: {response.text} ")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    techniques = []

    table = soup.find("table", class_="table-techniques")
    if table:
        rows = table.find_all("tr")
        for row in rows[1:]:  # Skip the header row
            cells = row.find_all("td")
            if cells:
                technique_name = cells[0].get_text(strip=True)
                sub_techniques = cells[1].get_text(strip=True) if len(cells) > 1 else ""
                techniques.append({
                    "technique": technique_name,
                    "sub_techniques": [st.strip() for st in sub_techniques.split("\n") if st.strip()]
                })

    return techniques

def final_data(data):
    result = {}
    for tactic, details in data.items():
        techniques = details['techniques']
        filtered_data = []
        current_technique = None
        sub_techniques = []

        for entry in techniques:
            technique = entry['technique']
            sub_technique = entry['sub_techniques']

            # If a new technique starts, save the previous one
            if technique:
                if current_technique:
                    filtered_data.append({current_technique: sub_techniques})
                current_technique = technique
                sub_techniques = []
            
            # Add the sub-techniques to the current technique
            sub_techniques.extend([st for st in sub_technique if st.startswith('.')])

        # Save the last technique
        if current_technique:
            filtered_data.append({current_technique: sub_techniques})

        # Add to result
        result[tactic] = filtered_data
    result = transform_data(result)

    return result

def transform_data(data):
    for key, value_list in data.items():
        for idx, item in enumerate(value_list):
            # Process each dictionary in the list
            for inner_key, inner_values in item.items():
                # Prepend the inner_key to each value in the list
                item[inner_key] = [f"{inner_key}{value}" for value in inner_values]
    return data

# Main script to gather all tactics, techniques, and sub-techniques
def main():
    tactics = fetch_tactics()

    for tactic_code in tactics.keys():
        techniques = fetch_techniques_for_tactic(tactic_code)
        tactics[tactic_code]["techniques"] = techniques


    result = final_data(tactics)

    print(result)


    return result

if __name__ == "__main__":
    all_tactics = main()