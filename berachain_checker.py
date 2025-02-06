import requests
import time

def check_berachain_allocation(address_file_path):
    with open(address_file_path, 'r') as file:
        addresses = [line.strip() for line in file if line.strip()]
    
    qualified_addresses = []
    base_url = "https://checker-api.berachain.com/whitelist/wallet/allocation?address="

    headers = {
        'Origin': 'https://checker.berachain.com',
        'Referer': 'https://checker.berachain.com/',
    }

    print(f"Checking {len(addresses)} addresses...")
    
    for address in addresses:
        try:
            response = requests.get(base_url + address, headers=headers)
            data = response.json()
            
            token_qualified = float(data.get('tokenQualified', 0))
            if token_qualified > 0:
                qualified_addresses.append({
                    'address': address,
                    'tokens_qualified': token_qualified,
                    'details': data.get('detail', {})
                })
            
            time.sleep(0.1)
            
        except Exception as e:
            print(f"Error checking address {address}: {str(e)}")
    
    return qualified_addresses

def main():
    file_path = 'addresses.txt'
    
    try:
        results = check_berachain_allocation(file_path)
        
        print("\nQualified Addresses:")
        print("===================")
        
        for item in results:
            print(f"\nAddress: {item['address']}")
            print(f"Tokens Qualified: {item['tokens_qualified']}")
            print(f"Details: {item['details']}")
        
        print(f"\nTotal qualified addresses found: {len(results)}")
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
