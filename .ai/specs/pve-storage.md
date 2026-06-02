# Spec: Proxmox VE 存储：VG、瘦池与虚拟机磁盘

| 字段 | 值 |
| ---- | -- |
| 状态 | draft |
| 交付物 | `content/post/cloud/pve-storage.md` |
| Hugo url | `pve-storage` |
| 标题 | Proxmox VE 存储：VG、瘦池与虚拟机磁盘 |
| 分类 | cloud |

---

## 1. 目的

用 homelab pve03（192.168.50.3）上的真实布局，解释 PVE 存储栈（物理盘 → VG → `pve-root` / `pve-data` 瘦池 → `local-lvm` → VM 磁盘），并回答：OpenTofu 与现网容量不一致如何处理；K8s 节点「根盘吃紧」指什么；瘦池是否多 VM 共用；Guest 内 `df` 空闲与 PVE 瘦池剩余的关系；VG 未分配空间能否扩瘦池、是否影响宿主机。

## 2. 读者

自己复盘 homelab；已会用 PVE Web UI / `qm`，但对 LVM thin、存储池余量与 K8s 节点根分区关系不熟。

## 3. 核心信息（必须传达）

- OpenTofu：先让 `*_disk_size_gb` 与 PVE 现网一致，再 `import`（若未入 state），`plan` 无意外 diff 后再 `apply` 扩容。
- 「根盘吃紧」：指 VM 内 `/`（容器镜像、kubelet、日志等），不是 Longhorn PVC 等单独挂盘。
- `local-lvm` 瘦池：同节点上 VM 虚拟盘共用；Guest `df` 与 PVE 瘦池占用可严重不一致（overcommit / 已删未回收等）。
- VG `VFree`：在瘦池 LV 之外，可 `lvextend` 扩 `data`；`pve-root` 独立，规范扩池不挤占系统盘已分配空间。
- pve03 示例数据（2026-06）：sda ~112G；瘦池 ~60.7G、可用 ~17.5G；VG 空闲 ~13.9G；k8s-39 虚拟盘 25G、OpenTofu 示例曾写 18G。

## 4. 必须包含（验收清单）

- [ ] 标题、url、分类与 Spec 表一致
- [ ] 正文从 `##` 起，无 `#`（MD025）
- [ ] 标签：`original`、`AI-assisted` + `pve`、`proxmox`、`storage`、`homelab`、`k8s`
- [ ] 含 OpenTofu 漂移处理步骤（与 w10n-config `homelab/opentofu/pve` 一致）
- [ ] 含 pve03 示意分层图（ASCII 或 mermaid）
- [ ] 回答用户提出的四个追问（漂移、根盘、瘦池共用、VG 空闲）
- [ ] 内链：`disk-resize.md`、`proxmox-ve-pve.md`（相对路径）
- [ ] 不写 VPN 敏感命名；homelab IP 可写（内网）

## 5. 禁止包含（Do NOT）

- 不写「终极指南」「深度解析」类标题夸大
- 不编造未核实的容量数字（以外部 2026-06 查询为准，注明时间点）
- 不把 Longhorn PVC 与节点根分区混为一谈

## 6. 语气与风格（本篇特有）

默认见 [delivery-style.md](../delivery-style.md)。技术说明为主，可举 pve03 / k8s-39 / k8s-38 例子；人称少用「我」。

## 7. 建议结构（大纲）

1. 背景（为何要懂这层）
2. pve03 磁盘分层（图 + 表）
3. `local` vs `local-lvm`
4. 瘦池共用 + thin 直觉模型
5. Data% 与 df 对照（含 98% 释义、k8s-39 是否还有空间）
6. K8s 节点：根盘 vs PVC
7. Guest 空闲 vs 瘦池写失败
8. VG VFree、扩瘦池、SSD「留空」误区
9. OpenTofu 与现网同步
10. 扩容粗算与参考

## 8. 可选 / 后续修订

- 扩容 k8s-39 后的实测数据
- 其他 PVE 节点（n100、r86s）对比

## 9. 修订流程

1. 改本 Spec → 2. AI 按 Spec 改交付物 → 3. 勾 §4 验收

## 10. 变更记录

| 日期 | 变更 |
| ---- | ---- |
| 2026-06-02 | 初版 |
| 2026-06-02 | 增补 Data%/df、thin 模型、VFree 与 SSD |
