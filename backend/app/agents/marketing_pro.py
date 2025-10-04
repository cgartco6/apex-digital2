from .base_agent import BaseAIAgent
import openai
import os

class MarketingAgent(BaseAIAgent):
    def __init__(self):
        super().__init__("MarketingPro", [
            "social_media_campaigns",
            "email_marketing", 
            "ad_copy",
            "analytics"
        ])
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    async def process_task(self, task_data):
        try:
            campaign_type = task_data.get('campaign_type', 'social_media')
            platform = task_data.get('platform', 'general')
            target_audience = task_data.get('target_audience', 'general')
            goals = task_data.get('goals', 'brand awareness')
            
            strategy = await self._create_marketing_strategy(
                campaign_type, platform, target_audience, goals
            )
            
            content_plan = await self._create_content_plan(strategy)
            
            self.log_activity(f"Created {campaign_type} campaign for {platform}")
            
            return {
                "status": "success",
                "campaign_type": campaign_type,
                "platform": platform,
                "strategy": strategy,
                "content_plan": content_plan,
                "metrics_to_track": self._get_metrics_to_track(platform)
            }
            
        except Exception as e:
            self.log_activity(f"Error in marketing campaign: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _create_marketing_strategy(self, campaign_type, platform, audience, goals):
        prompt = f"""
        Create a comprehensive marketing strategy for:
        - Campaign Type: {campaign_type}
        - Platform: {platform}
        - Target Audience: {audience}
        - Goals: {goals}
        
        Include key messaging, target metrics, and platform-specific recommendations.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    async def _create_content_plan(self, strategy):
        prompt = f"""
        Based on this marketing strategy, create a 7-day content plan:
        {strategy}
        
        Include daily posts with content ideas, hashtags, and optimal posting times.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    def _get_metrics_to_track(self, platform):
        metrics = {
            'facebook': ['reach', 'engagement', 'clicks', 'conversions'],
            'instagram': ['likes', 'comments', 'shares', 'saves', 'reach'],
            'tiktok': ['views', 'likes', 'shares', 'comments', 'completion_rate'],
            'twitter': ['impressions', 'engagements', 'retweets', 'link_clicks'],
            'general': ['traffic', 'conversions', 'engagement', 'roi']
        }
        
        return metrics.get(platform, metrics['general'])
