## Install MariaDB server via Docker on WSL2 (one time)
- Pull image from dockerhub\
  `docker pull mariadb:latest`
- Check if image is now available
  `docker image ls`
- For persisting DB data, it is recommened to create a volume & when running\
  the container, specify the "-v" option in "docker run" command to mount that\
  volume to the container path "/var/lib/mysql" which is used by MariaDB to\
  store data
- Create a new Docker volume called "mariadb-data":\
  `docker volume create mariadb-data`
- Run the container with the volume\
  Now, modify your docker run command to mount this new volume. Use the -v flag\
  in the format `-v <volume_name>:<container_path>`:\
  `docker run --name mariadb-server -e MARIADB_ROOT_PASSWORD=manish -p 3306:3306 -v mariadb-data:/var/lib/mysql -d mariadb:latest`\
  (Note: this command is only for 1st time running)
- This "-v flag" in above command instructs Docker to mount the named volume\
  mariadb-data to the /var/lib/mysql directory inside the container.\
  All data (databases, tables, users, etc.) written by the MariaDB server to\
  this location will now be stored in the mariadb-data volume on your host\
  machine.
- Check running containers\
  `docker ps`
- When work is done with the DB server, stop the container using:\
  `docker stop mariadb-server`


## Install `mysql-client` on Ubuntu (one time)
To connect to the running MariaDB server, we can use `mysql-client` which we
will install as follows:
- `sudo apt install mysql-client`

## Connecting to the MariaDB server
Above command installs "mysql-client" package on Ubuntu. Which makes available\
a CLI tool called "mysql" on system path - which we can use to connect to our\
MariaDB server as follows:\
`mysql -h 127.0.0.1 -u root -p`

Note: We had to specify "-h" or hostname option, since normally connection to a\
locally running MySQL/MariaDB server uses a Unix .sock socket file - but since\
we're running DB server within docker, so our MySQL client running on docker\
host WSL2 Ubuntu OS doesn't have that file - so we specify we need to connect\
using the network port, & not a Unix sock file.

We can also specify the database we wish to be selected when we connect\
instead of having to manually do `USE swimDB;` to select every time:\
`mysql -h 127.0.0.1 -u root -p swimDB`

To confirm which database is currently selected we can say:\
`SELECT DATABASE();`

And this should output "NULL" if we didn't specify database name when\
connecting, or "swimDB" if we did.


## Create DB and user (one time)
- Connect to the DB server
- Create a new DB called "swimDB":\
  `CREATE DATABASE swimDB;`
- Confirm if "swimDB" database has been created:\
  `SHOW DATABASES;`
- Create a new user called "swimuser" (setting "swimpasswd" as password):\
  `GRANT ALL ON swimDB.* TO 'swimuser'@'localhost' IDENTIFIED BY 'swimpasswd';`
- Confirm if "swimuser" user has been created:\
  `SELECT User, Host FROM mysql.user;`


## Take dump of table create scripts SQL code from SQLite (one time)
- Install `sqlite3` CLI command on ubuntu\
  `sudo apt install sqlite3`
- Confirm if installed successfully\
  `sqlite3 --version` or `sqlite3 --help`
- Navigate to directory which contains the "CoachDB.sqlite3" database file
  and run below:\
  `sqlite3 CoachDB.sqlite3 .schema > schema.sql`\
- Here `.schema` is a type of [dot command](https://sqlite.org/cli.html#special_commands_to_sqlite3_dot_commands_) provided by sqlite3 CLI


## Running MariaDB container every time:
- When work is done with the DB server, stop the container using:\
  `docker stop mariadb-server`
- To start the same container again:
  `docker start mariadb-server`
