"""Setup script for the Beer Computer project.

This script generates .command files for Mac users to easily run the scripts in the repository."""
import os
import platform

def generate_mac_command_files():
    """Generate .command files for Mac users to easily run the scripts in the repository."""
    mac_os_dir = 'mac_scripts'

    # Generate the run_scanner.command file
    os.makedirs(mac_os_dir, exist_ok=True)
    command_filename = os.path.join(mac_os_dir, "scanner.command")
    repo_dir = os.path.abspath(os.path.dirname(__file__))

    command_content = f"""
    #!/bin/bash
    cd "{repo_dir}"
    python3 scanner.py
    """

    command_path = os.path.join(repo_dir, command_filename)

    with open(command_path, "w", encoding="utf-8") as f:
        f.write(command_content)

    os.chmod(command_path, 0o755)

    # Generate the run_find_prices.command file
    command_filename = os.path.join(mac_os_dir, "find_prices.command")
    command_content = f"""
    #!/bin/bash
    cd "{repo_dir}"
    python3 find_prices_divide_losses_equally.py
    read -p "Press Enter to close..."
    """

    command_path = os.path.join(repo_dir, command_filename)

    with open(command_path, "w", encoding="utf-8") as f:
        f.write(command_content)
    
    os.chmod(command_path, 0o755)

    # Generate the generate_qr_codes.command file
    command_filename = os.path.join(mac_os_dir, "generate_qr_codes.command")
    command_content = f"""
    #!/bin/bash
    cd "{repo_dir}"
    python3 generate_qr_codes.py
    read -p "Press Enter to close..."
    """

    command_path = os.path.join(repo_dir, command_filename)

    with open(command_path, "w", encoding="utf-8") as f:
        f.write(command_content)

    os.chmod(command_path, 0o755)

    # Generate the generate_barcodes.command file
    command_filename = os.path.join(mac_os_dir, "generate_barcodes.command")
    command_content = f"""
    #!/bin/bash
    cd "{repo_dir}"
    python3 generate_barcodes.py
    read -p "Press Enter to close..."
    """

    command_path = os.path.join(repo_dir, command_filename)

    with open(command_path, "w", encoding="utf-8") as f:
        f.write(command_content)

    os.chmod(command_path, 0o755)

def generate_windows_bat_files():
    """Generate .bat files for Windows users to easily run the scripts in the repository."""
    windows_dir = 'windows_scripts'
    
    # Generate the run_scanner.bat file
    os.makedirs(windows_dir, exist_ok=True)

    bat_filename = os.path.join(windows_dir, "run_scanner.bat")
    repo_dir = os.path.abspath(os.path.dirname(__file__))
    
    bat_content = f"""
    @echo off
    cd "{repo_dir}"
    python3 scanner.py
    """

    bat_path = os.path.join(repo_dir, bat_filename)

    with open(bat_path, "w") as f:
        f.write(bat_content)
        
    os.chmod(bat_path, 0o755)
    
    # Generate the run_find_prices.bat file
    bat_filename = os.path.join(windows_dir, "run_find_prices.bat")
    bat_content = f"""
    @echo off
    cd "{repo_dir}"
    python3 find_prices_divide_losses_equally.py
    """

    bat_path = os.path.join(repo_dir, bat_filename)

    with open(bat_path, "w") as f:
        f.write(bat_content)
    
    os.chmod(bat_path, 0o755)

    # Generate the generate_qr_codes.bat file
    bat_filename = os.path.join(windows_dir, "generate_qr_codes.bat")
    bat_content = f"""
    @echo off
    cd "{repo_dir}"
    python3 generate_qr_codes.py
    """

    bat_path = os.path.join(repo_dir, bat_filename)

    with open(bat_path, "w") as f:
        f.write(bat_content)

    os.chmod(bat_path, 0o755)

    # Generate the generate_barcodes.bat file
    bat_filename = os.path.join(windows_dir, "generate_barcodes.bat")
    bat_content = f"""
    @echo off
    cd "{repo_dir}"
    python3 generate_barcodes.py
    pause
    """

    bat_path = os.path.join(repo_dir, bat_filename)

    with open(bat_path, "w") as f:
        f.write(bat_content)

    os.chmod(bat_path, 0o755)

def generate_linux_sh_files():
    """Generate .sh files for Linux users to easily run the scripts in the repository."""
    linux_dir = 'linux_scripts'
    
    # Generate the run_scanner.bat file
    os.makedirs(linux_dir, exist_ok=True)

    sh_filename = os.path.join(linux_dir, "run_scanner.sh")
    repo_dir = os.path.abspath(os.path.dirname(__file__))
    
    sh_content = f"""
    cd "{repo_dir}"
    python3 scanner.py
    """

    sh_path = os.path.join(repo_dir, sh_filename)

    with open(sh_path, "w") as f:
        f.write(sh_content)
        
    os.chmod(sh_path, 0o755)
    
    # Generate the run_find_prices.bat file
    sh_filename = os.path.join(linux_dir, "run_find_prices.sh")
    sh_content = f"""
    cd "{repo_dir}"
    python3 find_prices_divide_losses_equally.py
    """

    sh_path = os.path.join(repo_dir, sh_filename)

    with open(sh_path, "w") as f:
        f.write(sh_content)
    
    os.chmod(sh_path, 0o755)

    # Generate the generate_qr_codes.bat file
    sh_filename = os.path.join(linux_dir, "generate_qr_codes.sh")
    sh_content = f"""
    cd "{repo_dir}"
    python3 generate_qr_codes.py
    """

    sh_path = os.path.join(repo_dir, sh_filename)

    with open(sh_path, "w") as f:
        f.write(sh_content)

    os.chmod(sh_path, 0o755)

    # Generate the generate_barcodes.bat file
    sh_filename = os.path.join(linux_dir, "generate_barcodes.sh")
    sh_content = f"""
    cd "{repo_dir}"
    python3 generate_barcodes.py
    pause
    """

    sh_path = os.path.join(repo_dir, sh_filename)

    with open(sh_path, "w") as f:
        f.write(sh_content)

    os.chmod(sh_path, 0o755)

def main():
    """Main function."""    
    system = platform.system()
    if system == "MacOS":
        generate_mac_command_files()
    elif system == "Windows":
        generate_windows_bat_files()
    elif system == 'Linux':
        generate_linux_sh_files()

if __name__ == "__main__":
    main()
