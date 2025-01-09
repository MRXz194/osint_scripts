
import requests
import time
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
from tqdm import tqdm

init()  

class UsernameOSINT:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        self.platforms = {
            'Facebook': 'https://www.facebook.com/{}',
            'Instagram': 'https://www.instagram.com/{}',
            'Twitter': 'https://twitter.com/{}',
            'Pinterest': 'https://www.pinterest.com/{}/',
            'GitHub': 'https://github.com/{}',
            'LinkedIn': 'https://www.linkedin.com/in/{}',
            'TikTok': 'https://www.tiktok.com/@{}',
            'Zalo': 'https://zalo.me/{}',  
            'YouTube': 'https://www.youtube.com/@{}',
            'Reddit': 'https://www.reddit.com/user/{}',
        }

    def check_username(self, username):
        print(f"\n{Fore.CYAN}Searching for username: {username}{Style.RESET_ALL}\n")
        
        results = []
        for platform, url_pattern in tqdm(self.platforms.items(), desc="Checking platforms"):
            try:
                url = url_pattern.format(username)
                response = requests.get(url, headers=self.headers, timeout=5)
                
                if response.status_code == 200:
                    results.append((platform, url, True))
                elif response.status_code == 404:
                    results.append((platform, url, False))
                else:
                    results.append((platform, url, None))
                    
                time.sleep(1)  
                
            except requests.RequestException:
                results.append((platform, url, None))
                
        self.display_results(results)

    def display_results(self, results):
        print("\n" + "="*50)
        print(f"{Fore.YELLOW}Results:{Style.RESET_ALL}")
        print("="*50 + "\n")
        
        for platform, url, exists in results:
            if exists is True:
                print(f"{Fore.GREEN}[+] {platform}: found!")
                print(f"    {url}{Style.RESET_ALL}")
            elif exists is False:
                print(f"{Fore.RED}[-] {platform}: No pro5 found{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[?] {platform}: Couldn't determine{Style.RESET_ALL}")

def main():
    print(f"""{Fore.CYAN}
+=====================================+
          simple OSINT Tool         
+=====================================+
{Style.RESET_ALL}""")
    
    while True:
        username = input("\nEnter username (or 'quit' to exit): ").strip()
        
        if username.lower() == 'quit':
            break
            
        if username:
            osint = UsernameOSINT()
            osint.check_username(username)
        else:
            print(f"{Fore.RED}enter a valid username!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
