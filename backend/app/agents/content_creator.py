from .base_agent import BaseAIAgent
import openai
import os

class ContentCreationAgent(BaseAIAgent):
    def __init__(self):
        super().__init__("ContentCreator", [
            "website_content", 
            "social_media", 
            "blog_posts", 
            "marketing_copy"
        ])
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    async def process_task(self, task_data):
        try:
            content_type = task_data.get('content_type', 'website')
            topic = task_data.get('topic', '')
            tone = task_data.get('tone', 'professional')
            word_count = task_data.get('word_count', 500)
            
            prompt = self._build_prompt(content_type, topic, tone, word_count)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=word_count
            )
            
            content = response.choices[0].message.content
            
            self.log_activity(f"Created {content_type} content about {topic}")
            
            return {
                "status": "success",
                "content_type": content_type,
                "content": content,
                "word_count": len(content.split()),
                "metadata": {
                    "tone": tone,
                    "topic": topic
                }
            }
            
        except Exception as e:
            self.log_activity(f"Error in content creation: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _build_prompt(self, content_type, topic, tone, word_count):
        prompts = {
            "website": f"Create engaging {tone} website content about {topic}. Approximately {word_count} words.",
            "social_media": f"Create {tone} social media posts about {topic}. Include hashtags and emojis where appropriate.",
            "blog": f"Write a {tone} blog post about {topic}. Approximately {word_count} words with engaging headline.",
            "marketing": f"Create compelling {tone} marketing copy about {topic}. Focus on benefits and call-to-action."
        }
        
        return prompts.get(content_type, prompts["website"])
