from mongokit import Connection

# Create a connection to the MongoDB server
client = Connection()

# Set the default database and collection
database = client['my_database']
collection = database['my_collection']
