
# SFTP Connection Setup Between Two Windows Machines

This guide walks you through setting up an SFTP connection between two **Windows machines** (a *host* and a *remote*) using **OpenSSH**. It enables secure file transfers using public-key authentication.

---

## Instructions

### 1. Enable OpenSSH (Host & Remote)

**Done on: Both Machines**

1. Press `Win + I` to open **Settings**
2. Go to **Apps > Optional Features**
3. Click **Add a feature**
4. Search for **OpenSSH Client** and **OpenSSH Server**
   - Install both on each machine

5. Start the SSH server (on **remote** only):

   ```powershell
   Start-Service sshd
   Set-Service -Name sshd -StartupType 'Automatic'
   ```

---

### 2. Create SSH Key (on Host)

**Done on: Host**

In PowerShell or CMD:

```bash
ssh-keygen
```

- When prompted for a file location, just press **Enter** (uses default: `C:\Users\<YourName>\.ssh\id_rsa`)
- Press **Enter** twice when asked for a passphrase (leave empty for passwordless login)

---

### 3. Find `user@remote_ip`

Done on: **Remote**

On the **remote machine**, find the IP address:

```cmd
ipconfig
```

Look under the correct adapter (e.g. Wi-Fi). Example result:

```cmd
IPv4 Address. . . . . . . . . . . : 172.30.102.138
```

Find the current username:

```cmd
echo %USERNAME%
```

So the remote user@host will be something like: `Lab_PC@172.30.102.138`

---

### 4. Transfer the Public Key to Remote

**Done on: Host**

Use the following command to copy your public key to the remote machine:

```bash
scp C:\Users\<YourName>\.ssh\id_rsa.pub john@192.168.1.24:C:\Users\john\.ssh\authorized_keys
```

> If `authorized_keys` doesn’t exist, it will be created.

Alternatively, connect with `ssh`, create the `.ssh` folder if missing, and copy manually:

```bash
ssh john@192.168.1.24
mkdir %USERPROFILE%\.ssh
notepad %USERPROFILE%\.ssh\authorized_keys
```

Paste the public key content into the file and save.

---

### 5. Enable SSH Login with Key (Remote)

**Done on: Remote**

Make sure permissions are correct on the remote machine:

```powershell
icacls %USERPROFILE%\.ssh\authorized_keys /inheritance:r /grant:r %USERNAME%:F
```

Restart the SSH service:

```powershell
Restart-Service sshd
```

---

## File Transfer Commands (From Host)

### Send a file from Host to Remote

```sftp
put C:\path\to\local\file.txt C:\Users\<username>\Desktop\
```

### Retrieve a file from Remote to Host

```sftp
get C:\Users\john\Desktop\file.txt C:\Users\YourName\Downloads\
```

---

## 🔧 Useful SFTP Commands

| Command             | Description                            |
|---------------------|----------------------------------------|
| `lpwd`              | Show local working directory           |
| `pwd`               | Show remote working directory          |
| `lcd <path>`        | Change local working directory         |
| `cd <path>`         | Change remote working directory        |
| `ls` / `dir`        | List files on remote                   |
| `put <src> <dest>`  | Upload file to remote                  |
| `get <src> <dest>`  | Download file from remote              |
| `exit` / `bye`      | Exit the SFTP session                  |

---

## Tips

- Ensure both firewalls allow SSH (port 22)
- You can test SSH before SFTP:  

  ```bash
  ssh john@192.168.1.24
  ```

---
