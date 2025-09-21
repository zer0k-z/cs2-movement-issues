# Warning: Now obsolete as exec_async is patched to stop working when sv_cheats is 0.

### Usage:
1. Put `ak47.cfg` and `loop.cfg` inside `cfg` folder
2. In the main menu, open console and type `exec ak47`

`ak47.cfg` will run `exec_async loop`, which fires an alias that runs every ~10ms[^1] for 11.5 minutes (not forever because file size is limited at 1 MB). Press `c` to start firing, press `v` to stop early. When the script starts firing, your fps will be limited at 125 because the script depends a lot on FPS values.

- If you don't have at least a stable 125 fps, this script does not work.
- It's possible to make it run for unlimited amount of time, but you would need to create and queue up another file that starts with a `sleep` with a large value.
- Unlike a real cheat, the auto-recoil does not compensate for inaccuracy because it is not able to compensate for RNG ahead of time. **You won't have perfect accuracy using this script**. The real cheats can manipulate the RNG and tell the server where the bullet will hit, this cannot.
- If you test with `weapon_accuracy_nospread true`, you might still see some inaccuracy. This is because nospread doesn't actually remove all spread of a weapon and there's another spread modifier that is unaffected by this convar.
- **Use it at your own risk!** People have been VAC banned in the past for spamming `yaw` and `pitch` commands to snap to angles, which falsely triggered the anticheat.

[^1]: It actually waits more than 10ms on 125fps for some reason.