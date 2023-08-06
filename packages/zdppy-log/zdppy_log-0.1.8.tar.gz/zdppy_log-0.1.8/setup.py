# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_log', 'zdppy_log.colorama', 'zdppy_log.loguru']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zdppy-log',
    'version': '0.1.8',
    'description': 'Python中用于记录日志的工具库，简单而优美，灵活而强大',
    'long_description': '# zdppy_log\n\npython的日志库\n\n项目地址：https://github.com/zhangdapeng520/zdppy_log\n\n安装方式\n\n```shell script\npip install zdppy_log\n```\n\n使用方式\n\n```python\nfrom zdppy_log import Log\n\nlog1 = Log("logs/zdppy/zdppy_log1.log")\n\n\n@log1.catch()\ndef my_function(x, y, z):\n    # An error? It\'s caught anyway!\n    return 1 / (x + y + z)\n\n\nmy_function(0, 0, 0)\n# logger.add("out.log", backtrace=True, diagnose=True)  # Caution, may leak sensitive data in prod\n\nlog2 = Log("logs/zdppy/zdppy_log2.log")\nlog2.debug("log2日志")\nlog2.info("log2日志")\nlog2.warning("log2日志")\nlog2.error("log2日志")\nlog2.critical("log2日志")\n\nlog3 = Log("logs/zdppy/zdppy_log3.log", debug=False)\nlog3.debug("log3日志")\nlog3.info("log3日志")\nlog3.warning("log3日志")\nlog3.error("log3日志")\nlog3.critical("log3日志")\n```\n\n## 版本历史\n\n- v0.1.2 2022/2/19  增加debug模式；默认json日志为False\n- v0.1.3 2022/3/4   增加记录日志文件，日志方法，日志行数的功能\n- v0.1.4 2022/3/5   移除第三方依赖\n- v0.1.5 2022/3/5   增加控制是否开启日志全路径的开关量\n- v0.1.6 2022/3/16  增加只输出到控制台的开关量及底层代码优化\n- v0.1.7 2022/3/16  BUG修复及完善使用文档\n- v0.1.8 2022/5/17  优化：底层代码结构优化\n\n## 使用案例\n\n### 案例1：基本使用\n\n```python\nfrom zdppy_log import Log\n\nlog1 = Log("logs/zdppy/zdppy_log1.log")\n\nlog2 = Log("logs/zdppy/zdppy_log2.log")\nlog2.debug("log2日志")\nlog2.info("log2日志")\nlog2.warning("log2日志")\nlog2.error("log2日志")\nlog2.critical("log2日志")\n\nlog3 = Log("logs/zdppy/zdppy_log3.log", debug=False)\nlog3.debug("log3日志")\nlog3.info("log3日志")\nlog3.warning("log3日志")\nlog3.error("log3日志")\nlog3.critical("log3日志")\n```\n\n### 案例2：捕获方法错误\n\n```python\nfrom zdppy_log import Log\n\nlog1 = Log("logs/zdppy/zdppy_log1.log")\n\n\n@log1.catch()\ndef my_function(x, y, z):\n    return 1 / (x + y + z)\n\n\nmy_function(0, 0, 0)\n```\n\n### 案例3：只往控制台输出\n\n```python\nfrom zdppy_log import Log\n\n# 记录所有级别的日志到控制台\nlog1 = Log(debug=True, is_only_console=True)\nlog1.debug("log1 debug")\nlog1.info("log1 info")\nlog1.warning("log1 warning")\nlog1.error("log1 error")\nlog1.critical("log1 critical")\n\n# 记录info以上级别的日志到控制台\nlog2 = Log(debug=False, is_only_console=True)\nlog2.debug("log2 debug")\nlog2.info("log2 info")\nlog2.warning("log2 warning")\nlog2.error("log2 error")\nlog2.critical("log2 critical")\n\n# 记录error以上级别的日志到控制台\nlog3 = Log(debug=False, level="ERROR", is_only_console=True)\nlog3.debug("log3 debug")\nlog3.info("log3 info")\nlog3.warning("log3 warning")\nlog3.error("log3 error")\nlog3.critical("log3 critical")\n```\n\n### 案例4：同时输出到控制台和日志文件\n\n```python\nfrom zdppy_log import Log\n\n# 记录info级别的日志，并将所有级别日志输出到控制台\nlog1 = Log(debug=True)\nlog1.debug("log1 debug")\nlog1.info("log1 info")\nlog1.warning("log1 warning")\nlog1.error("log1 error")\nlog1.critical("log1 critical")\n\n# 记录info以上级别的日志，不输出到控制台\nlog2 = Log(debug=False)\nlog2.debug("log2 debug")\nlog2.info("log2 info")\nlog2.warning("log2 warning")\nlog2.error("log2 error")\nlog2.critical("log2 critical")\n\n# 记录error以上级别的日志不输出到控制台\nlog3 = Log(debug=False, level="ERROR")\nlog3.debug("log3 debug")\nlog3.info("log3 info")\nlog3.warning("log3 warning")\nlog3.error("log3 error")\nlog3.critical("log3 critical")\n```\n\n### 案例5：日志序列化为JSON\n\n```python\nfrom zdppy_log import Log\n\n# 记录info级别的日志，并将所有级别日志输出到控制台\nlog1 = Log(serialize=True, debug=True)\nlog1.debug("log1 debug")\nlog1.info("log1 info")\nlog1.warning("log1 warning")\nlog1.error("log1 error")\nlog1.critical("log1 critical")\n\n# 记录info以上级别的日志，不输出到控制台\nlog2 = Log(serialize=True, debug=False)\nlog2.debug("log2 debug")\nlog2.info("log2 info")\nlog2.warning("log2 warning")\nlog2.error("log2 error")\nlog2.critical("log2 critical")\n```',
    'author': 'zhangdapeng',
    'author_email': 'pygosuperman@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zhangdapeng520/zdppy_log',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
