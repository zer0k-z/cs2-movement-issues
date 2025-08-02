# Bhopping branch notes (2025/07/31)

The bhopping branch introduced in 2025/07/31 update makes a few changes to, as the name suggests, several functions related to bhopping related mechanics. Most relevant function is the jump button check, as demonstrated by the following reverse engineered function:

```c++
/* Notes:
	this->m_bButtons[0] & IN_JUMP means the jump button is currently pressed.
	IsButtonNewlyPressed returns true when the jump input is newly pressed (IN_BUTTON_UP_DOWN, IN_BUTTON_UP_DOWN_UP, IN_BUTTON_DOWN_UP_DOWN, IN_BUTTON_DOWN_UP_DOWN_UP, IN_BUTTON_UP_DOWN_UP_DOWN)
	Scrolling will result in IN_BUTTON_UP_DOWN_UP, normal newly pressed jump using spacebars will result in IN_BUTTON_UP_DOWN.
*/

// Old version
void CCSPlayer_MovementServices::CheckJumpButton(CMoveData *mv)
{
    if (this->m_bButtons[0] & IN_JUMP || this->IsButtonNewlyPressed(IN_JUMP))  
    {
        if (this->m_bOldJumpPressed) 
        {
            float nextPossibleJumpTime = sv_jump_spam_penalty_time.Get() + this->m_flJumpPressedTime;
            
            if (gpGlobals->curtime > nextPossibleJumpTime)
            {
                this->m_bOldJumpPressed = false;
            }
			// Note: HandleJump does nothing if the jump button is held (and not newly pressed)
            this->HandleJump(mv);
        }
        else if (sv_autobunnyhopping.Get())
        {
            this->HandleJump(mv);
        }
        this->m_bOldJumpPressed = true;
        this->m_flJumpPressedTime = gpGlobals->curtime;
    }
}

// New version
void CCSPlayer_MovementServices::CheckJumpButton(CMoveData *mv)
{
    if (this->m_bButtons[0] & IN_JUMP || this->IsButtonNewlyPressed(IN_JUMP))  
    {
        if (this->m_bOldJumpPressed) 
        {
            float nextPossibleJumpTime = sv_jump_spam_penalty_time.Get() + this->m_flJumpPressedTime;
            
            if (gpGlobals->curtime > nextPossibleJumpTime)
            {
                this->m_bOldJumpPressed = false;
            }
            this->HandleJump(mv);
        }
        else if (sv_autobunnyhopping.Get())
        {
            this->HandleJump(mv);
        }
        this->m_bOldJumpPressed = true;
        if (this->IsButtonNewlyPressed(IN_JUMP)) // <- This is new
        {
            this->m_flJumpPressedTime = gpGlobals->curtime - gpGlobals->frametime;
        }
    }
}
```

The jump pressed time has been shifted from the end of the movement step to the start of the movement step instead, reducing the effective cooldown between valid inputs. The cooldown is now actually 0.015625 now, and not a ranging value from 0.015625 to 0.03125. (Still not 0.01171875 like CSGO 128 tick, but again it is not viable to go under 0.015625, as mentioned in the original README)

This effectively fixed the jump cooldown input issue as mentioned in the README article; however, the way it was fixed creates new avenue for exploit.

### The desubtick exploit
As mentioned in the initial README, with `sv_jump_spam_penalty_time` just ever so slightly smaller than 1/64th of a second, you can achieve effectively 100% perf rate[^1] with desubticked jumps. 

With the new update, even this value will cause 100% perfect bhops.

In order to better understand how this happens, we need to understand what happens when an input is desubticked.
#### Desubtick
Desubticking inputs buffer to the very start of the next tick, guaranteeing them to be executed first in the next tick.

For instance, normally when the player presses W at tick 1.23, the packet responsible for simulating all movement between tick 1 and 2 will contain this input with the `when` field value equals to 0.23.

With desubticking, the input will be buffered to 2.0 instead and sent as part of the next packet, with the `when` value equal to 0.0.

This effectively makes every jump (and every desubticked input) input to be at least 0.015625 away from each other. But in the public version, this means `gpGlobals->curtime > nextPossibleJumpTime` will never be true if the player scrolls too fast with desubtick. They will always be equal, never greater, so they cannot perform jump every tick.

To get around this, players could desubtick and set their maximum framerate to 32 in order to ensure this condition always pass and allow 100% perfect bhop rate on flat ground. (see [this video](https://www.youtube.com/watch?v=FbfGp_oemUQ) for demonstration, keep in mind that newer NVIDIA drivers and all AMD drivers will no longer allow fps lower than 64)

The new update now subtract `m_flJumpPressedTime` by `frametime` (which is always greater than 0), ensuring that `m_flJumpPressedTime + 0.015625` will *always* be smaller than `curtime`, making `gpGlobals->curtime > nextPossibleJumpTime` always pass, allowing them to be able to jump on every tick. As long as the player do not have other subtick inputs[^2], they will hit 100% perfect bhops.

Using scripts that desubticks or automatically executes inputs (see bhopping_scripts folder), you can create autobhops scripts that enables perfect autobhop.

# Conclusion (TL;DR)

#### Pros
- Jump cooldown is effectively lowered.

#### Cons
- More exploits using desubtick/exec_async and low fps.

#### Things that haven't changed
- Perfect bhops are still RNG (more RNG than ever, in fact, because of `sv_subtick_movement_view_angles`...?)

[^1]: This is actually not fully accurate, see [2]

[^2]: Any other input might cause you to land on the ground before you get the chance to hit the perfect bhop, see the section related to perf window in the original README. `sv_subtick_movement_view_angles true` also causes the game to generate extra inputs if the client predicts that the player will be on the ground. The higher the fps, the more subtick inputs generated, the higher chance the player gets their speed clamped on the ground, the more likely you will fail a perfect bhop with desubtick inputs. Alternatively, player can completely stop turning before landing, preventing from subtick view angles inputs from being generated.