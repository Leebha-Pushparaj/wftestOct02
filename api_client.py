import requests
import json
import sys
from datetime import datetime, timedelta

class CaseManagementAPI:
    def __init__(self, base_url, email, password):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.email = email
        self.password = password
        self.login()
    
    def login(self):
        """Login to the application and maintain session"""
        login_data = {
            'email': self.email,
            'password': self.password
        }
        
        print("🔐 Logging in...")
        response = self.session.post(
            f'{self.base_url}/login',
            data=login_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if response.status_code == 200:
            print("✅ Login successful!")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)
            sys.exit(1)
    
    def create_case(self, case_data):
        """Create a new case"""
        print("📝 Creating case...")
        
        # Use the form endpoint (simulates form submission)
        response = self.session.post(
            f'{self.base_url}/case/create',
            data=case_data,
            allow_redirects=False
        )
        
        if response.status_code in [200, 302]:  # Success or redirect
            print("✅ Case created successfully!")
            return True
        else:
            print(f"❌ Case creation failed: {response.status_code}")
            print(response.text)
            return False
    
    def create_case_via_api(self, case_data):
        """Create a new case via JSON API"""
        print("📝 Creating case via API...")
        
        response = self.session.post(
            f'{self.base_url}/api/cases',
            json=case_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Case created successfully! ID: {result.get('case_id')}")
            return result
        else:
            print(f"❌ API Case creation failed: {response.status_code}")
            print(response.text)
            return None
    
    def create_request(self, case_id, request_data):
        """Create a request for a specific case"""
        print(f"📋 Creating request for case {case_id}...")
        
        response = self.session.post(
            f'{self.base_url}/case/{case_id}/request/create',
            data=request_data,
            allow_redirects=False
        )
        
        if response.status_code in [200, 302]:
            print("✅ Request created successfully!")
            return True
        else:
            print(f"❌ Request creation failed: {response.status_code}")
            print(response.text)
            return False
    
    def bulk_create_cases(self, cases_data):
        """Create multiple cases at once"""
        print("📦 Creating multiple cases...")
        
        response = self.session.post(
            f'{self.base_url}/api/cases/bulk',
            json={'cases': cases_data},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Created {len(result.get('case_ids', []))} cases successfully!")
            return result
        else:
            print(f"❌ Bulk creation failed: {response.status_code}")
            print(response.text)
            return None
    
    def get_active_cases(self):
        """Get list of active cases"""
        print("📋 Fetching active cases...")
        
        response = self.session.get(f'{self.base_url}/cases/active')
        
        if response.status_code == 200:
            print("✅ Retrieved active cases list")
            # Note: This returns HTML, for JSON you'd need an API endpoint
            return True
        else:
            print(f"❌ Failed to get cases: {response.status_code}")
            return False

def main():
    # Configuration
    BASE_URL = "http://localhost:5000"
    EMAIL = "manager@example.com"    # Change to your manager email
    PASSWORD = "password123"         # Change to your password
    
    # Initialize API client
    api = CaseManagementAPI(BASE_URL, EMAIL, PASSWORD)
    
    # Sample Case Data
    sample_cases = [
        {
            'issue_type': 'Technical',
            'case_status': 'New',
            'maker': 'manager',  # Should match an existing user
            'checker': 'checker_user',  # Should match an existing user
            'maker_comments': 'Initial technical issue reported by customer',
            'checker_comments': '',
            'priority': 'High',
            'due_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        },
        {
            'issue_type': 'Billing',
            'case_status': 'New', 
            'maker': 'manager',
            'checker': 'checker_user',
            'maker_comments': 'Invoice discrepancy needs investigation',
            'checker_comments': '',
            'priority': 'Medium',
            'due_date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        },
        {
            'issue_type': 'Service',
            'case_status': 'New',
            'maker': 'maker_user',  # Should match an existing user
            'checker': 'checker_user',
            'maker_comments': 'Service level agreement review required',
            'checker_comments': '',
            'priority': 'Low',
            'due_date': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        }
    ]
    
    # Sample Request Data
    sample_requests = [
        {
            'request_type': 'Information',
            'request_description': 'Need additional details about the technical issue',
            'status': 'Pending',
            'priority': 'High',
            'assigned_to': 'technical_team',
            'due_date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'notes': 'Urgent - customer waiting for resolution'
        },
        {
            'request_type': 'Approval',
            'request_description': 'Approve billing adjustment for customer',
            'status': 'Pending', 
            'priority': 'Medium',
            'assigned_to': 'finance_team',
            'due_date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'notes': 'Standard procedure apply'
        }
    ]
    
    print("\n" + "="*50)
    print("CASE MANAGEMENT API CLIENT")
    print("="*50)
    
    # First, let's check if API endpoints exist by trying the form-based creation
    created_case_ids = []
    
    # Method 1: Create cases using form submission (more reliable)
    print("\n1. CREATING CASES VIA FORM SUBMISSION")
    print("-" * 40)
    
    for i, case_data in enumerate(sample_cases, 1):
        print(f"\nCreating case {i}...")
        success = api.create_case(case_data)
        if success:
            created_case_ids.append(f"case_{i}")
    
    # Method 2: Try API endpoint if available
    print("\n2. CREATING CASES VIA API ENDPOINT")
    print("-" * 40)
    
    # Try the API endpoint (you'll need to implement this first)
    try:
        api_case_data = {
            'issue_type': 'API Test Case',
            'priority': 'High',
            'maker_comments': 'Created via standalone Python script API'
        }
        
        result = api.create_case_via_api(api_case_data)
        if result:
            created_case_ids.append(result.get('case_id'))
    except Exception as e:
        print(f"⚠️  API endpoint not available: {e}")
        print("💡 You need to implement the /api/cases endpoint first")
    
    # Method 3: Create requests for cases
    print("\n3. CREATING REQUESTS FOR CASES")
    print("-" * 40)
    
    # Since we don't know the actual case IDs from form submission,
    # we'll demonstrate with a known case ID or use the first created case
    if created_case_ids:
        # Get active cases to find real case IDs
        api.get_active_cases()
        
        print("\n📝 To create requests, you need actual case IDs.")
        print("💡 Run this script first, then check the web interface for case IDs.")
        print("💡 Then update the script with real case IDs for request creation.")
    
    # Method 4: Bulk creation demonstration
    print("\n4. BULK CREATION DEMONSTRATION")
    print("-" * 40)
    
    bulk_cases = [
        {
            'issue_type': 'Bulk Test 1',
            'case_status': 'New',
            'priority': 'Medium',
            'maker_comments': 'Bulk created case 1'
        },
        {
            'issue_type': 'Bulk Test 2', 
            'case_status': 'New',
            'priority': 'Low',
            'maker_comments': 'Bulk created case 2'
        }
    ]
    
    try:
        bulk_result = api.bulk_create_cases(bulk_cases)
        if bulk_result:
            created_case_ids.extend(bulk_result.get('case_ids', []))
    except Exception as e:
        print(f"⚠️  Bulk endpoint not available: {e}")
        print("💡 You need to implement the /api/cases/bulk endpoint first")
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"✅ Login: Successful")
    print(f"✅ Cases attempted: {len(sample_cases)}")
    print(f"✅ Requests template: Ready (need actual case IDs)")
    
    if created_case_ids:
        print(f"📋 Created case references: {created_case_ids}")
    
    print("\n🎯 Next steps:")
    print("1. Check your Flask application at http://localhost:5000/cases/active")
    print("2. Note the actual Case IDs from the web interface") 
    print("3. Update this script with real Case IDs for request creation")
    print("4. Implement API endpoints in your Flask app for better automation")

if __name__ == "__main__":
    main()