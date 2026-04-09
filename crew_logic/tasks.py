from crewai import Task

def create_suggestion_task(researcher, topic):
    """
    Creates the first task for generating 5 unique blog angles.
    """
    return Task(
        description=f"Generate EXACTLY 5 unique, relevant, and interesting blog post topics based on this base topic: '{topic}'.\n\n"
                    f"Rules for the 5 suggestions:\n"
                    f"- Each suggestion must be DIFFERENT (not just rephrased).\n"
                    f"- Cover different angles (e.g., styling, history, budget, body types, seasonal).\n"
                    f"- Use current fashion trends (2024-2025).\n"
                    f"- Be specific, not generic.\n"
                    f"- Include a 'hook' in the title.\n\n"
                    f"Output strictly just the 5 titles formatted as a numbered list.",
        expected_output="A numbered list of 5 catchy, unique blog post titles.",
        agent=researcher
    )

def create_writing_tasks(researcher, writer, editor, selected_topic, word_count):
    """
    Creates and returns the tasks for researching and writing the selected topic.
    """
    research_task = Task(
        description=f"Conduct deep research on the following fashion topic: '{selected_topic}'. "
                    f"You must find and compile: credible sources, data points, expert quotes, "
                    f"image references, and reference links relevant to the topic. "
                    f"Provide this research brief to the writer.",
        expected_output="A deep research brief containing sources, data points, quotes, and image links.",
        agent=researcher
    )

    template = (
        "TITLE (ALL CAPS, no hashtags)\n\n"
        "Introduction\n"
        "...\n\n"
        "SUBTITLE 1 (No hashtags, ALL CAPS)\n"
        "...\n\n"
        "SUBTITLE 2 (No hashtags, ALL CAPS)\n"
        "...\n\n"
        "Conclusion\n"
        "...\n\n"
        "--- \n\n"
        "Slogan: [Insert 1 punchy, memorable Slogan string here]\n\n"
        "--- \n\n"
        "Colors You Want To Try\n"
        "- **[Color 1]**: [HEX_1] - [Desc]\n"
        "- **[Color 2]**: [HEX_2] - [Desc]\n"
        "- **[Color 3]**: [HEX_3] - [Desc]\n"
        "- **[Color 4]**: [HEX_4] - [Desc]\n"
        "- **[Color 5]**: [HEX_5] - [Desc]\n\n"
        "--- \n\n"
        "3 Expert Tips\n"
        "1. [Tip 1]\n"
        "2. [Tip 2]\n"
        "3. [Tip 3]\n\n"
        "--- \n\n"
        "Frequently Asked Questions\n"
        "**Q: [Question 1]**\n"
        "A: [Answer]\n\n"
        "**Q: [Question 2]**\n"
        "A: [Answer]\n\n"
        "**Q: [Question 3]**\n"
        "A: [Answer]\n\n"
        "--- \n\n"
        "Visual Inspiration\n"
        "- **[Image 1 Desc]**: [Link]\n"
        "- **[Image 2 Desc]**: [Link]\n"
        "- **[Image 3 Desc]**: [Link]\n"
        "- **[Image 4 Desc]**: [Link]\n\n"
        "--- \n\n"
        "Reference Links\n"
        "- [Ref 1]\n"
        "- [Ref 2]\n"
        "- [Ref 3]\n"
        "- [Ref 4]\n"
        "- [Ref 5]\n\n"
        "--- \n\n"
        "Discussion Questions\n"
        "1. [Question 1]\n"
        "2. [Question 2]\n"
        "3. [Question 3]\n"
    )

    writing_task = Task(
        description=f"Using the research brief, write a highly engaging, professional fashion ARTICLE about '{selected_topic}'.\n\n"
                    f"CRITICAL FORMATTING INSTRUCTION:\n"
                    f"Generate the blog article as PURE MARKDOWN only. NO HTML tags. NO div tags. NO CSS classes. NO inline styles. NO style attributes. NO swatch-container. NO tips-container. NO visual-grid. NO reference-container. NO colorful-box. NO faq-box. NO expert-tip-card. NO image tags.\n\n"
                    f"DO NOT USE '#' HASH TAGS FOR HEADINGS OR SUBTITLES.\n"
                    f"Use plain text, uppercase, plain paragraphs, bullet points (-), bold text (**), italic text (*), plain text links, and (---) horizontal rules.\n\n"
                    f"DETAILED REQUIREMENTS:\n"
                    f"- Exactly 2 subtitles.\n"
                    f"- Introduction: 2-3 paragraphs, 3-4 full sentences each.\n"
                    f"- Subtitles 1 & 2: 3-4 paragraphs per subtitle, 3-5 sentences each. Subtitle 1 gets a stat. Subtitle 2 gets an expert quote.\n"
                    f"- Conclusion: 1-2 paragraphs.\n"
                    f"- Slogan: After conclusion.\n"
                    f"- Exactly 5 color swatches with hex codes as a bulleted list.\n"
                    f"- Exactly 3 expert tips as a numbered list.\n"
                    f"- Exactly 3 FAQs as Bold Q / Normal A.\n"
                    f"- Exactly 4 visual links as a bulleted list.\n"
                    f"- Exactly 5 reference links as a bulleted list.\n"
                    f"- Exactly 3 discussion questions as a numbered list.\n\n"
                    f"The total main content should hit approximately {word_count} words.\n\n"
                    f"TEMPLATE YOU MUST FOLLOW EXACTLY:\n\n"
                    f"{template}",
        expected_output="An article formatted exactly matching the pure Markdown rules provided without any '#'.",
        agent=writer
    )

    editing_task = Task(
        description=f"Review the blog post draft on '{selected_topic}'. "
                    f"Ensure PERFECT adherence to the PURE MARKDOWN instruction. "
                    f"Verify absolutely ZERO HTML (`<div>`, `<span>`, `<br>`, etc.) exists anywhere in the code. "
                    f"Verify NO hashes ('#') are used for headings or subheadings.",
        expected_output="A final, pure markdown article containing zero HTML and zero hashtags.",
        agent=editor
    )

    return research_task, writing_task, editing_task
