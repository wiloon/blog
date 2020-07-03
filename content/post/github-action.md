+++
author = "w1100n"
date = 2020-06-25T05:33:56Z
title = "github action"

+++
# Deploy to vm
      - name: Deploy to vm
        uses: easingthemes/ssh-deploy@v2.1.2
        env:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          ARGS: "-avz --delete"
          SOURCE: "public/"
          REMOTE_HOST: "192.168.0.xxx"
          REMOTE_PORT: 38785
          REMOTE_USER: "blog"
          TARGET: "/home/blog/public/"

secrets.SSH_PRIVATE_KEY
粘贴私钥时后面加一个换行，否则会报错，invalid format
