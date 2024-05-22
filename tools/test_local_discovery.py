from panduza import Client

# Test the comportement of local discovery to connect a 
# client without precising url and port, the user can choose 
# to use a plaform name to look for a platform with his given
# name on the local network, or just using it without parameters 
# to look fot the first platform found
if __name__ == "__main__":

    platform_name = "panduza_platform"

    # Test with platform name 

    print(f"Try to find a platform on the local network with the name {platform_name}")

    client = Client(platform_name=platform_name)
    client.connect()

    print(f"Success to connecting to the broker of the platform with the name {platform_name}\n")

    # Test looking for the fist platform found

    print(f"Try to find a platform on the local network")

    client2 = Client()
    client2.connect()

    print("Success to connect to the first platform found on the local network")
