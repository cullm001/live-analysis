import geoip2.database

GEOIP_DATABASE_PATH = "GeoLite2-Country.mmdb"

def get_country_from_ip(ip):
    try:
        with geoip2.database.Reader(GEOIP_DATABASE_PATH) as reader:
            response = reader.country(ip)
            return response.country.name
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    ip = input("Enter an IP address: ")

    country = get_country_from_ip(ip)

    print(f"IP: {ip} -> Country: {country}")
