#!/usr/bin/env python3
import os
import re
from datetime import datetime
import shutil

def create_default_config():
    return '''server
{
    listen 80;
    server_name _;
    index index.html;
    root /www/server/nginx/html;
}
'''

def create_domain_config(domain, php_version, root_path, has_rewrite):
    config = f'''server {{
    listen 80;
    server_name {domain};
    
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options SAMEORIGIN;
    
    root {root_path};
    index index.php index.html index.htm default.php default.htm default.html;
    
    location / {{
        try_files $uri $uri/ /index.php$is_args$args;
    }}

    location /.well-known {{
        root /www/wwwroot/{domain};
        try_files $uri $uri/ =404;
    }}
    
    location ~ \.php$ {{
        try_files $uri =404;
        include enable-php-{php_version}.conf;
    }}

    location ~ ^/(\.user.ini|\.htaccess|\.git|\.env|\.svn|\.project|LICENSE|README.md) {{
        return 404;
    }}
    
    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$ {{
        expires      30d;
        error_log /dev/null;
        access_log /dev/null;
    }}
    
    location ~ .*\.(js|css)?$ {{
        expires      12h;
        error_log /dev/null;
        access_log /dev/null;
    }}
    '''

    if has_rewrite:
        config += f'''
    include /www/server/panel/vhost/rewrite/{domain}.conf;
    '''
    
    config += f'''
    error_page 404 /404.html;
    error_page 502 /502.html;
    
    access_log  /www/wwwlogs/{domain}.log;
    error_log  /www/wwwlogs/{domain}.error.log;
}}
'''
    return config

def backup_config(file_path):
    """Create backup of the original config file"""
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    return backup_path

def fix_domain_config(config_path):
    """Fix configuration for a specific domain"""
    try:
        # Extract domain name from filename
        domain = os.path.basename(config_path).replace('.conf', '')
        
        # Read original config
        with open(config_path, 'r') as f:
            content = f.read()
            
        # Extract PHP version
        php_version = '74'  # default
        if 'enable-php-' in content:
            php_match = re.search(r'enable-php-(\d+)\.conf', content)
            if php_match:
                php_version = php_match.group(1)
        
        # Extract root path
        root_path = '/www/wwwroot/' + domain
        root_match = re.search(r'root\s+([^;]+);', content)
        if root_match:
            root_path = root_match.group(1).strip()
        
        # Check if rewrite file exists
        rewrite_path = f"/www/server/panel/vhost/rewrite/{domain}.conf"
        has_rewrite = os.path.exists(rewrite_path)
        
        # Create backup
        backup_path = backup_config(config_path)
        
        # Generate and write new config
        new_config = create_domain_config(domain, php_version, root_path, has_rewrite)
        with open(config_path, 'w') as f:
            f.write(new_config)
            
        return True, f"Fixed. Backup: {backup_path}"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def fix_default_config(config_path):
    """Fix the default configuration file"""
    try:
        # Create backup
        backup_path = backup_config(config_path)
        
        # Write new default config
        with open(config_path, 'w') as f:
            f.write(create_default_config())
            
        return True, f"Default config fixed. Backup: {backup_path}"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    nginx_dir = '/www/server/panel/vhost/nginx'
    
    if not os.path.exists(nginx_dir):
        print(f"Error: Directory {nginx_dir} not found!")
        return
    
    print("Starting Nginx configuration fix...")
    results = []
    
    # Process all .conf files
    for filename in os.listdir(nginx_dir):
        if not filename.endswith('.conf'):
            continue
            
        filepath = os.path.join(nginx_dir, filename)
        print(f"\nProcessing: {filename}")
        
        # Handle default config differently
        if filename == '0.default.conf':
            success, message = fix_default_config(filepath)
        else:
            success, message = fix_domain_config(filepath)
            
        results.append({
            'file': filename,
            'success': success,
            'message': message
        })
    
    # Print summary
    print("\nSummary:")
    print("=" * 50)
    for result in results:
        status = "✓" if result['success'] else "✗"
        print(f"{status} {result['file']}")
        print(f"  {result['message']}")
    
    print("\nNext steps:")
    print("1. Verify configurations: nginx -t")
    print("2. If verification successful, restart Nginx:")
    print("   - Via aaPanel web interface, or")
    print("   - Run: /etc/init.d/nginx restart")

if __name__ == "__main__":
    main()