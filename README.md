# Canopy.io
Canopy.io is an umbrella tool designed to optimize security processes. It includes a variety of features such as scanning, network mapping, reporting, and even an attack feature for educational purposes only. Please note that it is illegal to hack into systems without permission, and the attack feature should be used in a controlled environment, preferably a virtual machine (VM) with Metasploit.

## Installation

To use Canopy.io, ensure you have the following dependencies installed:

- Python 3
- Make sure to download all necessary images for the full GUI experience

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/SnackAttacks/Canopy.io.git
cd Canopy.io
```

## Usage

To start Canopy.io, run the following command:

```bash
python3 start.py
```

The menu bar will help you navigate across all the different pages in Canopy.io.

### Features

- **Scan**: Use Pyshark or Nmap to perform network scans.
- **Attack**: For educational purposes, you can initiate a reverse shell exploit on port 21 (ensure you have the appropriate permissions and use a VM with Metasploit).
- **Reporting**: View past scans and save reports to your device.

**Instructions for Attack Feature**

Follow these steps to use the attack feature in Canopy.io:

**Step 1**: Set the target IP address
- In the first box, set the target designator using the word "target."
- In the second box, input the target IP address.

**Step 2**: Set the reverse shell IP address
- In the first box, set the reverse shell designator using the phrase "revshell_ip."
- In the second box, input your computer's IP address.

**Step 3**: Set the port for the attack (e.g., "21")
- In the first box, set the port designator using the word "port."
- In the second box, specify the port you want to attack (e.g., "21").

In the third box (with the module button):
- Set the exploit using the word "use" in the first box (no space after "use").
- In the second box, input "Vsftpd," and then click "module" to set everything up.

Now, you can hit the exploit button to initiate the reverse shell connection.

In the first box with the "send" button next to it, you can type commands such as:
- `ifconfig`: To show that you've made the connection to the target machine.
- `whoami`: To demonstrate that you've gained root privilege on the target machine.
- `ls`: To list the file system and everything you have access to.

### Credits

- Antonio Spaccavento (antonio.spaccavento95@gmail.com) - Co-writer of Canopy.io

### Contact

For support or questions, please reach out to Kathryn Rasmussen at kathryn.g.rasmussen@gmail.com.

---

**Note**: Canopy.io is intended for educational purposes only. Always ensure you have the appropriate permissions before using any of its features in a real-world scenario.
```
