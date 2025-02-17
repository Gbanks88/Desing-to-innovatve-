import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def export_drawio_to_png():
    # Paths
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    drawio_file = os.path.join(current_dir, 'docs', 'workspace_architecture.drawio')
    output_dir = os.path.join(current_dir, 'docs', 'images')
    output_file = os.path.join(output_dir, 'workspace_architecture.png')

    # Create images directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Check if draw.io desktop is installed
    try:
        # Try using draw.io CLI if available
        subprocess.run([
            'drawio',
            '--export',
            '--format', 'png',
            '--scale', '2.0',
            '--output', output_file,
            drawio_file
        ], check=True)
        print(f"Successfully exported diagram to: {output_file}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Draw.io desktop not found. Using web-based export...")
        # Use Selenium with Chrome for web-based export
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            
            driver = webdriver.Chrome(options=chrome_options)
            
            # Load draw.io
            driver.get('https://app.diagrams.net/')
            
            # Wait for the initial dialog
            time.sleep(2)
            
            # Click "Open Existing Diagram"
            open_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Open Existing Diagram')]"))
            )
            open_button.click()
            
            # Upload the file
            file_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            file_input.send_keys(drawio_file)
            
            time.sleep(2)
            
            # Export as PNG
            driver.find_element(By.XPATH, "//span[contains(text(), 'File')]").click()
            driver.find_element(By.XPATH, "//span[contains(text(), 'Export as')]").click()
            driver.find_element(By.XPATH, "//span[contains(text(), 'PNG')]").click()
            
            time.sleep(2)
            
            print(f"Please check your downloads folder for the exported PNG")
            
        except Exception as e:
            print(f"Error exporting diagram: {str(e)}")
        finally:
            driver.quit()

if __name__ == "__main__":
    export_drawio_to_png()
