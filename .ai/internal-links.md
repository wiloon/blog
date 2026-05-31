# 站内 Markdown 内链规范

> **适用范围**：所有 `content/post/**/*.md`（SDD 与非 SDD）。  
> 与 [AGENTS.md](../AGENTS.md) 的 front matter / URL 规则并列。

## 背景

博客使用 Hugo `url` 字段生成 permalink（如 `url: hotspot` → 线上 `/hotspot/`）。若在 Markdown 里写 `[text](/hotspot)`：

- **线上（Chrome）**：可跳转
- **VS Code 预览 / 源码 Cmd+点击**：`/hotspot` 被当作工作区根路径，**无法**打开对应 `.md`

兼顾两者的方式：

1. 源码写 **相对 `.md` 路径**：`[text](./hotspot.md)`
2. `config.toml` 启用 Hugo **embedded link render hook**，构建时解析回 permalink

## 写法规则

| 场景 | 写法 |
| ---- | ---- |
| 同目录 | `[HotSpot](./hotspot.md)` |
| 跨目录 | `[DCEVM](../../cs/dcevm-hotswapagent.md)` |
| 带锚点 | `[Spring Boot](./spring/spring-boot.md#依赖注入方式)` |
| 外链 | `[title](https://example.com)`（不变） |

**禁止**新建站内互链 `[text](/permalink)`。

链到 **目标 `.md` 文件路径**，不要仅按 front matter `url` 猜文件名（例：`java-gc.md` 的 `url` 为 `java/gc`，应写 `./java-gc.md`，由 Hugo hook 解析）。

## 代码块与纯文本

fenced code block（`` ``` ``）内的 `` `/hotspot` `` 等 permalink 字面量 **不要** 改为 `.md`——它们不是可点击链接，线上读者也可能更熟悉 `/hotspot` 形式。

## 站点配置

`config.toml` 须包含：

```toml
[markup.goldmark.renderHooks.link]
useEmbedded = "always"
```

项目内 **不要** 添加自定义 `layouts/_markup/render-link.html`（会覆盖 embedded hook）。

## 批量迁移脚本

`scripts/migrate-internal-links.py`：

```bash
# 单篇试点
python3 scripts/migrate-internal-links.py --dry-run --file content/post/language/java/java-knowledge-map.md
python3 scripts/migrate-internal-links.py --write   --file content/post/language/java/java-knowledge-map.md

# 全站
python3 scripts/migrate-internal-links.py --dry-run
python3 scripts/migrate-internal-links.py --write
```

| 选项 | 说明 |
| ---- | ---- |
| `--file PATH` | 只改指定一篇（与 `--scope` 互斥） |
| `--scope all` | 默认；全 `content/` |
| `--scope java` | 仅 `language/java` + `cs` |

链接格式迁移 **不改** `lastmod`（不算内容修订）。

## AI 改稿时

1. 新增或修改 **站内互链** 时，默认写相对 `.md`。
2. 不确定目标文件：`find content -name 'hotspot.md'` 或查 front matter。
3. 互链密集的文章可参考 [specs/java-knowledge-map.md](specs/java-knowledge-map.md)。

## 例外

- `https://` 外链
- 静态资源路径（如 `/user/desktop/...`）
- 文档示例中的 `/url` 等占位符
