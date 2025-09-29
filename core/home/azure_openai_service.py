import os
import json
from openai import AzureOpenAI
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureOpenAIService:
    """Service class for interacting with Azure OpenAI API"""
    
    def __init__(self):
        # Azure OpenAI credentials for generation
        self.generation_client = AzureOpenAI(
            api_key="EzJLxZQRf8MEWAKA2F9f46lIukbOBYn0Orv5YA96lSOUVRcwUR52JQQJ99BGACHYHv6XJ3w3AAAAACOGSQqB",
            api_version="2024-02-15-preview",
            azure_endpoint="https://karam-mdc6aytc-eastus2.openai.azure.com/"
        )
        
        # Azure OpenAI credentials for embeddings (if needed later)
        self.embedding_client = AzureOpenAI(
            api_key="ACAThiJJscBMSmQRA6UnBGtKAXxkcE77EgQOZal184mJuS1i4GNxJQQJ99BGAC77bzfXJ3w3AAABACOGJnaG",
            api_version="2024-02-15-preview",
            azure_endpoint="https://karam-hackrx-openai.openai.azure.com/"
        )
        
        # Model deployment names (adjust these based on your actual deployments)
        self.generation_model = "gpt-35-turbo"  # or "gpt-4" if available
        self.embedding_model = "text-embedding-ada-002"
    
    def generate_work_analysis(self, work_type: str, work_type_mr: str, district: str, district_mr: str, 
                              taluka: str, taluka_mr: str, gram_panchayat: str, gram_panchayat_mr: str,
                              sector: str, sector_mr: str, is_specialty: bool = False, 
                              language: str = "en") -> Dict[str, Any]:
        """
        Generate comprehensive AI analysis for a work suggestion based on location and work type
        
        Args:
            work_type: Work type name in English
            work_type_mr: Work type name in Marathi
            district: District name in English
            district_mr: District name in Marathi
            taluka: Taluka name in English
            taluka_mr: Taluka name in Marathi
            gram_panchayat: Gram Panchayat name in English
            gram_panchayat_mr: Gram Panchayat name in Marathi
            sector: Sector name in English
            sector_mr: Sector name in Marathi
            is_specialty: Whether this work is a local specialty
            language: Target language for response ("en" or "mr")
        
        Returns:
            Dictionary containing generated analysis
        """
        
        try:
            # Create the prompt based on language preference
            if language == "mr":
                prompt = self._create_marathi_prompt(
                    work_type_mr, district_mr, taluka_mr, gram_panchayat_mr, 
                    sector_mr, is_specialty
                )
            else:
                prompt = self._create_english_prompt(
                    work_type, district, taluka, gram_panchayat, 
                    sector, is_specialty
                )
            
            # Generate response using Azure OpenAI
            response = self.generation_client.chat.completions.create(
                model=self.generation_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert business advisor for rural entrepreneurship in Maharashtra, India. Provide practical, location-specific business advice for village-level entrepreneurs."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            # Parse the response
            analysis_text = response.choices[0].message.content.strip()
            
            # Structure the response
            return self._parse_analysis_response(analysis_text, language)
            
        except Exception as e:
            logger.error(f"Error generating work analysis: {str(e)}")
            return self._get_fallback_analysis(work_type, gram_panchayat, language)
    
    def _create_english_prompt(self, work_type: str, district: str, taluka: str, 
                              gram_panchayat: str, sector: str, is_specialty: bool) -> str:
        """Create English prompt for AI analysis"""
        
        specialty_text = f" This work is considered a local specialty of {gram_panchayat}." if is_specialty else ""
        
        prompt = f"""
        Analyze the business opportunity for "{work_type}" in {gram_panchayat} village, {taluka} taluka, {district} district, Maharashtra.{specialty_text}
        
        This work falls under the {sector} sector. Please provide:
        
        1. WHY this work is suitable for {gram_panchayat}:
        - Local market demand and opportunities
        - Geographic and demographic advantages
        - Available resources and skills in the area
        
        2. BUSINESS POTENTIAL:
        - Market size and growth potential
        - Revenue expectations for a small entrepreneur
        - Investment requirements and profitability
        
        3. LOCAL ADVANTAGES:
        - Why {gram_panchayat} is particularly good for this work
        - Transportation and infrastructure benefits
        - Local supplier/customer network possibilities
        
        4. GOVERNMENT SUPPORT:
        - Available schemes and subsidies for this sector
        - Training programs and mentorship opportunities
        - Licensing and regulatory support
        
        5. SUCCESS FACTORS:
        - Key requirements for success in this location
        - Common challenges and how to overcome them
        - Timeline for business establishment
        
        Please make the response practical, actionable, and specific to rural Maharashtra context. Use simple language that village entrepreneurs can understand.
        """
        
        return prompt
    
    def _create_marathi_prompt(self, work_type_mr: str, district_mr: str, taluka_mr: str,
                              gram_panchayat_mr: str, sector_mr: str, is_specialty: bool) -> str:
        """Create Marathi prompt for AI analysis"""
        
        specialty_text = f" हे काम {gram_panchayat_mr}ची विशिष्ट कामगिरी मानली जाते." if is_specialty else ""
        
        prompt = f"""
        {gram_panchayat_mr} गाव, {taluka_mr} तालुका, {district_mr} जिल्हा, महाराष्ट्र येथे "{work_type_mr}" या व्यवसायाच्या संधीचे विश्लेषण करा.{specialty_text}
        
        हे काम {sector_mr} क्षेत्रात येते. कृपया पुढील गोष्टी सांगा:
        
        1. {gram_panchayat_mr}साठी हे काम का योग्य आहे:
        - स्थानिक बाजारातील मागणी आणि संधी
        - भौगोलिक आणि लोकसंख्याशास्त्रीय फायदे
        - या भागातील उपलब्ध संसाधने आणि कौशल्ये
        
        2. व्यवसायाची शक्यता:
        - बाजाराचा आकार आणि वाढीची शक्यता
        - छोट्या उद्योजकासाठी कमाईची अपेक्षा
        - गुंतवणुकीची आवश्यकता आणि नफ्याची शक्यता
        
        3. स्थानिक फायदे:
        - या कामासाठी {gram_panchayat_mr} का विशेष चांगले आहे
        - वाहतूक आणि पायाभूत सुविधांचे फायदे
        - स्थानिक पुरवठादार/ग्राहक नेटवर्कची शक्यता
        
        4. सरकारी सहाय्य:
        - या क्षेत्रासाठी उपलब्ध योजना आणि अनुदान
        - प्रशिक्षण कार्यक्रम आणि मार्गदर्शन संधी
        - परवाना आणि नियामक सहाय्य
        
        5. यशाचे घटक:
        - या ठिकाणी यशस्वी होण्यासाठी मुख्य आवश्यकता
        - सामान्य आव्हाने आणि ती कशी सोडवायची
        - व्यवसाय स्थापनेसाठी वेळसारणी
        
        कृपया ग्रामीण महाराष्ट्राच्या संदर्भात व्यावहारिक, कृतीशील आणि विशिष्ट उत्तर द्या. गावातील उद्योजकांना समजेल अशी सोपी भाषा वापरा.
        """
        
        return prompt
    
    def _parse_analysis_response(self, analysis_text: str, language: str) -> Dict[str, Any]:
        """Parse and structure the AI response"""
        
        # Split the response into sections (this is a simple approach)
        lines = analysis_text.strip().split('\n')
        
        # Extract different sections based on content
        sections = {
            'overview': '',
            'why_suitable': [],
            'business_potential': [],
            'local_advantages': [],
            'government_support': [],
            'success_factors': []
        }
        
        current_section = 'overview'
        section_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Simple section detection based on keywords
            if any(keyword in line.lower() for keyword in ['why', 'suitable', 'का योग्य']):
                if section_content and current_section == 'overview':
                    sections['overview'] = ' '.join(section_content)
                current_section = 'why_suitable'
                section_content = []
            elif any(keyword in line.lower() for keyword in ['business', 'potential', 'व्यवसाय', 'शक्यता']):
                if section_content:
                    sections[current_section] = section_content
                current_section = 'business_potential'
                section_content = []
            elif any(keyword in line.lower() for keyword in ['local', 'advantage', 'स्थानिक', 'फायदे']):
                if section_content:
                    sections[current_section] = section_content
                current_section = 'local_advantages'
                section_content = []
            elif any(keyword in line.lower() for keyword in ['government', 'support', 'सरकारी', 'सहाय्य']):
                if section_content:
                    sections[current_section] = section_content
                current_section = 'government_support'
                section_content = []
            elif any(keyword in line.lower() for keyword in ['success', 'factor', 'यश', 'घटक']):
                if section_content:
                    sections[current_section] = section_content
                current_section = 'success_factors'
                section_content = []
            else:
                # Clean and add line to current section
                if line.startswith('-') or line.startswith('•') or line.startswith('*'):
                    line = line[1:].strip()
                if line and not line.isdigit() and len(line) > 5:
                    section_content.append(line)
        
        # Add the last section
        if section_content:
            sections[current_section] = section_content
        
        # If overview is empty, create one from the full text
        if not sections['overview']:
            sections['overview'] = analysis_text[:200] + "..." if len(analysis_text) > 200 else analysis_text
        
        return sections
    
    def _get_fallback_analysis(self, work_type: str, gram_panchayat: str, language: str) -> Dict[str, Any]:
        """Provide fallback analysis if AI generation fails"""
        
        if language == "mr":
            return {
                'overview': f'{gram_panchayat}मध्ये {work_type} हा एक चांगला व्यवसायिक पर्याय आहे.',
                'why_suitable': [
                    'स्थानिक मागणी आणि बाजार उपलब्धता',
                    'ग्रामीण भागासाठी योग्य व्यवसाय',
                    'कमी गुंतवणुकीत सुरुवात करता येते'
                ],
                'business_potential': [
                    'चांगली कमाईची शक्यता',
                    'वाढत्या मागणीमुळे व्यवसाय वाढू शकतो',
                    'स्थानिक ग्राहकांची निष्ठा मिळते'
                ],
                'local_advantages': [
                    'स्थानिक कच्चा माल उपलब्ध',
                    'कमी वाहतूक खर्च',
                    'समुदायाचा पाठिंबा मिळतो'
                ],
                'government_support': [
                    'सरकारी योजना आणि अनुदान उपलब्ध',
                    'कौशल्य विकास प्रशिक्षण',
                    'सुलभ कर्ज योजना'
                ],
                'success_factors': [
                    'गुणवत्तेवर भर द्या',
                    'ग्राहक सेवेला प्राधान्य द्या',
                    'नियमित उत्पादन आणि पुरवठा'
                ]
            }
        else:
            return {
                'overview': f'{work_type} is a good business opportunity in {gram_panchayat}.',
                'why_suitable': [
                    'Local demand and market availability',
                    'Suitable business for rural areas',
                    'Can start with low investment'
                ],
                'business_potential': [
                    'Good earning potential',
                    'Business can grow with increasing demand',
                    'Builds loyal local customer base'
                ],
                'local_advantages': [
                    'Local raw materials available',
                    'Lower transportation costs',
                    'Community support'
                ],
                'government_support': [
                    'Government schemes and subsidies available',
                    'Skill development training',
                    'Easy loan schemes'
                ],
                'success_factors': [
                    'Focus on quality',
                    'Prioritize customer service',
                    'Maintain regular production and supply'
                ]
            }

# Global instance
azure_openai_service = AzureOpenAIService()