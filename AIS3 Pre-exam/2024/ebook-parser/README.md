# Ebook Parser
- Tags: `Web` `Easy`
- Score: 480/500
- Solves: 35/321
- Solves (MyFirstCTF): 0/101

## Description
I made a simple ebook parser for my ebook collection. Can you read the flag?
*Flag path: `/flag`*

## Overview
EPUB / FB2 格式中有 XML
Dependency Auditing -> 舊版 lxml -> XXE

## Solution
`app.py` 的功能非常簡單，僅透過 `ebookmeta.get_metadata` parse 電子書的 metadata 之後，回傳標題、作者跟語言。

查看 [dnkorpushov/ebookmeta](https://github.com/dnkorpushov/ebookmeta) 可以發現其支援 EPUB 2/3 與 FB2 (Fiction Book) 兩種電子書格式。
另外也可以看到其 [Requirements](https://github.com/dnkorpushov/ebookmeta?tab=readme-ov-file#requirements) 有 lxml。

接著再檢查 `requirements.txt` 發現 lxml 是有點舊的版本 `4.9.1 (2022-07-01)`，可能可以做 [XXE 攻擊](https://portswigger.net/web-security/xxe)。
並且再檢查 library code ([ebookmeta/fb2.py#L32](https://github.com/dnkorpushov/ebookmeta/blob/master/ebookmeta/fb2.py#L32)) 可發現其使用的是危險的 `lxml.etree`，且並未

### FictionBook
查看 [FictionBook 檔案格式官網](http://fictionbook.org/index.php/FictionBook) 可得知其基本上是個 XML。
先用任一款電子書編輯器做一個簡單的 `.fb2` 檔案，再將標題/作者/語言任一欄位替換成指到 `/flag` 的 External Entity 即可。
[參考 exploit](sol/exp.fb2)

### EPUB
查看 [EPUB 3.3](https://www.w3.org/TR/epub-33/#sec-package-doc) 可得知 EPUB 是一個 ZIP 包含所需檔案，以及其 metadata 是 XML。
metadata 位於 `META-INF/container.xml` 中所指定的 [OPF](https://idpf.org/epub/20/spec/OPF_2.0_latest.htm) 檔案中。
先用任一款電子書編輯器做一個簡單的 `.epub` 檔案，再將標題/作者/語言任一欄位替換成指到 `/flag` 的 External Entity 即可。
[參考 exploit](sol/exp.epub)

## Flag
<details>
  <summary>Spoiler</summary>
  
  `AIS3{LP#1742885: lxml no longer expands external entities (XXE) by default}`

</details>

---

賽中打到一半突然冒出了這個 [issue](https://github.com/dnkorpushov/ebookmeta/issues/16) 直接把解都打出來了
而且 dependency version lock 在相同版本 ~~是不是有人找外援~~