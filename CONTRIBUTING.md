# 贡献主题包（.overgrowpack）

一个主题包就是一个完整的桌面世界：配色、边缘的草、氛围光、抬头页、菜单栏图标——全在一个 zip 里。

## 提交流程

1. Fork 本仓库，在 `themes/` 放入你的 `你的主题名.overgrowpack`（zip 格式，内含 `theme.json`）
2. 在 `themes/previews/` 放一张至少 1600px 宽的预览图（文件名对应）
3. [开一个 Issue](https://github.com/LoxoTechIO/OverGrow-Theme/issues/new/choose)，附一句话介绍 + 预览图
4. 通过 App 内置校验后合入，你的名字会出现在下面的主题列表里，并自动出现在官网画廊

## 本地自查（发布前必做）

```bash
git clone https://github.com/LoxoTechIO/overgrow  # 主工程，含校验工具
cd overgrow
swift run biomecheck /path/to/你的包目录
```

- 退出码 0 = 可安装；`--strict` 会把警告也算失败
- 也可以直接双击 `.overgrowpack` 导入 OverGrow，校验不通过 App 会告诉你原因

## 引擎词汇表（format 3 现在支持的配方 id）

主题的立意靠换配方，不是换颜色。下面这些 id 都可以直接写进 `theme.json`：

| 类别 | 可用 id |
|---|---|
| 边缘元素 `layers[].element` | `blade` 草丛 · `bamboo` 竹 · `vine` 藤 · `moss` 苔 · `sakura` 樱枝 · `frost` 霜 · `cloudWisp` 低云 · `paw` 爪垫 · `firefly` 萤火 |
| 地面堆积 `layers[].pile` | `grassTuft` 草垫 · `snow` 积雪 · `mossCushion` 苔垫 · `wetMoss` 湿苔 · `petalCarpet` 落花 · `cloudPuff` 云絮 · `pawPrint` 爪印 |
| 空气粒子 `layers[].ambient` | `snow` 雪 · `rain` 雨 · `petal` 花瓣 · `leaf` 落叶 · `dandelion` 蒲公英絮 · `pollen` 花粉光尘 · `firefly` 萤火 |
| 休息页粒子 `rest.ambient` | `snow` `petal` `leaf` `pollen` `firefly` `none` |
| 休息页远景 `rest.horizon` | `mountain` 山影 · `field` 平野/海平线 · `none` |
| 仪式 `ritual.kind` / 缓动 | `bloom` `none` / `linear` `outCubic` `outBack` `inOut` |
| 调色盘 `palette` | 八槽全可控：`deep` `mid` `pale` `tip` `vignette` `accent` `drift` `ambient`（六位 hex，不带 #） |
| 暗色主题 UI | `"ui": { "paper": "…", "ink": "…", "soft": "…" }` 声明深色纸色，对比度按它判 |

可以写多个 slot 图层叠加（如苔径 = `moss` 层 + `vine` 层）。官方示例包由
`Scripts/make_packs.py` 生成——参考它的组合方式最快：暗黑风（烬烛）用枯草调色盘 +
萤火 + 重渐晕；雪天（初雪）用 `frost` + `snow` 堆积 + `snow` 粒子三层叠加；
森系（苔径）用 `moss` + `vine` 双层 + `pollen`。

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
- 不收真实 IP 的同人主题（王者荣耀、原神、海贼王等）：角色名、Logo、立绘、台词都是商标/版权风险；风格致敬（像峡谷夜巡、伟大航路这样原创命名）可以
- `id` 不得与已有主题冲突；`name`/`subtitle` 中英任一语言均可
- 中心区永不遮挡是产品红线，配方层面已经保证——不要尝试绕过
