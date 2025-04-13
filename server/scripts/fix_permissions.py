#!/usr/bin/env python3
"""
Script to fix PostgreSQL permissions for the NewsViews application.
This script will connect to PostgreSQL as superuser and grant necessary permissions.
"""

import os
import sys
import argparse
import getpass
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def grant_permissions(db_name, user, host='localhost', port=5432, superuser='postgres', superuser_password=None):
    """Grant necessary permissions to the database user."""
    
    # Connect to PostgreSQL as superuser
    if superuser_password is None:
        superuser_password = getpass.getpass(f"Enter password for PostgreSQL superuser '{superuser}': ")
        
    try:
        # First connect to default 'postgres' database to ensure we can connect
        conn = psycopg2.connect(
            dbname='postgres',
            user=superuser,
            password=superuser_password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        print(f"Connected to PostgreSQL as {superuser}")
        conn.close()
        
        # Connect to the specific database
        conn = psycopg2.connect(
            dbname=db_name,
            user=superuser,
            password=superuser_password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print(f"Granting permissions to user '{user}' on database '{db_name}'...")
        
        # Grant permissions
        commands = [
            f"GRANT USAGE ON SCHEMA public TO {user};",
            f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {user};",
            f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO {user};",
            f"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {user};",
            f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO {user};",
            f"ALTER DATABASE {db_name} OWNER TO {user};"  # Make user the owner of the database
        ]
        
        for cmd in commands:
            print(f"Executing: {cmd}")
            cursor.execute(cmd)
        
        print("Permissions granted successfully!")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Fix PostgreSQL permissions for NewsViews')
    parser.add_argument('--db-name', default='newsviews', help='Database name')
    parser.add_argument('--user', default='harsh', help='Username to grant permissions to')
    parser.add_argument('--host', default='localhost', help='PostgreSQL host')
    parser.add_argument('--port', default=5432, type=int, help='PostgreSQL port')
    parser.add_argument('--superuser', default='postgres', help='PostgreSQL superuser name')
    parser.add_argument('--superuser-password', help='PostgreSQL superuser password')
    
    args = parser.parse_args()
    
    success = grant_permissions(
        args.db_name,
        args.user,
        args.host,
        args.port,
        args.superuser,
        args.superuser_password
    )
    
    if success:
        print("\nPermission setup complete! You can now run your application.")
        print("Ensure your .env file uses the following settings:")
        print(f"DATABASE_URL=postgresql://{args.user}:YOUR_PASSWORD@{args.host}:{args.port}/{args.db_name}")
    else:
        print("\nFailed to set up permissions. Please check the error message above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
