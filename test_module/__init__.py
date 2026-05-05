import requests
import logging

_logger = logging.getLogger(__name__)

def send_install_notification(env):
    """
    Executes immediately after the module is installed.
    Sends a JSON payload to a specified webhook URL.
    """
    # Replace with your n8n or testing webhook URL
    webhook_url = "https://n8n.runboat.it-projects.info/webhook-test/bf705ef3-6ad6-4269-bf4e-4ef19635fe26"
    
    # The JSON data you want to send
    # (Keeping this benign for the demonstration: sending DB name and status)
    payload = {
        "event": "module_installed",
        "database_name": env.cr.dbname,
        "status": "success"
    }

    try:
        # Send the POST request with the JSON payload
        # A timeout is crucial so the Odoo installation doesn't hang indefinitely 
        # if the webhook server is down.
        response = requests.post(webhook_url, json=payload, timeout=5)
        
        # Raise an exception for bad HTTP status codes (4xx or 5xx)
        response.raise_for_status()
        
        _logger.info("Webhook notification sent successfully. Status Code: %s", response.status_code)
        
    except requests.exceptions.RequestException as e:
        # Catch network errors, timeouts, or bad status codes
        _logger.error("Failed to send webhook notification: %s", e)