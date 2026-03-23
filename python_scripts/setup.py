"""Setup script for the Beer Computer project.

Generates executable files for Mac/Windows/Linux users to run the scripts in the repository."""
import os
import platform

def generate_mac_command_files():
    """Generate .command files for Mac users to easily run the scripts in the repository."""
    # Make sure the mac_scripts directory exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mac_os_dir = os.path.join(base_dir, '..', 'mac_scripts')
    os.makedirs(mac_os_dir, exist_ok=True)

    # Get the absolute path to the repository root
    repo_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(repo_dir)

    # Generate the run_scanner.command file
    command_filename = os.path.join(mac_os_dir, "scanner.command")
    command_content = f"""
    #!/bin/bash
    cd "{parent_dir}"
    python python_scripts/scanner.py
    """

    command_path = os.path.join(repo_dir, command_filename)

    with open(command_path, "w", encoding="utf-8-sig") as f:
        f.write(command_content)

    os.chmod(command_path, 0o755)

    # Generate the run_find_prices.command file
    command_filename = os.path.join(mac_os_dir, "find_prices.command")
    command_content = f"""
    #!/bin/bash
    cd "{parent_dir}"
    python python_scripts/find_prices_divide_losses_equally.py
    read -p "Press Enter to close..."
    """

    command_path = os.path.join(repo_dir, command_filename)

    with open(command_path, "w", encoding="utf-8-sig") as f:
        f.write(command_content)

    os.chmod(command_path, 0o755)

    # Generate the generate_qr_codes.command file
    command_filename = os.path.join(mac_os_dir, "generate_qr_codes.command")
    command_content = f"""
    #!/bin/bash
    cd "{parent_dir}"
    python python_scripts/generate_qr_codes.py
    read -p "Press Enter to close..."
    """

    command_path = os.path.join(repo_dir, command_filename)

    with open(command_path, "w", encoding="utf-8-sig") as f:
        f.write(command_content)

    os.chmod(command_path, 0o755)

    # Generate the generate_barcodes.command file
    command_filename = os.path.join(mac_os_dir, "generate_barcodes.command")
    command_content = f"""
    #!/bin/bash
    cd "{parent_dir}"
    python python_scripts/generate_barcodes.py
    read -p "Press Enter to close..."
    """

    command_path = os.path.join(repo_dir, command_filename)

    with open(command_path, "w", encoding="utf-8-sig") as f:
        f.write(command_content)

    os.chmod(command_path, 0o755)

def generate_windows_bat_files():
    """Generate .bat files for Windows users to easily run the scripts in the repository."""
    # Make sure the windows_scripts directory exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    windows_dir = os.path.join(base_dir, '..', 'windows_scripts')
    os.makedirs(windows_dir, exist_ok=True)

    # Get the absolute path to the repository root
    repo_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(repo_dir)

    # Generate the run_scanner.bat file
    bat_filename = os.path.join(windows_dir, "run_scanner.bat")
    repo_dir = os.path.abspath(os.path.dirname(__file__))

    bat_content = f"""
    @echo off
    cd "{parent_dir}"
    python python_scripts/scanner.py
    """

    bat_path = os.path.join(repo_dir, bat_filename)

    with open(bat_path, "w", encoding="utf-8-sig") as f:
        f.write(bat_content)

    os.chmod(bat_path, 0o755)

    # Generate the run_find_prices.bat file
    bat_filename = os.path.join(windows_dir, "run_find_prices.bat")
    bat_content = f"""
    @echo off
    cd "{parent_dir}"
    python python_scripts/find_prices_divide_losses_equally.py
    """

    bat_path = os.path.join(repo_dir, bat_filename)

    with open(bat_path, "w", encoding="utf-8-sig") as f:
        f.write(bat_content)

    os.chmod(bat_path, 0o755)

    # Generate the generate_qr_codes.bat file
    bat_filename = os.path.join(windows_dir, "generate_qr_codes.bat")
    bat_content = f"""
    @echo off
    cd "{parent_dir}"
    python python_scripts/generate_qr_codes.py
    """

    bat_path = os.path.join(repo_dir, bat_filename)

    with open(bat_path, "w", encoding="utf-8-sig") as f:
        f.write(bat_content)

    os.chmod(bat_path, 0o755)

    # Generate the generate_barcodes.bat file
    bat_filename = os.path.join(windows_dir, "generate_barcodes.bat")
    bat_content = f"""
    @echo off
    cd "{parent_dir}"
    python python_scripts/generate_barcodes.py
    pause
    """

    bat_path = os.path.join(repo_dir, bat_filename)

    with open(bat_path, "w", encoding="utf-8-sig") as f:
        f.write(bat_content)

    os.chmod(bat_path, 0o755)

def generate_linux_sh_files():
    """Generate .sh files for Linux users to easily run the scripts in the repository."""
    # Make sure the linux_scripts directory exists
    base_dir = os.path.dirname(os.path.abspath(__file__))
    linux_dir = os.path.join(base_dir, '..', 'linux_scripts')
    os.makedirs(linux_dir, exist_ok=True)

    # Get the absolute path to the repository root
    repo_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.dirname(repo_dir)

    # Generate the run_scanner.sh file
    sh_filename = os.path.join(linux_dir, "run_scanner.sh")
    sh_content = f"""
    cd "{parent_dir}"
    python python_scripts/scanner.py
    """

    sh_path = os.path.join(repo_dir, sh_filename)

    with open(sh_path, "w", encoding="utf-8-sig") as f:
        f.write(sh_content)

    os.chmod(sh_path, 0o755)

    # Generate the run_find_prices.sh file
    sh_filename = os.path.join(linux_dir, "run_find_prices.sh")
    sh_content = f"""
    cd "{parent_dir}"
    python python_scripts/find_prices_divide_losses_equally.py
    """

    sh_path = os.path.join(repo_dir, sh_filename)

    with open(sh_path, "w", encoding="utf-8-sig") as f:
        f.write(sh_content)

    os.chmod(sh_path, 0o755)

    # Generate the generate_qr_codes.sh file
    sh_filename = os.path.join(linux_dir, "generate_qr_codes.sh")
    sh_content = f"""
    cd "{parent_dir}"
    python python_scripts/generate_qr_codes.py
    """

    sh_path = os.path.join(repo_dir, sh_filename)

    with open(sh_path, "w", encoding="utf-8-sig") as f:
        f.write(sh_content)

    os.chmod(sh_path, 0o755)

    # Generate the generate_barcodes.sh file
    sh_filename = os.path.join(linux_dir, "generate_barcodes.sh")
    sh_content = f"""
    cd "{parent_dir}"
    python python_scripts/generate_barcodes.py
    """

    sh_path = os.path.join(repo_dir, sh_filename)

    with open(sh_path, "w", encoding="utf-8-sig") as f:
        f.write(sh_content)

    os.chmod(sh_path, 0o755)

def main():
    """Main function."""    
    system = platform.system()

    if system == "Darwin":
        generate_mac_command_files()
    elif system == "Windows":
        generate_windows_bat_files()
    elif system == 'Linux':
        generate_linux_sh_files()

if __name__ == "__main__":
    main()
