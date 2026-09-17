# README 视觉维护

[← 返回首页](../README.md)

## 设计方向

**Obsidian / Editorial Cinema**：黑曜石底色、暖白大字、低饱和紫色、少量鼠尾草绿。画框、光带和时间线呼应视频制作；品牌名保留 `{一起 Vibe} × 秒悟 Meoo`，不修改或冒充官方 Logo。

首页阅读顺序：主视觉与下载入口 → 真实作品工作流 → 历史案例 → 两种安装入口 → 可复制提示词 → 运行边界与文档。技术细节放在原生折叠区内，入口与关键信息保持可复制的 Markdown / HTML 文字，不烘焙进图片。

## 素材清单

新素材统一放在 `docs/media/readme/`，直接编辑 SVG 即可，无需安装设计工具或上传字体。

| 内容 | 桌面版 | 手机竖向重排版 |
| :--- | :--- | :--- |
| 首屏主视觉 | `hero.svg` · 1600 × 830 | `hero-mobile.svg` · 800 × 1120 |
| 五步工作流 | `workflow.svg` · 1600 × 346 | `workflow-mobile.svg` · 800 × 770 |
| 历史案例封面 | `case-cover.svg` · 1600 × 390 | `case-cover-mobile.svg` · 800 × 604 |

README 使用 `<picture>`，在 600px 及以下的视口选择手机图，普通 `<img>` 作为回退。暗色图有自己的不透明背景和边框，因此不会因 GitHub 明暗主题改变而丢失对比。

主视觉仅有缓慢的光感和时间线位移动画，尊重 `prefers-reduced-motion`。动画不运行时，默认静态画面也包含完整信息。所有图形是流程说明，不是产品实测或 Skill 生成效果证明。

## 为什么更换原来的横幅引用

原 `docs/media/hero.gif` 和其他品牌、案例文件仍保留，没有删除或覆盖。旧首页把 GIF 首屏和徽章交给外链加载；新首页改为轻量、仓库内相对路径的 SVG，不依赖 shields.io 或远程生成横幅服务。历史案例 GIF 移到案例页，首页只加载案例封面。

在本次检查中，旧媒体文件确实存在。没有证据可以把所有人的加载失败都归因于单一问题；网络、GitHub 图片代理和缓存仍可能影响图片加载。仓库内图片用相对路径，也能避免把 README 固定到 `main` 分支。

GitHub 官方依据：

- [相对链接与仓库图片](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [README 中的 picture 元素](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github)
- [图片代理与缓存排查](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-anonymized-urls)

## 保持稳定的几条规则

1. 图片用相对路径；从子目录引用时重新计算路径。不要复制当前浏览器的 `blob/main` 页面地址当图片源。
2. SVG 保持自包含：不用脚本、`foreignObject`、外链图片、远程字体或 `@import`。单张预算不超过 32 KB。
3. 标题继续用真实中文，系统字体栈保留中文回退；文字加长后检查实际字宽，不靠无限缩小字号解决。
4. 桌面与手机素材一起改。正文保留图片的文字等价内容和有意义的 `alt`，重要操作不要只出现在图里。
5. 新增案例必须说明来源及验证范围。不要把装饰画框当作真实产品截图，也不要删掉历史案例的原作者标识。

## 检查与验收

在完整仓库中运行：

```bash
python3 scripts/check-readme.py
```

检查本地链接、图片的相对路径、图片替代文字、显式页内锚点、SVG XML、体积预算和外部依赖。稀疏检出时，可用 `--known-paths` 提供同版本 Git tree 的逐行路径清单；这只证明文件路径存在，不证明对应媒体可以在线加载。

视觉验收应同时检查：1440px 桌面明暗主题、390px 手机，以及 320px 窄屏；确认图片选择、标题换行、正文可读性和横向溢出。动画分别检查默认模式和减少动态效果模式。

本次改版的浏览器截图属于本地 Chromium + GitHub 风格 Markdown 预览，不是线上 GitHub 网页截图。没有重新运行视频生成、解码历史 GIF 或重做 Skill 功能验收；原技能版本、代码、Release ZIP 和原媒体保持不变。
