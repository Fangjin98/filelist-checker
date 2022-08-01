# NAS Monitor

This script is used to monitor file changes in the specified directory of the NAS and will notify users at each friday.

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

Then execute `sudo nohup python3 monitor.py --dir /volume1/share/Movies  >log.txt 2>&1 &`.

To stop the service, run `ps aux | grep monitor` to obtain the pid. Then, run `pkill -9 pid`.
