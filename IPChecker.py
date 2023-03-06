import requests
import json

class iptester():
    def runthis(self, input):

        check_list = input.splitlines()

        no_duplicated_check_list = list(set(check_list)) #no dublicated ips
        output_txt = "out.txt"

        # Open the output file
        with open(output_txt, 'w') as f:
            # Use the values in a for loop
            for value in no_duplicated_check_list:
                base_url = "https://www.virustotal.com/api/v3/ip_addresses/"
                url = f"{base_url}{value}"

                headers = {
                    "accept": "application/json",
                    "x-apikey": "" ######################### API KEY HERE 
                }

                response = requests.get(url, headers=headers)
                json_file = json.loads(response.text)

                ip_address = json_file["data"]["id"]
                print(ip_address)
                as_owner = json_file["data"]["attributes"]["as_owner"]
                print(as_owner)
                last_analysis_stats = json_file["data"]["attributes"]["last_analysis_stats"]
                print(last_analysis_stats)

                f.write(f"IP Address: {ip_address}\n")
                f.write(f"AS Owner: {as_owner}\n")
                f.write("Last Analysis Stats:\n")
                for engine, result in last_analysis_stats.items():
                    if isinstance(result, dict):
                        category = str(result['category'])
                        method = str(result['method'])
                        f.write(f"\t{engine}: {category} ({method})\n")
                    else:
                        f.write(f"\t{engine}: {result}\n")
                f.write("="*50 + "\n")
    
