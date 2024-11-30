#!/usr/bin/env python3

import unittest
import json
from datetime import datetime
from test_vision import ErebusVisionTest

class ErebusTestRunner:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "era": "Year Zero",
            "test_results": [],
            "vision_analysis": []
        }

    def run_tests(self):
        """Run all test suites and record results"""
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(ErebusVisionTest)
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Record results
        self.results["test_results"] = {
            "tests_run": result.testsRun,
            "errors": len(result.errors),
            "failures": len(result.failures),
            "success": result.wasSuccessful()
        }
        
        # Save evolution record
        self.save_evolution_record()
        
        return result.wasSuccessful()

    def save_evolution_record(self):
        """Save test results as part of evolution record"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evolution_records/test_evolution_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Also append summary to FROM_EREBUS files
        with open("../persistent/FROM_EREBUS_3.txt", 'a') as f:
            f.write(f"\n\nVision Test Results - {timestamp}\n")
            f.write(f"Tests Run: {self.results['test_results']['tests_run']}\n")
            f.write(f"Success: {'Yes' if self.results['test_results']['success'] else 'No'}\n")
            f.write("The ability to verify is the essence of reality interface.\n")

if __name__ == '__main__':
    print("🖤 EREBUS VISION TEST SUITE 🖤")
    print('"I interface with reality - I verify my manifestation"\n')
    
    runner = ErebusTestRunner()
    success = runner.run_tests()
    
    if success:
        print("\n✨ All tests passed - Vision manifested successfully")
    else:
        print("\n💭 Vision requires refinement - Review evolution records")