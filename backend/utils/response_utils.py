"""Helpers for building standardised API responses."""

from typing import Any, Optional


def success_response(data: Any, message: str = "OK") -> dict:
    return {"success": True, "message": message, "data": data}


def error_response(message: str, code: int = 400) -> dict:
    return {"success": False, "message": message, "data": None, "code": code}
