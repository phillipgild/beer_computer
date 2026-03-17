"""Setup script for the Beer Computer project.

This script generates .command files for Mac users to easily run the scripts in the repository."""
import os

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


def main():
    """Main function."""
    # Generate the .command files for Mac users
    generate_mac_command_files()

if __name__ == "__main__":
    main()
