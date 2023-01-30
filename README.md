# File List Monitor

This script is used to check file changes in the specified directory and notify users. The file list will be saved as a json file.

## How to use

Create the config.json file as follow:

```json
{
    "usr" : "sending email",
    "password": "password",
    "receiver_list":[
        "xxx@mail.ustc.edu.cn",
        "xxx@mail.ustc.edu.cn",
        "xxx@mail.ustc.edu.cn"
    ]
}
```

Run `python3 monitor.py --dir /volume1/share/Movies`.
