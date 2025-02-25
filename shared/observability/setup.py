"""Setup helpers for OpenLit observability."""

import os
from typing import Optional

import openlit


def setup_openlit(
    service_name: str, 
    otlp_endpoint: Optional[str] = None,
    disable: bool = False
) -> None:
    """
    Configure OpenLit for tracing and observability.
    
    Args:
        service_name: Name of the service for tracing
        otlp_endpoint: OTLP endpoint (defaults to env var OPENLIT_ENDPOINT)
        disable: Whether to disable OpenLit (useful for testing)
    """
    if disable:
        return
        
    endpoint = otlp_endpoint or os.getenv("OPENLIT_ENDPOINT", "http://127.0.0.1:4318")
    
    openlit.init(
        otlp_endpoint=endpoint,
        service_name=service_name,
    )
    
    print(f"OpenLit initialized for {service_name} with endpoint {endpoint}")