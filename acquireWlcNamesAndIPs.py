#!/usr/bin/env python3


import ipaddress, re, sys


def acquireWlcName(inputName):

    # Acquire the WLC name
    wlcName = input("\n" + inputName + " WLC name (leave blank and press Enter to skip): ")
    
    # Return if None or keep verifying that it contains only valid characters (a-z, A-Z, ., -, _)
    if not wlcName:
        return
    else:
        while not re.fullmatch('^[a-zA-Z0-9\.\-\_]+$', wlcName):
            wlcName = input("\nName format not valid. Please re-enter the " + inputName + " WLC name: ")

    return str(wlcName)


def acquireWlcIP(inputName):

    # Acquire the WLC IPv4 and verify its format
    try:
        wlcIP = ipaddress.IPv4Address(input("\n" + inputName + " WLC IPv4: "))
    except ipaddress.AddressValueError:
        while True:
            try:
                wlcIP = ipaddress.IPv4Address(input("IP address format not valid. Please re-enter the " + inputName + " WLC IPv4: "))
                break
            except ipaddress.AddressValueError:
                pass

    # Keep asking while it's not a valid IPv4 (link local, loopback, multicast, broadcast, etc.)
    while wlcIP.is_global or wlcIP.is_link_local or wlcIP.is_loopback or wlcIP.is_multicast or wlcIP.is_reserved or wlcIP.is_unspecified or re.match(".*\.0$|.*\.255$", format(wlcIP)):
        try:
            wlcIP = ipaddress.IPv4Address(input("Not a valid IP address. Please re-enter the " + inputName + " WLC IPv4: "))
        except ipaddress.AddressValueError:
            while True:
                try:
                    wlcIP = ipaddress.IPv4Address(input("IP address format not valid. Please re-enter the " + inputName + " WLC IPv4: "))
                    break
                except ipaddress.AddressValueError:
                    pass
    
    return format(wlcIP) # Return the IPv4 as a string


def confirmChanges():

    answer = input("\nAre you ok with these changes? (yes/no) ") # Ask to confirm the settings or exit the script

    # Keep asking while the end user does not type 'yes' or 'no' and ignoring upper/lower cases
    while not (re.fullmatch('no', answer, re.IGNORECASE) or re.fullmatch('yes', answer, re.IGNORECASE)):
        try:
            answer = input("Please answer yes or no. Are you ok with these changes? (yes/no) ") # Ask to confirm the settings or exit the script
        except KeyboardInterrupt:
            print("\n\nThank you, the script will stop here.\n")
            sys.exit()
    
    if re.fullmatch('no', answer, re.IGNORECASE): # If changes are not confirmed, exit the script
        print("\nThank you, the script will stop here.\n")
        sys.exit()
    else:
        return


# Acquire WLC names and IPs and accept CTRL+C to interrupt the script
tmp_wlcNamesAndIPs = [{'type': 'Primary', 'name': None, 'IP': None}, {'type': 'Secondary', 'name': None, 'IP': None}, {'type': 'Tertiary', 'name': None, 'IP': None}]
try:
    for i, wlc in enumerate(tmp_wlcNamesAndIPs):
        tmp_wlcNamesAndIPs[i]['name'] = acquireWlcName(wlc['type'])
        if tmp_wlcNamesAndIPs[i]['name']: # Acquire the WLC's IP only if the end user already provided the WLC's name
            tmp_wlcNamesAndIPs[i]['IP'] = acquireWlcIP(wlc['type'])
except KeyboardInterrupt:
    print("\n\nThank you, the script will stop here.\n")
    sys.exit()

if any(wlc['name'] and wlc['IP'] for wlc in tmp_wlcNamesAndIPs): # Check if there is any WLC dictionary entry with a valid name and IP
    print("\nThe script will configure WLC HA settings on the APs to the following:")
    
    for wlc in tmp_wlcNamesAndIPs: # For each WLC dictionary entry with a valid name and IP, print a resume of the settings
        if wlc['name'] and wlc['IP']:
            print(f"""
    {wlc['type']} WLC name: {wlc['name']}
    {wlc['type']} WLC IP: {wlc['IP']}""")
    
    confirmChanges() # Call the function to confirm changes
    print("\nThank you, your WLC HA settings have been saved.\n")

else: # If no WLC dictionary entry with a valid IP (and name) exists, exit the script
    print("\nThank you, the script will stop here.\n")
    sys.exit()

# Build the final list, only with WLC dictionary entries having valid names/IPs
wlcNamesAndIPs = []
for wlc in tmp_wlcNamesAndIPs:
    if wlc['name'] and wlc['IP']: # Check both a valid name and IP for robustness
        wlcNamesAndIPs.append(wlc)
print(wlcNamesAndIPs) # Checkpoint to confirm the final list



