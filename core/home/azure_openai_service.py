import os
import json
from openai import AzureOpenAI
from typing import Dict, Any, Optional
import logging
from django.conf import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureOpenAIService:
    """Service class for interacting with Azure OpenAI API"""
    
    def __init__(self):
        # Debug configuration values
        logger.info("=== Azure OpenAI Configuration Debug ===")
        logger.info(f"AZURE_OPENAI_GENERATION_API_KEY: {'SET' if settings.AZURE_OPENAI_GENERATION_API_KEY else 'MISSING'}")
        logger.info(f"AZURE_OPENAI_GENERATION_ENDPOINT: {settings.AZURE_OPENAI_GENERATION_ENDPOINT}")
        logger.info(f"AZURE_OPENAI_EMBEDDING_API_KEY: {'SET' if settings.AZURE_OPENAI_EMBEDDING_API_KEY else 'MISSING'}")
        logger.info(f"AZURE_OPENAI_EMBEDDING_ENDPOINT: {settings.AZURE_OPENAI_EMBEDDING_ENDPOINT}")
        logger.info(f"AZURE_OPENAI_API_VERSION: {settings.AZURE_OPENAI_API_VERSION}")
        
        # Validate that required settings are present
        missing_configs = []
        if not settings.AZURE_OPENAI_GENERATION_API_KEY:
            missing_configs.append("AZURE_OPENAI_GENERATION_API_KEY")
        if not settings.AZURE_OPENAI_GENERATION_ENDPOINT:
            missing_configs.append("AZURE_OPENAI_GENERATION_ENDPOINT")
        if not settings.AZURE_OPENAI_EMBEDDING_API_KEY:
            missing_configs.append("AZURE_OPENAI_EMBEDDING_API_KEY")
        if not settings.AZURE_OPENAI_EMBEDDING_ENDPOINT:
            missing_configs.append("AZURE_OPENAI_EMBEDDING_ENDPOINT")
            
        if missing_configs:
            error_msg = f"Azure OpenAI configuration is missing: {', '.join(missing_configs)}. Please check your environment variables."
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Azure OpenAI credentials for generation
        self.generation_client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_GENERATION_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_GENERATION_ENDPOINT
        )
        
        # Azure OpenAI credentials for embeddings (if needed later)
        self.embedding_client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_EMBEDDING_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_EMBEDDING_ENDPOINT
        )
        
        # Model deployment names from settings
        self.generation_model = settings.AZURE_OPENAI_GENERATION_MODEL
        self.embedding_model = settings.AZURE_OPENAI_EMBEDDING_MODEL
    
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
                        "content": "You are an expert business advisor and rural development specialist for Maharashtra, India. You have deep knowledge of village-level entrepreneurship, local markets, government schemes, and practical business implementation. Provide comprehensive, actionable, and location-specific business guidance that village entrepreneurs can immediately implement."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,  # Increased for more comprehensive responses
                temperature=0.6   # Slightly reduced for more focused responses
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
        Conduct a comprehensive business analysis for "{work_type}" in {gram_panchayat} village, {taluka} taluka, {district} district, Maharashtra.{specialty_text}
        
        This business falls under the {sector} sector. Provide detailed, practical information:

        1. WHY this work is perfect for {gram_panchayat}:
        - Local demand, customer base, and market conditions in this village
        - Position of this business in {district} district and competition analysis
        - Geographic, climate, and infrastructure advantages of this area
        - Local skills, traditions, and experience of people
        - Availability of raw materials, energy, and labor

        2. BUSINESS POTENTIAL detailed analysis:
        - Expected monthly earnings (mention in ₹)
        - Initial investment required (detailed cost breakdown)
        - Time to recover investment (payback period)
        - Business expansion opportunities and future plans
        - Local and external market sales opportunities

        3. LOCAL ADVANTAGES specific to {gram_panchayat}:
        - Special advantages this village has compared to other villages
        - Connectivity to nearby cities, transport facilities, and road conditions
        - Local supplier, customer, and trader networks
        - Collaboration possibilities with other local businesses
        - Support from local institutions, cooperatives, and community

        4. GOVERNMENT SUPPORT and schemes:
        - Available Central/State government schemes for this business (mention names)
        - Detailed information about loans, grants, and subsidies
        - Skill development, training centers, and technical assistance
        - Licensing, registration, and legal requirements
        - Marketing, sales, and export assistance

        5. SUCCESS FACTORS for guaranteed success:
        - What to do in the first 6 months (step-by-step guide)
        - Common problems and their immediate solutions
        - Quality control and customer satisfaction tips
        - Financial planning and record-keeping advice
        - Ways to grow the business and future opportunities

        Provide detailed, practical, and immediately actionable suggestions for each point. Use simple English that rural entrepreneurs can easily understand and implement.
        """
        
        return prompt
    
    def _create_marathi_prompt(self, work_type_mr: str, district_mr: str, taluka_mr: str,
                              gram_panchayat_mr: str, sector_mr: str, is_specialty: bool) -> str:
        """Create Marathi prompt for AI analysis"""
        
        specialty_text = f" हे काम {gram_panchayat_mr}ची विशिष्ट कामगिरी मानली जाते." if is_specialty else ""
        
        prompt = f"""
        महाराष्ट्रातील {district_mr} जिल्ह्यातील {taluka_mr} तालुक्यातील {gram_panchayat_mr} गावामध्ये "{work_type_mr}" या व्यवसायाचे सखोल विश्लेषण करा.{specialty_text}
        
        हे काम {sector_mr} क्षेत्रातील आहे. कृपया तपशीलवार आणि व्यावहारिक माहिती द्या:

        1. WHY {gram_panchayat_mr}साठी हे काम योग्य आहे:
        - या गावातील स्थानिक मागणी, ग्राहकवर्ग आणि बाजारपेठेची परिस्थिती
        - {district_mr} जिल्ह्यातील या व्यवसायाची स्थिती आणि स्पर्धा
        - या भागातील भौगोलिक, हवामान आणि पायाभूत सुविधांचे फायदे
        - स्थानिक लोकांची कौशल्ये, परंपरा आणि अनुभव
        - कच्चा माल, उर्जा आणि मजुरांची उपलब्धता

        2. BUSINESS व्यवसायाची शक्यता:
        - महिन्याला किती कमाई अपेक्षित (₹ मध्ये नमूद करा)
        - सुरुवातीची किती गुंतवणूक लागेल (तपशीलवार खर्चाची यादी)
        - किती काळात गुंतवणूक परत येईल
        - व्यवसाय वाढवण्याच्या संधी आणि भविष्यातील योजना
        - स्थानिक आणि बाहेरील बाजारपेठेतील विक्रीच्या संधी

        3. LOCAL {gram_panchayat_mr}चे विशेष फायदे:
        - इतर गावांच्या तुलनेत या गावाचे कोणते विशेष फायदे आहेत
        - जवळच्या शहरांशी जोडणी, वाहतूक सुविधा आणि रस्ते परिस्थिती  
        - स्थानिक पुरवठादार, ग्राहक आणि व्यापारी नेटवर्क
        - गावातील इतर व्यवसायांसोबत सहकार्याची शक्यता
        - स्थानिक संस्था, सहकारी संस्था आणि समुदायाचा पाठिंबा

        4. GOVERNMENT सरकारी सहाय्य आणि योजना:
        - या व्यवसायासाठी उपलब्ध केंद्र/राज्य सरकारी योजना (नावं सांगा)
        - कर्ज, अनुदान आणि सबसिडीची तपशीलवार माहिती
        - कौशल्य विकास, प्रशिक्षण केंद्रे आणि तांत्रिक सहाय्य
        - परवाना, नोंदणी आणि कायदेशीर आवश्यकता
        - मार्केटिंग, विक्री आणि निर्यात सहाय्य

        5. SUCCESS यशस्वी होण्यासाठी महत्वाचे घटक:
        - पहिल्या ६ महिन्यांत काय करावे (स्टेप बाय स्टेप)
        - सामान्य समस्या आणि त्यांचे तत्काळ उपाय
        - गुणवत्ता नियंत्रण आणि ग्राहक समाधानाच्या टिप्स
        - आर्थिक नियोजन आणि हिशेब ठेवण्याच्या सूचना
        - व्यवसाय वाढवण्याचे मार्ग आणि भविष्यातील संधी

        प्रत्येक मुद्द्यासाठी तपशीलवार, व्यावहारिक आणि तत्काळ अंमलात आणता येणारे सुझावणी द्या. ग्रामीण उद्योजकांना सहज समजेल अशी सरल मराठी भाषा वापरा.
        """
        
        return prompt
    
    def _parse_analysis_response(self, analysis_text: str, language: str) -> Dict[str, Any]:
        """Parse and structure the AI analysis response with improved logic"""
        
        # Initialize sections
        sections = {
            'overview': '',
            'why_suitable': [],
            'business_potential': [],
            'local_advantages': [],
            'government_support': [],
            'success_factors': []
        }
        
        # Split text into sections using numbered patterns and keywords
        text_sections = []
        current_section_text = ""
        
        lines = analysis_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for section headers (numbered or keyword-based)
            if (line.startswith(('1.', '2.', '3.', '4.', '5.')) or 
                any(keyword in line.upper() for keyword in ['WHY', 'BUSINESS', 'LOCAL', 'GOVERNMENT', 'SUCCESS'])):
                if current_section_text:
                    text_sections.append(current_section_text.strip())
                current_section_text = line + "\n"
            else:
                current_section_text += line + "\n"
        
        # Add the last section
        if current_section_text:
            text_sections.append(current_section_text.strip())
        
        # Map sections to appropriate categories
        for section_text in text_sections:
            section_lines = [line.strip() for line in section_text.split('\n') if line.strip()]
            if not section_lines:
                continue
                
            header = section_lines[0].lower()
            content_lines = section_lines[1:] if len(section_lines) > 1 else section_lines
            
            # Process content lines into bullet points
            processed_content = []
            for line in content_lines:
                if line.startswith(('-', '•', '*', '→', '➤')):
                    processed_content.append(line[1:].strip())
                elif line and not line.isdigit() and len(line) > 10:
                    processed_content.append(line)
            
            # Categorize based on keywords
            if any(keyword in header for keyword in ['why', 'suitable', 'का योग्य', 'योग्य आहे']):
                sections['why_suitable'] = processed_content[:6]  # Limit to 6 points
            elif any(keyword in header for keyword in ['business', 'potential', 'व्यवसाय', 'शक्यता']):
                sections['business_potential'] = processed_content[:6]
            elif any(keyword in header for keyword in ['local', 'advantage', 'स्थानिक', 'फायदे']):
                sections['local_advantages'] = processed_content[:6]
            elif any(keyword in header for keyword in ['government', 'support', 'सरकारी', 'सहाय्य']):
                sections['government_support'] = processed_content[:6]
            elif any(keyword in header for keyword in ['success', 'factor', 'यश', 'घटक']):
                sections['success_factors'] = processed_content[:6]
            elif not sections['overview']:  # First section becomes overview
                sections['overview'] = ' '.join(processed_content[:2]) if processed_content else section_text[:300]
        
        # Ensure we have an overview
        if not sections['overview']:
            sections['overview'] = analysis_text[:300] + "..." if len(analysis_text) > 300 else analysis_text
        
        # Ensure each section has at least some content
        default_content = {
            'why_suitable': ['स्थानिक मागणी आणि बाजार उपलब्धता', 'कमी गुंतवणुकीत सुरुवात', 'समुदायिक समर्थन'] if language == 'mr' else ['Local market demand available', 'Low investment start possible', 'Community support'],
            'business_potential': ['चांगली कमाईची शक्यता', 'व्यवसाय वाढवण्याची संधी', 'स्थिर ग्राहकवर्ग'] if language == 'mr' else ['Good earning potential', 'Business growth opportunities', 'Stable customer base'],
            'local_advantages': ['स्थानिक कच्चा माल', 'कमी वाहतूक खर्च', 'स्थानिक कौशल्य'] if language == 'mr' else ['Local raw materials', 'Lower transport costs', 'Local skills available'],
            'government_support': ['सरकारी योजना उपलब्ध', 'कौशल्य विकास प्रशिक्षण', 'कर्ज सुविधा'] if language == 'mr' else ['Government schemes available', 'Skill development training', 'Loan facilities'],
            'success_factors': ['गुणवत्तेवर भर', 'ग्राहक सेवा', 'नियमित उत्पादन'] if language == 'mr' else ['Focus on quality', 'Customer service', 'Regular production']
        }
        
        for key, default_list in default_content.items():
            if not sections[key]:
                sections[key] = default_list
        
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

# Singleton instance - lazy initialization
_azure_openai_service_instance = None

def get_azure_openai_service():
    """Get the Azure OpenAI service instance with lazy initialization"""
    global _azure_openai_service_instance
    
    if _azure_openai_service_instance is None:
        try:
            _azure_openai_service_instance = AzureOpenAIService()
            logger.info("Azure OpenAI service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI service: {str(e)}")
            _azure_openai_service_instance = None
            raise
    
    return _azure_openai_service_instance

# For backward compatibility
azure_openai_service = None