# GlazeWM on the Windows Laptop

Brief written 2026-09-07 on bespin. **Purpose: paste this whole note into a Claude Code
session running on the Windows laptop.** It carries over the AeroSpace setup from the Mac
(`~/code/bespin/dotfiles/aerospace.toml`) so the muscle memory transfers.

Companion note: the Mac side is documented in this vault and in `bespin/CLAUDE.md`.

---

## Goal

Reproduce the bespin AeroSpace experience on Windows using **GlazeWM v3**:
Omarchy-style keybindings, **Alt as the mod key**, letter-named workspaces that each own
one app, 10px gaps, a focused-window border, and a handful of apps that float instead of
tiling.

GlazeWM was chosen over komorebi because it is a single declarative YAML file that holds
keybindings, gaps, workspaces and window rules together — the closest structural match to
`aerospace.toml`. komorebi needs komorebi.json + whkd + often an AHK shim for the same job.

---

## Install

```powershell
winget install glzr-io.glazewm
```

- Config lives at `%USERPROFILE%\.glzr\glazewm\config.yaml` (v3 path; v2's
  `~/.glaze-wm/` is dead).
- Override with `GLAZEWM_CONFIG_PATH` or `glazewm.exe start --config="..."`.
- Reload config with the `wm-reload-config` command — **no restart needed**, the same
  fast edit→reload loop as `alt-shift-;` → `esc` on the Mac.
- Set it to run at login (Startup folder shortcut or Task Scheduler).
---

## The Mac config being ported

Read this before writing anything — it is the source of truth for intent.

**Alt is SUPER.** On macOS this was forced (Cmd is reserved by the OS). On Windows it is
a free choice, and it should stay Alt so the two machines match. It is also GlazeWM's own
default.

**Workspaces are named by letter, one app each. Numbers 1–4 are scratch:**

| Key         | WS  | App (macOS)                      | Windows equivalent                                       |
| ----------- | --- | -------------------------------- | -------------------------------------------------------- |
| `alt+enter` | T   | Ghostty                          | Powershell                                               |
| `alt+b`     | B   | Zen                              | Firefox                                                  |
| `alt+o`     | O   | Obsidian                         | Obsidian                                                 |
| `alt+g`     | G   | Google Messages (Safari web app) | Edge PWA: `msedge --app=https://messages.google.com/web` |
| `alt+m`     | M   | Spotify                          | Need to create Spotify webapp                            |
| `alt+p`     | P   | Proton Mail (Safari web app)     | Need to create Proton Mail webapp                        |
| `alt+a`     | A   | Claude                           | Claude for Windows                                       |

`alt+shift+<same letter>` moves the focused window to that workspace.
Letters deliberately avoid a separate "go there" binding — the launcher key does both.

**Floating, no home workspace** (they overlay whatever you're doing rather than reflowing
it): Finder→**Explorer**, Todoist, Proton Pass, 1Password, System Settings→**Settings**,
Activity Monitor→**Task Manager**. Safari's float rule has no Windows analogue; drop it.

**Other keys:** `alt+f` file manager · `alt+/` Proton Pass · `alt+l` Todoist ("L for
list" — `alt+t` was taken by the terminal workspace) · `alt+k` keymap cheatsheet ·
`alt+d` Dozzle at `http://10.10.10.35:8888` · `alt+space` launcher · `alt+w` close ·
arrows to focus, `alt+shift+arrows` to move · `alt+j` toggle split orientation ·
`alt+shift+v` toggle float · `alt+-`/`alt+=` width, shifted for height.

---

## GlazeWM v3 syntax cheatsheet

Verified against `glzr-io/glazewm` `resources/assets/sample-config.yaml`, 2026-09-07.
**Do not trust older blog posts or the v2 docs** — v2 used `command:` +
`match_process_name:` and that syntax is gone.

```yaml
general:
  startup_commands: []
  shutdown_commands: []
  config_reload_commands: []
  focus_follows_cursor: false
  toggle_workspace_on_refocus: false
  cursor_jump: { enabled: true, trigger: 'monitor_focus' }
  hide_method: 'cloak'        # recommended on Windows; 'hide' is buggy
  show_all_in_taskbar: false

gaps:
  scale_with_dpi: true
  inner_gap: '10px'
  outer_gap: { top: '10px', right: '10px', bottom: '10px', left: '10px' }

window_effects:
  focused_window:
    border: { enabled: true, color: '#8dbcff' }   # replaces JankyBorders — Win11 only
  other_windows:
    border: { enabled: false, color: '#a1a1a1' }

window_behavior:
  initial_state: 'tiling'
  state_defaults:
    floating: { centered: true, shown_on_top: false }

workspaces:
  - name: 'T'
    keep_alive: true          # <- the equivalent of persistent-workspaces

window_rules:
  - commands: ['move --workspace B', 'focus --workspace B']
    match:
      - window_process: { equals: 'zen' }
  - commands: ['set-floating']
    match:
      - window_process: { equals: 'explorer' }
  - commands: ['ignore']
    match:
      - window_title: { regex: '[Pp]icture.in.[Pp]icture' }

binding_modes:
  - name: 'resize'
    keybindings:
      - commands: ['resize --width -2%']
        bindings: ['h', 'left']
      - commands: ['wm-disable-binding-mode --name resize']
        bindings: ['escape', 'enter']

keybindings:
  - commands: ['focus --direction left']
    bindings: ['alt+left']
  - commands: ['move --workspace 1', 'focus --workspace 1']
    bindings: ['alt+shift+1']
  - commands: ['shell-exec wt']
    bindings: ['alt+enter']
```

Match operators: `equals`, `regex`, `not_regex` on `window_process`, `window_title`,
`window_class`. Multiple `- ` entries under `match:` are OR'd; keys within one entry are
AND'd.

Commands worth knowing: `focus --direction|--workspace|--next-active-workspace|
--prev-active-workspace|--recent-workspace`, `move --direction|--workspace`,
`move-workspace --direction`, `resize --width|--height`, `toggle-floating --centered`,
`toggle-tiling`, `toggle-fullscreen`, `toggle-minimized`, `toggle-tiling-direction`,
`close`, `shell-exec`, `ignore`, `set-floating`, `wm-cycle-focus`, `wm-reload-config`,
`wm-redraw`, `wm-toggle-pause`, `wm-exit`, `wm-enable/disable-binding-mode --name`.

---

## Mapping table: AeroSpace → GlazeWM

| AeroSpace | GlazeWM |
|---|---|
| `persistent-workspaces = [...]` | `workspaces:` list with `keep_alive: true` |
| `[[on-window-detected]]` + `if.app-id` | `window_rules:` + `window_process: { equals: }` |
| `run = ['layout floating']` | `commands: ['set-floating']` |
| `move-node-to-workspace X` | `move --workspace X` |
| `... --focus-follows-window` | `['move --workspace X', 'focus --workspace X']` |
| `workspace X` | `focus --workspace X` |
| `focus left` | `focus --direction left` |
| `move left` | `move --direction left` |
| `layout horizontal vertical` (alt-j) | `toggle-tiling-direction` |
| `layout floating tiling` (alt-shift-v) | `toggle-floating --centered` |
| `fullscreen` | `toggle-fullscreen` |
| `resize width +50` | `resize --width +2%` (percentages, not px) |
| `exec-and-forget open -a Foo` | `shell-exec foo` — **see gotcha below** |
| `mode service` / `reload-config` | `binding_modes:` / `wm-reload-config` |
| `[gaps] inner.horizontal` etc. | `gaps.inner_gap` / `gaps.outer_gap` |
| JankyBorders (`exec borders`) | `window_effects.focused_window.border` (built in) |
| `move-node-to-monitor next` | `move-workspace --direction right` (moves the *workspace*) |

---

## Gotchas to solve on the laptop — read before writing config

1. **`shell-exec` launches, it does not focus.** This is the one genuine behavioural gap.
   On macOS `open -a Foo` focuses a running app and launches it only if needed, which is
   what makes `alt+b` work as both "launch browser" and "go to my browser". `shell-exec`
   will happily start a *second* Zen every press.
   **Fix:** write a small PowerShell helper (e.g. `%USERPROFILE%\.glzr\launch.ps1`) that
   does `Get-Process <name> -ErrorAction SilentlyContinue` and only `Start-Process`es if
   nothing is running, then bind
   `['focus --workspace B', 'shell-exec powershell -WindowStyle Hidden -File ... zen']`.
   Test this early — everything else is mechanical, this is the part that needs thought.

2. **Windows owns Alt+Tab.** The Mac config has `alt-tab = workspace next` (free there
   because macOS uses Cmd+Tab). On Windows Alt+Tab is the OS switcher and GlazeWM cannot
   reliably take it. Use `focus --next-active-workspace` / `--prev-active-workspace` on
   different keys — the sample config puts them on `alt+s` / `alt+a`, but **`alt+a` is
   the Claude workspace here**, so pick something else. `alt+.` / `alt+,` is a reasonable
   pair. `focus --recent-workspace` replaces `workspace-back-and-forth`.

3. **Other Alt keys Windows claims:** `alt+space` (system menu — GlazeWM does override it,
   the sample uses it for `wm-cycle-focus`), `alt+F4` (close), `alt+esc`. Alt alone
   activates the menu bar in many apps; harmless but you'll see it flash.

4. **`window_process` is the process name without `.exe`.** Get real values with
   `Get-Process | Select-Object ProcessName, MainWindowTitle | Where-Object MainWindowTitle`
   while each app is open. Don't guess — `zen`, `Obsidian`, `Spotify`, `codium`, `claude`,
   `Todoist`, `msedge`. Electron apps often need `window_class` too.

5. **PWAs share one process.** Google Messages and Proton Mail as Edge PWAs both run as
   `msedge`, so they cannot be told apart by process — match on `window_title` instead
   (`{ regex: 'Google Messages' }`). Same class of problem as the Safari web apps on the
   Mac, where the bundle id was a per-install UUID and name-matching was the answer.

6. **No Raycast on Windows.** `alt+space` on the Mac opens Raycast. Windows options are
   PowerToys Run (`alt+space` by default — will collide, pick one) or Flow Launcher.
   Ask Jason before installing either.

7. **Resize is percentage-based**, not the Mac's ±50px. `--width -2%` per press feels
   about right; tune after using it.

8. **Multi-monitor differs.** AeroSpace's `move-node-to-monitor next` moves a *window*;
   GlazeWM's `move-workspace --direction` moves a whole *workspace* to another monitor.
   Not a like-for-like port — mention it rather than papering over it.

9. **Ghostty does not exist on Windows.** Use powershell

---

## Approach for the laptop session

1. Confirm the terminal and launcher choices with Jason before installing anything.
2. Install GlazeWM, let it generate the default config, and **back that up** before
   overwriting.
3. Collect real `window_process` / `window_class` / `window_title` values for every app in
   the table above. Do this *first* — every window rule depends on it.
4. Write `config.yaml`, keeping the Mac file's comment style: explain *why* a rule exists,
   not just what it does. That commentary is why the Mac config survived six revisions.
5. Solve the focus-or-launch helper (gotcha #1), then bind the letter keys.
6. Reload with `wm-reload-config` and walk every binding once.
7. Version-control it. The Mac keeps its config in the `bespin` repo; consider a small
   `windows-wm` repo, or a `windows/` directory in an existing one, so it isn't only on
   the laptop.
8. Update this note and the Homelab note in the vault when it's working.

---

## Sources

- [glzr-io/glazewm](https://github.com/glzr-io/glazewm)
- [sample-config.yaml](https://github.com/glzr-io/glazewm/blob/main/resources/assets/sample-config.yaml)
- [glazewm.com](https://glazewm.com/)
