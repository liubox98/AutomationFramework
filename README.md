# AutomationFramework
>##### 简介：这是一个基于Python，Poco以及Tidevice库实现的自动化测试框架😁
>##### 目的: 在版本发布阶段完成一些简单场景的自动化作业，达到快速校验
### 项目结构：

```markdown
AutomationFramework
├── config
│   ├── config.ini # IPA相关配置
│   └── path.py # 文件路径配置
├── package
│   └── *.ipa
├── script
│   ├── file1 # 测试用例
│   └── file2 # 函数封装
├── tools
│   ├── GmApi.py # GM函数封装
│   └── TestApi.py # 通用API
└── run.py # 程序执行入口
```
#### 最后说明：[WebDriverAgent](https://github.com/facebookarchive/WebDriverAgent) 是一个开源的 iOS 自动化测试框架，由 Facebook 开发和维护，用于在真机和模拟器上运行自动化测试。它是基于 XCUITest 框架构建的，可以与 Appium 和 Selenium 等测试框架集成使用, 感谢阿里团队开源项目[tidevice](https://github.com/alibaba/taobao-iphone-device) 提供了简单易用的命令行工具和 Python API，使得 iOS 设备的管理和自动化测试变得更加容易🤑