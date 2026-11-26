# 贡献主题包（.overgrowpack）

一个主题包就是一个完整的桌面世界：配色、边缘的草、氛围光、抬头页、菜单栏图标——全在一个 zip 里。

## 提交流程

1. Fork 本仓库，在 `themes/` 放入你的 `你的主题名.overgrowpack`（zip 格式，内含 `theme.json`）
2. 在 `themes/previews/` 放一张至少 1600px 宽的预览图（文件名对应）
3. [开一个 Issue](https://github.com/LoxoTechIO/OverGrow-Theme/issues/new/choose)，附一句话介绍 + 预览图

```
/Users/zhangbo/Develop/ai/overgrow-site
```

1. 通过 App 内置校验后合入，你的名字会出现在下面的主题列表里

## 本地自查（发布前必做）

```bash
git clone https://github.com/LoxoTechIO/overgrow  # 主工程，含校验工具
cd overgrow
swift run biomecheck /path/to/你的包目录
```

- 退出码 0 = 可安装；`--strict` 会把警告也算失败
- 也可以直接双击 `.overgrowpack` 导入 OverGrow，校验不通过 App 会告诉你原因

## theme.json 最小骨架（format 3）

```json
{
  "format": 3,
  "id": "your.theme",            // 全局唯一，用点分命名空间，如 yourname.theme
  "name": "你的主题名",
  "subtitle": "一句话气质",
  "author": "你的 GitHub 用户名",
  "version": "1.0.0",
  "baseScene": "grass",
  "requires": ["slot", "ritual", "rest.scene", "menuBar", "tokens"],
  "palette": { "accent": "e2a44f", "vignette": "3a2a18" },
  "layers": [
    { "type": "slot", "slot": "edge", "element": "blade",
      "pile": "grassTuft", "ambient": "firefly", "opacity": 1 },
    { "type": "vignette", "strength": 0.45 }
  ],
  "ritual": { "kind": "bloom", "duration": 2.6, "growth": [0.02, 1],
              "colors": ["f2c27a", "b8a07e"], "copy": "草退了",
              "easing": "outCubic", "respectsReducedMotion": true },
  "rest": { "backdrop": ["8a7a9e", "f0d9b5"], "ambient": "petal",
            "horizon": "mountain", "focusCopy": "抬头 · …", "doneCopy": "…"
          }
}
```

进阶：`actors`（角色）、`motions`（动画）、`bubbles`（台词）、`tokens`（设计令牌）  
都是可选字段——完整说明见主工程 [docs/THEME-PACK.md](https://github.com/LoxoTechIO/overgrow/blob/main/docs/THEME-PACK.md)。

## 规矩

- 只收原创或你有权分发的素材；引用照片必须注明来源与许可
- 不收你无法授权的 AI 生成素材
- `id` 不得与已有主题冲突；`name`/`subtitle` 中英任一语言均可
- 中心区永不遮挡是产品红线，配方层面已经保证——不要尝试绕过
