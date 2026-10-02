import os
from typing import Any, Dict, List, Optional
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ServiceNowClient:
    """Client for interacting with ServiceNow Table API."""

    def __init__(
        self,
        instance_url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.instance_url = (instance_url or os.getenv("SERVICENOW_INSTANCE_URL", "")).rstrip("/")
        self.username = username or os.getenv("SERVICENOW_USERNAME", "")
        self.password = password or os.getenv("SERVICENOW_PASSWORD", "")

        if not self.instance_url or not self.username or not self.password:
            raise ValueError(
                "Missing ServiceNow credentials. Ensure SERVICENOW_INSTANCE_URL, "
                "SERVICENOW_USERNAME, and SERVICENOW_PASSWORD are set."
            )

        self.auth = HTTPBasicAuth(self.username, self.password)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def test_connection(self) -> Dict[str, Any]:
        """Test authentication and connection against the instance."""
        url = f"{self.instance_url}/api/now/table/incident"
        params = {"sysparm_limit": 1}
        response = requests.get(
            url, auth=self.auth, headers=self.headers, params=params, timeout=20
        )
        response.raise_for_status()
        return {
            "status": "connected",
            "status_code": response.status_code,
            "instance_url": self.instance_url,
        }

    def query_table(
        self,
        table_name: str,
        query: Optional[str] = None,
        limit: int = 10,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Query records from any ServiceNow table."""
        url = f"{self.instance_url}/api/now/table/{table_name}"
        params: Dict[str, Any] = {"sysparm_limit": limit}

        if query:
            params["sysparm_query"] = query
        if fields:
            params["sysparm_fields"] = ",".join(fields)

        response = requests.get(
            url, auth=self.auth, headers=self.headers, params=params, timeout=30
        )
        response.raise_for_status()
        return response.json().get("result", [])

    def get_incidents(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetch recent incidents."""
        fields = ["sys_id", "number", "short_description", "priority", "state", "sys_created_on"]
        return self.query_table("incident", limit=limit, fields=fields)

    def create_incident(
        self,
        short_description: str,
        description: str,
        urgency: str = "2",
        impact: str = "2",
        additional_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new incident record in ServiceNow."""
        url = f"{self.instance_url}/api/now/table/incident"
        payload = {
            "short_description": short_description,
            "description": description,
            "urgency": urgency,
            "impact": impact,
        }
        if additional_fields:
            payload.update(additional_fields)

        response = requests.post(
            url, auth=self.auth, headers=self.headers, json=payload, timeout=30
        )
        response.raise_for_status()
        return response.json().get("result", {})


if __name__ == "__main__":
    print("Testing connection to ServiceNow instance...")
    try:
        client = ServiceNowClient()
        res = client.test_connection()
        print(f"[SUCCESS] Connected to: {res['instance_url']} (HTTP {res['status_code']})")

        print("\nFetching latest 3 incidents...")
        incidents = client.get_incidents(limit=3)
        print(f"Retrieved {len(incidents)} incident(s):")
        for inc in incidents:
            print(
                f" - [{inc.get('number')}] {inc.get('short_description')} (Priority: {inc.get('priority')})"
            )

    except Exception as exc:
        print(f"[ERROR] Failed to connect: {exc}")
