# ZhihuWeiboHotFilter-Selenium
根据自定义关键字，过滤知乎、微博的热榜中个人可能感兴趣的话题。<p>
目前仅支持Windows10系统、Chrome浏览器。<p>
包含邮件发送功能，有兴趣的朋友可以放到自己服务器上配置成定时任务。<p>
测试代码没有清理干净，先保留，方便以后改进。<p>
知乎和微博的热榜总数都只能扫描到44条，原因不明，暂时不作深究。<p>
作者：<a href="https://www.zhihu.com/people/nidaye2" target="_blank">尼尼尼@知乎</a>

**使用过程概述：**<p>
下载解压后运行exe -> 修改自定义关键词 -> 运行main.exe <p>

**下载地址：**<p>
百度网盘: https://pan.baidu.com/s/1cYQtcfRqW_IsrOBNch4Zew?pwd=6666  <p>
Github: https://github.com/ninini1990/ZhihuWeiboHotFilter-Selenium <p>

**运行环境需求：**<p>
Windows 10 (64位), Chrome浏览器 (v104 或其他较高版本, 64位）<p>
暂时未对其它环境/版本进行详细测试。<p>

**问题反馈：**<p>
知乎私信，或发送邮件到 ninini19900319@gmail.com <p>
 
---
<h2>使用提示</h2> <p>

**安全性：**<p>
1. 此工具只发布于上述 Github和百度网盘指定的两个分享链接。不要从其它来源下载。<p>
2. 此工具不会获取、保存、发送你的用户密码。<p>
3. 如果仍然担心安全性，可从Github下载源码。在本地安装Python环境，并执行脚本。入口是main.py<p>

**使用风险提示：**<p>
请勿过度频繁使用，防止被网站识别为爬虫。<p>

**开源协议:**<p>
使用GPL3协议，请保持代码开源及遵守GPL3其他规则。<p>

---
<h2>安装及使用详细说明</h2><p>

1. 从Github或百度网盘指定地址，下载最新版本的zip压缩包。<p>  
2. 解压到任意目录。路径中不要包含中文。<p>

![image](https://user-images.githubusercontent.com/112439804/196353028-b4b87b9e-0c8a-4298-8922-ac15892c9c10.png) <p>

3. 修改config.json中的自定义参数。<p>
参数说明：<p>
keyWordList -- 自定义关键词，可随意修改为个人感兴趣的词。<b>注意单引号、逗号必须为英文符号。</b><p>
saveToDesktop -- 默认为1，结果文件保存到桌面。如改为0，则保存到与工具相同的目录下。<p>
autoOpenResult -- 默认为1，执行完成后在浏览器中打开。如改为0，则不自动打开。<p>

其它“mail” 相关的参数是发送邮件所用，主要用于定时脚本配置，一般不需要修改，这里不作详细说明。<p>

![image](https://user-images.githubusercontent.com/112439804/196354343-075e8e10-066b-46e8-85d8-cabb0384c760.png) <p>

4.执行main.exe, 会弹出命令行窗口。 <p>

<b>注意：执行时间较长，大约需要3分钟。知乎这边很快。主要是微博的热搜页面作了修改，现在是跟随用户滑动动态渲染，所以需要做相应的等待处理。</b><p>

![image](https://user-images.githubusercontent.com/112439804/196355999-7f901cae-a686-4225-adf7-e3110cd674db.png) <p>

5.结果示例。<p>

![image](https://user-images.githubusercontent.com/112439804/196356115-77691d09-9090-4f5e-a8bc-d1b8cb6f4e70.png) <p>

<p>





