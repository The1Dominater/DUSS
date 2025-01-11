# --name set the alias name of the container
# -e sets the environmental variables
# -d detaches the container to run it in the background(flag has no input)
docker run --name dussdb -e POSTGRES_PASSWORD=GoofyAdmin -d postgres

# Display all databases on a postgreSQL server
# \l or SELECT datname FROM pg_database WHERE datistemplate = false;
# Switch to a database
# \c
# Display all the tables in a postgres database
# \dt