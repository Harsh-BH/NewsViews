# PostgreSQL Database Setup

This guide explains how to set up the PostgreSQL database for the NewsViews application.

## 1. Install PostgreSQL

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### macOS (using Homebrew)
```bash
brew install postgresql
```

### Windows
Download and install from [PostgreSQL official website](https://www.postgresql.org/download/windows/)

## 2. Start the PostgreSQL Service

### Ubuntu/Debian
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS
```bash
brew services start postgresql
```

### Windows
PostgreSQL should start automatically as a service.

## 3. Create a Database and User

```bash
# Connect to PostgreSQL as postgres user
sudo -u postgres psql

# Inside the PostgreSQL shell
CREATE DATABASE newsviews;
CREATE USER newsuser WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE newsviews TO newsuser;

# Exit PostgreSQL shell
\q
```

## 4. Configure the Application

Edit your `.env` file or update the `config.py` file with your database connection details:

```
DATABASE_URL=postgresql://newsuser:your_password@localhost:5432/newsviews
```

## 5. Install Required Python Packages

The application needs `psycopg2` to connect to PostgreSQL:

```bash
pip install psycopg2-binary
```

## 6. Verify Connection

You can verify the database connection by running:

```bash
# Connect to your database
psql -U newsuser -d newsviews -h localhost
```

If everything is set up correctly, you should be able to connect.

## Troubleshooting

### Connection Issues

If you get connection errors, check:

1. PostgreSQL service is running
2. Database credentials are correct
3. PostgreSQL is configured to accept connections
4. Firewall settings allow connections to port 5432

### Database Configuration

If you need to modify PostgreSQL configuration:

- Configuration files are typically in `/etc/postgresql/[version]/main/` on Linux
- Use `pg_hba.conf` to configure access permissions
- Use `postgresql.conf` to configure server settings
