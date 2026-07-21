
"""
Mosaab CV - ATS Compatibility Checker Engine
=============================================
أداة فحص توافق السيرة الذاتية مع أنظمة ATS
"""

import re
import json
from collections import Counter
from typing import Dict, List, Tuple, Optional
import math

class ATSEngine:
    """المحرك الرئيسي لفحص توافق السيرة الذاتية مع ATS"""

    def __init__(self):
        self.ats_rules = self._load_ats_rules()
        self.section_keywords = self._load_section_keywords()

    def _load_ats_rules(self) -> Dict:
        """تحميل قواعد فحص ATS"""
        return {
            'max_score': 100,
            'weights': {
                'keywords': 35,           # توافق الكلمات المفتاحية
                'format': 25,             # التنسيق والهيكل
                'readability': 20,        # سهولة القراءة
                'contact_info': 10,       # معلومات التواصل
                'length': 10,             # الطول المناسب
            }
        }

    def _load_section_keywords(self) -> Dict:
        """الأقسام الأساسية التي يبحث عنها ATS"""
        return {
            'experience': [
                'experience', 'work experience', 'professional experience',
                'employment history', 'career history', 'work history',
                'خبرة', 'خبرات', 'الخبرات المهنية', 'العمل'
            ],
            'education': [
                'education', 'academic background', 'qualifications',
                'academic qualifications', 'degrees',
                'تعليم', 'مؤهلات', 'شهادات', 'الدراسة'
            ],
            'skills': [
                'skills', 'technical skills', 'core competencies',
                'key skills', 'professional skills', 'expertise',
                'مهارات', 'الكفاءات', 'المهارات التقنية'
            ],
            'summary': [
                'summary', 'professional summary', 'career summary',
                'profile', 'objective', 'about me',
                'ملخص', 'نبذة', 'هدف وظيفي', 'عن نفسي'
            ],
            'certifications': [
                'certifications', 'certificates', 'professional certifications',
                'licenses', 'accreditations',
                'شهادات', 'اعتمادات', 'رخص مهنية'
            ],
            'projects': [
                'projects', 'key projects', 'portfolio',
                'مشاريع', 'أعمال', 'معرض الأعمال'
            ],
            'languages': [
                'languages', 'language proficiency',
                'لغات', 'إتقان اللغات'
            ]
        }

    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """استخراج الكلمات المفتاحية من النص"""
        # تنظيف النص
        text = text.lower()
        # إزالة الرموز الخاصة والاحتفاظ بالكلمات والأرقام
        words = re.findall(r'[a-zA-Zأ-ي]{3,}', text)
        # تصفية الكلمات الشائعة
        stop_words = self._get_stop_words()
        keywords = [w for w in words if w not in stop_words and len(w) >= min_length]
        return keywords

    def _get_stop_words(self) -> set:
        """الكلمات الشائعة التي يجب تجاهلها"""
        return {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who', 'boy',
            'did', 'she', 'use', 'her', 'way', 'many', 'oil', 'sit', 'set', 'run',
            'eat', 'far', 'sea', 'eye', 'ago', 'off', 'too', 'any', 'say', 'man',
            'try', 'ask', 'end', 'why', 'let', 'put', 'say', 'she', 'try', 'way',
            'own', 'say', 'too', 'old', 'tell', 'very', 'when', 'much', 'would',
            'there', 'their', 'what', 'said', 'each', 'which', 'will', 'about',
            'could', 'other', 'after', 'first', 'never', 'these', 'think', 'where',
            'being', 'every', 'great', 'might', 'shall', 'still', 'those', 'while',
            'this', 'that', 'with', 'have', 'from', 'they', 'know', 'want', 'been',
            'good', 'much', 'some', 'time', 'than', 'them', 'well', 'were'
        }

    def calculate_keyword_score(self, cv_text: str, job_description: str) -> Tuple[float, Dict]:
        """حساب توافق الكلمات المفتاحية مع الوصف الوظيفي"""
        cv_keywords = set(self.extract_keywords(cv_text))
        job_keywords = set(self.extract_keywords(job_description))

        if not job_keywords:
            return 0.0, {'matched': [], 'missing': [], 'match_rate': 0}

        matched = cv_keywords.intersection(job_keywords)
        missing = job_keywords - cv_keywords

        # حساب النسبة مع وزن للكلمات الأكثر تكراراً
        job_word_freq = Counter(self.extract_keywords(job_description))
        total_weight = sum(job_word_freq.values())

        matched_weight = sum(job_word_freq[w] for w in matched)
        match_rate = (matched_weight / total_weight * 100) if total_weight > 0 else 0

        # تطبيع النتيجة إلى 35 نقطة كحد أقصى
        score = min(match_rate, 100) * 0.35

        details = {
            'matched': list(matched)[:20],
            'missing': list(missing)[:20],
            'match_rate': round(match_rate, 2),
            'total_job_keywords': len(job_keywords),
            'matched_count': len(matched)
        }

        return score, details

    def check_format(self, cv_text: str) -> Tuple[float, Dict]:
        """فحص التنسيق والهيكل"""
        issues = []
        score = 25  # البداية الكاملة

        # 1. فحص الجداول (Tables) - ATS لا يقرأها جيداً
        table_indicators = ['|', '\t\t', '  \t', '\t  ']
        table_found = any(ind in cv_text for ind in table_indicators)
        if table_found:
            score -= 5
            issues.append({
                'severity': 'high',
                'issue': 'تم اكتشاف جداول أو أعمدة قد لا تقرأها ATS بشكل صحيح',
                'fix': 'استخدم تنسيقاً بسيطاً بدون أعمدة متعددة'
            })

        # 2. فحص الصور والأيقونات
        image_indicators = ['[image]', 'img', 'icon', r'\u', r'\x']
        if any(ind in cv_text.lower() for ind in image_indicators):
            score -= 5
            issues.append({
                'severity': 'high',
                'issue': 'قد تحتوي على صور أو أيقونات لا يمكن قراءتها',
                'fix': 'استبدل الأيقونات بنص عادي'
            })

        # 3. فحص الخطوط الخاصة والزخرفة
        special_chars = len(re.findall(r'[^\w\s\-_.@/+]', cv_text))
        if special_chars > 50:
            score -= 3
            issues.append({
                'severity': 'medium',
                'issue': 'كثرة الرموز الخاصة قد تسبب مشاكل في القراءة',
                'fix': 'قلل من استخدام الرموز الزخرفية'
            })

        # 4. فحص الأقسام الأساسية
        text_lower = cv_text.lower()
        required_sections = ['experience', 'education', 'skills']
        found_sections = []
        missing_sections = []

        for section_name, keywords in self.section_keywords.items():
            if any(kw in text_lower for kw in keywords):
                found_sections.append(section_name)
            else:
                missing_sections.append(section_name)

        if len(found_sections) < 3:
            score -= 5
            issues.append({
                'severity': 'high',
                'issue': f'أقسام مفقودة: {", ".join(missing_sections[:3])}',
                'fix': 'أضف الأقسام الأساسية: الخبرات، التعليم، المهارات'
            })

        # 5. فحص الرؤوس والتنسيق
        headers = re.findall(r'^[A-Z][A-Z\s]{2,}$', cv_text, re.MULTILINE)
        if len(headers) < 2:
            score -= 2
            issues.append({
                'severity': 'low',
                'issue': 'قليل من العناوين الواضحة للأقسام',
                'fix': 'استخدم عناوين واضحة بأحرف كبيرة للأقسام'
            })

        # 6. فحص الروابط
        urls = re.findall(r'https?://\S+|www\.\S+', cv_text)
        if not urls:
            issues.append({
                'severity': 'info',
                'issue': 'لا يوجد رابط LinkedIn أو موقع شخصي',
                'fix': 'أضف رابط LinkedIn المحدث'
            })

        score = max(0, score)

        details = {
            'found_sections': found_sections,
            'missing_sections': missing_sections,
            'issues': issues,
            'section_count': len(found_sections)
        }

        return score, details

    def check_readability(self, cv_text: str) -> Tuple[float, Dict]:
        """فحص سهولة القراءة"""
        issues = []
        score = 20

        sentences = re.split(r'[.!?\n]+', cv_text)
        sentences = [s.strip() for s in sentences if s.strip()]

        words = cv_text.split()

        # 1. متوسط طول الجملة
        if sentences:
            avg_sentence_length = len(words) / len(sentences)
            if avg_sentence_length > 25:
                score -= 3
                issues.append({
                    'severity': 'medium',
                    'issue': f'جمل طويلة جداً (متوسط {avg_sentence_length:.1f} كلمة)',
                    'fix': 'استخدم جمل أقصر وأكثر وضوحاً (١٥-٢٠ كلمة)'
                })

        # 2. الكثافة الكلمة
        word_count = len(words)
        if word_count > 1000:
            score -= 3
            issues.append({
                'severity': 'medium',
                'issue': f'السيرة الذاتية طويلة جداً ({word_count} كلمة)',
                'fix': 'اختصر إلى ٤٠٠-٦٠٠ كلمة كحد أقصى'
            })
        elif word_count < 200:
            score -= 3
            issues.append({
                'severity': 'medium',
                'issue': f'السيرة الذاتية قصيرة جداً ({word_count} كلمة)',
                'fix': 'أضف المزيد من التفاصيل حول إنجازاتك'
            })

        # 3. كثافة الأرقام والإنجازات
        numbers = re.findall(r'\b\d+%?\b', cv_text)
        if len(numbers) < 3:
            score -= 3
            issues.append({
                'severity': 'high',
                'issue': 'قليل من الأرقام والإنجازات القابلة للقياس',
                'fix': 'أضف أرقاماً: نسب التحسين، المبالغ، أعداد المشاريع'
            })

        # 4. كلمات القياس (Action Verbs)
        action_verbs = [
            'achieved', 'improved', 'developed', 'managed', 'created', 'implemented',
            'increased', 'decreased', 'led', 'designed', 'built', 'launched',
            'optimized', 'streamlined', 'negotiated', 'coordinated', 'analyzed',
            'developed', 'engineered', 'architected', 'transformed', 'spearheaded'
        ]
        found_verbs = [v for v in action_verbs if v in cv_text.lower()]
        if len(found_verbs) < 3:
            score -= 2
            issues.append({
                'severity': 'medium',
                'issue': 'استخدام محدود لأفعال القياس والإنجاز',
                'fix': 'ابدأ الجمل بأفعال قوية: حققت، طوّرت، أدارت...'
            })

        # 5. تكرار الكلمات
        word_freq = Counter(w.lower() for w in words if len(w) > 3)
        most_common = word_freq.most_common(1)
        if most_common and most_common[0][1] > word_count * 0.05:
            score -= 2
            issues.append({
                'severity': 'low',
                'issue': f'تكرار مفرط لكلمة "{most_common[0][0]}"',
                'fix': 'استخدم مرادفات متنوعة'
            })

        score = max(0, score)

        details = {
            'word_count': word_count,
            'sentence_count': len(sentences),
            'avg_sentence_length': round(avg_sentence_length, 1) if sentences else 0,
            'numbers_found': len(numbers),
            'action_verbs_found': found_verbs,
            'issues': issues
        }

        return score, details

    def check_contact_info(self, cv_text: str) -> Tuple[float, Dict]:
        """فحص معلومات التواصل"""
        score = 10
        issues = []
        found = {}

        # البريد الإلكتروني
        email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
        emails = re.findall(email_pattern, cv_text)
        found['email'] = len(emails) > 0
        if not emails:
            score -= 3
            issues.append({
                'severity': 'high',
                'issue': 'لم يتم العثور على بريد إلكتروني',
                'fix': 'أضف بريدك الإلكتروني في الأعلى'
            })

        # رقم الهاتف
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}',
            r'\b\d{10}\b',
            r'\b\d{4}[-.\s]?\d{3}[-.\s]?\d{3}\b'
        ]
        phone_found = False
        for pattern in phone_patterns:
            if re.search(pattern, cv_text):
                phone_found = True
                break
        found['phone'] = phone_found
        if not phone_found:
            score -= 3
            issues.append({
                'severity': 'high',
                'issue': 'لم يتم العثور على رقم هاتف',
                'fix': 'أضف رقم هاتفك مع رمز الدولة'
            })

        # LinkedIn
        linkedin = re.search(r'linkedin\.com/in/\S+|linkedin\.com/\S+', cv_text, re.IGNORECASE)
        found['linkedin'] = linkedin is not None
        if not linkedin:
            score -= 2
            issues.append({
                'severity': 'medium',
                'issue': 'لا يوجد رابط LinkedIn',
                'fix': 'أضف رابط LinkedIn المحدث'
            })

        # الموقع/المدونة
        website = re.search(r'https?://\S+|www\.\S+', cv_text)
        found['website'] = website is not None

        # الموقع الجغرافي
        location_indicators = ['amman', 'jordan', 'irbid', 'aqaba', 'zarqa', 'madaba', 
                               'عمان', 'الأردن', 'إربد', 'العقبة', 'الزرقاء']
        location_found = any(loc in cv_text.lower() for loc in location_indicators)
        found['location'] = location_found
        if not location_found:
            issues.append({
                'severity': 'info',
                'issue': 'لم يتم العثور على موقع جغرافي',
                'fix': 'أضف مدينتك/دولتك'
            })

        score = max(0, score)

        details = {
            'found': found,
            'issues': issues,
            'email': emails[0] if emails else None
        }

        return score, details

    def check_length(self, cv_text: str) -> Tuple[float, Dict]:
        """فحص الطول المناسب"""
        words = cv_text.split()
        word_count = len(words)
        score = 10

        # الصفحات التقريبية (٢٥٠ كلمة = صفحة)
        pages = word_count / 250

        if pages > 2.5:
            score -= 5
            recommendation = 'السيرة الذاتية طويلة جداً. اختصر إلى صفحتين كحد أقصى.'
        elif pages < 0.5:
            score -= 5
            recommendation = 'السيرة الذاتية قصيرة جداً. أضف المزيد من التفاصيل.'
        elif pages > 2:
            score -= 2
            recommendation = 'حاول الاختصار إلى صفحة واحدة إن أمكن.'
        else:
            recommendation = 'الطول مثالي!'

        details = {
            'word_count': word_count,
            'estimated_pages': round(pages, 1),
            'recommendation': recommendation
        }

        return score, details

    def analyze(self, cv_text: str, job_description: str = "") -> Dict:
        """التحليل الشامل"""
        # تنظيف النص
        cv_text = self._clean_text(cv_text)

        # إجراء جميع الفحوصات
        keyword_score, keyword_details = self.calculate_keyword_score(cv_text, job_description)
        format_score, format_details = self.check_format(cv_text)
        readability_score, readability_details = self.check_readability(cv_text)
        contact_score, contact_details = self.check_contact_info(cv_text)
        length_score, length_details = self.check_length(cv_text)

        # حساب النتيجة الإجمالية
        total_score = round(
            keyword_score + format_score + readability_score + 
            contact_score + length_score, 1
        )

        # تحديد التصنيف
        if total_score >= 85:
            grade = 'A'
            status = 'ممتاز - جاهز للتقديم! 🎯'
            color = 'green'
        elif total_score >= 70:
            grade = 'B'
            status = 'جيد - يحتاج لتحسينات بسيطة'
            color = 'blue'
        elif total_score >= 55:
            grade = 'C'
            status = 'مقبول - تحسينات ضرورية'
            color = 'orange'
        elif total_score >= 40:
            grade = 'D'
            status = 'ضعيف - إعادة بناء مطلوبة'
            color = 'red'
        else:
            grade = 'F'
            status = 'فاشل - يحتاج لإعادة كتابة كاملة'
            color = 'darkred'

        # تجميع كل المشاكل
        all_issues = []
        all_issues.extend(format_details.get('issues', []))
        all_issues.extend(readability_details.get('issues', []))
        all_issues.extend(contact_details.get('issues', []))

        # ترتيب حسب الخطورة
        severity_order = {'high': 0, 'medium': 1, 'low': 2, 'info': 3}
        all_issues.sort(key=lambda x: severity_order.get(x.get('severity', 'info'), 4))

        result = {
            'overall_score': total_score,
            'grade': grade,
            'status': status,
            'color': color,
            'breakdown': {
                'keywords': {
                    'score': round(keyword_score, 1),
                    'max': 35,
                    'percentage': round(keyword_score / 35 * 100, 1),
                    'details': keyword_details
                },
                'format': {
                    'score': round(format_score, 1),
                    'max': 25,
                    'percentage': round(format_score / 25 * 100, 1),
                    'details': format_details
                },
                'readability': {
                    'score': round(readability_score, 1),
                    'max': 20,
                    'percentage': round(readability_score / 20 * 100, 1),
                    'details': readability_details
                },
                'contact_info': {
                    'score': round(contact_score, 1),
                    'max': 10,
                    'percentage': round(contact_score / 10 * 100, 1),
                    'details': contact_details
                },
                'length': {
                    'score': round(length_score, 1),
                    'max': 10,
                    'percentage': round(length_score / 10 * 100, 1),
                    'details': length_details
                }
            },
            'all_issues': all_issues,
            'top_priorities': [i for i in all_issues if i['severity'] == 'high'][:5],
            'recommendations': self._generate_recommendations(all_issues, total_score)
        }

        return result

    def _clean_text(self, text: str) -> str:
        """تنظيف النص من العناصر غير المرغوبة"""
        # إزالة الروابط
        text = re.sub(r'https?://\S+', '', text)
        # إزالة البريد الإلكتروني
        text = re.sub(r'\S+@\S+', '', text)
        # إزالة الأرقام الطويلة
        text = re.sub(r'\b\d{10,}\b', '', text)
        return text

    def _generate_recommendations(self, issues: List[Dict], score: float) -> List[str]:
        """توليد توصيات مخصصة"""
        recommendations = []

        if score < 70:
            recommendations.append('🔴 أولوية قصوى: أعد كتابة السيرة الذاتية باستخدام قالب ATS-friendly')

        high_issues = [i for i in issues if i['severity'] == 'high']
        if high_issues:
            recommendations.append(f'⚠️ يوجد {len(high_issues)} مشكلة خطيرة تحتاج إصلاح فوري')

        if not any('linkedin' in i['issue'].lower() for i in issues):
            recommendations.append('💡 نصيحة: أضف رابط LinkedIn المحدث مع صورة احترافية')

        recommendations.append('📏 استخدم خطوطاً قياسية: Arial, Calibri, أو Times New Roman')
        recommendations.append('🎯 ركّز على الإنجازات القابلة للقياس لا الواجبات الوظيفية')
        recommendations.append('📄 احفظ الملف بصيغة PDF مع نص قابل للنسخ (لا صورة)')

        return recommendations


if __name__ == '__main__':
    engine = ATSEngine()
    print("✅ ATS Engine loaded successfully!")
