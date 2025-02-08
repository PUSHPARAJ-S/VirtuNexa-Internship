import requests
from bs4 import BeautifulSoup
import pandas as pd

# ===================== Web Scraper =====================

def fetch_data(url):
    try:
        # Send GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Extracting all links
        links = []
        for a_tag in soup.find_all('a', href=True):
            links.append(a_tag['href'])

        # Save data to CSV
        df = pd.DataFrame(links, columns=['Links'])
        df.to_csv('scraped_links.csv', index=False)

        print("Scraping complete. Data saved to 'scraped_links.csv'.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

# ===================== Calculator =====================

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

def calculator():
    print("Welcome to the Python Calculator!")
    while True:
        try:
            num1 = float(input("Enter first number: "))
            op = input("Enter operation (+, -, *, /): ")
            num2 = float(input("Enter second number: "))
            
            if op == "+":
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif op == "-":
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif op == "*":
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            elif op == "/":
                print(f"{num1} / {num2} = {divide(num1, num2)}")
            else:
                print("Invalid operation. Try again.")
            
            again = input("Do you want to calculate again? (yes/no): ")
            if again.lower() != 'yes':
                break
        except ValueError:
            print("Invalid input. Please enter numeric values.")

# ===================== Main Program =====================

def main():
    print("Choose an option:")
    print("1. Web Scraper")
    print("2. Calculator")
    
    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        url = input("Enter the URL to scrape: ")
        fetch_data(url)
    elif choice == '2':
        calculator()
    else:
        print("Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    main()
