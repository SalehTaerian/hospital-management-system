import psycopg2
import psycopg2.extras
from psycopg2 import pool
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.config import Config
import logging
from contextlib import contextmanager
import os

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """PostgreSQL connection pool"""
    
    _pool = None
    
    @classmethod
    def ensure_database_exists(cls):
        """Create database if it doesn't exist"""
        try:
            try:
                test_conn = psycopg2.connect(
                    host=Config.DB_HOST,
                    port=Config.DB_PORT,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME
                )
                test_conn.close()
                return True
            except psycopg2.OperationalError as e:
                if "does not exist" not in str(e):
                    raise e
            
            conn = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {Config.DB_NAME}")
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error creating database: {e}")
            raise
    
    @classmethod
    def ensure_tables_exist(cls):
        """Create tables if they don't exist"""
        try:
            conn = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'icdcode'
                )
            """)
            exists = cursor.fetchone()[0]
            
            if exists:
                cursor.close()
                conn.close()
                return
            
            # Create tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS icdCode (
                    icdID SERIAL PRIMARY KEY,
                    code VARCHAR(20) UNIQUE NOT NULL,
                    diseaseName VARCHAR(50) NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS icdmCode (
                    icdmID SERIAL PRIMARY KEY,
                    icdID INTEGER NOT NULL REFERENCES icdCode(icdID) ON DELETE CASCADE,
                    medicineName VARCHAR(20) NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS icdtCode (
                    icdtID SERIAL PRIMARY KEY,
                    testName VARCHAR(50),
                    cost NUMERIC(15, 0)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS icdsCode (
                    icdsID SERIAL PRIMARY KEY,
                    surgeryName VARCHAR(20),
                    cost NUMERIC(15, 0)
                )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    @classmethod
    def initialize_pool(cls, min_conn=1, max_conn=10):
        """Initialize connection pool"""
        if cls._pool is None:
            try:
                cls.ensure_database_exists()
                cls.ensure_tables_exist()
                cls._pool = psycopg2.pool.SimpleConnectionPool(
                    min_conn,
                    max_conn,
                    dsn=Config.get_db_url()
                )
                logger.info("Database connection pool initialized")
            except Exception as e:
                logger.error(f"Failed to initialize database pool: {e}")
                raise
    
    @classmethod
    @contextmanager
    def get_connection(cls):
        """Get a connection from the pool"""
        conn = None
        try:
            conn = cls._pool.getconn()
            yield conn
        finally:
            if conn:
                cls._pool.putconn(conn)
    
    @classmethod
    def execute_query(cls, query, params=None, fetch_one=False, fetch_all=False, fetch_dict=False, commit=False):
        """Execute a query and return results"""
        with cls.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor if fetch_dict else None)
            try:
                cursor.execute(query, params)
                
                if commit:
                    conn.commit()
                    # For INSERT with RETURNING, fetch the result
                    if fetch_one or fetch_all:
                        pass  # Continue to fetch
                    else:
                        return cursor.rowcount
                
                if fetch_one:
                    result = cursor.fetchone()
                    if fetch_dict and result:
                        return dict(result)
                    return result  # Returns tuple like (1,)
                
                if fetch_all:
                    results = cursor.fetchall()
                    if fetch_dict:
                        return [dict(row) for row in results]
                    return results
                
                return cursor.rowcount
                
            except Exception as e:
                if commit:
                    conn.rollback()
                logger.error(f"Database error: {e}")
                raise
            finally:
                cursor.close()
    
    @classmethod
    def close_all_connections(cls):
        """Close all connections in the pool"""
        if cls._pool:
            cls._pool.closeall()