# Theory of Computation Final Project
# 美食碰碰看
## 是否每天到了用餐時間都在煩惱該吃什麼？ 不想再被育樂街折磨的你，趕緊下載"sumikko"讓它告訴你哪裡有美食吧。

### 功能1：連接Imgur，讀取照片
當輸入“大家都吃什麼”或“suggestion”時，Linebot會從Imgur的album 中隨機回傳一張美食照片。

### 功能2：爬文即時新聞
當輸入“新聞”或是“news”時，Linebot會回傳即時新聞的標題和連接。

### 功能3：sticker
目前輸入以下詞彙Linebot將會回傳相關Sticker。
【sleep,yes,shock.love.narcissism,angry,ugly,scared,cry,smile】

# Usage
-state: user
-input: “大家都吃什麼”或“suggestion”
-nxt_state: food
-reply: 隨機的美食照片

-state: user
-input: “新聞”或是“news”
-nxt_state: news
-reply: 蘋果即時新聞

-state: user
-input: 【sleep,yes,shock.love.narcissism,angry,ugly,scared,cry,smile】
-nxt_state: sticker
-reply: Line sticker




