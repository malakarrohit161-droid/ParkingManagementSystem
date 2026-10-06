def normalize_vehicle_number(vehicle_number):
    """
    Convert vehicle registration number into a standard format.

    Examples:
    uk04 ab 1234  -> UK04AB1234
    UK04-AB-1234  -> UK04AB1234
    uk04ab1234    -> UK04AB1234
    """

    vehicle_number = vehicle_number.strip()

    # Convert lowercase letters to uppercase
    vehicle_number = vehicle_number.upper()

    # Remove spaces
    vehicle_number = vehicle_number.replace(" ", "")

    # Remove hyphens
    vehicle_number = vehicle_number.replace("-", "")

    return vehicle_number