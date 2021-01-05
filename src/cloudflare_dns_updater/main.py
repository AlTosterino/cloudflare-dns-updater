from cloudflare_dns_updater.queries import get_device_ip

if __name__ == "__main__":
    # Settings.disable_logging()
    device_ip = get_device_ip()
