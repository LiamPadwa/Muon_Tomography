# RCLONE google drive - config

1. Startup

    ```bash
    cd path\to\rclone.exe
    rclone config
    ```

2. New Remote
new remote -> n
name -> Jerusalem (Does not matter)
GoogleDrive -> 20 (need to be verified)
Default (enter) X2
Full Access -> 1
Default (enter)
Edit Advanced Config -> n (No)
Use Web Browser -> y (Yes)

3. Sign in to Google account
Opens browser to sign in to jerusalemdetector@gmail.com
should get Success message

Configure as a shared drive -> y 
Keep Jerusalem Remote -> y

Done!!

Quit -> q

rclone commands:
rclone <command> Jerusalem:

1. lsd - list directories in top level
2. ls - all files in your drive
3. copy path_to_file_on_machine Jerusalem:path_on_google_drive





