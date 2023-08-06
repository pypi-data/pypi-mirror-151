# Personal Tools

写这个个人仓库的目的是为自己的代码提供一些可以直接调用的常用的东西。

当前一个需求是以邮件/QQ消息（需要结合服务器部署的QQrobot来做，比较烦）的形式来实现远端跑代码时候的自动化提醒，就不需要我自己一个个的去check。

## 使用

查看当前有哪些写好的文件：

```python
import lcytools.help
lcytools.help.fileList()
```

# code

## qqmessage

这是个很有意思的工具接口，通过这个接口，只要添加QQ 1794957373为好友之后调用函数就可以直接获得推送的消息。

一个样例：

```python
import lcytools.qqmessage as qqPush
qqPush.lcy_qqmessage_help()
qqPush.lcy_qqmessage(qq="1157***882就是你的QQ",message = "来一条测试消息~")
```

然后你的QQ就可以接收到相应的消息推送。

<img src="https://luochengyu.oss-cn-beijing.aliyuncs.com/img/image-20220519151316793.png" alt="image-20220519151316793" style="zoom:80%;" />

这比较有利于在远端跑程序的时候可以直接调这个函数，通过QQ接收进度推送。不需要不停的连接到远端，在手机上就可以便捷的查看进度了~

## emailMe

给自己发送文件，调用方式：

```python
import lcytools.emailMe as eM
eM.lcy_email(["11158340882@qq.com"],key = "这是一个防止SMTP密码丢掉的自己密码hh")
```


## help

提供一个查询接口，发送一下当前有哪些东西