#!/usr/bin/env python3
"""Generate the theme packs for OverGrow-Theme.

Each theme is written to a temp dir (theme.json + README.md) and zipped
into themes/<slug>.overgrowpack. Engine vocabulary (v3):

  edge element: blade bamboo vine moss paw firefly frost sakura cloudWisp
  air particle: snow rain petal leaf dandelion pollen firefly
  ground pile : snow grassTuft pawPrint mossCushion wetMoss petalCarpet cloudPuff
  rest.ambient: snow petal leaf pollen firefly none
  rest.horizon: mountain field none
  ritual.kind : bloom none   ritual.easing: linear outCubic outBack inOut
  palette     : deep mid pale tip vignette accent drift ambient (hex, no #)

Usage: python3 Scripts/make_packs.py [--only slug,slug]
"""
import argparse
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "themes"

# ---------------------------------------------------------------------------
# 主题定义：每个主题一条完整"立意"，吃满引擎而不是换个颜色。
# ---------------------------------------------------------------------------

THEMES = [
    # ---- 暗黑游戏风 ----
    {
        "slug": "ember-crypt",
        "pack": {
            "id": "ember.crypt", "name": "烬烛", "version": "1.0.0",
            "author": "LoxoTechIO",
            "subtitle": "地牢边缘的枯草间，烬火聚拢——你盯得越久，火越亮",
            "baseScene": "grass",
            "format": 3,
            "requires": ["slot", "ritual", "rest.scene", "menuBar", "tokens"],
            "budget": {"maxActors": 0, "maxAssetMB": 0},
            "actors": [], "motions": [], "assets": [],
            "layers": [
                {"type": "slot", "slot": "edge", "element": "thorn",
                 "ambient": "firefly"},
                {"type": "vignette", "strength": 0.62},
            ],
            "palette": {
                "deep": "0d0b08", "mid": "2a1f14", "pale": "6b4a26",
                "tip": "c9772e", "vignette": "000000", "accent": "e8862e",
                "drift": "d98a3d", "ambient": "f2a44c",
            },
            "ritual": {
                "kind": "bloom", "duration": 2.6, "easing": "outCubic",
                "anchor": "bottomCenter", "height": 0.26,
                "copy": "火把举起来了，黑暗退后半步",
                "colors": ["f2a44c", "8a4b1e"], "respectsReducedMotion": True,
            },
            "rest": {
                "backdrop": ["0e0c14", "3a1f1a"], "horizon": "mountain",
                "buddy": "ember.flame",
                "ambient": "firefly",
                "focusCopy": "抬眼 · 火光照不到的地方才是远方",
                "doneCopy": "草退了，火堆 +1",
            },
            "menuBar": {"symbol": "flame"},
            "tokens": {"accent": "e8862e"},
            "ui": {"paper": "1c1814", "ink": "e8ddcc", "soft": "9a8f7d"},
            "accessibility": {"reducedMotion": "static"},
        },
        "preview": "dark",
    },
    # ---- MOBA 风格致敬（原创，不含任何 IP 元素）----
    {
        "slug": "rift-night",
        "pack": {
            "id": "rift.night", "name": "峡谷夜巡", "version": "1.0.0",
            "author": "LoxoTechIO",
            "subtitle": "野区之夜：金色的符文萤光在草丛里游走，回城前先护眼",
            "baseScene": "grass",
            "format": 3,
            "requires": ["slot", "ritual", "rest.scene", "menuBar", "tokens"],
            "budget": {"maxActors": 0, "maxAssetMB": 0},
            "actors": [], "motions": [], "assets": [],
            "layers": [
                {"type": "slot", "slot": "edge", "element": "crystal",
                 "ambient": "firefly"},
                {"type": "vignette", "strength": 0.58},
            ],
            "palette": {
                "deep": "101826", "mid": "1e3050", "pale": "3c6a9e",
                "tip": "6aa0d8", "vignette": "060a12", "accent": "e8b23c",
                "drift": "f2c14c", "ambient": "f2c14c",
            },
            "ritual": {
                "kind": "bloom", "duration": 2.4, "easing": "outCubic",
                "anchor": "bottomCenter", "height": 0.26,
                "copy": "回城泉水闭目 20 秒，满血再战",
                "colors": ["f2c14c", "3c6a9e"], "respectsReducedMotion": True,
            },
            "rest": {
                "backdrop": ["0a1220", "1c3050"], "horizon": "mountain",
                "buddy": "rune.sprite",
                "ambient": "firefly",
                "focusCopy": "离开战场 20 秒 · 水晶不会自己掉",
                "doneCopy": "草退了，回城 +1",
            },
            "menuBar": {"symbol": "shield"},
            "tokens": {"accent": "e8b23c"},
            "ui": {"paper": "0e1626", "ink": "d8e2f0", "soft": "7a8ca4"},
            "accessibility": {"reducedMotion": "static"},
        },
        "preview": "dark",
    },
    # ---- 大航海冒险风致敬（原创，不含任何 IP 元素）----
    {
        "slug": "grand-voyage",
        "pack": {
            "id": "grand.voyage", "name": "伟大航路", "version": "1.0.0",
            "author": "LoxoTechIO",
            "subtitle": "甲板上的草随风长，日落金洒在桅杆——望远的理由是海平线",
            "baseScene": "grass",
            "format": 3,
            "requires": ["slot", "ritual", "rest.scene", "menuBar", "tokens"],
            "budget": {"maxActors": 0, "maxAssetMB": 0},
            "actors": [], "motions": [], "assets": [],
            "layers": [
                {"type": "slot", "slot": "edge", "element": "wave",
                 "ambient": "pollen"},
                {"type": "vignette", "strength": 0.4},
            ],
            "palette": {
                "deep": "1a4a66", "mid": "2e7a9e", "pale": "6ab0c8",
                "tip": "a8d8e0", "vignette": "122e42", "accent": "e0902e",
                "drift": "f2d9a8", "ambient": "f2c88a",
            },
            "ritual": {
                "kind": "bloom", "duration": 2.8, "easing": "outCubic",
                "anchor": "bottomCenter", "height": 0.26,
                "copy": "风向转好 · 抬眼看看海平线",
                "colors": ["f2c88a", "2e7a9e"], "respectsReducedMotion": True,
            },
            "rest": {
                "backdrop": ["2a5a8a", "f2d9a8"], "horizon": "field",
                "buddy": "sea.gull",
                "ambient": "pollen",
                "focusCopy": "望向 20 英尺外的海 · 船不会跑",
                "doneCopy": "草退了，航行 +1 海里",
            },
            "menuBar": {"symbol": "water.waves"},
            "tokens": {"accent": "b06a1e"},
            "accessibility": {"reducedMotion": "static"},
        },
        "preview": "cloud",
    },
    # ---- 森系治愈 ----
    {
        "slug": "moss-path",
        "pack": {
            "id": "moss.path", "name": "苔径", "version": "1.0.0",
            "author": "LoxoTechIO",
            "subtitle": "林间小径：苔藓贴着桌沿漫上来，藤蔓垂下，光斑浮在空气里",
            "baseScene": "grass",
            "format": 3,
            "requires": ["slot", "ritual", "rest.scene", "menuBar", "tokens"],
            "budget": {"maxActors": 0, "maxAssetMB": 0},
            "actors": [], "motions": [], "assets": [],
            "layers": [
                {"type": "slot", "slot": "edge", "element": "moss",
                 "pile": "mossCushion", "ambient": "pollen"},
                {"type": "slot", "slot": "edge", "element": "vine"},
                {"type": "vignette", "strength": 0.42},
            ],
            "palette": {
                "deep": "27401f", "mid": "3d6630", "pale": "7fae6a",
                "tip": "b8d9a0", "vignette": "1a2a16", "accent": "5a8a4a",
                "drift": "a8c890", "ambient": "d8e8b0",
            },
            "ritual": {
                "kind": "bloom", "duration": 2.8, "easing": "outCubic",
                "anchor": "bottomCenter", "height": 0.26,
                "copy": "苔上生凉，绿意漫过桌沿",
                "colors": ["a8c890", "5a8a4a"], "respectsReducedMotion": True,
            },
            "rest": {
                "backdrop": ["9ec8b0", "f2f7ee"], "horizon": "field",
                "buddy": "moss.mushroom",
                "ambient": "pollen",
                "focusCopy": "看远一点 · 让眼睛也晒晒树荫",
                "doneCopy": "草退了，林间 +1 口深呼吸",
            },
            "menuBar": {"symbol": "leaf"},
            "tokens": {"accent": "3f6f35"},
            "accessibility": {"reducedMotion": "static"},
        },
        "preview": "cloud",
    },
    # ---- 雪夜 ----
    {
        "slug": "first-snow",
        "pack": {
            "id": "first.snow", "name": "初雪", "version": "1.0.0",
            "author": "LoxoTechIO",
            "subtitle": "霜从玻璃边缘结晶进来，雪在桌沿堆起——今晚的屏幕是一扇冷窗",
            "baseScene": "grass",
            "format": 3,
            "requires": ["slot", "ritual", "rest.scene", "menuBar", "tokens"],
            "budget": {"maxActors": 0, "maxAssetMB": 0},
            "actors": [], "motions": [], "assets": [],
            "layers": [
                {"type": "slot", "slot": "edge", "element": "frost"},
                {"type": "slot", "slot": "edge", "pile": "snow"},
                {"type": "slot", "slot": "edge", "ambient": "snow"},
                {"type": "vignette", "strength": 0.4},
            ],
            "palette": {
                "deep": "5a6a7e", "mid": "8fa3b8", "pale": "c8d8e8",
                "tip": "f4f8fc", "vignette": "2a3646", "accent": "4a7ca8",
                "drift": "eef4fa", "ambient": "f4f8fc",
            },
            "ritual": {
                "kind": "bloom", "duration": 3.0, "easing": "outCubic",
                "anchor": "bottomCenter", "height": 0.26,
                "copy": "雪落无声，屋里有灯",
                "colors": ["d8e8f4", "8fa3b8"], "respectsReducedMotion": True,
            },
            "rest": {
                "backdrop": ["2e3d52", "e8eef4"], "horizon": "mountain",
                "buddy": "snow.snowman",
                "ambient": "snow",
                "focusCopy": "雪停之前，看一眼远处",
                "doneCopy": "草退了，炉火 +1",
            },
            "menuBar": {"symbol": "snowflake"},
            "tokens": {"accent": "3a6a96"},
            "accessibility": {"reducedMotion": "static"},
        },
        "preview": "cloud",
    },
    # ---- 夜樱 ----
    {
        "slug": "sakura-night",
        "pack": {
            "id": "sakura.night", "name": "夜樱", "version": "1.0.0",
            "author": "LoxoTechIO",
            "subtitle": "夜色里的樱枝压低，花瓣落满桌沿——抬头时花正往下落",
            "baseScene": "grass",
            "format": 3,
            "requires": ["slot", "ritual", "rest.scene", "menuBar", "tokens"],
            "budget": {"maxActors": 0, "maxAssetMB": 0},
            "actors": [], "motions": [], "assets": [],
            "layers": [
                {"type": "slot", "slot": "edge", "element": "sakura",
                 "pile": "petalCarpet", "ambient": "petal"},
                {"type": "vignette", "strength": 0.48},
            ],
            "palette": {
                "deep": "3a2c44", "mid": "7a5a78", "pale": "d8a8c0",
                "tip": "f2d4e0", "vignette": "241a30", "accent": "c87a9e",
                "drift": "f2c4d4", "ambient": "f2d4e0",
            },
            "ritual": {
                "kind": "bloom", "duration": 2.8, "easing": "outCubic",
                "anchor": "bottomCenter", "height": 0.26,
                "copy": "花落一寸，倦意退一寸",
                "colors": ["f2c4d4", "c87a9e"], "respectsReducedMotion": True,
            },
            "rest": {
                "backdrop": ["3a2c44", "f2dce6"], "horizon": "mountain",
                "buddy": "sakura.butterfly",
                "ambient": "petal",
                "focusCopy": "抬头 · 花落下来的方向",
                "doneCopy": "草退了，花枝 +1",
            },
            "menuBar": {"symbol": "sparkles"},
            "tokens": {"accent": "a85a80"},
            "accessibility": {"reducedMotion": "static"},
        },
        "preview": "dark",
    },
    # ---- 云海 ----
    {
        "slug": "cloud-nap",
        "pack": {
            "id": "cloud.nap", "name": "云眠", "version": "1.0.0",
            "author": "LoxoTechIO",
            "subtitle": "低云贴着桌沿浮过，絮状的风从边上游走——屏幕上方是高原的天空",
            "baseScene": "grass",
            "format": 3,
            "requires": ["slot", "ritual", "rest.scene", "menuBar", "tokens"],
            "budget": {"maxActors": 0, "maxAssetMB": 0},
            "actors": [], "motions": [], "assets": [],
            "layers": [
                {"type": "slot", "slot": "edge", "element": "cloudWisp",
                 "pile": "cloudPuff", "ambient": "dandelion"},
                {"type": "vignette", "strength": 0.36},
            ],
            "palette": {
                "deep": "4a6a8e", "mid": "7a9ec0", "pale": "b8d0e4",
                "tip": "e8f2fa", "vignette": "3a4a5e", "accent": "5a8ac0",
                "drift": "f4f8fc", "ambient": "d8e8f4",
            },
            "ritual": {
                "kind": "bloom", "duration": 2.6, "easing": "outCubic",
                "anchor": "bottomCenter", "height": 0.26,
                "copy": "云散了，风把眼睛吹亮",
                "colors": ["b8d0e4", "7a9ec0"], "respectsReducedMotion": True,
            },
            "rest": {
                "backdrop": ["6a9ec8", "f4f8fc"], "horizon": "field",
                "buddy": "cloud.cloudlet",
                "ambient": "none",
                "focusCopy": "看云去 · 最远的那一朵",
                "doneCopy": "草退了，晴空 +1",
            },
            "menuBar": {"symbol": "cloud"},
            "tokens": {"accent": "3a6a9e"},
            "accessibility": {"reducedMotion": "static"},
        },
        "preview": "cloud",
    },
    # ---- 竹雨 ----
    {
        "slug": "bamboo-rain",
        "pack": {
            "id": "bamboo.rain", "name": "竹雨", "version": "1.0.0",
            "author": "LoxoTechIO",
            "subtitle": "雨天的竹林：竹节从桌沿长出来，湿苔爬上侧壁，雨丝斜着过",
            "baseScene": "grass",
            "format": 3,
            "requires": ["slot", "ritual", "rest.scene", "menuBar", "tokens"],
            "budget": {"maxActors": 0, "maxAssetMB": 0},
            "actors": [], "motions": [], "assets": [],
            "layers": [
                {"type": "slot", "slot": "edge", "element": "bamboo",
                 "pile": "wetMoss", "ambient": "rain"},
                {"type": "vignette", "strength": 0.45},
            ],
            "palette": {
                "deep": "24382a", "mid": "3c5c40", "pale": "6a9268",
                "tip": "9cbe8e", "vignette": "18241c", "accent": "4a7a52",
                "drift": "9ab4c0", "ambient": "a8c8b0",
            },
            "ritual": {
                "kind": "bloom", "duration": 2.6, "easing": "outCubic",
                "anchor": "bottomCenter", "height": 0.26,
                "copy": "雨小了，竹尖还挂着水",
                "colors": ["a8c8b0", "4a7a52"], "respectsReducedMotion": True,
            },
            "rest": {
                "backdrop": ["42566a", "dde8e2"], "horizon": "field",
                "buddy": "bamboo.frog",
                "ambient": "none",
                "focusCopy": "听一次雨 · 看一次远处",
                "doneCopy": "草退了，檐下 +1 场雨",
            },
            "menuBar": {"symbol": "drop"},
            "tokens": {"accent": "35603e"},
            "accessibility": {"reducedMotion": "static"},
        },
        "preview": "cloud",
    },
]

README_TMPL = """# {name}

{subtitle}

- 引擎元素：{elements}
- 预览：`themes/previews/{slug}.png`

由 `Scripts/make_packs.py` 生成，请改脚本后重新生成，不要手改 zip。
"""


def build_one(t: dict, tmp_root: Path) -> Path:
    pack = t["pack"]
    d = tmp_root / t["slug"]
    d.mkdir(parents=True)
    (d / "theme.json").write_text(
        json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    layers = pack["layers"]
    elements = " + ".join(
        x.get("element") or x.get("pile") or x.get("ambient")
        for x in layers if x["type"] == "slot")
    (d / "README.md").write_text(
        README_TMPL.format(name=pack["name"], subtitle=pack["subtitle"],
                           slug=t["slug"], elements=elements), encoding="utf-8")
    out = OUT / f"{t['slug']}.overgrowpack"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(d.iterdir()):
            z.write(f, f.name)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated slugs")
    args = ap.parse_args()
    only = set(args.only.split(",")) if args.only else None

    tmp = Path(tempfile.mkdtemp(prefix="og-make-"))
    try:
        for t in THEMES:
            if only and t["slug"] not in only:
                continue
            out = build_one(t, tmp)
            print(f"built {out.name} ({out.stat().st_size} B)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
