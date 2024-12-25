import os
import subprocess
import colors
from typing import List

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.extension.window_list import WindowList
from libqtile.layout.columns import Columns
from libqtile.layout.stack import Stack
from libqtile.layout.floating import Floating
from libqtile import hook, qtile
from subprocess import call

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration

mod = "mod4"
browser = "brave-browser"
terminal = "gnome-terminal"
font = "Awesome Font 6 Free Solid"

##### KEYBINDINGS #####
keys = [
    # Apps
    Key([mod], "b", lazy.spawn(browser),
        desc="Launch Brave"),
    Key([mod], "Return", lazy.spawn(terminal),
        desc="Launch Terminal"),
    Key([mod], "d", lazy.spawn('slack'),
        desc="Launch Discord"),
    Key([mod], "p", lazy.spawn('keepassxc'),
        desc="Launch Keepassxc"),
    Key([mod], "f", lazy.spawn('nautilus'),
        desc="Launch File Manager"),
    Key([mod], "v", lazy.spawn('virt-manager'),
        desc="Launch Virt-Manager"),
    Key([mod], "o", lazy.spawn('obs-studio'),
        desc="Launch OBS recorder"),
    Key([], "Print", lazy.spawn('flameshot gui'),
        desc="Launch Flameshot"),
    Key([mod], "s", lazy.spawn('slock'),
        desc="Launch Slock"),
  
    # Toggle floating and fullscreen
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen mode"),
    Key([mod, "shift"], "space", lazy.window.toggle_floating(),
        desc="Toggle fullscreen mode"),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(),
        desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(),
        desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(),
        desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(),
        desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(),
        desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(),
        desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(),
        desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    Key([mod, "shift"],"Return",lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(),
        desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(),
        desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(),
        desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(),
        desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    ]

##### GROUPS ######
groups = [
    Group('1', label="",
          matches=[Match(wm_class=browser)],
          layout="columns"),
    Group('2', label="",
          matches=[Match(wm_class=browser)],
          layout="columns"),
    Group('3', label="",
          matches=[Match(wm_class=terminal)],
          layout="columns"),
        Group('4', label=",",
          matches=[Match(wm_class='slack')],
          layout="columns"),
    Group('5', label="",
          matches=[Match(wm_class='nautilus')],
          layout="columns"),
    Group('6', label="",
          matches=[Match(wm_class='virt-manager')],
          layout="columns"),
        ]
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

###### LAYOUTS #######

layout_theme = {"border_width": 2,
                "margin": 4,
                "border_focus": colors.colors_nord["nord06"],
                "border_normal": colors.colors_nord["nord01"],
                }

layouts = [
    #layout.MonadTall(**layout_theme),
    layout.Columns(**layout_theme),    
    layout.Floating(**layout_theme)
]

widget_defaults = dict(
    font = font,
    fontsize = 15,
    padding = 5,
    foreground = colors.colors_nord["nord06"],
    background = colors.colors_nord["nord01"]
)

border_decorations_defaults = dict(
        colour = colors.colors_nord["nord09"],
        border_width = [0, 0, 0, 0],
        padding_x = None,
        padding_y = None)

extension_defaults = widget_defaults.copy()

###### SCREENS AND WIDGETS ######
screens = [
    Screen(
        wallpaper='~/Pictures/scarlet-tree.png',
        wallpaper_mode='fill',
        top=bar.Bar(
            [
                widget.GroupBox(
                       **widget_defaults,
                       active = colors.colors_nord["nord05"],
                       inactive = colors.colors_nord["nord04"],
                       rounded = False,
                       highlight_color = colors.colors_nord["nord01"],
                       highlight_method = "line",
                       this_current_screen_border = colors.colors_nord["nord08"],
                       this_screen_border = colors.colors_nord["nord09"],
                       other_current_screen_border = colors.colors_nord["nord10"],
                       other_screen_border = colors.colors_nord["nord10"],
                ),
                widget.Spacer(**widget_defaults),
                widget.WindowName(**widget_defaults),
                widget.Prompt(**widget_defaults),
                #widget.Systray(**widget_defaults), 
                widget.BatteryIcon(
                    theme_path = '~/.config/qtile/Assets/Battery/',
                    background = colors.colors_nord["nord01"],
                    scale      = 0.7,
                ),
                widget.Battery(
                    font       = font,
                    foreground = colors.colors_nord["nord07"],
                    background = colors.colors_nord["nord01"],
                    format='{percent:2.0%}',
                    decorations=[
                            BorderDecoration(**border_decorations_defaults)
                    ],
                ),
                widget.Clock(
                    format=" %d-%m-%Y  %I:%M %p",
                    foreground = colors.colors_nord["nord09"],
                    background = colors.colors_nord["nord01"],
                    decorations=[
                            BorderDecoration(**border_decorations_defaults)
                       ],
                       ),
                widget.CPU(
                    format     = ' {freq_current}GHz, {load_percent}%',
                    foreground = colors.colors_nord["nord12"],
                    background = colors.colors_nord["nord01"],
                    decorations=[
                           BorderDecoration(**border_decorations_defaults)
                       ],
                       ),
                widget.DF(
                 update_interval = 60,
                 foreground = colors.colors_nord["nord11"],
                 partition = '/',
                 format = '{uf}{m} free',
                 fmt = '🖴  {}',
                 visible_on_warn = False,
                 decorations=[
                           BorderDecoration(**border_decorations_defaults)
                    ],
                    ),
                widget.Memory(
                    foreground = colors.colors_nord["nord13"],
                    background = colors.colors_nord["nord01"],
                    fmt        = '  {}',
                    measure_mem= 'G',
                    decorations=[
                           BorderDecoration(**border_decorations_defaults)
                       ],
                       ),
            ],
            20,
             margin = [0, 4, 0, 4],  # Draw top and bottom borders
             border_color = ["#ebcb8b", "#ebcb8b", "#ebcb8b", "#ebcb8b"],  
             #opacity=0.8,
             background = colors.colors_nord["nord09"],
        ),
    ),
    Screen(
        wallpaper='~/Pictures/scarlet-tree.png',
        wallpaper_mode='fill',
        top=bar.Bar(
            [
                widget.GroupBox(
                       **widget_defaults,
                       active = colors.colors_nord["nord05"],
                       inactive = colors.colors_nord["nord04"],
                       rounded = False,
                       highlight_color = colors.colors_nord["nord01"],
                       highlight_method = "line",
                       this_current_screen_border = colors.colors_nord["nord08"],
                       this_screen_border = colors.colors_nord["nord09"],
                       other_current_screen_border = colors.colors_nord["nord10"],
                       other_screen_border = colors.colors_nord["nord10"],
                ),
                widget.Spacer(**widget_defaults),
                widget.WindowName(**widget_defaults),
                widget.Prompt(**widget_defaults),
                widget.BatteryIcon(
                    theme_path = '~/.config/qtile/Assets/Battery/',
                    background = colors.colors_nord["nord01"],
                    scale      = 0.7,
                ),
                widget.Battery(
                    font       = font,
                    foreground = colors.colors_nord["nord07"],
                    background = colors.colors_nord["nord01"],
                    format='{percent:2.0%}',
                    decorations=[
                            BorderDecoration(**border_decorations_defaults)
                    ],
                ),

                widget.Clock(
                    format=" %d-%m-%Y  %I:%M %p",
                    foreground = colors.colors_nord["nord09"],
                    background = colors.colors_nord["nord01"],
                    decorations=[
                           BorderDecoration(**border_decorations_defaults)
                       ],
                       ),
                widget.CPU(
                    format = ' {freq_current}GHz, {load_percent}%',
                    foreground = colors.colors_nord["nord12"],
                    background = colors.colors_nord["nord01"],
                    decorations=[
                           BorderDecoration(**border_decorations_defaults)
                       ],
                       ),
                widget.DF(
                 update_interval = 60,
                 foreground = colors.colors_nord["nord11"],
                 partition = '/',
                 format = '{uf}{m} free',
                 fmt = '🖴  {}',
                 visible_on_warn = False,
                 decorations=[
                           BorderDecoration(**border_decorations_defaults)
                    ],
                    ),
                widget.Memory(
                       foreground = colors.colors_nord["nord13"],
                       background = colors.colors_nord["nord01"],
                       fmt = '  {}',
                       measure_mem = 'G',
                       decorations=[
                           BorderDecoration(**border_decorations_defaults)
                       ],
                       ),
            ],
            20,
             margin = [0, 4, 0, 4],  # Draw top and bottom borders
             border_color = ["#ebcb8b", "#ebcb8b", "#ebcb8b", "#ebcb8b"],  
             #opacity=0.8,
             background = colors.colors_nord["nord09"],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"

