# Hash Guesser
- Tags: `Misc` `Easy`
- Score: 492/500
- Solves: 23/321
- Solves (MyFirstCTF): 0/101

## Description
I have a hash for you, can you guess it?

## Overview
`ImageChop` 取 min(size) 來做 difference + `util.is_same_image` 沒有檢查 size  
Turnstile (Captcha) 是提示不需要 bruteforce

## Solution
題目每次會隨機生成一個 hash 並轉成 16x16 的圖片，解題者需要上傳一張"相同"圖片來得到 flag。
前端並不會拿到生成的 hash 相關資訊，因此只能用猜的。

而此題的漏洞與 `util.is_same_image` ([chal/util.py#L3-L4](chal/util.py#L3-L4)) 有關。
裡面呼叫了 `ImageChops.difference(img1, img2).getbbox()` 來比較兩張圖片，若回傳 None 則代表兩張圖片沒有差異。

第一眼可能會想，若兩張圖片大小不同，這個 function 會回傳什麼呢?
這題可以透過拿不同尺寸的圖片做實驗，或是如以下翻閱 Pillow 的實作。

### Dig into Pillow (libImaging) Source Code
可查看 [ImageChops Module - Pillow Docs](https://pillow.readthedocs.io/en/stable/reference/ImageChops.html#PIL.ImageChops.difference) 得知其對應的底層 C code ([src/libImaging/Chops.c#L90-L93](https://github.com/python-pillow/Pillow/blob/main/src/libImaging/Chops.c#L90-L93))。

其中裡面的 `CHOP` macro 是這樣 alloc 輸出的 image:
[src/libImaging/Chops.c#L24](https://github.com/python-pillow/Pillow/blob/main/src/libImaging/Chops.c#L24)
```c
    imOut = create(imIn1, imIn2, NULL);
```

觀察其中的 `create`:
[src/libImaging/Chops.c#L74-L75](https://github.com/python-pillow/Pillow/blob/main/src/libImaging/Chops.c#L74-L75)
```c
    xsize = (im1->xsize < im2->xsize) ? im1->xsize : im2->xsize;
    ysize = (im1->ysize < im2->ysize) ? im1->ysize : im2->ysize;
```
可以發現 `imOut` 的 size 會是 `(min(im1->xsize, im2->xsize), min(im1->ysize, im2->ysize))`，也就是兩張圖片取重疊的部分。

### Exploit
若上傳 1x1 的圖片，實際上在做 difference 的只有一個 pixel。

從 [chal/app.py#L31](chal/app.py#L31) 可以看到每個 pixel 只有兩種可能的顏色 (`0x00`、`0xFF`)。
因此猜中的機率是 1/2，隨手造一個 1x1 的白色或黑色圖片，多猜幾次即可得到 flag。

可參考 [solve.py](sol/solve.py) 來造 1x1 的 PNG。 (其實不用這麼麻煩，用 Pillow 就好了)

## Flag
<details>
  <summary>Spoiler</summary>
  
  `AIS3{https://github.com/python-pillow/Pillow/issues/2982}`

</details>
