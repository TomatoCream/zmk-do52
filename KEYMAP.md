# ZMK Complete Key Reference

Sourced directly from the ZMK headers in this workspace:
- `zmk/app/include/dt-bindings/zmk/keys.h`
- `zmk/app/include/dt-bindings/zmk/modifiers.h`
- `zmk/app/include/dt-bindings/zmk/mouse.h`
- `zmk/app/include/dt-bindings/zmk/bt.h`
- `zmk/app/include/dt-bindings/zmk/ext_power.h`

Aliases marked *(deprecated)* exist but should not be used in new keymaps.

---

## Alphabet

| Key   | Preferred Code | Aliases |
|-------|----------------|---------|
| a / A | `A`            |         |
| b / B | `B`            |         |
| c / C | `C`            |         |
| d / D | `D`            |         |
| e / E | `E`            |         |
| f / F | `F`            |         |
| g / G | `G`            |         |
| h / H | `H`            |         |
| i / I | `I`            |         |
| j / J | `J`            |         |
| k / K | `K`            |         |
| l / L | `L`            |         |
| m / M | `M`            |         |
| n / N | `N`            |         |
| o / O | `O`            |         |
| p / P | `P`            |         |
| q / Q | `Q`            |         |
| r / R | `R`            |         |
| s / S | `S`            |         |
| t / T | `T`            |         |
| u / U | `U`            |         |
| v / V | `V`            |         |
| w / W | `W`            |         |
| x / X | `X`            |         |
| y / Y | `Y`            |         |
| z / Z | `Z`            |         |

---

## Numbers & Shifted Symbols

Each physical key produces two characters depending on Shift.

| Char | Preferred Code | Full Name           | Aliases                |
|------|----------------|---------------------|------------------------|
| 1    | `N1`           | `NUMBER_1`          | `NUM_1` *(deprecated)* |
| !    | `EXCL`         | `EXCLAMATION`       | `BANG` *(deprecated)*  |
| 2    | `N2`           | `NUMBER_2`          | `NUM_2` *(deprecated)* |
| @    | `AT`           | `AT_SIGN`           | `ATSN` *(deprecated)*  |
| 3    | `N3`           | `NUMBER_3`          | `NUM_3` *(deprecated)* |
| #    | `HASH`         | `HASH`              | `POUND`                |
| 4    | `N4`           | `NUMBER_4`          | `NUM_4` *(deprecated)* |
| $    | `DLLR`         | `DOLLAR`            |                        |
| 5    | `N5`           | `NUMBER_5`          | `NUM_5` *(deprecated)* |
| %    | `PRCNT`        | `PERCENT`           | `PRCT` *(deprecated)*  |
| 6    | `N6`           | `NUMBER_6`          | `NUM_6` *(deprecated)* |
| ^    | `CARET`        | `CARET`             | `CRRT` *(deprecated)*  |
| 7    | `N7`           | `NUMBER_7`          | `NUM_7` *(deprecated)* |
| &    | `AMPS`         | `AMPERSAND`         |                        |
| 8    | `N8`           | `NUMBER_8`          | `NUM_8` *(deprecated)* |
| *    | `ASTRK`        | `ASTERISK`          | `STAR`                 |
| 9    | `N9`           | `NUMBER_9`          | `NUM_9` *(deprecated)* |
| (    | `LPAR`         | `LEFT_PARENTHESIS`  | `LPRN` *(deprecated)*  |
| 0    | `N0`           | `NUMBER_0`          | `NUM_0` *(deprecated)* |
| )    | `RPAR`         | `RIGHT_PARENTHESIS` | `RPRN` *(deprecated)*  |

---

## Symbols & Punctuation

| Char | Preferred Code | Full Name          | Notes                                       |
|------|----------------|--------------------|---------------------------------------------|
| -    | `MINUS`        | `MINUS`            |                                             |
| _    | `UNDER`        | `UNDERSCORE`       |                                             |
| =    | `EQUAL`        | `EQUAL`            | `EQL` *(deprecated)*                        |
| +    | `PLUS`         | `PLUS`             |                                             |
| [    | `LBKT`         | `LEFT_BRACKET`     |                                             |
| {    | `LBRC`         | `LEFT_BRACE`       | `LCUR` *(deprecated)*                       |
| ]    | `RBKT`         | `RIGHT_BRACKET`    |                                             |
| }    | `RBRC`         | `RIGHT_BRACE`      | `RCUR` *(deprecated)*                       |
| \    | `BSLH`         | `BACKSLASH`        |                                             |
| \|   | `PIPE`         | `PIPE`             |                                             |
| #~   | `NUHS`         | `NON_US_HASH`      | Non-US layout                               |
| ~²   | `TILDE2`       |                    | Non-US shifted hash                         |
| ;    | `SEMI`         | `SEMICOLON`        | `SCLN` *(deprecated)*                       |
| :    | `COLON`        | `COLON`            | `COLN` *(deprecated)*                       |
| '    | `SQT`          | `SINGLE_QUOTE`     | `APOSTROPHE`, `APOS`; `QUOT` *(deprecated)* |
| "    | `DQT`          | `DOUBLE_QUOTES`    |                                             |
| \`   | `GRAVE`        | `GRAVE`            | `GRAV` *(deprecated)*                       |
| ~    | `TILDE`        | `TILDE`            | `TILD` *(deprecated)*                       |
| ,    | `COMMA`        | `COMMA`            | `CMMA` *(deprecated)*                       |
| <    | `LT`           | `LESS_THAN`        | `LABT` *(deprecated)*                       |
| .    | `DOT`          | `PERIOD`           |                                             |
| >    | `GT`           | `GREATER_THAN`     | `RABT` *(deprecated)*                       |
| /    | `FSLH`         | `SLASH`            |                                             |
| ?    | `QMARK`        | `QUESTION`         |                                             |
| \|²  | `PIPE2`        |                    | Non-US backslash+pipe shifted               |
| \|³  | `NON_US_BSLH`  | `NON_US_BACKSLASH` | `NUBS`                                      |

---

## Control & Editing

| Key                | Preferred Code | Aliases                              |
|--------------------|----------------|--------------------------------------|
| Enter / Return     | `RET`          | `RETURN`, `ENTER`                    |
| Escape             | `ESC`          | `ESCAPE`                             |
| Backspace          | `BSPC`         | `BACKSPACE`; `BKSP` *(deprecated)*   |
| Tab                | `TAB`          |                                      |
| Space              | `SPACE`        | `SPC` *(deprecated)*                 |
| Delete (forward)   | `DEL`          | `DELETE`                             |
| Insert             | `INS`          | `INSERT`                             |
| Caps Lock          | `CAPS`         | `CAPSLOCK`, `CLCK`                   |
| Print Screen       | `PSCRN`        | `PRINTSCREEN`; `PRSC` *(deprecated)* |
| Scroll Lock        | `SLCK`         | `SCROLLLOCK`; `SCLK` *(deprecated)*  |
| Pause / Break      | `PAUSE_BREAK`  | `PAUS` *(deprecated)*                |
| Alternate Erase    | `ALT_ERASE`    |                                      |
| SysRq / Attention  | `SYSREQ`       | `ATTENTION`                          |
| Cancel             | `K_CANCEL`     |                                      |
| Clear              | `CLEAR`        |                                      |
| Prior              | `PRIOR`        |                                      |
| Return (alternate) | `RET2`         | `RETURN2`                            |
| Separator          | `SEPARATOR`    |                                      |
| Out                | `OUT`          |                                      |
| Oper               | `OPER`         |                                      |
| Clear/Again        | `CLEAR_AGAIN`  |                                      |
| CrSel/Props        | `CRSEL`        |                                      |
| ExSel              | `EXSEL`        |                                      |

---

## Navigation

| Key         | Preferred Code | Aliases                              |
|-------------|----------------|--------------------------------------|
| Left Arrow  | `LEFT`         | `LEFT_ARROW`; `LARW` *(deprecated)*  |
| Right Arrow | `RIGHT`        | `RIGHT_ARROW`; `RARW` *(deprecated)* |
| Up Arrow    | `UP`           | `UP_ARROW`; `UARW` *(deprecated)*    |
| Down Arrow  | `DOWN`         | `DOWN_ARROW`; `DARW` *(deprecated)*  |
| Home        | `HOME`         |                                      |
| End         | `END`          |                                      |
| Page Up     | `PG_UP`        | `PAGE_UP`; `PGUP` *(deprecated)*     |
| Page Down   | `PG_DN`        | `PAGE_DOWN`; `PGDN` *(deprecated)*   |

---

## Function Keys

| Key | Code  |
|-----|-------|
| F1  | `F1`  |
| F2  | `F2`  |
| F3  | `F3`  |
| F4  | `F4`  |
| F5  | `F5`  |
| F6  | `F6`  |
| F7  | `F7`  |
| F8  | `F8`  |
| F9  | `F9`  |
| F10 | `F10` |
| F11 | `F11` |
| F12 | `F12` |
| F13 | `F13` |
| F14 | `F14` |
| F15 | `F15` |
| F16 | `F16` |
| F17 | `F17` |
| F18 | `F18` |
| F19 | `F19` |
| F20 | `F20` |
| F21 | `F21` |
| F22 | `F22` |
| F23 | `F23` |
| F24 | `F24` |

---

## Modifiers

### Modifier Keys

| Key                      | Preferred Code | Aliases                                                                          |
|--------------------------|----------------|----------------------------------------------------------------------------------|
| Left Control             | `LCTRL`        | `LEFT_CONTROL`; `LCTL` *(deprecated)*                                            |
| Left Shift               | `LSHFT`        | `LEFT_SHIFT`, `LSHIFT`; `LSFT` *(deprecated)*                                    |
| Left Alt                 | `LALT`         | `LEFT_ALT`                                                                       |
| Left GUI (Win/Cmd/Meta)  | `LGUI`         | `LEFT_GUI`, `LEFT_WIN`, `LWIN`, `LEFT_COMMAND`, `LCMD`, `LEFT_META`, `LMETA`     |
| Right Control            | `RCTRL`        | `RIGHT_CONTROL`; `RCTL` *(deprecated)*                                           |
| Right Shift              | `RSHFT`        | `RIGHT_SHIFT`, `RSHIFT`; `RSFT` *(deprecated)*                                   |
| Right Alt                | `RALT`         | `RIGHT_ALT`                                                                      |
| Right GUI (Win/Cmd/Meta) | `RGUI`         | `RIGHT_GUI`, `RIGHT_WIN`, `RWIN`, `RIGHT_COMMAND`, `RCMD`, `RIGHT_META`, `RMETA` |

### Modifier Combinators

Apply a held modifier to any key. Can be chained: `LC(LS(A))`.

| Modifier            | Code      | Example           |
|---------------------|-----------|-------------------|
| Left Control + key  | `LC(key)` | `LC(C)` = Ctrl+C  |
| Left Shift + key    | `LS(key)` | `LS(A)` = Shift+A |
| Left Alt + key      | `LA(key)` | `LA(F4)` = Alt+F4 |
| Left GUI + key      | `LG(key)` | `LG(L)` = Win+L   |
| Right Control + key | `RC(key)` |                   |
| Right Shift + key   | `RS(key)` |                   |
| Right Alt + key     | `RA(key)` | `RA(E)` = AltGr+E |
| Right GUI + key     | `RG(key)` |                   |

---

## Keypad / Numpad

| Key               | Preferred Code   | Aliases                              |
|-------------------|------------------|--------------------------------------|
| Num Lock / Clear  | `KP_NUM`         | `KP_NUMLOCK`, `KP_NLCK`              |
| Keypad Clear      | `KP_CLEAR`       |                                      |
| Keypad /          | `KP_DIVIDE`      | `KP_SLASH`; `KDIV` *(deprecated)*    |
| Keypad *          | `KP_MULTIPLY`    | `KP_ASTERISK`; `KMLT` *(deprecated)* |
| Keypad -          | `KP_MINUS`       | `KP_SUBTRACT`; `KMIN` *(deprecated)* |
| Keypad +          | `KP_PLUS`        | `KPLS` *(deprecated)*                |
| Keypad Enter      | `KP_ENTER`       |                                      |
| Keypad =          | `KP_EQUAL`       |                                      |
| Keypad = (AS/400) | `KP_EQUAL_AS400` |                                      |
| Keypad .          | `KP_DOT`         |                                      |
| Keypad ,          | `KP_COMMA`       |                                      |
| Keypad (          | `KP_LPAR`        | `KP_LEFT_PARENTHESIS`                |
| Keypad )          | `KP_RPAR`        | `KP_RIGHT_PARENTHESIS`               |
| Keypad 0          | `KP_N0`          | `KP_NUMBER_0`                        |
| Keypad 1          | `KP_N1`          | `KP_NUMBER_1`                        |
| Keypad 2          | `KP_N2`          | `KP_NUMBER_2`                        |
| Keypad 3          | `KP_N3`          | `KP_NUMBER_3`                        |
| Keypad 4          | `KP_N4`          | `KP_NUMBER_4`                        |
| Keypad 5          | `KP_N5`          | `KP_NUMBER_5`                        |
| Keypad 6          | `KP_N6`          | `KP_NUMBER_6`                        |
| Keypad 7          | `KP_N7`          | `KP_NUMBER_7`                        |
| Keypad 8          | `KP_N8`          | `KP_NUMBER_8`                        |
| Keypad 9          | `KP_N9`          | `KP_NUMBER_9`                        |

---

## System

| Action                     | Preferred Code  | Aliases                                                            |
|----------------------------|-----------------|--------------------------------------------------------------------|
| System Power Down          | `SYS_PWR`       | `SYSTEM_POWER`                                                     |
| System Sleep               | `SYS_SLEEP`     | `SYSTEM_SLEEP`                                                     |
| System Wake Up             | `SYS_WAKE`      | `SYSTEM_WAKE_UP`                                                   |
| Keyboard Power             | `K_PWR`         | `K_POWER`                                                          |
| Application / Context Menu | `K_APP`         | `K_APPLICATION`, `K_CONTEXT_MENU`, `K_CMENU`; `GUI` *(deprecated)* |
| Execute                    | `K_EXEC`        | `K_EXECUTE`                                                        |
| Help                       | `K_HELP`        |                                                                    |
| Menu                       | `K_MENU`        |                                                                    |
| Select                     | `K_SELECT`      |                                                                    |
| Stop                       | `K_STOP`        |                                                                    |
| Again / Redo               | `K_AGAIN`       | `K_REDO`                                                           |
| Undo                       | `K_UNDO`        | `UNDO` *(deprecated)*                                              |
| Cut                        | `K_CUT`         | `CUT` *(deprecated)*                                               |
| Copy                       | `K_COPY`        | `COPY` *(deprecated)*                                              |
| Paste                      | `K_PASTE`       | `PSTE` *(deprecated)*                                              |
| Find                       | `K_FIND`        |                                                                    |
| Mute                       | `K_MUTE`        |                                                                    |
| Volume Up                  | `K_VOL_UP`      | `K_VOLUME_UP`                                                      |
| Volume Down                | `K_VOL_DN`      | `K_VOLUME_DOWN`                                                    |
| Play/Pause                 | `K_PP`          | `K_PLAY_PAUSE`                                                     |
| Stop (alt)                 | `K_STOP2`       |                                                                    |
| Previous                   | `K_PREV`        | `K_PREVIOUS`                                                       |
| Next                       | `K_NEXT`        |                                                                    |
| Eject                      | `K_EJECT`       |                                                                    |
| Volume Up (alt)            | `K_VOL_UP2`     | `K_VOLUME_UP2`                                                     |
| Volume Down (alt)          | `K_VOL_DN2`     | `K_VOLUME_DOWN2`                                                   |
| Mute (alt)                 | `K_MUTE2`       |                                                                    |
| WWW                        | `K_WWW`         |                                                                    |
| Back                       | `K_BACK`        |                                                                    |
| Forward                    | `K_FORWARD`     |                                                                    |
| Stop (alt 2)               | `K_STOP3`       |                                                                    |
| Find (alt)                 | `K_FIND2`       |                                                                    |
| Scroll Up                  | `K_SCROLL_UP`   |                                                                    |
| Scroll Down                | `K_SCROLL_DOWN` |                                                                    |
| Edit                       | `K_EDIT`        |                                                                    |
| Sleep                      | `K_SLEEP`       |                                                                    |
| Lock / Screensaver         | `K_LOCK`        | `K_SCREENSAVER`, `K_COFFEE`                                        |
| Refresh                    | `K_REFRESH`     |                                                                    |
| Calculator                 | `K_CALC`        | `K_CALCULATOR`                                                     |

---

## Locking & International

### Locking Keys

| Key                 | Preferred Code | Aliases          |
|---------------------|----------------|------------------|
| Locking Caps Lock   | `LCAPS`        | `LOCKING_CAPS`   |
| Locking Num Lock    | `LNLCK`        | `LOCKING_NUM`    |
| Locking Scroll Lock | `LSLCK`        | `LOCKING_SCROLL` |

### International Keys (for non-US layouts)

| Key                                 | Preferred Code | Aliases                                               |
|-------------------------------------|----------------|-------------------------------------------------------|
| International 1 (Ro)                | `INT1`         | `INTERNATIONAL_1`, `INT_RO`                           |
| International 2 (Katakana/Hiragana) | `INT2`         | `INTERNATIONAL_2`, `INT_KATAKANAHIRAGANA`, `INT_KANA` |
| International 3 (Yen)               | `INT3`         | `INTERNATIONAL_3`, `INT_YEN`                          |
| International 4 (Henkan)            | `INT4`         | `INTERNATIONAL_4`, `INT_HENKAN`                       |
| International 5 (Muhenkan)          | `INT5`         | `INTERNATIONAL_5`, `INT_MUHENKAN`                     |
| International 6 (KP JP comma)       | `INT6`         | `INTERNATIONAL_6`, `INT_KPJPCOMMA`                    |
| International 7                     | `INT7`         | `INTERNATIONAL_7`                                     |
| International 8                     | `INT8`         | `INTERNATIONAL_8`                                     |
| International 9                     | `INT9`         | `INTERNATIONAL_9`                                     |
| Language 1 (Hangeul)                | `LANG1`        | `LANGUAGE_1`, `LANG_HANGEUL`                          |
| Language 2 (Hanja)                  | `LANG2`        | `LANGUAGE_2`, `LANG_HANJA`                            |
| Language 3 (Katakana)               | `LANG3`        | `LANGUAGE_3`, `LANG_KATAKANA`                         |
| Language 4 (Hiragana)               | `LANG4`        | `LANGUAGE_4`, `LANG_HIRAGANA`                         |
| Language 5 (Zenkaku/Hankaku)        | `LANG5`        | `LANGUAGE_5`, `LANG_ZENKAKUHANKAKU`                   |
| Language 6                          | `LANG6`        | `LANGUAGE_6`                                          |
| Language 7                          | `LANG7`        | `LANGUAGE_7`                                          |
| Language 8                          | `LANG8`        | `LANGUAGE_8`                                          |
| Language 9                          | `LANG9`        | `LANGUAGE_9`                                          |

---

## Consumer / Media Keys (`C_` prefix)

### Power & Sleep

| Action              | Code           | Aliases   |
|---------------------|----------------|-----------|
| Consumer Power      | `C_PWR`        | `C_POWER` |
| Consumer Reset      | `C_RESET`      |           |
| Consumer Sleep      | `C_SLEEP`      |           |
| Consumer Sleep Mode | `C_SLEEP_MODE` |           |

### Transport / Playback

| Action                | Code               | Aliases                                 |
|-----------------------|--------------------|-----------------------------------------|
| Play/Pause            | `C_PP`             | `C_PLAY_PAUSE`; `M_PLAY` *(deprecated)* |
| Play                  | `C_PLAY`           |                                         |
| Pause                 | `C_PAUSE`          |                                         |
| Stop                  | `C_STOP`           | `M_STOP` *(deprecated)*                 |
| Next Track            | `C_NEXT`           | `M_NEXT` *(deprecated)*                 |
| Previous Track        | `C_PREV`           | `C_PREVIOUS`; `M_PREV` *(deprecated)*   |
| Fast Forward          | `C_FF`             | `C_FAST_FORWARD`                        |
| Rewind                | `C_RW`             | `C_REWIND`                              |
| Record                | `C_REC`            | `C_RECORD`                              |
| Eject                 | `C_EJECT`          | `M_EJCT` *(deprecated)*                 |
| Stop/Eject            | `C_STOP_EJECT`     |                                         |
| Shuffle / Random Play | `C_SHUFFLE`        | `C_RANDOM_PLAY`                         |
| Repeat                | `C_REPEAT`         |                                         |
| Slow                  | `C_SLOW`           |                                         |
| Slow Tracking         | `C_SLOW2`          | `C_SLOW_TRACKING`                       |
| Mode Step             | `C_MODE_STEP`      | `C_MEDIA_STEP`                          |
| Recall Last (channel) | `C_CHAN_LAST`      | `C_RECALL_LAST`                         |
| VCR Plus              | `C_MEDIA_VCR_PLUS` |                                         |

### Volume & Audio

| Action                    | Code              | Aliases                                  |
|---------------------------|-------------------|------------------------------------------|
| Mute                      | `C_MUTE`          | `M_MUTE` *(deprecated)*                  |
| Volume Up                 | `C_VOL_UP`        | `C_VOLUME_UP`; `M_VOLU` *(deprecated)*   |
| Volume Down               | `C_VOL_DN`        | `C_VOLUME_DOWN`; `M_VOLD` *(deprecated)* |
| Bass Boost                | `C_BASS_BOOST`    |                                          |
| Voice Command             | `C_VOICE_COMMAND` |                                          |
| Alternate Audio Increment | `C_ALT_AUDIO_INC` | `C_ALTERNATE_AUDIO_INCREMENT`            |

### Brightness & Display

| Action             | Code         | Aliases                         |
|--------------------|--------------|---------------------------------|
| Brightness Up      | `C_BRI_UP`   | `C_BRI_INC`, `C_BRIGHTNESS_INC` |
| Brightness Down    | `C_BRI_DN`   | `C_BRI_DEC`, `C_BRIGHTNESS_DEC` |
| Brightness Minimum | `C_BRI_MIN`  | `C_BRIGHTNESS_MINIMUM`          |
| Brightness Maximum | `C_BRI_MAX`  | `C_BRIGHTNESS_MAXIMUM`          |
| Brightness Auto    | `C_BRI_AUTO` | `C_BRIGHTNESS_AUTO`             |
| Backlight Toggle   | `C_BKLT_TOG` | `C_BACKLIGHT_TOGGLE`            |

### Channel

| Action            | Code         | Aliases         |
|-------------------|--------------|-----------------|
| Channel Increment | `C_CHAN_INC` | `C_CHANNEL_INC` |
| Channel Decrement | `C_CHAN_DEC` | `C_CHANNEL_DEC` |

### OSD / Menu

| Action              | Code           | Aliases           |
|---------------------|----------------|-------------------|
| Consumer Menu       | `C_MENU`       |                   |
| Menu Pick/Select    | `C_MENU_PICK`  | `C_MENU_SELECT`   |
| Menu Up             | `C_MENU_UP`    |                   |
| Menu Down           | `C_MENU_DOWN`  |                   |
| Menu Left           | `C_MENU_LEFT`  |                   |
| Menu Right          | `C_MENU_RIGHT` |                   |
| Menu Escape         | `C_MENU_ESC`   | `C_MENU_ESCAPE`   |
| Menu Value Increase | `C_MENU_INC`   | `C_MENU_INCREASE` |
| Menu Value Decrease | `C_MENU_DEC`   | `C_MENU_DECREASE` |

### TV / AV

| Action               | Code                           |
|----------------------|--------------------------------|
| Data on Screen       | `C_DATA_ON_SCREEN`             |
| Captions / Subtitles | `C_CAPTIONS` / `C_SUBTITLES`   |
| Snapshot             | `C_SNAPSHOT`                   |
| Picture-in-Picture   | `C_PIP`                        |
| Aspect Ratio         | `C_ASPECT`                     |
| Red Button           | `C_RED` / `C_RED_BUTTON`       |
| Green Button         | `C_GREEN` / `C_GREEN_BUTTON`   |
| Blue Button          | `C_BLUE` / `C_BLUE_BUTTON`     |
| Yellow Button        | `C_YELLOW` / `C_YELLOW_BUTTON` |

### Media Source Select

| Action        | Code                 |
|---------------|----------------------|
| Computer      | `C_MEDIA_COMPUTER`   |
| TV            | `C_MEDIA_TV`         |
| WWW           | `C_MEDIA_WWW`        |
| DVD           | `C_MEDIA_DVD`        |
| Phone         | `C_MEDIA_PHONE`      |
| Program Guide | `C_MEDIA_GUIDE`      |
| Video Phone   | `C_MEDIA_VIDEOPHONE` |
| Games         | `C_MEDIA_GAMES`      |
| Messages      | `C_MEDIA_MESSAGES`   |
| CD            | `C_MEDIA_CD`         |
| VCR           | `C_MEDIA_VCR`        |
| Tuner         | `C_MEDIA_TUNER`      |
| Tape          | `C_MEDIA_TAPE`       |
| Cable         | `C_MEDIA_CABLE`      |
| Satellite     | `C_MEDIA_SATELLITE`  |
| Home          | `C_MEDIA_HOME`       |

### App Launch (`AL`) Keys

| Application             | Code                       | Aliases                              |
|-------------------------|----------------------------|--------------------------------------|
| Consumer Control Config | `C_AL_CCC`                 |                                      |
| Word Processor          | `C_AL_WORD`                |                                      |
| Text Editor             | `C_AL_TEXT_EDITOR`         |                                      |
| Spreadsheet             | `C_AL_SHEET`               | `C_AL_SPREADSHEET`                   |
| Graphics Editor         | `C_AL_GRAPHICS_EDITOR`     |                                      |
| Presentation            | `C_AL_PRESENTATION`        |                                      |
| Database                | `C_AL_DB`                  | `C_AL_DATABASE`                      |
| Email                   | `C_AL_EMAIL`               | `C_AL_MAIL`                          |
| Newsreader              | `C_AL_NEWS`                |                                      |
| Voicemail               | `C_AL_VOICEMAIL`           |                                      |
| Contacts / Address Book | `C_AL_CONTACTS`            | `C_AL_ADDRESS_BOOK`                  |
| Calendar                | `C_AL_CAL`                 | `C_AL_CALENDAR`                      |
| Task / Project Manager  | `C_AL_TASK_MANAGER`        |                                      |
| Journal / Timecard      | `C_AL_JOURNAL`             |                                      |
| Finance                 | `C_AL_FINANCE`             |                                      |
| Calculator              | `C_AL_CALC`                | `C_AL_CALCULATOR`                    |
| A/V Capture/Playback    | `C_AL_AV_CAPTURE_PLAYBACK` |                                      |
| My Computer             | `C_AL_MY_COMPUTER`         |                                      |
| Internet Browser        | `C_AL_WWW`                 |                                      |
| Network Chat            | `C_AL_CHAT`                | `C_AL_NETWORK_CHAT`                  |
| Logoff                  | `C_AL_LOGOFF`              |                                      |
| Lock / Screensaver      | `C_AL_LOCK`                | `C_AL_SCREENSAVER`, `C_AL_COFFEE`    |
| Control Panel           | `C_AL_CONTROL_PANEL`       |                                      |
| Select Task             | `C_AL_SELECT_TASK`         |                                      |
| Next Task               | `C_AL_NEXT_TASK`           |                                      |
| Previous Task           | `C_AL_PREV_TASK`           | `C_AL_PREVIOUS_TASK`                 |
| Help Center             | `C_AL_HELP`                |                                      |
| Documents               | `C_AL_DOCS`                | `C_AL_DOCUMENTS`                     |
| Spell Check             | `C_AL_SPELL`               | `C_AL_SPELLCHECK`                    |
| Keyboard Layout         | `C_AL_KEYBOARD_LAYOUT`     |                                      |
| Screen Saver            | `C_AL_SCREEN_SAVER`        |                                      |
| File Browser            | `C_AL_FILES`               | `C_AL_FILE_BROWSER`                  |
| Image Browser           | `C_AL_IMAGES`              | `C_AL_IMAGE_BROWSER`                 |
| Audio Browser           | `C_AL_AUDIO`               | `C_AL_AUDIO_BROWSER`, `C_AL_MUSIC`   |
| Movie Browser           | `C_AL_MOVIES`              | `C_AL_MOVIE_BROWSER`                 |
| Instant Messaging       | `C_AL_IM`                  | `C_AL_INSTANT_MESSAGING`             |
| OEM Tips/Tutorial       | `C_AL_TIPS`                | `C_AL_OEM_FEATURES`, `C_AL_TUTORIAL` |

### App Control (`AC`) Keys

| Action                | Code                                 | Aliases                             |
|-----------------------|--------------------------------------|-------------------------------------|
| New                   | `C_AC_NEW`                           |                                     |
| Open                  | `C_AC_OPEN`                          |                                     |
| Close                 | `C_AC_CLOSE`                         |                                     |
| Exit                  | `C_AC_EXIT`                          |                                     |
| Save                  | `C_AC_SAVE`                          |                                     |
| Print                 | `C_AC_PRINT`                         |                                     |
| Properties            | `C_AC_PROPS`                         | `C_AC_PROPERTIES`                   |
| Undo                  | `C_AC_UNDO`                          |                                     |
| Copy                  | `C_AC_COPY`                          |                                     |
| Cut                   | `C_AC_CUT`                           |                                     |
| Paste                 | `C_AC_PASTE`                         |                                     |
| Find                  | `C_AC_FIND`                          |                                     |
| Search                | `C_AC_SEARCH`                        |                                     |
| Go To                 | `C_AC_GOTO`                          |                                     |
| Home                  | `C_AC_HOME`                          |                                     |
| Back                  | `C_AC_BACK`                          |                                     |
| Forward               | `C_AC_FORWARD`                       |                                     |
| Stop                  | `C_AC_STOP`                          |                                     |
| Refresh               | `C_AC_REFRESH`                       |                                     |
| Bookmarks / Favorites | `C_AC_BOOKMARKS`                     | `C_AC_FAVORITES`, `C_AC_FAVOURITES` |
| Zoom In               | `C_AC_ZOOM_IN`                       |                                     |
| Zoom Out              | `C_AC_ZOOM_OUT`                      |                                     |
| Zoom                  | `C_AC_ZOOM`                          |                                     |
| View Toggle           | `C_AC_VIEW_TOGGLE`                   |                                     |
| Scroll Up             | `C_AC_SCROLL_UP`                     |                                     |
| Scroll Down           | `C_AC_SCROLL_DOWN`                   |                                     |
| Edit                  | `C_AC_EDIT`                          |                                     |
| Cancel                | `C_AC_CANCEL`                        |                                     |
| Insert Mode           | `C_AC_INS`                           | `C_AC_INSERT`                       |
| Delete                | `C_AC_DEL`                           |                                     |
| Redo/Repeat           | `C_AC_REDO`                          |                                     |
| Reply                 | `C_AC_REPLY`                         |                                     |
| Forward Mail          | `C_AC_FORWARD_MAIL`                  |                                     |
| Send                  | `C_AC_SEND`                          |                                     |
| Show All Windows      | `C_AC_DESKTOP_SHOW_ALL_WINDOWS`      |                                     |
| Show All Applications | `C_AC_DESKTOP_SHOW_ALL_APPLICATIONS` |                                     |

### Input Assist

| Action                      | Code              | Aliases                                  |
|-----------------------------|-------------------|------------------------------------------|
| Input Assist Previous       | `C_KBIA_PREV`     | `C_KEYBOARD_INPUT_ASSIST_PREVIOUS`       |
| Input Assist Next           | `C_KBIA_NEXT`     | `C_KEYBOARD_INPUT_ASSIST_NEXT`           |
| Input Assist Previous Group | `C_KBIA_PREV_GRP` | `C_KEYBOARD_INPUT_ASSIST_PREVIOUS_GROUP` |
| Input Assist Next Group     | `C_KBIA_NEXT_GRP` | `C_KEYBOARD_INPUT_ASSIST_NEXT_GROUP`     |
| Input Assist Accept         | `C_KBIA_ACCEPT`   | `C_KEYBOARD_INPUT_ASSIST_ACCEPT`         |
| Input Assist Cancel         | `C_KBIA_CANCEL`   | `C_KEYBOARD_INPUT_ASSIST_CANCEL`         |

### Misc Consumer

| Action                             | Code     | Aliases                            |
|------------------------------------|----------|------------------------------------|
| Quit                               | `C_QUIT` |                                    |
| Help                               | `C_HELP` |                                    |
| Globe (Apple next keyboard layout) | `GLOBE`  | `C_AC_NEXT_KEYBOARD_LAYOUT_SELECT` |

---

## Mouse (`&mkp` / `&mmv` / `&msc`)

Used with the `&mkp`, `&mmv`, and `&msc` behaviors.

### Buttons (`&mkp`)

| Button         | Code  | Aliases |
|----------------|-------|---------|
| Left Click     | `MB1` | `LCLK`  |
| Right Click    | `MB2` | `RCLK`  |
| Middle Click   | `MB3` | `MCLK`  |
| Mouse Button 4 | `MB4` |         |
| Mouse Button 5 | `MB5` |         |

### Movement (`&mmv`)

| Direction     | Code         |
|---------------|--------------|
| Up            | `MOVE_UP`    |
| Down          | `MOVE_DOWN`  |
| Left          | `MOVE_LEFT`  |
| Right         | `MOVE_RIGHT` |
| Custom (x, y) | `MOVE(x, y)` |

### Scroll (`&msc`)

| Direction    | Code         |
|--------------|--------------|
| Scroll Up    | `SCRL_UP`    |
| Scroll Down  | `SCRL_DOWN`  |
| Scroll Left  | `SCRL_LEFT`  |
| Scroll Right | `SCRL_RIGHT` |

---

## Bluetooth (`&bt`)

| Action             | ZMK Syntax       |
|--------------------|------------------|
| Select profile 0   | `&bt BT_SEL 0`   |
| Select profile 1   | `&bt BT_SEL 1`   |
| Select profile 2   | `&bt BT_SEL 2`   |
| Select profile 3   | `&bt BT_SEL 3`   |
| Next profile       | `&bt BT_NXT`     |
| Previous profile   | `&bt BT_PRV`     |
| Disconnect current | `&bt BT_DISC`    |
| Clear current bond | `&bt BT_CLR`     |
| Clear all bonds    | `&bt BT_CLR_ALL` |

---

## External Power (`&ext_power`)

| Action    | ZMK Syntax          |
|-----------|---------------------|
| Power on  | `&ext_power EP_ON`  |
| Power off | `&ext_power EP_OFF` |
| Toggle    | `&ext_power EP_TOG` |

---

## Layer & Behavior Controls

These are behaviors (not key codes) — they go in the binding position directly.

| Behavior        | Syntax            | Description                           |
|-----------------|-------------------|---------------------------------------|
| Key press       | `&kp KEY`         | Send a key                            |
| Momentary layer | `&mo N`           | Layer N while held                    |
| Layer tap       | `&lt N KEY`       | Layer N when held, KEY when tapped    |
| Toggle layer    | `&tog N`          | Toggle layer N on/off                 |
| Go to layer     | `&to N`           | Switch to layer N permanently         |
| Transparent     | `&trans`          | Pass through to next active layer     |
| Blocked         | `&none`           | No action                             |
| Sticky key      | `&sk KEY`         | Key applies to next keypress only     |
| Sticky layer    | `&sl N`           | Layer N applies to next keypress only |
| Hold-tap        | `&ht MOD KEY`     | Custom hold-tap (configured in `&ht`) |
| Tap-dance       | `&td0` …          | Defined in `tap_dances` node          |
| Macro           | `&m0` …           | Defined in `macros` node              |
| Reset           | `&sys_reset`      | Reset the controller                  |
| Bootloader      | `&bootloader`     | Enter USB bootloader (for flashing)   |
| Bluetooth       | `&bt BT_*`        | See Bluetooth section                 |
| External power  | `&ext_power EP_*` | See External Power section            |
| Mouse button    | `&mkp MB1`…`MB5`  | See Mouse section                     |
| Mouse move      | `&mmv MOVE_*`     | See Mouse section                     |
| Mouse scroll    | `&msc SCRL_*`     | See Mouse section                     |
