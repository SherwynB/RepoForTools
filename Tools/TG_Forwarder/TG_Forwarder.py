import requests

# -------------------------------
# Telegram Bot Configuration:
# chat_id: -{numbers}        (destination group)
# from_chat_id: {numbers}       (source group or user)
# bot_token: {numberrs}:{alphanumeric}
# -------------------------------

def telegram_api_request(token, method, payload=None, use_get=False):
    url = f"https://api.telegram.org/bot{token}/{method}"
    print(f"\nRequesting URL: {url}")
    if payload:
        print(f"Payload: {payload}")
    try:
        if use_get:
            response = requests.get(url, params=payload)
        else:
            response = requests.post(url, json=payload)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"ok": False, "error": str(e)}

def main():
    # Step 1: Ask the user for all required inputs
    bot_token = input("Enter your bot token: ").strip()
    chat_id_to = input("Enter the group chat ID to forward TO: ").strip()
    chat_id_from = input("Enter the original group chat ID to forward FROM: ").strip()
    starting_message_id = int(input("Enter the starting message ID: ").strip())
    number_of_messages = int(input("Enter the number of messages to forward: ").strip())

    # Step 2: Display webhook info (if set)
    print("\nGetting current webhook info...")
    webhook_info = telegram_api_request(bot_token, "getWebhookInfo", use_get=True)
    print(webhook_info)

    # Step 3: Remove any existing webhook
    print("\nDeleting webhook (if set)...")
    delete_response = telegram_api_request(bot_token, "deleteWebhook")
    print(delete_response)

    # Step 4: Fetch recent updates (with offset = -1)
    print("\nFetching updates with offset = -1...")
    updates = telegram_api_request(bot_token, "getUpdates", {"offset": -1}, use_get=True)
    print(updates)

    # Step 5: Fetch updates after the latest update_id + 1
    if updates.get("result"):
        last_update_id = updates["result"][-1]["update_id"]
        print(f"\nFetching updates starting from offset = {last_update_id + 1}...")
        next_updates = telegram_api_request(
            bot_token, "getUpdates", {"offset": last_update_id + 1}, use_get=True
        )
        print(next_updates)
    else:
        print("\nNo updates found using offset = -1.")

    # Step 6: Start forwarding messages from the source to the destination
    print("\nForwarding messages...")
    for i in range(number_of_messages):
        message_id_to_forward = starting_message_id + i
        payload = {
            "chat_id": chat_id_to,
            "from_chat_id": chat_id_from,
            "message_id": message_id_to_forward
        }
        response = telegram_api_request(bot_token, "forwardMessage", payload)
        print(f"\nForwarded message ID {message_id_to_forward}:")
        print(response)

    # Step 7: Optionally set a new webhook
    print("\nSet a new webhook (optional)")
    choice = input("Do you want to set a new webhook? (y/n): ").strip().lower()
    if choice == "y":
        webhook_url = input("Enter the full HTTPS URL to set as the webhook: ").strip()
        if not webhook_url.startswith("https://"):
            print("Invalid URL. Webhook must start with https://")
        else:
            response = telegram_api_request(bot_token, "setWebhook", {"url": webhook_url})
            print("\nWebhook set response:")
            print(response)
    else:
        print("Skipped setting a new webhook.")

if __name__ == "__main__":
    main()
