# 心灵终结 Mac 原版规则封装

《心灵终结 3.3.6》Mac 兼容封装的源码与构建工具。保留原版游戏规则，不含加钱、快速生产或随地建造修改。非官方项目。

本仓库只提供我们编写的启动器、封装和界面汉化脚本，不提供游戏本体、Mental Omega 资源、Wine 二进制或预装游戏的下载包。MIT 许可仅适用于本仓库自有代码，不覆盖第三方内容。

## 准备

- macOS 11+、Xcode Command Line Tools、Python 3。
- Apple 芯片运行 x86 Wine 需要 Rosetta 2。
- 自行准备《红警2／尤里的复仇》1.001 文件，以及官方 Mental Omega 3.3.0 基础包和 3.3.6 补丁，合并成独立游戏目录。
- 自行准备 macOS Wine app，布局为 Contents/Resources/wine/bin/wine。
- 可选：从官方下载页安装 3.3.6 简体中文包到游戏目录。

[官方安装说明](https://mentalomega.com/index.php?page=install) · [官方下载](https://mentalomega.com/index.php?page=download) · [Wine macOS 构建](https://github.com/Gcenx/macOS_Wine_builds)

## 构建

```sh
python3 scripts/build.py --game-dir /path/to/Game --engine-app '/path/to/Wine Devel.app' --output 'dist/Mental Omega.app'
```

使用干净的官方游戏文件，不要把有其他补丁的游戏目录作为输入。脚本清理本项目的作弊启动程序、生成地图、个人存档和对局记录，恢复标准启动程序和一万元默认资金；不会修复任意第三方对游戏数据文件的修改。

首次运行会创建独立数据目录 `~/Library/Application Support/MentalOmegaMacOriginal/`，初始化 Wine 并复制游戏文件，可能等待一两分钟。已有运行目录不会被覆盖；重新构建不会自动升级其中的游戏。不要删除该目录来升级，以免丢失存档。

## 可选的常用界面汉化

```sh
python3 -m pip install Pillow
python3 scripts/localize.py /path/to/Game
```

脚本使用 macOS 自带黑体生成中文字库，翻译常用菜单和遭遇战选项；不提供官方游戏内汉化资源，不翻译全部地图名。先备份游戏目录。脚本同时将主菜单中带英文的按钮图片替换为游戏自带的空白按钮底图，避免中英文叠字。

## 验证范围和限制

曾在 Apple M5 Pro、macOS 26 上完成首次初始化、启动器及对局运行测试。Intel Mac 和其他 macOS 版本尚未实机验证；最低系统标记不代表全部机型兼容。源码构建采用本地签名，未通过 Apple 开发者公证。

游戏显示兼容设置取决于提供的游戏目录。已验证过的一组设置是：游戏内 Windowed=False；cnc-ddraw windowed=true、renderer=gdi、maxfps=60、forcefps=true；Wine 启用原生 ddraw。原版生产速度、资金与建造限制保持不变。

不要提交游戏资源、个人运行目录、存档、令牌或崩溃转储。报告问题时请提供系统版本、芯片型号和去除个人路径后的错误信息。

## 第三方项目

Mental Omega / Mentalmeisters、EA / Westwood、Wine、MonoGame、cnc-ddraw 的名称和素材归各自权利人所有。本项目不代表这些项目，也不授予其游戏文件的再分发许可。
