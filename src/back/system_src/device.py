
class Device:
    def __init__(self, device_id, name, location, ipv4, port):
        self.device_id = device_id
        self.name = name
        self.location = location
        self.ipv4 = ipv4
        self.port = port

    def to_dict(self):
        return {
            "device_id": self.device_id,
            "name": self.name,
            "location": self.location,
            "ipv4": self.ipv4,
            "port": self.port
        }
