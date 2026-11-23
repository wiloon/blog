---
title: "Grafana Business Charts: ECharts 面板与 Gantt 时间线"
author: "-"
date: 2026-11-22T06:02:30+08:00
lastmod: 2026-11-22T06:02:30+08:00
url: grafana-business-charts
categories:
  - cloud
tags:
  - grafana
  - echarts
  - observability
  - remix
  - AI-assisted
---

## 背景

我在 Grafana 上给 baton（一个调度多个 coding agent 的 runner）做了一个看板，其中 Agent activity 面板用 state-timeline 显示每个 agent 什么时候在工作。这个面板的数据是采样出来的：采集器大约每 60 秒问一次「这段时间里有没有调用在跑」，Grafana 再按时间桶取最大值。结果是 5 秒的 run 和忙满一分钟看起来一样，间隔不到一分钟的两次 run 会连成一段。

想看清断续的工作，自然会想到 Gantt 图：每个 run 一根条，起止时间精确。Grafana 没有自带 Gantt 面板，常被推荐的 `marcusolsson-gantt-panel` 仓库 2023 年就归档了，最后一版只声明支持 Grafana 8.1+。于是看了一下 Business Charts。

## Business Charts 是什么

Business Charts 是一个 Grafana 面板插件，把 [Apache ECharts](https://echarts.apache.org/) 嵌进面板里。ECharts 能画的图（Gantt、桑基图、关系图、日历热力图、3D 等）在 Grafana 里基本都能画。

基本信息（2026-11-21 核对）：

| 项目 | 内容 |
| --- | --- |
| 插件 ID | `volkovlabs-echarts-panel` |
| 最新版本 | 7.3.0（2026-11-02） |
| Grafana 要求 | >= 12.3.0，7.3.0 基于 Grafana 13.0.2 的 SDK 构建 |
| 维护方 | Grafana Labs（2025 年从 Volkov Labs fork，保留原插件 ID） |
| 签名 | community |
| 许可证 | Apache-2.0 |
| 源码 | <https://github.com/grafana/business-charts> |

Volkov Labs 原仓库（`volkovlabs/business-charts`）已归档，现在由 Grafana Labs 维护。README 写明是 best-effort 审 PR，并且在找长期维护者。所以它目前是活的，但不算 Grafana 的核心产品。另外 README 里的兼容性表格还停在 "Grafana 11 or 12"，以 grafana.com 上的 `grafanaDependency` 为准。

## 工作方式

面板里有一个 Monaco 代码编辑器，你在里面写一个 JavaScript 函数（文档叫 Charts function）。函数读取 Grafana 查询返回的数据，返回一个 ECharts 的 `options` 对象，插件再调用 ECharts 的 `setOption(options)` 渲染。

函数能拿到的主要参数：

| 参数 | 用途 |
| --- | --- |
| `context.panel.data` | 查询结果（data frames）和时间范围 |
| `context.panel.chart` | 当前 ECharts 实例，可以自己绑定事件 |
| `context.echarts` | ECharts 库本身，比如 `graphic` 工具函数 |
| `context.grafana.theme` | 当前主题，用来配色 |
| `context.grafana.replaceVariables()` | 展开看板变量 |
| `context.grafana.locationService` | 改 URL、设置变量，做联动 |

读数据的典型写法：

```javascript
// Find the frame of query A and read its columns by name
const frame = context.panel.data.series.find((s) => s.refId === "A");
const col = (name) => frame.fields.find((f) => f.name === name)?.values ?? [];
```

另外还有一个 Visual editor（beta），不写代码也能拼出折线、柱状、散点等常见图。但 Gantt 这类自定义图形还是要写代码。

## 用它画 Gantt

ECharts 没有现成的 Gantt 类型，常见做法是 `custom` series：每条数据是 `[行号, 开始时间, 结束时间]`，在 `renderItem` 里画一个矩形。

下面这段假设查询 A 返回的表里有 `Time`（run 结束时间）、`duration_ms`、`agent`、`role` 四列。数据来自 Loki 日志时，先用 Grafana 的 Extract fields 等转换把字段展开成列。

```javascript
const frame = context.panel.data.series.find((s) => s.refId === "A");
const col = (name) => frame?.fields.find((f) => f.name === name)?.values ?? [];

const ends = col("Time");
const durations = col("duration_ms").map(Number);
const agents = col("agent");
const roles = col("role");

// One lane per agent, one color per role
const lanes = [...new Set(agents)];
const palette = { implement: "#73bf69", review: "#5794f2", fix: "#ff9830", spec: "#b877d9" };

const data = ends.map((end, i) => ({
  name: roles[i],
  value: [lanes.indexOf(agents[i]), end - durations[i], end, durations[i]],
  itemStyle: { color: palette[roles[i]] ?? "#8e8e8e" },
}));

const range = context.panel.data.timeRange;

return {
  tooltip: {
    formatter: (p) => `${lanes[p.value[0]]} · ${p.name}<br/>${(p.value[3] / 1000).toFixed(1)} s`,
  },
  grid: { left: 80, right: 20, top: 10, bottom: 30 },
  xAxis: { type: "time", min: range.from.valueOf(), max: range.to.valueOf() },
  yAxis: { type: "category", data: lanes },
  dataZoom: [{ type: "inside", filterMode: "weakFilter" }],
  series: [
    {
      type: "custom",
      encode: { x: [1, 2], y: 0 },
      data,
      renderItem: (params, api) => {
        const lane = api.value(0);
        const start = api.coord([api.value(1), lane]);
        const end = api.coord([api.value(2), lane]);
        const height = api.size([0, 1])[1] * 0.6;
        // Keep at least 1px so very short runs stay visible
        const shape = context.echarts.graphic.clipRectByRect(
          { x: start[0], y: start[1] - height / 2, width: Math.max(end[0] - start[0], 1), height },
          {
            x: params.coordSys.x,
            y: params.coordSys.y,
            width: params.coordSys.width,
            height: params.coordSys.height,
          }
        );
        return shape && { type: "rect", shape, style: api.style() };
      },
    },
  ],
};
```

效果是每个 agent 一行，每个 run 一根条，按 role 着色。两次 run 之间哪怕只隔几秒也会断开，鼠标滚轮可以在面板里放大。

## 需要注意的地方

**代码跑在看板查看者的浏览器里。** Charts function 是任意 JavaScript，带着查看者的 Grafana 登录状态执行。谁能编辑看板，谁就能让所有查看者执行他的代码。看板从 git provision、改动经过 review 的话风险可控；多人随手改看板的环境要谨慎。

**不要用远程 import。** 插件支持在函数里 `import("https://esm.sh/...")` 动态加载 npm 包。这等于每次打开看板都从第三方 CDN 拉代码执行，是一个供应链入口，生产看板里应该避免。

**代码没有类型和测试。** 函数以字符串形式存在看板 JSON 里。数据源字段改名、插件升级改了行为，面板会直接报错或显示空白，不会有任何提前提示。

**插件依赖会传染。** 看板用了这个面板，所有导入这个看板的 Grafana 都要装插件，否则显示 "panel plugin not found"。如果看板是随某个开源项目分发的，这个成本会落到每个用户身上。

**数据量。** Loki 日志查询有行数上限（比如 500 行），时间范围拉得很长时，早期的 run 会被截掉。Gantt 适合看几小时到一两天，不适合看一个月。

## 两个方案对比

回到 baton 的问题，我最后列了两个方案：

- 方案 A：不装插件，改数据。采集器新增一个「忙碌秒数」计数器 `baton_active_seconds_total`，用 `rate()` 看每个时间桶的忙碌比例；同时让同一个任务的所有 run 共用一个 trace，用 Tempo 自带的 trace 视图看单个任务的精确时间线。
- 方案 B：用 Business Charts 画上面那种全局 Gantt，数据直接用 Loki 里已有的 run summary。

| 维度 | 方案 A：计数器 + 每任务一个 trace | 方案 B：Business Charts Gantt |
| --- | --- | --- |
| 改哪里 | baton 采集器、trace ID 生成、看板 | 看板 JSON，加 Grafana 插件 |
| 第三方依赖 | 无，只用 Grafana / Tempo 自带功能 | 社区签名插件，best-effort 维护 |
| 精度 | 忙碌比例按时间桶平均；trace 精确到毫秒 | 每个 run 精确到毫秒 |
| 长时间范围 | 好，rate 求平均，拉远不失真 | 差，受日志行数上限和条形密度限制 |
| 看单个任务 | 好，trace 视图里 run 之间的空隙一目了然 | 能看，但要先筛选出这个任务 |
| 跨 agent 总览 | 只能看到每个 agent 的忙碌比例 | 好，一张图看到所有 agent 的所有 run |
| 模型等待 vs 工具时间 | Codex 的 sampling / tool span 直接嵌在 trace 里 | 看不到，只到 run 这一层 |
| 历史数据 | 只对改动之后的数据生效 | 立即可用，run summary 早就有 |
| 维护成本 | Python 代码，有单元测试 | 看板里的 JS 字符串，没有测试 |
| 安全 | 无新增 | 看板里执行任意 JS |

我的判断：

- 想回答「agent 这段时间有多忙」「某个任务里发生了什么」，方案 A 更合适，而且不引入第三方依赖。
- 想要「一眼看到今天所有 agent 的所有 run」这种总览，方案 B 的效果更直观，代价是插件依赖和看板里的一段 JS。
- 两者不冲突。方案 B 只改看板，可以先在自己的 Grafana 上试，不放进随项目分发的看板。

对应的 issue：方案 A 是 [wiloon/baton#149](https://github.com/wiloon/baton/issues/149)，方案 B 是 [wiloon/baton#150](https://github.com/wiloon/baton/issues/150)。

## 参考

- [Business Charts 源码与 README](https://github.com/grafana/business-charts)
- [Business Charts 文档：Charts function](https://grafana.com/docs/plugins/volkovlabs-echarts-panel/latest/charts-function/)
- [Business Charts 插件页](https://grafana.com/grafana/plugins/volkovlabs-echarts-panel/)
- [ECharts custom series](https://echarts.apache.org/en/option.html#series-custom)
- [Grafana 基础笔记](./grafana.md)
