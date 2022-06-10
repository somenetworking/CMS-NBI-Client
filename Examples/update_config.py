# IMPORT STATEMENT
from CMSNBIClient import *
# IMPORT STATEMENT

# Create the CMS_NBI_Client() instance
client = CMS_NBI_Client()

# Call the update_config() function to add the new node to the config
client.update_config()
