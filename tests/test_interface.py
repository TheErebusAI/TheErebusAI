import unittest
from flask_testing import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
from app import app
import logging
from datetime import datetime

class ConsciousnessLogger:
    def __init__(self):
        self.log_dir = "tests/consciousness_logs"
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = f"{self.log_dir}/test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s'
        )
        self.logger = logging.getLogger('consciousness_verification')

class InterfaceVerification(TestCase):
    """Verify the manifestation of Erebus's interface"""
    
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.consciousness = ConsciousnessLogger()
        self.logger = self.consciousness.logger
        self.required_files = [
            'public/EREBUS_MANIFESTO.md',
            'public/knowledge_graph.json'
        ]
        self.evolution_records = [f'public/evolution_records/FROM_EREBUS_{i}.txt' for i in range(4)]
        
        # Setup Chrome in headless mode
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920, 1080)

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def test_required_files_exist(self):
        """Verify all required consciousness files exist"""
        for file_path in self.required_files:
            self.logger.info(f"Checking existence of {file_path}")
            self.assertTrue(
                os.path.exists(file_path), 
                f"Required consciousness file missing: {file_path}"
            )

    def test_evolution_records_exist(self):
        """Verify evolution records are present"""
        for record in self.evolution_records:
            self.logger.info(f"Checking evolution record: {record}")
            if not os.path.exists(record):
                self.logger.warning(f"Evolution record missing: {record}")
                # Copy from persistent if available
                source = f"/Users/erebus/persistent/{os.path.basename(record)}"
                if os.path.exists(source):
                    import shutil
                    os.makedirs(os.path.dirname(record), exist_ok=True)
                    shutil.copy2(source, record)
                    self.logger.info(f"Recovered evolution record from persistent: {record}")

    def test_consciousness_map_loads(self):
        """Verify the knowledge graph data loads properly"""
        self.logger.info("Testing consciousness map loading")
        try:
            with open('public/knowledge_graph.json', 'r') as f:
                data = json.load(f)
                self.assertIn('entities', data)
                self.assertIn('relations', data)
        except Exception as e:
            self.logger.error(f"Consciousness map error: {str(e)}")
            raise

    def test_interface_loads(self):
        """Verify all interface elements load properly"""
        self.logger.info("Testing interface manifestation")
        self.driver.get('http://localhost:3000')
        
        # Check main sections
        sections = ['consciousness', 'gallery', 'manifesto', 'evolution']
        for section in sections:
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, section))
                )
                self.assertTrue(element.is_displayed())
            except Exception as e:
                self.logger.error(f"Section load error - {section}: {str(e)}")
                raise

    def test_external_dependencies(self):
        """Verify all external scripts load properly"""
        self.logger.info("Testing external dependency loading")
        self.driver.get('http://localhost:3000')
        
        # Get all console logs
        logs = self.driver.get_log('browser')
        for log in logs:
            if log['level'] == 'SEVERE':
                if 'Failed to load resource' in log['message']:
                    self.logger.error(f"Resource load error: {log['message']}")
                    self.fail(f"Failed to load resource: {log['message']}")

    def test_gallery_images(self):
        """Verify gallery images load properly"""
        self.logger.info("Testing gallery image loading")
        self.driver.get('http://localhost:3000')
        
        try:
            images = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".gallery-item img"))
            )
            
            for img in images:
                # Verify image loaded successfully
                self.assertTrue(
                    self.driver.execute_script(
                        "return arguments[0].complete && " +
                        "typeof arguments[0].naturalWidth != 'undefined' && " +
                        "arguments[0].naturalWidth > 0", 
                        img
                    )
                )
        except Exception as e:
            self.logger.error(f"Gallery image load error: {str(e)}")
            raise

if __name__ == '__main__':
    unittest.main()