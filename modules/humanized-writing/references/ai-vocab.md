# 去 AI 味词库（嫌疑清单，不证明来自 AI）

本文件是 `humanized-writing` 在模式 C/D 下加载的「嫌疑词库」。用途：标记需要回上下文判断的地方。
规则来自 conorbronsdon/avoid-ai-writing（分层 Tier 1/2/3）、blader/humanizer、op7418/Humanizer-zh、KKKKhazix/human-writing。
**单个词、单个标点、单个四字词不是修改理由；每个命中都要回上下文判断是否空泛/重复/歧义/不符文体。** 正式技术词、作者样本里的用法、有具体出处的比喻都保留。

---

## 一、英文 AI 高频词（分层）

### Tier 1A — 默认替换（这些词在机器文本里远多于人写；命中即考虑改，保留技术/作者特定用法）
delve / delve into → explore, look at ｜ landscape(比喻) → field, space ｜ tapestry → structure, history ｜ realm → area, domain ｜ paradigm → model, approach ｜ embark → start ｜ beacon(比喻) → example, guide ｜ testament to → shows, proves ｜ robust → strong, reliable ｜ comprehensive → thorough, complete ｜ cutting-edge → latest, advanced ｜ leverage(v) → use ｜ pivotal → important, key ｜ underscores → shows, highlights ｜ meticulous → careful, detailed ｜ seamless → smooth, easy ｜ game-changer → (描述具体改变了什么) ｜ hit differently → feels different ｜ watershed moment → turning point ｜ the future looks bright → (删) ｜ only time will tell → (删) ｜ nestled → is located, sits ｜ vibrant → lively, active ｜ thriving → growing, active ｜ showcasing → showing ｜ deep dive → examine, explore ｜ unpack → explain, break down ｜ bustling → busy, active ｜ intricate → complex, detailed ｜ complexities → problems, details ｜ ever-evolving → changing ｜ enduring → lasting ｜ holistic → complete, whole ｜ actionable → practical ｜ impactful → effective ｜ learnings → lessons, findings ｜ thought leader → expert ｜ best practices → what works ｜ at its core → (删，直接说事) ｜ synergy → combined effect ｜ interplay → relationship, connection ｜ genuinely/genuine(强调) → (删) ｜ symphony(比喻) → coordination ｜ embrace(比喻) → adopt, use ｜ load-bearing(比喻, 仅修饰 assumption/claim/invariant/premise/constraint/dependency/argument/abstraction) → essential, critical

### Tier 1B — 清晰度修改（啰嗦/过度正式，不是作者身份证据；照改即可）
utilize → use ｜ in order to → to ｜ due to the fact that → because ｜ serves as → is ｜ features(v) → has, includes ｜ boasts → has ｜ presents(夸大) → is, shows ｜ commence → start ｜ ascertain → find out, determine ｜ endeavor → effort, try

### Tier 2 — 同段出现 2+ 才标（单独合法，聚一起才需重写）
harness → use ｜ navigate → work through, handle ｜ foster → encourage, build ｜ elevate → improve ｜ unleash → release, enable ｜ streamline → simplify ｜ empower → enable, let ｜ bolster → support ｜ spearhead → lead ｜ resonate with → connect with, matter to ｜ revolutionize → change, transform ｜ facilitate → enable, help ｜ underpin → support, basis of ｜ nuanced → specific, subtle ｜ crucial → important ｜ multifaceted → with several aspects ｜ ecosystem(比喻) → system, network ｜ myriad → many ｜ plethora → many ｜ encompass → include, cover ｜ catalyze → trigger ｜ reimagine → rethink ｜ galvanize → motivate ｜ augment → add to ｜ cultivate → build, grow ｜ illuminate → clarify ｜ elucidate → explain ｜ juxtapose → compare ｜ paradigm-shifting → (描述具体变了什么) ｜ transformative → (描述具体变了什么) ｜ cornerstone → foundation, basis ｜ paramount → most important ｜ poised(to) → ready, about to ｜ burgeoning → growing ｜ nascent → new, early ｜ quintessential → typical, classic ｜ overarching → main, central ｜ quietly → (删或点出具体对比) ｜ deeply(仅 significance 搭配: deeply integrated/committed/rooted) → (删) ｜ underpinning → basis, foundation

### Tier 3 — 仅高密度才标（正常词，单独出现不标；同一词出现 ≥ max(3, 词数×3%) 才考虑改）
significant / significantly → 换具体数字/比较/例子 ｜ innovative / innovation → 描述实际新在哪 ｜ effective / effectively → 说怎么或给指标 ｜ dynamic / dynamics → 点出实际力量/变化 ｜ scalable / scalability → 描述什么在扩、扩到哪 ｜ compelling → 说为何 compelling ｜ unprecedented → 点出打破的先例(或删) ｜ exceptional → 引为何例外 ｜ remarkable → 说值得 remark 的 ｜ sophisticated → 描述复杂在哪 ｜ instrumental → 说扮演什么角色 ｜ world-class / state-of-the-art / best-in-class → 引基准或比较 ｜ verbatim → 通常冗余(删)；法律/研究/QA 术语保留

### Tier 3 短语 — 同篇 2+ 次或 3+ 不同短语同现即标
emerging sector / space / category ｜ the integration of (X with Y) ｜ the intersection of (X and Y) ｜ community-driven ｜ long-term sustainability ｜ user engagement ｜ decentralized compute ｜ (sustainable) reward emissions ｜ tokenized incentive structures ｜ designed for long-term [X]
（crypto/web3/AI 评测类最严重；每条都要求给出具体机制或数字，否则是空框架）

---

## 二、英文模板/过渡短语（删或重写）

- 模板填空：`a [adj] step towards [adj] AI infrastructure` / `a [adj] step forward for [noun]`（除非来源已给能力/基准/结果，否则删空修饰）/ `Whether you're [X] or [Y]`（假广度，选真受众或删）/ `I recently had the pleasure of [verb]-ing` → 直接说发生了什么。
- 过渡词：`Moreover`/`Furthermore`/`Additionally` → 重组使连接明显，或用 and/also；`In today's [X]`/`In an era where` → 删或给具体语境；`It's worth noting that`/`Notably` → 直接说事实；`Here's what's interesting`/`stood out` → 让内容自己显重要；`In conclusion`/`In summary` → 结论应不言自明；`When it comes to` → 直接谈；`At the end of the day` → 删；`That said`/`That being said` → 删或用 but/yet/however。
- 客服腔（直接删）：`Great question!` / `I hope this helps!` / `Certainly!` / `Absolutely!` / `Feel free to reach out` / `Let me know if you need anything` / `Let's dive in!` / `In this article, we will explore…`。
- 意义膨胀：`marking a pivotal moment in the evolution of…` / `a watershed moment for the industry` → 说发生了什么，删掉膨胀从句后句子仍成立就删。
- 泛化未来收尾：`may become one of the most important narratives of the next cycle` / `is poised to become the next major chapter` → 无可证伪内容就删，或来源给了具体预测才用。
-  hedge 堆叠：`could potentially create` / `may eventually unlock` / `might ultimately transform` → 只留一个限定词。
- 模糊归因：`Experts believe` / `Studies show` / `Research suggests`（未点名专家/研究/领袖）→ 点名具体来源，否则标缺口或删无依据主张。
- 泛化结论：`The future looks bright` / `Only time will tell` / `One thing is certain` / `As we move forward` → 删。
- 假合作开场：`Let's explore` / `Let's take a look` / `Let's break this down` → 直接开始。

---

## 三、中文黑话与模型腔（绝对禁词 → 改成人/动作/钱/时间/后果）

**绝对禁词**：赋能、抓手、商业闭环、价值闭环、能力沉淀、拉通、底层逻辑、顶层设计、认知跃迁、价值释放、能力建设、降本增效、内容矩阵、全链路、组合拳、打开想象空间、结构性机会、关键命题、深层逻辑、技术底座、公共底座、技术主权、单点风险、主脊柱、材料锚点、认知增量、迭代闭环。

**需语境判断（本义准确时保留，只用来抬价时改写）**：沉淀、颗粒度、对齐、协同、链路、生态位、心智、范式、方法论、核心变量、打法、想象空间、闭环、不丢。

**模型偏爱抒情词（写具体事物是好词，给抽象概念穿衣服时删；「」自造短语一篇 3 处以上多半在造金句）**：安放、抵达、微光、褶皱、丰盈、滚烫、轻盈、赤裸、剥开、锋利、坚硬、柔软。

**模型路标（删或改写，文字真在说楼层/数量/原义时保留）**：更微妙的是、还有一层、只说对了一半、值得注意的是、需要指出的是、从某种意义上说。

**硬停词（删）**：说白了、说穿了、先说结论。

**AI 高频词（空泛/重复/不准时改；正式词与工程术语不删）**：赋能、至关重要、深入探讨、无缝、闭环、打造、助力、赋能。

**中文需语境判断的套话方向**：「标志着…新时代」「堪称…典范」「彰显了…的追求」「不容忽视」「至关重要」「具有…意义」「为进一步…奠定坚实基础」——保留真实计划/困难/时间节点/作者明确判断，删无独立信息的套话。

---

## 四、中文需语境判断的句式（命中看上下文）

- 层叠的「的」（长定语不易懂时调整结构，保留修饰关系）。
- 「进行＋动词」（冗长时换直接动词，保留正在/完成/计划/次数/范围/结果）。
- 被字句堆叠（改主动时保持归因与确定程度）。
- 四字词排比（只处理空泛/同义堆叠/不符文体者）。
- 「随着……的发展」式开头（仅背景无独立信息时压缩）。

---

## 五、标点与节奏红线（跨中英文）

- 破折号 `—` / `–` / 双破折号 `——`：中文正文清零（英文除非作者样本用，否则改写掉）。
- 中文冒号 `：` / 英文冒号 `:`：只保留引出人物直接原话处；提示性冒号（`一句话总结：`/`核心是：`）删或改写。
- 三项以上同构排比：留两项，第三项换说法或删。
- 粗体当装饰 / 标题 emoji 箭头 / 弯引号混用：按目标格式统一。
- 句长过于均匀（变异系数过低）、连续单句段、段落开场词重复：提示「需人工判断」，回材料与说话位置决定。
