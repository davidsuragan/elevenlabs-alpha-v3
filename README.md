## How to use the official ElevenLabs TTS model: Eleven V3 with early access?

Official API returns a `403 model_access_denied` error:
`"You do not have access to Eleven v3 (alpha). For early access please contact sales."`

This script bypasses that by mimicking browser behavior — no API key or login required.
It uses the official API endpoint with different approaches.

---

## Available Methods

### method - 1 — Official API with Firebase login (**recommended**)
Uses real Firebase login (email + password) to retrieve Bearer token.

✅ Fully stable  
✅ Uses official ElevenLabs infrastructure  
✅ Supports all eleven-v3 voices  
✅ Fast  
🔐 Requires ElevenLabs account with login/password  
👇method - 1
[SCRIPT](https://github.com/dauitsuragan002/elevenlabs-alpha-v3/tree/main/method_1)

### method - 2 — Official API with browser headers
Mimics browser requests to access v3 voices without login.  

✅ Works without API key or login  
✅ Supports all eleven-v3 voices  
✅ Fast  
⚠️ May break or be rate-limited  
👍 Good for quick tests  

👇method - 2
[SCRIPT](https://github.com/dauitsuragan002/elevenlabs-alpha-v3/tree/main/method_2)

### ⚙️ Method 3 — Unofficial, Complex

> Uses **Playwright** to simulate a full browser session.

❌ **Not stable**
❌ **Not recommended**
❌ **Slow**

---
👇method - 3
[SCRIPT](https://github.com/dauitsuragan002/elevenlabs-alpha-v3/tree/main/method_3)

## Features Summary

| Method    | Type          | API Key    | Login | Stability | Recommended | Voices Supported                          |
| --------- | ------------- | ---------- | ----- | --------- | ----------- | ----------------------------------------- |
| method\_1 | Official      | ✅ Firebase | ✅     | ✅ High    | ✅ Yes       | ✅ All official voices (incl. `eleven_v3`) |
| method\_2 | Semi-Official | ❌          | ❌     | ⚠️ Medium | ⚠️ Partial  | ✅ All official voices (incl. `eleven_v3`)voices                    |
| method\_3 | Unofficial    | ❌          | ✅     | ❌ Low     | ❌ No        | ⚠️ Limited via browser UI                 |

---

## 🎙️ Voices and `voice_id`

You can freely use any `voice_id` supported by ElevenLabs.
✅ Just copy the `voice_id` and use it — no extra setup needed.

### 🔊 voice\_id examples

```txt
JESSICA   = "cgSgspJ2msm6clMCkdW9"  
LIAM      = "TX3LPaxmHKxFdv7VOQHJ"  
ANNOUNCER = "gU0LNdkMOQCOrPrwtbee"  
SAMMARA   = "19STyYD15bswVz51nqLf"  
SERGEANT  = "DGzg6RaUqxGRTHSBjfgF"  
SPUDS     = "NOpBlnGInO9m6vDvFkFC"
```

---

## Credit

* [Telegram](https://t.me/david667s)
* Gemini
* GPT
* Firebase REST API
* browser header spoofing technique

---

If you have questions, feel free to reach out.