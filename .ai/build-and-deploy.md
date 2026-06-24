# 构建与部署

> 本目录不参与 Hugo 发布。说明博客**如何构建**、**如何上线**，供 AI 与作者改构建流程时对照。

## 入口一览

| 入口 | 用途 | 环境 |
| ---- | ---- | ---- |
| [`build.sh`](../build.sh) | **Cloudflare Pages 生产构建**（OpenTofu 配置的 `build_command`） | CF 构建机 |
| [`scripts/build-site.sh`](../scripts/build-site.sh) | `hugo` + Pagefind 索引 | CF（经 `build.sh`）、本地 `task site:build`、容器 |
| [`Containerfile`](../Containerfile) | 多阶段镜像：Hugo → Pagefind → Nginx | homelab / 私有仓库 |
| [`Taskfile.yml`](../Taskfile.yml) | `task site:build`、`task preview`、`task preview:search` | 本地开发 |

Cloudflare Pages 项目由 **OpenTofu** 管理，见 `w10n-config/infra/cloudflare/README.md`；`build_command` 为 `bash build.sh`，**改构建步骤优先改本仓库的 `build.sh` / `scripts/build-site.sh`**，一般不必改 OpenTofu。

## `build.sh`（Cloudflare Pages）

CF 每次从 GitHub `main` 部署时执行：

1. 统计 `content/post` 文章数与总字符数，写入 `static/stats.json`（站点统计用）
2. 调用 `scripts/build-site.sh` 完成 Hugo 构建与 Pagefind 索引

```bash
bash build.sh
```

**新增构建步骤时**：若与 Hugo/Pagefind 无关（例如生成额外静态文件），加在 `exec scripts/build-site.sh` **之前**；若与站点 HTML 或搜索索引有关，改 `scripts/build-site.sh` 或两处配合。

## `scripts/build-site.sh`

```bash
hugo --minify          # 可用环境变量 HUGO_FLAGS 覆盖
pagefind --site public # 本地无二进制时用 npx pagefind@PAGEFIND_VERSION
```

| 变量 | 默认 | 说明 |
| ---- | ---- | ---- |
| `HUGO_FLAGS` | `--minify` | 传给 `hugo` |
| `PAGEFIND_VERSION` | `1.5.2` | `npx` 安装的 Pagefind 版本；npm 包默认带 **extended**（中文分词） |

产物：

- `public/` — Hugo 静态站
- `public/pagefind/` — 搜索索引与 UI 资源（**在 `.gitignore` 中，不提交**）

搜索相关模板与配置见 [content/post/web/hugo-static-site-search.md](../content/post/web/hugo-static-site-search.md)。

## 本地命令

| 命令 | 说明 |
| ---- | ---- |
| `task site:build` | 等同 `scripts/build-site.sh`（**不含** `stats.json`） |
| `task preview` | `hugo server` 热更新，**无** Pagefind 索引 |
| `task preview:search` | 完整构建后 `pagefind --serve`，访问 `:1414/search/` |

本地验证搜索请用 `task preview:search`，不要用 `task preview`。

## 容器构建

`Containerfile` 安装 `pagefind_extended` 二进制，执行：

```dockerfile
RUN hugo --minify && pagefind --site public
```

容器路径**不**经过 `build.sh`（无 `stats.json` 步骤）。若 CF 与容器需行为一致，把共用逻辑保持在 `scripts/build-site.sh`，容器侧可考虑改为调用该脚本。

## 修改检查清单

改动构建流程后建议确认：

1. `bash build.sh` 在仓库根目录能成功（需 Node/`npx` 或已安装 `pagefind`）
2. `public/pagefind/` 已生成
3. `task preview:search` 下 `/search/` 可搜到结果
4. 若改 Hugo 版本：同步 `Containerfile` 的 `HUGO_VERSION` 与 OpenTofu `deployment_configs.production.environment_variables.HUGO_VERSION`（`w10n-config/infra/cloudflare/opentofu/blog/main.tf`）
