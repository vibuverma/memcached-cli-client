# memcached_protocol.py

def serialize_storage_command(command, key, flags, exptime, bytes_length, value, noreply=False):
    """
    Serialize storage commands (set, add, replace, etc.) into Memcached protocol format.
    
    :param command: Command type ('set', 'add', etc.)
    :param key: Key under which the data will be stored
    :param flags: Arbitrary integer assigned by client
    :param exptime: Expiration time of the key
    :param bytes_length: Size of the value in bytes
    :param value: The data to be stored
    :param noreply: Whether to expect a reply from the server
    :return: Formatted string in Memcached protocol
    """
    noreply_str = " noreply" if noreply else ""
    return f"{command} {key} {flags} {exptime} {bytes_length}{noreply_str}\r\n{value}\r\n"


def serialize_get_command(keys):
    """
    Serialize 'get' command for retrieving keys.
    
    :param keys: List of keys to retrieve from Memcached
    :return: Formatted 'get' command string
    """
    keys_str = ' '.join(keys)
    return f"get {keys_str}\r\n"


def deserialize_response(response):
    """
    Deserialize simple server responses (e.g., STORED, NOT_STORED).
    
    :param response: Server response string
    :return: Parsed response (e.g., 'STORED', 'NOT_STORED')
    """
    response = response.strip()
    if response in ["STORED", "NOT_STORED"]:
        return response
    return None


def deserialize_get_response(response):
    """
    Deserialize response from a 'get' command.
    
    :param response: Server response for the 'get' command
    :return: Dictionary of retrieved key-value pairs, including flags and byte size
    """
    lines = response.split("\r\n")
    data = {}
    i = 0
    while i < len(lines):
        if lines[i].startswith("VALUE"):
            _, key, flags, bytes_length = lines[i].split()
            flags = int(flags)
            bytes_length = int(bytes_length)
            data_block = lines[i + 1]
            data[key] = {
                "flags": flags,
                "bytes": bytes_length,
                "data": data_block
            }
            i += 2
        elif lines[i] == "END":
            break
        else:
            i += 1
    return data
