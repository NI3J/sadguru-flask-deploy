# 🗄️ MySQL 8.0 Fresh Installation - Ubuntu 22.04.5 LTS (Jammy Jellyfish)
FROM ubuntu:22.04

# 🌿 Environment Variables
ENV DEBIAN_FRONTEND=noninteractive \
    MYSQL_ROOT_PASSWORD=spiritual123 \
    MYSQL_DATABASE=spiritual_db \
    MYSQL_USER=spiritual \
    MYSQL_PASSWORD=spiritual123 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# 🏗️ System Information
RUN echo "MySQL 8.0 Installation for Ubuntu 22.04.5 LTS" && \
    echo "Architecture: $(uname -m)" && \
    echo "Kernel: $(uname -r)" || echo "Kernel: Docker Container"

# ⚙️ Install System Dependencies & MySQL 8.0
RUN apt-get update && apt-get install -y \
    # Basic utilities
    wget \
    curl \
    gnupg \
    lsb-release \
    ca-certificates \
    software-properties-common \
    # MySQL and related packages
    mysql-server-8.0 \
    mysql-client-8.0 \
    mysql-common \
    # System utilities
    supervisor \
    nano \
    vim \
    less \
    procps \
    net-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 🔧 MySQL Configuration Setup
RUN mkdir -p /var/run/mysqld /var/log/mysql /docker-entrypoint-initdb.d && \
    chown -R mysql:mysql /var/run/mysqld /var/log/mysql /var/lib/mysql && \
    chmod 755 /var/run/mysqld

# 📝 Create MySQL Configuration File
RUN echo '[mysqld]\n\
# Basic Settings\n\
user = mysql\n\
pid-file = /var/run/mysqld/mysqld.pid\n\
socket = /var/run/mysqld/mysqld.sock\n\
port = 3306\n\
basedir = /usr\n\
datadir = /var/lib/mysql\n\
tmpdir = /tmp\n\
lc-messages-dir = /usr/share/mysql\n\
\n\
# Network Settings\n\
bind-address = 0.0.0.0\n\
mysqlx-bind-address = 0.0.0.0\n\
\n\
# Security Settings\n\
skip-external-locking\n\
\n\
# Performance Settings\n\
key_buffer_size = 16M\n\
max_allowed_packet = 16M\n\
thread_stack = 192K\n\
thread_cache_size = 8\n\
myisam-recover-options = BACKUP\n\
query_cache_limit = 1M\n\
query_cache_size = 16M\n\
\n\
# Logging\n\
log_error = /var/log/mysql/error.log\n\
expire_logs_days = 10\n\
max_binlog_size = 100M\n\
\n\
# Character Set\n\
character-set-server = utf8mb4\n\
collation-server = utf8mb4_unicode_ci\n\
\n\
[mysql]\n\
default-character-set = utf8mb4\n\
\n\
[client]\n\
default-character-set = utf8mb4\n' > /etc/mysql/mysql.conf.d/custom.cnf

# 🔧 Initialize MySQL Data Directory
RUN mysqld --initialize-insecure --user=mysql --datadir=/var/lib/mysql

# 📁 Copy SQL Backup File
COPY spiritual_backup.sql /docker-entrypoint-initdb.d/

# 🚀 Create MySQL Initialization Script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "🔧 Starting MySQL initialization..."\n\
\n\
# Start MySQL in safe mode\n\
mysqld_safe --user=mysql --datadir=/var/lib/mysql &\n\
MYSQL_PID=$!\n\
\n\
# Wait for MySQL to start\n\
echo "⏳ Waiting for MySQL to start..."\n\
for i in {1..30}; do\n\
    if mysqladmin ping -h"localhost" --silent; then\n\
        echo "✅ MySQL is ready!"\n\
        break\n\
    fi\n\
    echo "   Attempt $i/30..."\n\
    sleep 2\n\
done\n\
\n\
# Check if MySQL is running\n\
if ! mysqladmin ping -h"localhost" --silent; then\n\
    echo "❌ Failed to start MySQL"\n\
    exit 1\n\
fi\n\
\n\
echo "🔐 Setting up root password and security..."\n\
mysql -e "ALTER USER '\''root'\''@'\''localhost'\'' IDENTIFIED BY '\''${MYSQL_ROOT_PASSWORD}'\'';" || true\n\
mysql -e "DELETE FROM mysql.user WHERE User='\'''\'';" || true\n\
mysql -e "DELETE FROM mysql.user WHERE User='\''root'\'' AND Host NOT IN ('\''localhost'\'', '\''127.0.0.1'\'', '\''::1'\'');" || true\n\
mysql -e "DROP DATABASE IF EXISTS test;" || true\n\
mysql -e "DELETE FROM mysql.db WHERE Db='\''test'\'' OR Db='\''test\\_%'\'' ;" || true\n\
mysql -e "FLUSH PRIVILEGES;" || true\n\
\n\
echo "👤 Creating database and user..."\n\
mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"\n\
mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "CREATE USER IF NOT EXISTS '\''${MYSQL_USER}'\''@'\''%'\'' IDENTIFIED BY '\''${MYSQL_PASSWORD}'\'';"\n\
mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '\''${MYSQL_USER}'\''@'\''%'\'';"\n\
mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON *.* TO '\''${MYSQL_USER}'\''@'\''%'\'' WITH GRANT OPTION;"\n\
mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "FLUSH PRIVILEGES;"\n\
\n\
echo "📂 Restoring backup file..."\n\
if [ -f "/docker-entrypoint-initdb.d/spiritual_backup.sql" ]; then\n\
    echo "   Found spiritual_backup.sql, importing..."\n\
    mysql -uroot -p${MYSQL_ROOT_PASSWORD} ${MYSQL_DATABASE} < /docker-entrypoint-initdb.d/spiritual_backup.sql\n\
    echo "   ✅ Backup restored successfully!"\n\
else\n\
    echo "   ⚠️ No backup file found, skipping..."\n\
fi\n\
\n\
echo "🎉 MySQL initialization completed!"\n\
echo "📊 Database Status:"\n\
mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "SHOW DATABASES;"\n\
echo "👥 Users:"\n\
mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "SELECT User, Host FROM mysql.user;"\n\
\n\
# Stop the background MySQL process\n\
mysqladmin -uroot -p${MYSQL_ROOT_PASSWORD} shutdown\n\
wait $MYSQL_PID\n\
\n\
echo "🏁 Initialization script completed!"\n' > /usr/local/bin/mysql-init.sh && \
    chmod +x /usr/local/bin/mysql-init.sh

# 🔄 Create Supervisor Configuration
RUN echo '[supervisord]\n\
nodaemon=true\n\
user=root\n\
logfile=/var/log/supervisor/supervisord.log\n\
pidfile=/var/run/supervisord.pid\n\
\n\
[program:mysql]\n\
command=mysqld --user=mysql --console\n\
user=mysql\n\
autorestart=true\n\
stdout_logfile=/var/log/mysql/mysql.log\n\
stderr_logfile=/var/log/mysql/mysql-error.log\n\
environment=MYSQL_ROOT_PASSWORD="%(ENV_MYSQL_ROOT_PASSWORD)s"\n' > /etc/supervisor/conf.d/mysql.conf

# 🚀 Create Startup Script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "🔱 Spiritual MySQL Server Starting..."\n\
echo "📅 Date: $(date)"\n\
echo "🏗️ Ubuntu: $(lsb_release -d | cut -f2)"\n\
echo "🗄️ MySQL: $(mysqld --version | head -1)"\n\
echo "💾 Data Directory: /var/lib/mysql"\n\
echo "🔧 Config: /etc/mysql/mysql.conf.d/custom.cnf"\n\
echo "=" * 50\n\
\n\
# Check if MySQL data directory is initialized\n\
if [ ! -d "/var/lib/mysql/mysql" ]; then\n\
    echo "🔧 First run detected, initializing MySQL..."\n\
    /usr/local/bin/mysql-init.sh\n\
else\n\
    echo "✅ MySQL data directory already initialized"\n\
fi\n\
\n\
echo "🚀 Starting MySQL server with supervisor..."\n\
exec /usr/bin/supervisord -c /etc/supervisor/supervisord.conf\n' > /usr/local/bin/docker-entrypoint.sh && \
    chmod +x /usr/local/bin/docker-entrypoint.sh

# 🫀 Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD mysqladmin ping -h"localhost" -uroot -p${MYSQL_ROOT_PASSWORD} --silent || exit 1

# 🚪 Expose MySQL Port
EXPOSE 3306

# 📊 Add useful aliases and info script
RUN echo 'alias ll="ls -la"\n\
alias mysql-status="mysqladmin -uroot -p${MYSQL_ROOT_PASSWORD} status"\n\
alias mysql-logs="tail -f /var/log/mysql/error.log"\n\
alias mysql-connect="mysql -uroot -p${MYSQL_ROOT_PASSWORD}"\n\
\n\
# MySQL Info Script\n\
mysql-info() {\n\
    echo "🗄️ MySQL Server Information:"\n\
    echo "   Root Password: ${MYSQL_ROOT_PASSWORD}"\n\
    echo "   Database: ${MYSQL_DATABASE}"\n\
    echo "   User: ${MYSQL_USER}"\n\
    echo "   Password: ${MYSQL_PASSWORD}"\n\
    echo "   Port: 3306"\n\
    echo "   Data Dir: /var/lib/mysql"\n\
    echo "   Config: /etc/mysql/mysql.conf.d/custom.cnf"\n\
    echo "   Logs: /var/log/mysql/"\n\
}\n' >> /root/.bashrc

# 🎯 Default Command
CMD ["/usr/local/bin/docker-entrypoint.sh"]
