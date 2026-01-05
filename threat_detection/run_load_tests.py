import subprocess
import time
import sys
from datetime import datetime

def run_test(test_name, command, duration=30):
    """Run a single test and display results"""
    print(f"\n{'='*60}")
    print(f"🚀 STARTING: {test_name}")
    print(f"{'='*60}")
    print(f"⏰ Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📝 Command: {command}")
    print(f"{'-'*60}")
    
    start_time = time.time()
    
    try:
        # Run the test
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Display output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"⚠️  Errors:\n{result.stderr}")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    elapsed = time.time() - start_time
    print(f"{'-'*60}")
    print(f"⏱️  Test Duration: {elapsed:.1f} seconds")
    print(f"✅ COMPLETED: {test_name}")
    
    return elapsed

def main():
    """Run a complete load testing suite"""
    print("="*80)
    print("🔬 COMPREHENSIVE LOAD TESTING SUITE")
    print("="*80)
    
    tests = [
        {
            'name': 'BASIC LOAD TEST',
            'command': 'python src/threat_detection/heavy_load_tester.py --workers 20 --duration 15 --rps 2000'
        },
        {
            'name': 'MEMORY STRESS TEST',
            'command': 'python src/threat_detection/stress_tester.py --test memory --duration 10 --intensity high'
        },
        {
            'name': 'CPU STRESS TEST',
            'command': 'python src/threat_detection/stress_tester.py --test cpu --duration 10 --intensity high'
        },
        {
            'name': 'NETWORK STRESS TEST',
            'command': 'python src/threat_detection/stress_tester.py --test network --duration 10 --intensity medium'
        },
        {
            'name': 'EXTREME LOAD TEST',
            'command': 'python src/threat_detection/heavy_load_tester.py --mode extreme --duration 10'
        },
        {
            'name': 'DDoS SIMULATION (Educational)',
            'command': 'python src/threat_detection/ddos_simulator.py --duration 10 --bots 200 --type syn_flood'
        }
    ]
    
    total_duration = 0
    test_results = []
    
    for test in tests:
        duration = run_test(test['name'], test['command'])
        test_results.append({
            'name': test['name'],
            'duration': duration,
            'status': 'PASSED' if duration > 0 else 'FAILED'
        })
        time.sleep(2)  # Pause between tests
    
    # Summary Report
    print("\n" + "="*80)
    print("📊 LOAD TESTING SUITE - FINAL REPORT")
    print("="*80)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🧪 Total Tests: {len(tests)}")
    print(f"⏱️  Total Duration: {sum(r['duration'] for r in test_results):.1f} seconds")
    print("-"*80)
    
    for result in test_results:
        status_icon = "✅" if result['status'] == 'PASSED' else "❌"
        print(f"{status_icon} {result['name']:30} {result['duration']:6.1f}s")
    
    print("="*80)
    print("🎯 RECOMMENDATIONS:")
    print("   1. Monitor system resources during tests")
    print("   2. Run tests in isolated environments")
    print("   3. Increase load gradually")
    print("   4. Document all test results")
    print("="*80)

if __name__ == "__main__":
    main()
