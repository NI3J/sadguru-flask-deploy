import re

def clean_mysql_to_postgresql(input_path, output_path):
    skip_header = True

    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            # Skip MySQL dump headers and directives
            if skip_header:
                if 'CREATE TABLE' in line or 'INSERT INTO' in line:
                    skip_header = False
                else:
                    continue

            # Remove charset and collation declarations
            if 'CHARACTER SET utf8mb4' in line or 'COLLATE=utf8mb4_unicode_ci' in line:
                continue

            # Remove stray MySQL export artifacts like '=9' or '=4'
            if line.strip().endswith('=9') or line.strip().endswith('=4'):
                continue

            # Convert UNIQUE KEY to PostgreSQL-compatible CONSTRAINT syntax
            if 'UNIQUE KEY' in line:
                match = re.search(r'UNIQUE KEY\s+`?(\w+)`?\s*\(([^)]+)\)', line)
                if match:
                    constraint_name = match.group(1)
                    columns = match.group(2)
                    line = f'  CONSTRAINT {constraint_name} UNIQUE ({columns})\n'
                else:
                    line = re.sub(r'UNIQUE KEY\s*\(([^)]+)\)', r'UNIQUE (\1)', line)

            # Remove MySQL backticks
            line = line.replace('`', '')

            outfile.write(line)

# ✅ Now call the function with actual file names
clean_mysql_to_postgresql("spiritual_backup_postgres.sql", "spiritual_backup_cleaned.sql")
