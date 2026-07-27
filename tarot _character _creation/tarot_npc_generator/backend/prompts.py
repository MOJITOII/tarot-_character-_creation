def build_profile_prompt(
    card_keys: list[str],
    meanings: list[dict],
    background: str,
    feedback: str = "",
    character_name: str = ""
) -> str:
    prompt_template = """】
请根据以下3张塔罗牌及其解读，在【{Background}】的背景下，生成一位饱满的人物形象。请严格按照以下格式输出：

**XXX人物形象构建完成**

**人物姓名**：{CharacterNamePrompt}

**最终人物形象**：
---
人物的详细形象描述，包含：
1. 年龄、职业、外貌特征
2. 性格底色（基于第1张牌·内核）
3. 核心欲望（基于第1张牌·内核）
4. 出身背景与成长环境（基于第2张牌·土壤）
5. 行动动机与推动情节的力量（基于第3张牌·齿轮）
---

{ChangesSection}

**牌的本意解析**

1. **第1张·内核：牌名**
   *   **本意**：这张牌的核心含义解读。

2. **第2张·土壤：牌名**
   *   **本意**：这张牌的核心含义解读。

3. **第3张·齿轮：牌名**
   *   **本意**：这张牌的核心含义解读。

---

**牌的本意与最终形象映射关系**

1. **从"内核"到性格底色**：
   *   **本意**：第1张牌的核心含义。
   *   **解读**：如何将牌意转化为人物的性格底色和核心欲望。

2. **从"土壤"到出身背景**：
   *   **本意**：第2张牌的核心含义。
   *   **解读**：如何将牌意转化为人物的出身背景和成长环境。

3. **从"齿轮"到行动动机**：
   *   **本意**：第3张牌的核心含义。
   *   **解读**：如何将牌意转化为人物的行动动机和推动情节的力量。

{feedback_section}

以下是抽到的三张牌及其解读：
{cards_info}
"""
    if character_name:
        character_name_prompt = f"{character_name}（保持姓名不变，仅修改人物形象）"
    else:
        character_name_prompt = "姓名（寓意：姓名的深层含义解释）"
    
    if feedback:
        feedback_section = f"用户反馈：{feedback}\n请根据反馈进行修改和优化。"
        changes_section = """**本次改动说明**：
---
请列出本次修改相对于上一版的具体改动点，例如：
1. 性格调整：XXX
2. 背景修改：XXX
3. 动机变更：XXX
---
"""
    else:
        feedback_section = ""
        changes_section = ""

    cards_info_str = ""
    for i, (key, meaning) in enumerate(zip(card_keys, meanings)):
        desc = meaning["描述"]
        keywords = ", ".join(meaning["关键字"])
        cards_info_str += f"牌{i+1}: {key}\n描述: {desc}\n关键字: {keywords}\n\n"

    return prompt_template.format(
        Background=background,
        CharacterNamePrompt=character_name_prompt,
        ChangesSection=changes_section,
        feedback_section=feedback_section,
        cards_info=cards_info_str.strip()
    )