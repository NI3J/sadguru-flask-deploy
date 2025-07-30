# Sanitize MySQL .sql file for PostgreSQL compatibility

input_file = "spiritual_backup.sql"
output_file = "spiritual_backup_cleaned.sql"

with open(input_file, "r", encoding="utf-8") as infile:
    lines = infile.readlines()

cleaned_lines = []
for line in lines:
    # Skip MySQL-specific locking commands
    if "LOCK TABLES" in line or "UNLOCK TABLES" in line:
        continue
    # Replace backticks with double quotes
    cleaned_line = line.replace("`", '"')
    cleaned_lines.append(cleaned_line)

with open(output_file, "w", encoding="utf-8") as outfile:
    outfile.writelines(cleaned_lines)

print(f"Sanitized file saved as: {output_file}")
