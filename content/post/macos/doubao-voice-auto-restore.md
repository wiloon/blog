---
title: "Doubao IME Voice Input: 语音输入后自动切回英文输入法"
author: "-"
date: 2026-10-15T12:45:02+08:00
lastmod: 2026-10-15T12:45:02+08:00
url: doubao-voice-auto-restore
categories:
  - Desktop
tags:
  - macos
  - input-method
  - hammerspoon
  - original
  - AI-assisted
---

## 问题

我平时在 macOS 上停在英文 ABC 输入法。[豆包输入法](./doubao-ime.md) 开了「跨输入法启用语音」后，在任何输入法下都能用快捷键唤起豆包的语音输入，我设置了两个键：

| 模式 | 快捷键 | 用途 |
| ---- | ------ | ---- |
| 按住说话，松开结束 | Fn | 短句 |
| 按一下开始，再按一下结束 | 右 Option | 长段 |

唤起时豆包会把系统输入法切到豆包拼音，语音结束后不会切回来。接下来打字就是中文，每次都要再按一下切回 ABC。

我想要的效果是：语音输入结束后自动回到唤起前的输入法。豆包当前版本没有这个选项，所以用 Hammerspoon 补上。

## 第一版：监听按键（不成功）

最直接的思路是监听快捷键：按下时记下当前输入法，结束时切回去。

- Fn 模式：松开即结束，不用记状态
- 右 Option 模式：数按键次数，按单数次记下输入法，按双数次切回

写好后按 Fn 测试，没有切回。在脚本里加了日志才看出两个问题。

### Hammerspoon 没有辅助功能权限

日志里 `hs.accessibilityState()` 一直是 `false`。权限要在「系统设置 → 隐私与安全性 → 辅助功能」里开，不是左侧栏顶层那个「辅助功能」（那里是 VoiceOver、缩放这类功能）。

开了之后还是 `false`，原因是 macOS 的这个权限只在进程启动时生效。我在设置里关了再开、删掉再加回来都没用，Hammerspoon 一直是开权限之前启动的那个进程。退出 Hammerspoon 再打开后，权限才变成 `true`。

### 豆包把 Fn 吞掉了

权限正常以后，Control、Caps Lock、右 Option 都能在日志里看到，Fn 一次都没有出现。我又用 `hs.eventtap.checkKeyboardModifiers()` 轮询 Fn 的按下状态，按住 Fn 说话的整个过程中也一直读到未按下。

所以豆包在更底层把 Fn 拦截了，Hammerspoon 拿不到这个键的任何信息，靠按键判断的方案走不通。右 Option 倒是能收到，但切换模式要数按键次数，如果用 Esc 或鼠标结束语音，计数就会错位。

## 第二版：看麦克风

换个角度：豆包语音输入时一定在用麦克风。我加了一个探针，同时记录输入法的切换和麦克风的占用状态，测了一次 Fn 模式：

| 时间 | 事件 |
| ---- | ---- |
| 21:33:41 | Caps Lock 切到 ABC |
| 21:33:43 | 按下 Fn，豆包把输入法切到豆包拼音 |
| 21:33:44 | 麦克风占用（开始听写） |
| 21:33:55 | 麦克风空闲（松开 Fn，听写结束） |

右 Option 模式的规律一样：开始时麦克风占用，结束时变回空闲。于是判断规则改成：

1. 用 `hs.keycodes.inputSourceChanged` 记下豆包切进来的时间，以及切换前的输入法
2. 每 0.2 秒查一次 `hs.audiodevice.defaultInputDevice():inUse()`
3. 豆包切进来后 5 秒内麦克风被占用，就算一次语音输入开始
4. 麦克风变回空闲，等 0.8 秒让豆包把文字上屏，再切回切换前的输入法

这里的 5 秒是「豆包切换输入法」到「麦克风开始工作」之间的间隔，实测只有 1～2 秒，和说话时长无关，只说一两个字也能正常切回。它的作用是区分两种情况：我自己手动切到豆包拼音打字时不会开麦，所以不会被切走。

这个方案不依赖任何按键，Fn 和右 Option 两种模式都适用。

## 配置

`~/.hammerspoon/init.lua`：

```lua
require("hs.ipc") -- allow `hs -c` from the command line
hs.autoLaunch(true) -- launch at login

-- Doubao IME switches the input source to itself for voice input and never
-- switches back. Doubao swallows the Fn key, so watch the mic instead:
-- Doubao switched in + mic in use shortly after = voice session started;
-- mic idle = session ended, restore the input source from before Doubao.

local DOUBAO = "com.bytedance.inputmethod.doubaoime"
local START_WINDOW = 5    -- seconds between Doubao switching in and mic turning on
local RESTORE_DELAY = 0.8 -- seconds to let Doubao commit the recognized text
local POLL = 0.2          -- mic polling interval in seconds

local function isDoubao(src) return src and src:find(DOUBAO, 1, true) ~= nil end

local lastSrc = hs.keycodes.currentSourceID() -- most recent non-Doubao source
local prevBeforeDoubao = nil
local doubaoSince = nil
local voiceActive, restoreTo = false, nil
local micWasInUse = false

doubaoSrcWatcher = hs.keycodes.inputSourceChanged(function()
  local cur = hs.keycodes.currentSourceID()
  if isDoubao(cur) then
    if not doubaoSince then
      doubaoSince = hs.timer.secondsSinceEpoch()
      prevBeforeDoubao = lastSrc
    end
  else
    lastSrc = cur
    doubaoSince = nil
  end
end)

doubaoMicTimer = hs.timer.doEvery(POLL, function()
  local dev = hs.audiodevice.defaultInputDevice()
  local inUse = dev and dev:inUse() or false
  if inUse == micWasInUse then return end
  micWasInUse = inUse

  if inUse then
    local cur = hs.keycodes.currentSourceID()
    if isDoubao(cur) and doubaoSince and prevBeforeDoubao
        and (voiceActive or restoreTo
             or hs.timer.secondsSinceEpoch() - doubaoSince <= START_WINDOW) then
      voiceActive, restoreTo = true, prevBeforeDoubao
    end
  elseif voiceActive then
    voiceActive = false
    local target = restoreTo
    hs.timer.doAfter(RESTORE_DELAY, function()
      if micWasInUse then return end -- talking again, wait for the next stop
      restoreTo = nil
      if isDoubao(hs.keycodes.currentSourceID()) then
        hs.keycodes.currentSourceID(target)
      end
    end)
  end
end)
```

仓库里的版本还带一个 `DEBUG` 开关，打开后把输入法切换和语音开始、结束写到 `~/.hammerspoon/debug.log`，排查问题时用。

`require("hs.ipc")` 让命令行可以直接查询 Hammerspoon 的状态，排查时很方便：

```bash
# accessibility granted? timer running? current input source?
hs -c 'print(hs.accessibilityState(), doubaoMicTimer:running(), hs.keycodes.currentSourceID())'
hs -c 'hs.reload()'
```

## 部署

我用 Ansible 装软件、chezmoi 管配置文件，这次也按这个分工：

- Ansible playbook `install-hammerspoon.yml`：`brew install --cask hammerspoon`，并打印需要手动完成的步骤
- chezmoi：`dot_hammerspoon/init.lua`，只在 macOS 上下发

新机器上的步骤：

1. `chezmoi apply`，下发 `~/.hammerspoon/init.lua`
2. `task install-hammerspoon`
3. 打开 Hammerspoon，在「隐私与安全性 → 辅助功能」里打开它，然后退出 Hammerspoon 再重新打开
4. 豆包设置里开启「跨输入法启用语音」，按住说话设为 Fn，切换模式设为右 Option

## 已知局限

- 开会时 Zoom、腾讯会议这类软件一直占着麦克风，麦克风不会变回空闲，也就不会切回，这时手动按 Caps Lock 切换
- 如果切回后文字只上屏了一半，调大 `RESTORE_DELAY`
- 外接键盘没有 Fn 键的话，在那块键盘上用不了按住说话的模式，右 Option 不受影响
