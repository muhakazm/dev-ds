from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup

def get_wiki_id_from_page_title(page_title, open_browser=False):
    # Setup Edge WebDriver
    # service = Service(EdgeChromiumDriverManager().install())
    service = Service("drivers/msedgedriver.exe")  # "./" means same folder as notebook
    options = webdriver.EdgeOptions()
    if open_browser:
        pass
    else:
        options.add_argument("--headless")  # Optional: Uncomment for headless mode
    driver = webdriver.Edge(service=service, options=options)
    
    # Go to Wikidata Query Service
    driver.get("https://query.wikidata.org/")
    
    # Prepare your SPARQL query
    sparql_query = f'''
    SELECT ?item WHERE {{
      ?item rdfs:label "{page_title}"@en .
      ?article schema:about ?item ;
               schema:isPartOf <https://en.wikipedia.org/> .
    }}
    LIMIT 1
    '''
    
    try:
        # Wait for CodeMirror to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "CodeMirror"))
        )
        time.sleep(2)
    
        # Click on CodeMirror to focus
        cm_editor = driver.find_element(By.CLASS_NAME, "CodeMirror")
        cm_editor.click()
        time.sleep(1)
    
        # Locate the hidden textarea inside CodeMirror
        textarea = cm_editor.find_element(By.CSS_SELECTOR, "textarea")
        textarea.send_keys(Keys.CONTROL + "a")
        textarea.send_keys(Keys.DELETE)
        textarea.send_keys(sparql_query)
        time.sleep(1)
    
        # Click the "Execute" button
        run_button = driver.find_element(By.ID, "execute-button")
        run_button.click()
    
        # Wait for the results table
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.table"))
        )
        time.sleep(2)
    
        # Parse results
        table_rows = driver.find_elements(By.CSS_SELECTOR, "table.table tbody tr")
        results = []
        for row in table_rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            results.append([col.text for col in cols])
    
        # print("SPARQL Results:", results)
        try:
            wiki_id_target = results[4][0].replace('wd:','')
            return wiki_id_target
        except:
            return None
    
    except Exception as e:
        return wiki_id_target
    finally:
        driver.quit()

def get_dob_from_wikidata(wiki_id):
    url = f"https://www.wikidata.org/wiki/{wiki_id}"
    # Fetch the HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Step 1: Find all label elements
    labels = soup.find_all("div", class_="wikibase-statementgroupview-property-label")
    dob = None
    for label in labels:
        if label.text.strip().lower() == "date of birth":
            # Step 2: Get the parent container
            parent = label.find_parent("div", class_="wikibase-statementgroupview")
    
            # Step 3: Find the value inside this parent
            value = parent.find("div", class_="wikibase-snakview-value wikibase-snakview-variation-valuesnak")
            if value:
                dob = value.text.strip()
            break
    return dob