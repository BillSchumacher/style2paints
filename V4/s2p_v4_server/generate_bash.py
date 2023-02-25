lines = [
    "screen -dmS \"server.80"
    + str(_)
    + "\" bash -c \'while : ;do python3 server.py 80"
    + str(_)
    + "; done;\'\n"
    for _ in range(50, 66)
]
with open('run.bash', 'wt') as f:
    f.writelines(lines)

lines = ["screen -S \"server.80"+str(_)+"\" -X quit\n" for _ in range(50, 66)]
with open('kill.bash', 'wt') as f:
    f.writelines(lines)

lines = [
    f"server 127.0.0.1:80{str(_)}"
    + " weight=4 max_fails=2 fail_timeout=600s;\n"
    for _ in range(50, 66)
]
with open('nginx.txt', 'wt') as f:
    f.writelines(lines)

lines = ["ufw allow 80/tcp\n"]

lines.extend(f"ufw allow 80{str(_)}" + "/tcp\n" for _ in range(50, 66))
with open('tcp.bash', 'wt') as f:
    f.writelines(lines)

#/etc/nginx/sites-available
#/var/log/nginx

