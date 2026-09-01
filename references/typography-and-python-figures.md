# 深层参考：字体规范与 Python 图表生成

## 字体硬规则

Word/PDF 全文中文用宋体，英文、数字用 Times New Roman；题目、标题、正文、表格、图注及页眉页脚一致，所有标题为黑色。`python-docx` 须同时设置样式和 run 的 `w:ascii`、`w:hAnsi` 为 Times New Roman，`w:eastAsia` 为 SimSun，避免继承 Calibri、Arial、微软雅黑或等线。

覆盖 `Normal`、`Title`、`Heading 1`—`Heading 3`、表格和图注样式，并设置标题颜色为 RGB(0,0,0)。

## Python 图表

主体图必须用 matplotlib/seaborn、plotly、networkx、scipy/statsmodels 或 pandas 生成；禁用 AI 图、网页截图、Excel/PPT 默认图，PIL 只做后处理。绘图前加载宋体与 Times New Roman，设置 `axes.unicode_minus=False` 和至少 300 dpi。

在 Windows 中从字体目录加载 `simsun.ttc` 与 Times 字体，并检查标题、刻度、图例、注释及色条均能正确混排中文和英文数字。

统一白/浅灰底、细网格、轻边框与低饱和配色；补齐变量名、单位、图例和关键标注。避免彩虹色、3D、发光、渐变、玻璃拟态、装饰背景、遮挡和标签重叠。创新图应服务模型解释，可选复合图、校准+ROC/PR、森林/SHAP、分组轨迹、聚类热力图或敏感性响应面，并说明其支持的结论或暴露的不确定性。

图例必要时外置；图片宽高按正文版心设计，插入后不得拉伸。整篇统一 4—6 个主辅色和浅灰中性色。

## 交付检查

运行 `verify_docx_typography.py` 与 `verify_docx_figures.py` 后，仍须渲染 Word/PDF 逐页检查字体、标题颜色、图表清晰度、图例位置和图文衔接；发现错误应回到生成脚本修正，不能仅在 Word 中临时改色。
