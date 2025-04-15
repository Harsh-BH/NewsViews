#!/usr/bin/env python3

import requests
import json
import time
import sys
import argparse

def test_sync_api(base_url):
    """Test the synchronization service API endpoints"""
    api_base = f"{base_url.rstrip('/')}/sync"
    
    print("\n=== Testing Sync Service API ===")
    
    # Get current status
    print("\n--- Getting Current Status ---")
    response = requests.get(f"{api_base}/status")
    print(f"Status code: {response.status_code}")
    try:
        status = response.json()
        print(f"Current status: {json.dumps(status, indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    # Start the sync service
    print("\n--- Starting Sync Service ---")
    response = requests.post(f"{api_base}/start")
    print(f"Status code: {response.status_code}")
    try:
        result = response.json()
        print(f"Result: {json.dumps(result, indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    # Get status after starting
    print("\n--- Getting Status After Start ---")
    response = requests.get(f"{api_base}/status")
    print(f"Status code: {response.status_code}")
    try:
        status = response.json()
        print(f"Current status: {json.dumps(status, indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    # Run a sync operation manually
    print("\n--- Running Manual Sync ---")
    response = requests.post(f"{api_base}/sync-now")
    print(f"Status code: {response.status_code}")
    try:
        result = response.json()
        print(f"Result: {json.dumps(result, indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    # Get status after manual sync
    print("\n--- Getting Status After Manual Sync ---")
    response = requests.get(f"{api_base}/status")
    print(f"Status code: {response.status_code}")
    try:
        status = response.json()
        print(f"Current status: {json.dumps(status, indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    # Stop the sync service
    print("\n--- Stopping Sync Service ---")
    response = requests.post(f"{api_base}/stop")
    print(f"Status code: {response.status_code}")
    try:
        result = response.json()
        print(f"Result: {json.dumps(result, indent=2)}")
    except:
        print(f"Response: {response.text}")
    
    # Get status after stopping
    print("\n--- Getting Status After Stop ---")
    response = requests.get(f"{api_base}/status")
    print(f"Status code: {response.status_code}")
    try:
        status = response.json()
        print(f"Current status: {json.dumps(status, indent=2)}")
    except:
        print(f"Response: {response.text}")

def main():
    parser = argparse.ArgumentParser(description="Test the NewsViews Sync API")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL for the API")
    args = parser.parse_args()
    
    print(f"Testing Sync API at: {args.url}")
    
    # Health check first
    print("\n=== Testing Health Check ===")
    try:
        response = requests.get(f"{args.url}/health")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.RequestException as e:
        print(f"Error connecting to server: {e}")
        print("Make sure the server is running and the URL is correct.")
        sys.exit(1)
    
    # Test sync API endpoints
    test_sync_api(args.url)

if __name__ == "__main__":
    main()
