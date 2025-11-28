"""
SQL Exporter Module
Export data to SQL format for multiple database systems
"""

from typing import List, Dict
from datetime import datetime


class SQLExporter:
    """Export data to SQL format for various database systems"""
    
    # Database type constants
    ORACLE = 'oracle'
    POSTGRESQL = 'postgresql'
    MARIADB = 'mariadb'
    MYSQL = 'mysql'
    SQLSERVER = 'sqlserver'
    SQLITE = 'sqlite'
    
    # Output mode constants
    STRUCTURE_ONLY = 1
    DATA_ONLY = 2
    STRUCTURE_AND_DATA = 3
    
    # Table name
    TABLE_NAME = 'penduduk'
    
    # Column definitions
    COLUMNS = [
        ('NKK', 'VARCHAR', 16),
        ('NIK', 'VARCHAR', 16),
        ('NAMA', 'VARCHAR', 100),
        ('JENIS_KELAMIN', 'VARCHAR', 1),
        ('TEMPAT_LAHIR', 'VARCHAR', 100),
        ('TANGGAL_LAHIR', 'VARCHAR', 10),
        ('AGAMA', 'VARCHAR', 50),
        ('PENDIDIKAN', 'VARCHAR', 100),
        ('PEKERJAAN', 'VARCHAR', 100),
        ('STATUS_PERKAWINAN', 'VARCHAR', 50),
        ('STATUS_HUBUNGAN', 'VARCHAR', 50),
        ('GOLONGAN_DARAH', 'VARCHAR', 5),
        ('KEWARGANEGARAAN', 'VARCHAR', 10),
        ('NAMA_AYAH', 'VARCHAR', 100),
        ('NAMA_IBU', 'VARCHAR', 100),
        ('ALAMAT', 'VARCHAR', 255),
        ('RT', 'VARCHAR', 5),
        ('RW', 'VARCHAR', 5),
        ('KODE_KELURAHAN', 'VARCHAR', 15),
        ('KELURAHAN', 'VARCHAR', 100),
        ('KODE_KECAMATAN', 'VARCHAR', 10),
        ('KECAMATAN', 'VARCHAR', 100),
        ('KODE_KABUPATEN', 'VARCHAR', 10),
        ('KABUPATEN', 'VARCHAR', 100),
        ('KODE_PROVINSI', 'VARCHAR', 5),
        ('PROVINSI', 'VARCHAR', 100),
        ('LATITUDE', 'DECIMAL', (10, 7)),
        ('LONGITUDE', 'DECIMAL', (10, 7)),
    ]
    
    def __init__(self, db_type: str):
        """
        Initialize SQL Exporter
        
        Args:
            db_type: Database type (oracle, postgresql, mariadb, mysql, sqlserver, sqlite)
        """
        self.db_type = db_type.lower()
        
    def export(self, data: List[dict], mode: int) -> str:
        """
        Export data to SQL format
        
        Args:
            data: List of person records
            mode: 1=structure only, 2=data only, 3=structure+data
            
        Returns:
            SQL string
        """
        lines = []
        
        # Add header comment
        lines.append(self._get_header())
        
        # Add structure if needed
        if mode in [self.STRUCTURE_ONLY, self.STRUCTURE_AND_DATA]:
            lines.append(self._get_drop_table())
            lines.append("")
            lines.append(self._get_create_table())
            lines.append("")
        
        # Add data if needed
        if mode in [self.DATA_ONLY, self.STRUCTURE_AND_DATA]:
            lines.append(self._get_insert_statements(data))
        
        return "\n".join(lines)
    
    def _get_header(self) -> str:
        """Generate SQL header comment"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db_names = {
            self.ORACLE: 'Oracle',
            self.POSTGRESQL: 'PostgreSQL',
            self.MARIADB: 'MariaDB',
            self.MYSQL: 'MySQL',
            self.SQLSERVER: 'SQL Server',
            self.SQLITE: 'SQLite'
        }
        
        return f"""-- ============================================================
-- DUKCAPIL Data Generator - SQL Export
-- Database: {db_names.get(self.db_type, 'Unknown')}
-- Generated: {timestamp}
-- ============================================================
"""
    
    def _get_drop_table(self) -> str:
        """Generate DROP TABLE statement"""
        if self.db_type == self.SQLSERVER:
            return f"""IF OBJECT_ID('{self.TABLE_NAME}', 'U') IS NOT NULL
    DROP TABLE {self.TABLE_NAME};"""
        elif self.db_type == self.ORACLE:
            return f"""BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE {self.TABLE_NAME}';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/"""
        else:
            return f"DROP TABLE IF EXISTS {self.TABLE_NAME};"
    
    def _get_create_table(self) -> str:
        """Generate CREATE TABLE statement based on database type"""
        columns = []
        
        for col_name, col_type, col_size in self.COLUMNS:
            col_def = self._get_column_definition(col_name, col_type, col_size)
            columns.append(f"    {col_def}")
        
        # Add primary key
        pk_def = self._get_primary_key()
        if pk_def:
            columns.append(f"    {pk_def}")
        
        columns_str = ",\n".join(columns)
        
        # Build CREATE TABLE statement
        if self.db_type == self.MYSQL or self.db_type == self.MARIADB:
            return f"""CREATE TABLE {self.TABLE_NAME} (
{columns_str}
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""
        elif self.db_type == self.SQLSERVER:
            return f"""CREATE TABLE [{self.TABLE_NAME}] (
{columns_str}
);"""
        else:
            return f"""CREATE TABLE {self.TABLE_NAME} (
{columns_str}
);"""
    
    def _get_column_definition(self, name: str, col_type: str, size) -> str:
        """Get column definition for specific database"""
        if self.db_type == self.ORACLE:
            if col_type == 'VARCHAR':
                return f"{name} VARCHAR2({size})"
            elif col_type == 'DECIMAL':
                precision, scale = size
                return f"{name} NUMBER({precision},{scale})"
            return f"{name} {col_type}"
        
        elif self.db_type == self.SQLSERVER:
            if col_type == 'VARCHAR':
                return f"[{name}] NVARCHAR({size})"
            elif col_type == 'DECIMAL':
                precision, scale = size
                return f"[{name}] DECIMAL({precision},{scale})"
            return f"[{name}] {col_type}"
        
        elif self.db_type == self.SQLITE:
            if col_type == 'DECIMAL':
                return f"{name} REAL"
            return f"{name} TEXT"
        
        else:  # PostgreSQL, MySQL, MariaDB
            if col_type == 'VARCHAR':
                return f"{name} VARCHAR({size})"
            elif col_type == 'DECIMAL':
                precision, scale = size
                return f"{name} DECIMAL({precision},{scale})"
            return f"{name} {col_type}"
    
    def _get_primary_key(self) -> str:
        """Get primary key constraint"""
        if self.db_type == self.SQLSERVER:
            return "CONSTRAINT PK_penduduk PRIMARY KEY ([NIK])"
        elif self.db_type == self.ORACLE:
            return "CONSTRAINT PK_penduduk PRIMARY KEY (NIK)"
        else:
            return "PRIMARY KEY (NIK)"
    
    def _get_insert_statements(self, data: List[dict]) -> str:
        """Generate INSERT statements"""
        if not data:
            return "-- No data to insert"
        
        lines = []
        
        # Get column names
        col_names = [col[0] for col in self.COLUMNS]
        
        if self.db_type == self.SQLSERVER:
            col_names_str = ", ".join([f"[{c}]" for c in col_names])
        else:
            col_names_str = ", ".join(col_names)
        
        # Generate INSERT statements
        # Use batch insert for efficiency where supported
        if self.db_type in [self.MYSQL, self.MARIADB]:
            # MySQL/MariaDB supports multi-value INSERT
            lines.append(f"INSERT INTO {self.TABLE_NAME} ({col_names_str}) VALUES")
            
            values_list = []
            for i, record in enumerate(data):
                values = self._format_values(record, col_names)
                values_list.append(f"({values})")
                
                # Batch every 100 records
                if (i + 1) % 100 == 0 or i == len(data) - 1:
                    lines.append(",\n".join(values_list) + ";")
                    values_list = []
                    if i < len(data) - 1:
                        lines.append("")
                        lines.append(f"INSERT INTO {self.TABLE_NAME} ({col_names_str}) VALUES")
        
        elif self.db_type == self.POSTGRESQL:
            # PostgreSQL also supports multi-value INSERT
            lines.append(f"INSERT INTO {self.TABLE_NAME} ({col_names_str}) VALUES")
            
            values_list = []
            for i, record in enumerate(data):
                values = self._format_values(record, col_names)
                values_list.append(f"({values})")
                
                if (i + 1) % 100 == 0 or i == len(data) - 1:
                    lines.append(",\n".join(values_list) + ";")
                    values_list = []
                    if i < len(data) - 1:
                        lines.append("")
                        lines.append(f"INSERT INTO {self.TABLE_NAME} ({col_names_str}) VALUES")
        
        else:
            # Oracle, SQL Server, SQLite - individual INSERT statements
            for record in data:
                values = self._format_values(record, col_names)
                if self.db_type == self.SQLSERVER:
                    lines.append(f"INSERT INTO [{self.TABLE_NAME}] ({col_names_str}) VALUES ({values});")
                else:
                    lines.append(f"INSERT INTO {self.TABLE_NAME} ({col_names_str}) VALUES ({values});")
        
        # Add COMMIT for databases that need it
        if self.db_type == self.ORACLE:
            lines.append("")
            lines.append("COMMIT;")
        
        return "\n".join(lines)
    
    def _format_values(self, record: dict, col_names: List[str]) -> str:
        """Format values for INSERT statement"""
        values = []
        for col in col_names:
            value = record.get(col, '')
            if value is None:
                values.append('NULL')
            elif col in ['LATITUDE', 'LONGITUDE']:
                # Numeric values without quotes
                if value == '' or value is None:
                    values.append('NULL')
                else:
                    values.append(str(value))
            else:
                # Escape single quotes
                escaped = str(value).replace("'", "''")
                values.append(f"'{escaped}'")
        return ", ".join(values)
    
    @classmethod
    def get_database_options(cls) -> List[tuple]:
        """Get list of supported databases"""
        return [
            (1, cls.ORACLE, 'Oracle'),
            (2, cls.POSTGRESQL, 'PostgreSQL'),
            (3, cls.MARIADB, 'MariaDB'),
            (4, cls.MYSQL, 'MySQL'),
            (5, cls.SQLSERVER, 'SQL Server'),
            (6, cls.SQLITE, 'SQLite'),
        ]
    
    @classmethod
    def get_mode_options(cls) -> List[tuple]:
        """Get list of output modes"""
        return [
            (1, cls.STRUCTURE_ONLY, 'Structure only (CREATE TABLE)'),
            (2, cls.DATA_ONLY, 'Data only (INSERT)'),
            (3, cls.STRUCTURE_AND_DATA, 'Structure + Data'),
        ]


def export_to_sql(data: List[dict], db_type: str, mode: int) -> str:
    """
    Convenience function to export data to SQL
    
    Args:
        data: List of person records
        db_type: Database type string
        mode: Output mode (1, 2, or 3)
        
    Returns:
        SQL string
    """
    exporter = SQLExporter(db_type)
    return exporter.export(data, mode)
