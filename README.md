# primer-design
design primer DNA sequences for different PCR
[README.md](https://github.com/user-attachments/files/32594186/README.md)
# Primer3 输入文件生成器 v1.0.0

中文离线程序：输入 DNA、选择引物类型、指定目标区域，生成可交给 `primer3_core` 读取的 Boulder-IO `.txt` 文件。无需安装 Python、Node.js 或浏览器插件即可使用主程序。

## 快速开始

1. 将 `Primer3_Input_Builder.html` 下载到电脑，用 Edge、Chrome 或 Firefox 打开。若下载页面只显示源码，请先保存文件，再从本地打开。
2. 选择引物类型。可选普通 PCR、SYBR qPCR、克隆/指定片段扩增、巢式外引物或巢式内引物。
3. 粘贴 DNA 全长序列，或导入单条 FASTA 文件。序列按 5′→3′ 输入。
4. 用 bp 起止位置或目标序列指定区域，并确认扩增方式。
5. 点击“生成 Primer3 指令”，检查提示后点击“下载 .txt 文件”。
6. 将生成的文件交给已经安装的 Primer3 运行。程序右侧会给出与文件名对应的命令。

“载入演示序列”使用人工生成的 1,200 bp 序列，仅用于软件演示，不对应已知基因，也不是实验推荐序列。

所有输入只在当前浏览器中处理，不调用网络接口，不保存到浏览器存储。关闭或刷新页面会清除输入；下载的 TXT 包含完整 DNA 模板，仍会保留在下载目录。建议保存原始 FASTA 和导出的指令文件。

## 必须选对的三种扩增方式

| 扩增方式 | 适合的目标 | 程序如何限制位置 |
| --- | --- | --- |
| 两侧包围目标 | 扩增一个内部目标，同时允许包含周围序列 | 引物完全落在目标左右两侧，产物包含整个目标 |
| 区域内设计 | 在较长 cDNA 或候选区域中寻找短扩增子 | 两条引物及产物均位于所选区域，产物不必覆盖整个区域 |
| 精确扩增 | 克隆某个完整片段或 CDS | 固定产物两端为输入的起止位置，向内选择引物结合区长度 |

例如，输入模板的 101–200 bp：界面认为目标长 100 bp。包围模式把它当作必须完整跨过的内部目标；区域内模式只在这 100 bp 内寻找引物；精确模式把模板对应产物固定为 100 bp。

包围模式需要模板提供足够的侧翼。若目标就是整条模板，应选择精确扩增，或使用区域内模式设计局部扩增子。默认 qPCR 在区域内设计；默认克隆固定两端。

指令统一设置 `PRIMER_FIRST_BASE_INDEX=0`。上述区域转换为 `100,100`（起点、长度）；包围模式使用 `SEQUENCE_TARGET` 和左右引物允许区，区域内模式使用 `SEQUENCE_INCLUDED_REGION`，精确模式使用 `pick_cloning_primers`。相关字段遵循 [Primer3 官方手册](https://primer3.org/manual.html)。

## 引物类型与预设

以下为本程序的可修改初始筛选条件，不声称是 Primer3 官方用途预设或实验最优值。

| 类型 | 长度：最小/理想/最大 nt | Tm：最低/理想/最高 °C | GC% | 最大 Tm 差 °C | 自动产物范围的起始设定 |
| --- | --- | --- | --- | --- | --- |
| 普通 PCR | 18/20/27 | 57/60/63 | 35–65 | 3 | 100–1500 bp |
| SYBR qPCR | 18/20/25 | 59/60/61 | 40–60 | 1 | 80–200 bp |
| 克隆/指定片段 | 18/22/30 | 57/60/65 | 35–65 | 3 | 默认固定为目标长度 |
| 巢式外引物 | 18/22/27 | 58/60/63 | 35–65 | 2 | 400–2000 bp |
| 巢式内引物 | 18/22/27 | 58/60/63 | 35–65 | 2 | 100–1000 bp |

自动模式会根据几何可行性调整范围：包围模式至少容纳完整目标与两条最短引物，范围上限受可用模板限制；长目标可扩大普通/巢式 PCR 的自动上限。qPCR 不会为了覆盖长目标而自动改为长扩增子。手动填写范围时必须同时填写最小和最大值；精确模式即使提供范围，实际仍导出目标长度的固定区间。

共同设置包括：引物不含 N；不强制 GC clamp；末端 5 nt 最多 3 个 G/C；连续同碱基上限为 4（克隆为 5）；返回 5 对候选；寡核苷酸热力学检查开启。自身互补、3′ 自身互补、发卡和引物对互补的热力学阈值设为 47 °C。全模板热力学错配检查关闭，不加载全基因组或重复序列数据库。

反应条件初值为单价盐 50 mM、Mg²⁺ 1.5 mM、dNTP 总浓度 0.6 mM，以及退火寡核苷酸浓度模型参数 50 nM。应根据所用试剂修改；dNTP 为四种浓度之和，寡核苷酸模型参数不代表 cDNA 浓度，也不能直接当作引物加样终浓度。Tm 计算选择 SantaLucia 模型及其盐校正。

## 按序列定位目标

- 默认在输入模板上做正向完全匹配；可勾选同时搜索反向互补序列。
- 多处匹配必须由使用者选择，程序不会默认采用第一处。
- 反向互补匹配后，坐标与左右引物命名仍以输入模板为参考。
- 模板允许 N；目标序列含 N 时要求改用坐标。N 不作为通配符。
- 接受单条 FASTA、大小写字母、换行、空白及数字行号。RNA 的 U、其他 IUPAC 简并码、比对缺口及异常标点会被拒绝，不会静默转换。
- 当前每次处理一条线性模板，长度上限 500,000 bp，导入文件上限 2 MB；长模板的实际 Primer3 运行时间可能较长。

## 巢式 PCR

先设计外引物并选定一对，再填写它们在同一份全长模板上的实际结合区。四个坐标均为 1-based，包含首尾；反向引物也填写从小到大的区间。

例如，正向外引物结合于 101–122 bp，反向外引物结合于 979–1000 bp，间隔设为 5 bp，则内引物仅允许出现在 128–973 bp。目标必须完全位于这个范围中。该限制保证结合区位于外引物内侧，不代表已验证两轮 PCR 的特异性、效率或实验兼容性。

本程序导出的 Primer3 结果采用 0-based：

- 左引物结果 `PRIMER_LEFT_0=p,L` → 1-based 结合区 `p+1` 至 `p+L`。
- 右引物结果 `PRIMER_RIGHT_0=p,L` → 1-based 结合区 `p−L+2` 至 `p+1`。

这些公式只适用于本程序固定的 `PRIMER_FIRST_BASE_INDEX=0`。若使用其他来源的结果，请先核查坐标基准。

## 克隆引物的 5′ 附加序列

两条附加序列都按相应订购引物自身的 5′→3′ 方向输入；程序直接传给 Primer3，不会再次将右侧输入反向互补。酶切位点、保护碱基、同源臂、阅读框及起止密码子由使用者决定。

产物范围针对模板对应片段；最终产物长度还包括左右附加序列。结合区的长度、Tm 和 GC 与附加序列的处理方式遵循 [Primer3 2.6.1 发布说明](https://github.com/primer3-org/primer3/releases/tag/v2.6.1)。附加序列会影响二级结构筛选，有可能使原本可行的固定边界设计不再返回候选。

## 在 Primer3 中运行

面向 `primer3_core` 2.6.1+，不是 Primer3Plus 的网页导入格式。生成器本身不附带、安装或调用 Primer3。

以演示文件为例，在可执行程序目录下运行：

Git Bash / Linux / macOS：

```bash
./primer3_core --strict_tags --output=synthetic_demo_result.txt synthetic_demo_primer3_input.txt
```

Windows CMD：

```bat
primer3_core.exe --strict_tags --output=synthetic_demo_result.txt synthetic_demo_primer3_input.txt
```

Windows PowerShell：

```powershell
.\primer3_core.exe --strict_tags --output=synthetic_demo_result.txt synthetic_demo_primer3_input.txt
```

如果安装后可执行文件在其他目录，请填写其实际路径，或先切换目录。页面中的终端选择会自动生成这三种命令。使用命令行参数指定输入文件，因此 PowerShell 无需 `<` 输入重定向。

热力学计算需要 Primer3 配套的 `primer3_config` 目录。若未找到文件，在程序“高级参数”中填写本机实际目录，例如 `D:/primer3/src/primer3_config/`，不加引号，再重新导出。不要填写本生成器所在目录，除非参数文件确实在其中。

TXT 为 UTF-8 无 BOM、LF 换行，序列写在一行，记录以单独一行 `=` 结束。可直接下载，避免文字处理软件改变文件格式。

## 如何理解运行结果

生成成功仅表示输入通过本程序的格式与基本可行性检查。Primer3 实际运行后才会提供候选引物、Tm、二级结构指标和评分。

返回 0 对候选不一定是文件错误：固定边界、Tm/GC 条件、序列本身或附加序列造成的结构限制都可能导致无候选。先查看 `PRIMER_ERROR`、`PRIMER_LEFT_EXPLAIN`、`PRIMER_RIGHT_EXPLAIN`、`PRIMER_PAIR_EXPLAIN`，再决定是否调整条件。本程序不自动启用 `PRIMER_PICK_ANYWAY` 放宽筛选。

第一版不进行 BLAST、全基因组特异性检索、外显子识别、转录本区分、引物二聚体的跨反应组合分析，也不支持环状跨原点扩增、探针、等位基因特异性或测序引物设计。qPCR 仍需检查基因组 DNA 干扰、同源基因/转录本特异性、熔解曲线及扩增效率。

## 源代码与验证

```text
Primer3_Input_Builder.html   可直接打开的主程序
README.md                    使用说明
VERIFICATION.md              本次验证记录
build.py                     从源码重建单文件程序
src/generator.js             参数、校验与指令生成
src/ui.js                    界面交互和文件下载
src/index.html               页面结构
src/style.css                页面样式
tests/test_generator.cjs     核心与实际 Primer3 集成检查
tests/test_browser.mjs       浏览器功能检查（开发用）
examples/                    人工序列和五类输入文件
```

修改源码后运行 `python build.py` 即可重新生成 HTML，构建不需要额外 Python 包。使用 HTML 本身不需要 Python。

开发者可用 `node tests/test_generator.cjs` 检查核心逻辑；设置环境变量 `PRIMER3_CORE` 为本机 Primer3 可执行文件路径后，可额外核验真实引物结果。浏览器检查需 Playwright 和 Chromium，并可用 `PLAYWRIGHT_PATH`、`CHROMIUM_PATH` 指定安装位置。开发依赖未打包，使用主程序不需要它们。

参考：[Primer3 官方手册](https://primer3.org/manual.html) · [Primer3 官方代码库](https://github.com/primer3-org/primer3)
