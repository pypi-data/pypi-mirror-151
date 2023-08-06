# 轻量级权限管理工具：grantme || Lightweight access management tool: grantme

`grantme`是一个用python写的轻量级机器访问管理命令行工具。它可以授权用户一定时限内的共享访问权限（如，用于debug）和独占访问权限（如，用于性能测试），从而共享同一台机器的用户可以协调机器使用。它是非强制、纯建议性的因为它不能放置恶意用户无视访问权限授权地使用机器。

`grantme` is a lightweight machine access management CLI tool written in Python.
It can grant timed *shared access* (e.g., for debugging) and *exclusive access* (e.g., for performance evaluation) to individual users so that when users of shared machines can coordinate their usage.
It is noncompulsory and purely advisory because it cannot prevent malicious users from ignoring the access granted.

---

- [使用方式 || Usage](#使用方式--usage)
  - [规则 || Rules](#规则--rules)
  - [返回值 || Return values](#返回值--return-values)
  - [依赖 || Requirements](#依赖--requirements)
  - [安装与卸载 || Installation and uninstallation](#安装与卸载--installation-and-uninstallation)
- [参与开发 || Contribute](#参与开发--contribute)
  - [测试 || Testing](#测试--testing)

## 使用方式 || Usage

![overview](screenshots/all-in-one.png)

### 规则 || Rules

1. 当未授权任何访问权限时，用户可任意获取共享或独占全县。

   When no access is granted, users can require either shared or exclusive access.

2. 当已授予共享访问时，未授权用户可获取共享权限。若仅一位用户被授予共享权限，该用户可升级其为独占权限。

   When some shared access is granted, other users can require additional shared access.
   When there is only one user granted with shared access, that user can upgrade his/her access to be exclusive.

3. 当已授予独占访问时，未授权用户不可获取任何权限。

   When exclusive access is granted, other users cannot require any access.

4. 权限在过期后自动失效。已授予权限的用户可提前放弃或延长所持有权限。

   Grated access expires after given duration.
   Users with granted access can early revoke or prolong their access.

### 返回值 || Return values

`grantme`根据操作结果返回相应值。

`grantme` returns values according to operation results.

- 0：成功 || Success
- 6：升级权限失败 || Failed to upgrade access
- 7：获取权限失败 || Failed to obtain access
- 255：其他错误 || Other errors

这些返回值可于集成`grantme`于其他脚本（如，自动化测试）。

These return values can be used for integrating `grantme` into other scripts (e.g., automatic testing).

```shell
#!/bin/bash

./grantme --mode exclusive --duration 1h
if [ $? -ne 0 ]
then
    echo "I can't get the lock, cry cry."
    exit 1
fi

# do work

./grantme --revoke
```

### 依赖 || Requirements

`grantme`要求Python 3.7级以上版本。用户登陆是自动打印授权状态功能需要Ubuntu Linux发行版。

`grantme` requires Python 3.7+.
Automatically printing access status upon user login requires Ubuntu Linux distribution.

### 安装与卸载 || Installation and uninstallation

安装并初始化：

To install and initialize:

```shell
pip3 install grantme
grantme --init  # 可能需要sudo权限 || potentially requires sudo privilege
```

`grantme --init`会创建`/var/lib/grantme`目录，并在Ubuntu Linux发行版下在`/etc/update-motd.d`生成`<NN>-grantme-status`（`<NN>`数字，具体值由机器状态决定）脚本文件用于用户登录时打印授权状态。卸载时需手动删除：

`grantme --init` creates `/var/lib/grantme` directory，and under Ubuntu Linux distribution it creates `<NN>-grantme-status` (`<NN>` are numbers, whose exact values depend on the machines) script file under `/etc/update-motd.d` directory for automatically printing access status upon user login.
To uninstall, you need to manually remove them:

```shell
# 可能需要sudo权限 || potentially requires sudo privilege
rm -r /var/lib/grantme
rm /etc/update-motd.d/<NN>-grantme-status  # 将<NN>替换为具体数值 || replace <NN> with the actual numbers
```

## 参与开发 || Contribute

目前，`grantme`由个人维护。欢迎用户提交缺陷报告和Pull Request。

Currently, `grantme` is maintained by an individual.
Bug reports and pull requests are welcomed.

### 测试 || Testing

在项目根目录下执行以下命令以运行测试。

Execute the following command in the project's root directory to run tests.

```shell
python -m unittest discover
```

增加新功能、修补漏洞后请在`tests`目录下增加或修改相应测试。在所有测试通过后提交Pull Request。

Please add or modify test cases under the `tests` directory when adding new features or fixing bugs.
Make sure all tests have passed before submitting pull requests.
