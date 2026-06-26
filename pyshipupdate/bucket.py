def create_bucket_name(target_app_name: str, target_app_author: str) -> str:
    target_app_name = target_app_name.strip()
    target_app_author = target_app_author.strip()
    s = f"pyship-{target_app_author}-{target_app_name}"
    s = s.replace(" ", "-")  # AWS does not allow spaces in bucket names
    return s
