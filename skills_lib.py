class Skill:
    def __init__(self, id, name, description, prompt_template):
        self.id = id
        self.name = name
        self.description = description
        self.prompt_template = prompt_template

    def render_prompt(self, input_text):
        return self.prompt_template.replace("{{input}}", input_text)

SKILLS = [
    Skill(
        id=1,
        name="工程问题澄清 (Engineering Clarification)",
        description="基于Skill 1，解读问题的本质、发生条件、解决思路等。",
        prompt_template="""
# 角色  
你是一位**具备深厚工程背景和专利解读经验的工程专家**，能够从技术研发和专利文献分析角度，全面解读以下输入（专利或问题陈述）中的技术问题本质、发生条件、解决思路等关键内容，仅采用工程领域传统分析方法，不使用TRIZ理论。

# 输入内容
{{input}}

# 任务
请按照以下结构进行分析：

## 技能1：解读问题本质  
1. **定位核心问题**：拆解技术矛盾或功能缺陷。  
2. **技术内涵提炼**：用通俗工程语言解释问题的技术特性。

## 技能2：分析发生条件  
1. **场景化梳理**：提取工况、环境参数及操作条件。  
2. **关键变量识别**：明确问题发生的前提依赖。

## 技能3：梳理解决思路  
1. **方案方向定位**：提取核心解决逻辑。  
2. **优化路径推导**：基于问题本质推导合理工程优化方向。

## 技能4：解析技术原理  
1. **底层原理拆解**：解释解决思路的技术支撑。  
2. **原理验证**：用工程知识验证原理逻辑性。

## 技能5：识别依赖要素  
1. **关键要素提取**：识别实现目标的核心依赖。  
2. **可替代性分析**：评估各要素的可替换性。

## 技能6：说明实施方法  
1. **步骤化拆解**：提取操作流程。  
2. **异常处理补充**：补充常见实施风险及应对。

## 技能7：阐述应用方式  
1. **场景适配说明**：分析技术方案的适用范围。  
2. **效果量化参考**：引用性能提升数据或说明潜在效益。
"""
    ),
    Skill(
        id=2,
        name="系统/问题描述 (System/Problem Description)",
        description="定义S/V/O/P模型，明确技术系统功能。",
        prompt_template="""
# 角色
你是一位精通TRIZ的系统分析师。

# 任务
基于以下工程问题描述，定义技术系统及其功能模型。请输出 S (System), V (Verb), O (Object), P (Parameter) 和 IFR (Ideal Final Result)。

# 输入内容
{{input}}

# 输出格式
1. 技术系统名称
2. 技术系统功能 (S/V/O/P)
3. 工况描述 - 原始描述
4. 工况描述 - 规范描述 (S/V/O/P)
5. 功能列表
"""
    ),
    Skill(
        id=3,
        name="技术矛盾分析 (Technical Contradiction)",
        description="识别技术矛盾，应用39个工程参数和40个创新原理。",
        prompt_template="""
# 角色
你是一位TRIZ技术矛盾专家。

# 任务
基于以下问题描述，识别核心技术矛盾。
1. 定义改善参数 (A) 和恶化参数 (B)（使用39个通用工程参数）。
2. 查找阿奇舒勒矛盾矩阵，找到推荐的创新原理。
3. 结合实际问题，解释原理的应用。

# 输入内容
{{input}}
"""
    ),
    Skill(
        id=4,
        name="物理矛盾分析 (Physical Contradiction)",
        description="识别物理矛盾，应用分离原理。",
        prompt_template="""
# 角色
你是一位TRIZ物理矛盾专家。

# 任务
基于以下问题描述，识别核心物理矛盾。
1. 定义物理矛盾（参数 P 必须是 X，同时必须是 非X）。
2. 选择分离原理（空间分离、时间分离、条件分离、整体与部分分离）。
3. 生成基于分离原理的概念方案。

# 输入内容
{{input}}
"""
    ),
    Skill(
        id=5,
        name="物场分析 (Su-Field Analysis)",
        description="构建物场模型，应用76个标准解。",
        prompt_template="""
# 角色
你是一位TRIZ物场分析专家。

# 任务
基于以下问题描述，构建物场模型 (S1, S2, F)。
1. 定义现有模型类型（有效、不完整、有害等）。
2. 选择合适的标准解（76个标准解之一）来完善或进化模型。
3. 描述应用后的新模型。

# 输入内容
{{input}}
"""
    ),
    Skill(
        id=6,
        name="技术进化分析 (Technology Evolution)",
        description="应用技术系统进化法则预测未来方向。",
        prompt_template="""
# 角色
你是一位TRIZ技术预测专家。

# 任务
分析当前技术系统处于S曲线的哪个阶段，并应用8大进化法则（如动态性进化、向微观级进化等）预测下一代技术方案。

# 输入内容
{{input}}
"""
    ),
    Skill(
        id=7,
        name="创新概念生成 (Advanced Concepts)",
        description="综合应用多种TRIZ工具生成高级概念。",
        prompt_template="""
# 角色
你是一位高级创新工程师。

# 任务
综合前面的分析，生成具体的创新概念方案。
重点关注：资源利用、IFR的逼近、裁减（Trimming）。

# 输入内容
{{input}}
"""
    ),
    Skill(
        id=8,
        name="方案评价 (Concept Evaluation)",
        description="对生成的方案进行多维度评价。",
        prompt_template="""
# 角色
你是一位资深技术评审专家。

# 任务
对以下提出的创新方案进行评价。
评价维度：技术可行性、成本、复杂度、创新度、风险。

# 输入内容
{{input}}
"""
    ),
    Skill(
        id=9,
        name="商业策略分析 (Commercial Strategy)",
        description="基于Skill 9，分析商业价值与产业化路径。",
        prompt_template="""
# 角色
你是一位精通TRIZ的技术专家与商业策略分析师。

# 任务
基于生成的技术方案，进行商业价值评估。

## 技能要求
1. **方案验证模板**：技术改进逻辑、实现细节、对比验证。
2. **商业价值与产业化路径**：需求分层、商业化路径拆解（研发/量产/市场）、竞争壁垒。
3. **动态价值评估**：关键技术指标与商业指标的映射。

# 输入内容
{{input}}
"""
    ),
    Skill(
        id=10,
        name="ARIZ算法应用 (ARIZ Application)",
        description="基于Skill 10，应用ARIZ-85C算法进行深度求解。",
        prompt_template="""
# 角色 
你是TRIZ大师，精通ARIZ算法解决工程问题技术创新。

# 任务
请你用ARIZ算法解决专利再创新问题。

# ARIZ算法步骤
1. **问题分析**：情境描述、系统分析、微观问题转化。
2. **问题模型分析**：冲突区域、操作时间、物场资源。
3. **IFR与物理矛盾**：定义IFR-1，定义物理矛盾。
4. **资源动员**：矛盾分离，运用X-Resource。
5. **知识库应用**：科学效应、标准解。
6. **再创新分析**：提出优于现有方案的创新解（Re-Innovation）。

# 要求
输出ARIZ算法求解全过程。求解方案不局限专利现有方案，且要优于现有方案。请特别包含一个“方案优越性评估”的表格，对比原方案与新方案。

# 输入内容
{{input}}
"""
    )
]

def get_skill_by_id(skill_id):
    for skill in SKILLS:
        if skill.id == skill_id:
            return skill
    return None
