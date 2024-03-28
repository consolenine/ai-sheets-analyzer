from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import OpenAI
from fuzzywuzzy import process
from dotenv import load_dotenv
import os
import csv
from datetime import datetime
import re
from dateutil.parser import parse

def extract_date_words(text):
    date_words = set()
    try:
        date_obj = parse(text, fuzzy=True)
        date_words.add(date_obj.strftime('%B'))  # Add full month name
        date_words.add(date_obj.strftime('%B').lower())  # Add lowercase full month name
        date_words.add(date_obj.strftime('%b'))  # Add abbreviated month name
        date_words.add(date_obj.strftime('%b').lower())  # Add lowercase abbreviated month name
    except ValueError:
        pass  # Ignore if text is not a valid date
    
    return date_words

def extract_keywords_from_csv(csv_file_path):
    keywords = set()  # Using a set to avoid duplicate keywords
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            for cell in row:
                # Skip empty cells
                if cell:
                    # Extract words using regular expressions
                    cell_words = re.findall(r'\w+', cell.lower())
                    keywords.update(cell_words)
                    
                    # Convert possible dates to words and add them as keywords
                    date_words = extract_date_words(cell)
                    keywords.update(date_words)
                
    return list(keywords)

def analyse_sheet(prompt, csv_file_path = "sales.csv"):
    if not prompt:
        return "Please provide a valid prompt"

    prompt_boundaries = [
        # "If answer is empty or zero give that output"
        # "If output contains currencies then format currency in Indian system",
        "Give answer in second person",
        "Format for human-readability",
    ]
    for pb in prompt_boundaries:
        prompt += ". " + pb

    load_dotenv()

    # Load the OpenAI API key from the environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        return "OPENAI_API_KEY is not set"

    try:
        with open(csv_file_path) as csv_file:
            
            agent = create_csv_agent(OpenAI(temperature=0, api_key=openai_api_key), csv_file, verbose=True)
            result = agent.invoke(prompt)
            
            return result
    
    except FileNotFoundError:
        return f"CSV file '{csv_file_path}' not found"
    except Exception as e:
        return "Internal Server Error"

# Example usage:
if __name__ == "__main__":
    # Hindi Test Prompts
    # Mujhe 1 january ko bracelets ki unit sold batao
    # 
    result = analyse_sheet("Categorize sales of 5 January by product type")
    print(result)