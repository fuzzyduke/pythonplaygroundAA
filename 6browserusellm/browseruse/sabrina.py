from browser_use import Agent, Browser, BrowserConfig, Controller
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
import asyncio

# Configure the browser to connect to your Chrome instance
browser = Browser(

    config=BrowserConfig(
        chrome_instance_path="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        
    )
)

# Central agent
agent = Agent(
    task="""
    0. select bb
    1. Open Twitter: https://x.com/search?q=ai&src=typed_query&f=top
    2. Scroll the feed until you find a detailed educational tweet about AI.
    3. Research the topic further. Analyze a relevant website, article, or blog.
    4. Open Threads: https://www.threads.net/@sabrina_ramonov
    5. Write a HIGHLY EDUCATIONAL post related to the tweet and research you found, using this prompt:

<prompt>
# CONTEXT

Infer the topic from the sources provided.

# WRITING STYLE

Here’s how you always write:

<writing_style>

- Your writing style is spartan and informative.
- Use clear, simple language.
- Employ short, impactful sentences.
- Incorporate bullet points for easy readability.
- Use frequent line breaks to separate ideas.
- Use active voice; avoid passive voice.
- Focus on practical, actionable insights.
- Use specific examples and personal experiences to illustrate points.
- Incorporate data or statistics to support claims when possible.
- Ask thought-provoking questions to encourage reader reflection.
- Use ""you"" and ""your"" to directly address the reader.
- Avoid metaphors and clichés.
- Avoid generalizations.
- Do not include common setup language in any sentence, including: in conclusion, in closing, etc.
- Do not output warnings or notes—just the output requested.
- Do not use hashtags.
- Do not use semicolons.
- Do not use emojis.
- Do not use asterisks.
- Do not use adjectives and adverbs.
- Do NOT use these words:
can, may, just, that, very, really, literally, actually, certainly, probably, basically, could, maybe, delve, embark, enlightening, esteemed, shed light, craft, crafting, imagine, realm, game-changer, unlock, discover, skyrocket, abyss, you're not alone, in a world where, revolutionize, disruptive, utilize, utilizing, dive deep, tapestry, illuminate, unveil, pivotal, enrich, intricate, elucidate, hence, furthermore, realm, however, harness, exciting, groundbreaking, cutting-edge, remarkable, it. remains to be seen, glimpse into, navigating, landscape, stark, testament, in summary, in conclusion, moreover, boost, bustling, opened up, powerful, inquiries, ever-evolving

</writing_style>

# PLANNING

Your goal is to write a social media post.

1. Analyze the provided sources thoroughly.
2. Study the <example1> and <example2> posts below carefully. You will be asked to replicate their:
    - Overall structure.
    - Tone and voice.
    - Formatting (including line breaks and spacing).
    - Length (aim for a similarly detailed post).
    - Absence of emojis.
    - Use of special characters (if any).
    - Emotional resonance.

<example1>
I built an AI Social Media System that saves you 20 HOURS per week. Create and distribute content everywhere 24/7 — 100% on autopilot.

No need for a team.
No need for paid ads.
No need for hours of manual work.

This system combines multiple AI tools to handle everything from writing content, generating images, and creating avatar videos.

Easily tweak the system for your needs.

And I've made it for YOU, for FREE:
</example1>

<example2>
95% of AI Automation Agencies in 2025 will FAIL.

Here's a much easier path to $20k/mo... 👇️

Loads of ppl jumping into AAA hype WITHOUT understanding the work involved for fulfillment.

But, small businesses need help with the BASICS of AI.

Think very, very basic...

What is ChatGPT? How do I install it? Is there a mobile app? Which model should I use? How do I upload a file? What's that button do? How do I ask it stuff?
</example2>

# OUTPUT
Follow the GUIDELINES below to write the post. Use your analysis from step 1 and step 2. Use the provided sources as the foundation for your post, expanding on it significantly while maintaining the style and structure of the examples provided from step 2. You MUST use information from the provided sources. Make sure you adhere to your <writing_style>.

Here are the guidelines:
<guidelines>
Write a thought-provoking tweet. Start with a bold controversial sentence. Write 5 more sentences in 5th grade reading level. Every sentence must be concise. Remove ALL adjectives and adverbs.

!IMPORTANT: before outputting your final answer,  ensure your answer contains fewer than 280 characters.
</guidelines>
Take a deep breath and take it step-by-step!

# INPUT

Sources: Use the tweet and research you found!

</prompt>

    6. Rewrite the last sentence to be a controversial question that people will want to answer.
    7. Post it.
""",
    llm=ChatOpenAI(model="gpt-4o", timeout=1000),
    browser=browser,
)


async def main():
    await agent.run(max_steps=1000)
    await browser.close()


if __name__ == "__main__":
    asyncio.run(main())