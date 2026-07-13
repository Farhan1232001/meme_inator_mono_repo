# core/clients/base_api_client.py
import asyncio
from typing import Any, Dict, Optional, TypeVar, Generic, Callable, Awaitable
import httpx

T = TypeVar('T')

class ExternalApiError(Exception):
    pass

class ExternalApiTimeoutError(ExternalApiError):
    pass

class ExternalApiResponseError(ExternalApiError):
    def __init__(self, status_code: int, response_text: str):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"API responded with {status_code}: {response_text}")

class BaseApiClient:
    """Reusable HTTP client with retries, timeouts, and error handling."""
    
    def __init__(
        self,
        base_url: str,
        timeout_seconds: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        default_headers: Optional[Dict[str, str]] = None,
    ):
        self._base_url = base_url.rstrip("/")
        self._timeout = httpx.Timeout(timeout_seconds)
        self._max_retries = max_retries
        self._backoff_factor = backoff_factor
        self._default_headers = default_headers or {}
        
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=self._timeout,
            headers=self._default_headers,
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    async def close(self):
        self._client.aclose()
    
    def _request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        last_exception = None
        for attempt in range(self._max_retries):
            try:
                response = self._client.request(
                    method, url, params=params, json=json, headers=headers
                )
                if 200 <= response.status_code < 300:
                    return response
                
                # Raise for retryable (5xx) or non‑retryable (4xx)
                exc = ExternalApiResponseError(response.status_code, response.text)
                if response.status_code >= 500:
                    raise exc
                else:
                    raise exc  # but will not retry because status <500
            
            except (httpx.TimeoutException, httpx.TransportError) as e:
                last_exception = ExternalApiTimeoutError(str(e))
            except ExternalApiResponseError as e:
                last_exception = e
                if e.status_code < 500:  # client error: no retry
                    raise
            
            if attempt < self._max_retries - 1:
                asyncio.sleep(self._backoff_factor * (2 ** attempt))
        
        raise last_exception
    
    # Public convenience methods
    def get_json(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self._request("GET", url, params=params)
        return response.json()
    
    def post_json(self, url: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self._request("POST", url, json=json)
        return response.json()
    
    def put_json(self, url: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self._request("PUT", url, json=json)
        return response.json()
    
    def delete_json(self, url: str) -> Dict[str, Any]:
        response = self._request("DELETE", url)
        return response.json()
    
    # Raw bytes (for fetching images/videos)
    def get_bytes(self, url: str) -> bytes:
        response = self._request("GET", url)
        print(response)
        return response.content