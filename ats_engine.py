"""
Mosaab CV - ATS Compatibility Checker Engine v3.0 (Calibrated)
=============================================================
محرك فحص ATS معاير دقيقاً:
- CV احترافي ممتاز = 85-95%
- CV احترافي جيد = 70-84%
- CV عادي/متوسط = 50-69%
- CV ضعيف (صور، جداول، نص قصير) = 30-49%
- CV سيء جداً = <30%
"""

import re
from collections import Counter
from typing import Dict, List, Tuple

class ATSEngine:
    """المحرك الرئيسي لفحص توافق السيرة الذاتية مع ATS"""

    def __init__(self):
        self.section_keywords = self._load_section_keywords()
        self.action_verbs = self._load_action_verbs()
        self.industry_terms = self._load_industry_terms()
        self.weak_phrases = self._load_weak_phrases()

    def _load_section_keywords(self) -> Dict:
        return {
            'experience': [
                'experience', 'work experience', 'professional experience',
                'employment history', 'career history', 'work history',
                'الخبرات', 'الخبرات المهنية', 'العمل', 'خبرة', 'خبرات',
                'work experience'
            ],
            'education': [
                'education', 'academic background', 'qualifications',
                'academic qualifications', 'degrees', 'educational background',
                'التعليم', 'المؤهلات', 'الشهادات', 'الدراسة', 'التعليمية'
            ],
            'skills': [
                'skills', 'technical skills', 'core competencies',
                'key skills', 'professional skills', 'expertise',
                'المهارات', 'الكفاءات', 'المهارات التقنية', 'مهارات'
            ],
            'summary': [
                'summary', 'professional summary', 'career summary',
                'profile', 'objective', 'about me', 'professional profile',
                'الملخص', 'نبذة', 'هدف وظيفي', 'عن نفسي', 'نبذة مهنية'
            ],
            'certifications': [
                'certifications', 'certificates', 'professional certifications',
                'licenses', 'accreditations', 'courses',
                'الشهادات', 'الاعتمادات', 'رخص مهنية', 'دورات', 'كورسات'
            ],
            'projects': [
                'projects', 'key projects', 'portfolio',
                'المشاريع', 'أعمال', 'معرض الأعمال'
            ],
            'languages': [
                'languages', 'language proficiency',
                'اللغات', 'إتقان اللغات'
            ],
            'volunteers': [
                'volunteers', 'volunteer work', 'volunteering',
                'التطوع', 'عمل تطوعي'
            ]
        }

    def _load_action_verbs(self) -> List[str]:
        return [
            'achieved', 'improved', 'developed', 'managed', 'created', 'implemented',
            'increased', 'decreased', 'led', 'designed', 'built', 'launched',
            'optimized', 'streamlined', 'negotiated', 'coordinated', 'analyzed',
            'engineered', 'architected', 'transformed', 'spearheaded', 'delivered',
            'generated', 'reduced', 'enhanced', 'established', 'executed',
            'facilitated', 'initiated', 'integrated', 'maintained', 'mentored',
            'monitored', 'organized', 'oversaw', 'planned', 'produced',
            'resolved', 'reviewed', 'scheduled', 'trained', 'upgraded',
            'utilized', 'validated', 'wrote', 'collaborated', 'conducted',
            'directed', 'drove', 'evaluated', 'expanded', 'formulated',
            'governed', 'guided', 'headed', 'identified', 'influenced',
            'innovated', 'investigated', 'marketed', 'modernized', 'operated',
            'performed', 'pioneered', 'programmed', 'promoted', 'researched',
            'secured', 'solved', 'standardized', 'structured', 'supervised',
            'supported', 'tested', 'troubleshot', 'authored', 'automated',
            'boosted', 'calculated', 'centralized', 'communicated', 'configured',
            'consolidated', 'constructed', 'consulted', 'contributed', 'converted',
            'customized', 'debugged', 'defined', 'deployed', 'designed',
            'detected', 'determined', 'devised', 'diagnosed', 'directed',
            'discovered', 'documented', 'doubled', 'edited', 'educated',
            'effected', 'eliminated', 'enabled', 'encouraged', 'endorsed',
            'enforced', 'ensured', 'examined', 'exceeded', 'excelled',
            'exercised', 'exhibited', 'experimented', 'explained', 'explored',
            'expressed', 'extracted', 'fabricated', 'finalized', 'fixed',
            'forecasted', 'formed', 'fostered', 'founded', 'fulfilled',
            'funded', 'furnished', 'gained', 'gathered', 'generated',
            'grew', 'handled', 'hired', 'hosted', 'hypothesized',
            'illustrated', 'implemented', 'improved', 'increased', 'influenced',
            'informed', 'initiated', 'inspected', 'installed', 'instituted',
            'instructed', 'insured', 'integrated', 'interacted', 'interpreted',
            'interviewed', 'introduced', 'invented', 'inventoried', 'invested',
            'investigated', 'involved', 'issued', 'joined', 'judged',
            'justified', 'kept', 'knew', 'landed', 'launched',
            'learned', 'lectured', 'led', 'licensed', 'lifted',
            'linked', 'listed', 'litigated', 'lived', 'lobbied',
            'localized', 'located', 'logged', 'made', 'maintained',
            'managed', 'manufactured', 'mapped', 'marketed', 'mastered',
            'maximized', 'measured', 'mediated', 'met', 'minimized',
            'modeled', 'modified', 'monitored', 'motivated', 'moved',
            'named', 'narrowed', 'navigated', 'needed', 'negotiated',
            'netted', 'nominated', 'normalized', 'noted', 'noticed',
            'nurtured', 'obeyed', 'objected', 'observed', 'obtained',
            'occupied', 'occurred', 'offered', 'opened', 'operated',
            'opposed', 'opted', 'optimized', 'orchestrated', 'ordered',
            'organized', 'oriented', 'originated', 'outlined', 'overcame',
            'overhauled', 'oversaw', 'owned', 'paced', 'packaged',
            'paid', 'participated', 'partnered', 'passed', 'patented',
            'perceived', 'perfected', 'performed', 'persuaded', 'phased',
            'piloted', 'pinpointed', 'placed', 'planned', 'played',
            'polished', 'pooled', 'popularized', 'positioned', 'possessed',
            'posted', 'praised', 'preceded', 'predicted', 'prepared',
            'prescribed', 'presented', 'preserved', 'presided', 'pressed',
            'prevailed', 'prevented', 'priced', 'printed', 'prioritized',
            'probed', 'proceeded', 'processed', 'procured', 'produced',
            'profited', 'programmed', 'progressed', 'prohibited', 'projected',
            'promoted', 'prompted', 'proofread', 'proposed', 'prospected',
            'protected', 'proved', 'provided', 'published', 'pulled',
            'purchased', 'pursued', 'qualified', 'quantified', 'questioned',
            'quoted', 'raised', 'ranked', 'rated', 'reached',
            'reacted', 'read', 'realigned', 'realized', 'reasoned',
            'received', 'recognized', 'recommended', 'reconciled', 'recorded',
            'recovered', 'recruited', 'rectified', 'recycled', 'redesigned',
            'reduced', 'referred', 'refined', 'refocused', 'refreshed',
            'refunded', 'refused', 'regained', 'regulated', 'rehabilitated',
            'reinforced', 'reinstated', 'rejected', 'related', 'released',
            'remedied', 'remodeled', 'rendered', 'renewed', 'reorganized',
            'repaired', 'replaced', 'replenished', 'reported', 'represented',
            'reproduced', 'requested', 'required', 'researched', 'resolved',
            'responded', 'restored', 'restructured', 'retained', 'retired',
            'retrieved', 'returned', 'revealed', 'reversed', 'reviewed',
            'revised', 'revitalized', 'revived', 'revolutionized', 'rewarded',
            'rewrote', 'routed', 'ran', 'safeguarded', 'saved',
            'scheduled', 'scored', 'screened', 'scripted', 'searched',
            'secured', 'selected', 'sent', 'separated', 'served',
            'serviced', 'set', 'settled', 'shaped', 'shared',
            'sharpened', 'shifted', 'shipped', 'shopped', 'shortened',
            'showed', 'shrank', 'shut', 'simplified', 'simulated',
            'sold', 'solved', 'sorted', 'sought', 'sparked',
            'spearheaded', 'specialized', 'specified', 'sped', 'spent',
            'spoke', 'sponsored', 'spread', 'stabilized', 'staffed',
            'staged', 'standardized', 'started', 'steered', 'stimulated',
            'stopped', 'stored', 'streamlined', 'strengthened', 'stressed',
            'stretched', 'structured', 'studied', 'submitted', 'subscribed',
            'substituted', 'succeeded', 'suggested', 'summarized', 'supervised',
            'supplied', 'supported', 'surpassed', 'surveyed', 'sustained',
            'swapped', 'swept', 'swung', 'sympathized', 'synthesized',
            'systematized', 'tackled', 'taught', 'teamed', 'tempered',
            'tended', 'tested', 'tightened', 'took', 'told',
            'touched', 'traced', 'tracked', 'traded', 'trained',
            'transacted', 'transcended', 'transcribed', 'transferred', 'transformed',
            'transitioned', 'translated', 'transmitted', 'transported', 'traveled',
            'treated', 'trimmed', 'tripled', 'troubleshot', 'trusted',
            'tuned', 'turned', 'tutored', 'typed', 'uncovered',
            'understood', 'undertook', 'underwrote', 'unified', 'united',
            'updated', 'upgraded', 'upheld', 'upset', 'used',
            'utilized', 'validated', 'valued', 'vaulted', 'verbalized',
            'verified', 'versed', 'vetoed', 'visited', 'visualized',
            'voiced', 'volunteered', 'voted', 'vouched', 'waged',
            'waited', 'waived', 'walked', 'wandered', 'wanted',
            'warned', 'warranted', 'washed', 'wasted', 'watched',
            'weighed', 'welcomed', 'widened', 'won', 'wondered',
            'worked', 'worried', 'wrote', 'yielded', 'zeroed',
            'zoned', 'zoomed'
        ]

    def _load_industry_terms(self) -> List[str]:
        return [
            'python', 'java', 'javascript', 'sql', 'excel', 'aws', 'azure',
            'docker', 'kubernetes', 'react', 'angular', 'node', 'django',
            'flask', 'spring', 'hibernate', 'git', 'jenkins', 'ci/cd',
            'agile', 'scrum', 'devops', 'cloud', 'database', 'api',
            'rest', 'graphql', 'microservices', 'machine learning',
            'data analysis', 'business intelligence', 'tableau', 'power bi',
            'project management', 'leadership', 'communication', 'teamwork',
            'problem solving', 'critical thinking', 'time management',
            'customer service', 'sales', 'marketing', 'digital marketing',
            'seo', 'content', 'social media', 'branding', 'strategy',
            'financial analysis', 'accounting', 'budgeting', 'forecasting',
            'supply chain', 'logistics', 'procurement', 'inventory',
            'quality assurance', 'risk management', 'compliance',
            'pharmacy', 'pharmacist', 'pharmaceutical', 'clinical',
            'patient care', 'medication', 'prescription', 'healthcare',
            'nursing', 'medical', 'doctor', 'surgeon', 'diagnosis',
            'engineering', 'mechanical', 'electrical', 'civil', 'industrial',
            'autocad', 'solidworks', 'matlab', 'simulation', 'design',
            'hr', 'recruitment', 'talent', 'performance', 'training',
            'legal', 'contract', 'litigation', 'regulatory', 'compliance',
            'erp', 'sap', 'oracle', 'crm', 'salesforce',
            'data entry', 'data mining', 'etl', 'data warehouse',
            'cybersecurity', 'network', 'firewall', 'penetration testing',
            'blockchain', 'ai', 'artificial intelligence', 'deep learning',
            'nlp', 'computer vision', 'robotics', 'iot',
            'fmcg', 'retail', 'e-commerce', 'b2b', 'b2c',
            'lean', 'six sigma', 'kaizen', 'continuous improvement',
            'kpi', 'metrics', 'dashboard', 'reporting', 'analytics'
        ]

    def _load_weak_phrases(self) -> List[str]:
        """عبارات ضعيفة تدل على CV رديء"""
        return [
            'dealing with', 'responsible for', 'duties included', 'worked on',
            'helped with', 'assisted with', 'involved in', 'participated in',
            'hard worker', 'team player', 'detail oriented', 'motivated',
            'enthusiastic learner', 'fast learner', 'good communication',
            'ability to', 'skills include', 'references available',
            'achievements/tasks', 'tasks included', 'duties were'
        ]

    def _get_stop_words(self) -> set:
        return {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'who',
            'did', 'she', 'use', 'way', 'many', 'oil', 'sit', 'set', 'run',
            'eat', 'far', 'sea', 'eye', 'ago', 'off', 'too', 'any', 'say', 'man',
            'try', 'ask', 'end', 'why', 'let', 'put',
            'own', 'tell', 'very', 'when', 'much', 'would',
            'there', 'their', 'what', 'said', 'each', 'which', 'will', 'about',
            'could', 'other', 'after', 'first', 'never', 'these', 'think', 'where',
            'being', 'every', 'great', 'might', 'shall', 'still', 'those', 'while',
            'this', 'that', 'with', 'have', 'from', 'they', 'know', 'want', 'been',
            'good', 'some', 'time', 'than', 'them', 'well', 'were', 'just', 'like',
            'over', 'also', 'back', 'only', 'come', 'made', 'make', 'most',
            'such', 'take'
        }

    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        text = text.lower()
        words = re.findall(r'[a-zA-Z\u0621-\u064A]{3,}', text)
        stop_words = self._get_stop_words()
        keywords = [w for w in words if w not in stop_words and len(w) >= min_length]
        return keywords

    def calculate_keyword_score(self, cv_text: str, job_description: str) -> Tuple[float, Dict]:
        cv_lower = cv_text.lower()
        cv_words = self.extract_keywords(cv_text)

        # 1. Action verbs (max 12 pts)
        found_verbs = [v for v in self.action_verbs if v in cv_lower]
        verb_score = min(len(found_verbs) / 10, 1.0) * 12

        # 2. Industry terms (max 8 pts)
        found_terms = [t for t in self.industry_terms if t in cv_lower]
        term_score = min(len(found_terms) / 5, 1.0) * 8

        # 3. Measurable achievements (max 8 pts)
        achievements = re.findall(r'\b\d+[%$]?\b|\b\d+\.\d+[%$]?\b', cv_text)
        achievement_score = min(len(achievements) / 5, 1.0) * 8

        # 4. Keyword diversity (max 4 pts)
        unique_words = len(set(cv_words))
        total_words = len(cv_words)
        diversity = (unique_words / total_words) if total_words > 0 else 0
        diversity_score = min(diversity / 0.6, 1.0) * 4

        # 5. Weak phrases penalty (negative)
        weak_found = [p for p in self.weak_phrases if p in cv_lower]
        weak_penalty = min(len(weak_found) * 1.5, 8)  # Max 8 pts penalty

        # 6. Job description matching (max 3 pts)
        job_match_score = 0
        job_match_details = {'matched': [], 'missing': [], 'match_rate': 0}

        if job_description and len(job_description) > 20:
            job_keywords = set(self.extract_keywords(job_description))
            cv_keywords_set = set(cv_words)
            if job_keywords:
                matched = cv_keywords_set.intersection(job_keywords)
                missing = job_keywords - cv_keywords_set
                match_rate = len(matched) / len(job_keywords) * 100
                job_match_score = min(match_rate, 100) * 0.03
                job_match_details = {
                    'matched': list(matched)[:15],
                    'missing': list(missing)[:15],
                    'match_rate': round(match_rate, 1)
                }

        total_score = max(0, min(verb_score + term_score + achievement_score + diversity_score + job_match_score - weak_penalty, 35))

        details = {
            'action_verbs_found': found_verbs[:15],
            'action_verbs_score': round(verb_score, 1),
            'industry_terms_found': found_terms[:15],
            'industry_terms_score': round(term_score, 1),
            'achievements_found': len(achievements),
            'achievements_score': round(achievement_score, 1),
            'weak_phrases_found': weak_found,
            'weak_phrases_penalty': round(weak_penalty, 1),
            'diversity': round(diversity * 100, 1),
            'diversity_score': round(diversity_score, 1),
            'job_match': job_match_details,
            'job_match_score': round(job_match_score, 1),
            'total_keywords': len(cv_words),
            'unique_keywords': unique_words
        }

        return total_score, details

    def check_format(self, cv_text: str) -> Tuple[float, Dict]:
        issues = []
        score = 25
        text_lower = cv_text.lower()

        # 1. جداول معقدة (3+ أعمدة)
        table_pattern = r'\|\s*[^\n|]+\s*\|\s*[^\n|]+\s*\|\s*[^\n|]+\s*\|'
        tables = re.findall(table_pattern, cv_text)
        if len(tables) >= 2:
            score -= 5
            issues.append({
                'severity': 'high',
                'issue': 'تم اكتشاف جداول معقدة قد لا تقرأها ATS',
                'fix': 'استخدم تنسيقاً بسيطاً بدون أعمدة متعددة'
            })

        # 2. صور / عناصر مرئية
        image_indicators = ['<image>', '[image]', 'img src', '<img']
        image_found = any(ind in cv_text.lower() for ind in image_indicators)
        if image_found:
            score -= 8
            issues.append({
                'severity': 'high',
                'issue': 'يحتوي على صور أو عناصر مرئية لا يمكن قراءتها',
                'fix': 'أزل الصور والأيقونات — استخدم نصاً عادياً فقط'
            })

        # 3. أقسام أساسية
        found_sections = []
        missing_sections = []

        for section_name, keywords in self.section_keywords.items():
            if any(kw in text_lower for kw in keywords):
                found_sections.append(section_name)
            else:
                missing_sections.append(section_name)

        essential_sections = ['experience', 'education', 'skills']
        found_essential = sum(1 for s in essential_sections if s in found_sections)

        if found_essential < 2:
            score -= 6
            issues.append({
                'severity': 'high',
                'issue': f'أقسام أساسية مفقودة',
                'fix': 'أضف الأقسام الأساسية: الخبرات، التعليم، المهارات'
            })
        elif found_essential == 2:
            score -= 2
            issues.append({
                'severity': 'medium',
                'issue': 'قسم أساسي واحد مفقود',
                'fix': 'أضف القسم المفقود لتحسين الهيكل'
            })

        # 4. تكرار مفرط (نص مكرر = CV رديء/مولد آلياً)
        lines = [l.strip() for l in cv_text.split('\n') if l.strip() and len(l.strip()) > 5]
        line_counts = Counter(lines)
        repeated = [(line, count) for line, count in line_counts.most_common() if count >= 3]

        if repeated:
            score -= 4
            issues.append({
                'severity': 'high',
                'issue': f'نص مكرر بشكل مفرط ({len(repeated)} عبارات)',
                'fix': 'تجنب تكرار نفس الجمل — اكتب وصفاً فريداً لكل دور'
            })

        # 5. placeholder text مثل "Achievements/Tasks" بدون محتوى
        placeholder_pattern = r'(achievements/tasks?|responsibilities|duties)\s*$'
        placeholders = re.findall(placeholder_pattern, text_lower, re.MULTILINE)
        if len(placeholders) >= 2:
            score -= 3
            issues.append({
                'severity': 'high',
                'issue': 'عناوين placeholder بدون محتوى حقيقي',
                'fix': 'املأ الأقسام بإنجازات حقيقية قابلة للقياس'
            })

        # 6. رموز زخرفية كثيرة
        decorative_chars = re.findall(r'[^\w\s\-_.@/+•\-\*\+|\/\\\(\)\[\]\{\}\.\,\:\;\!\?\@\#\n\r\t]', cv_text)
        if len(decorative_chars) > 80:
            score -= 2
            issues.append({
                'severity': 'low',
                'issue': 'كثرة الرموز الزخرفية',
                'fix': 'استخدم رموزاً بسيطة فقط'
            })

        score = max(0, score)

        details = {
            'found_sections': found_sections,
            'missing_sections': missing_sections,
            'essential_found': found_essential,
            'repeated_lines': repeated[:5],
            'issues': issues,
            'section_count': len(found_sections)
        }

        return score, details

    def check_readability(self, cv_text: str) -> Tuple[float, Dict]:
        issues = []
        score = 20

        sentences = re.split(r'[.!?\n]+', cv_text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        words = cv_text.split()
        word_count = len(words)

        # 1. طول الجمل
        avg_sentence_length = 0
        if sentences:
            avg_sentence_length = len(words) / len(sentences)
            if avg_sentence_length > 30:
                score -= 2
                issues.append({
                    'severity': 'low',
                    'issue': f'جمل طويلة (متوسط {avg_sentence_length:.0f} كلمة)',
                    'fix': 'استخدم جمل أقصر وأكثر وضوحاً'
                })

        # 2. عدد الكلمات
        if word_count > 900:
            score -= 2
            issues.append({
                'severity': 'low',
                'issue': f'السيرة الذاتية طويلة ({word_count} كلمة)',
                'fix': 'اختصر إلى 400-600 كلمة'
            })
        elif word_count < 150:
            score -= 6
            issues.append({
                'severity': 'high',
                'issue': f'السيرة الذاتية قصيرة جداً ({word_count} كلمة)',
                'fix': 'أضف المزيد من التفاصيل عن إنجازاتك'
            })

        # 3. إنجازات قابلة للقياس
        numbers = re.findall(r'\b\d+[%$]?\b|\b\d+\.\d+[%$]?\b', cv_text)
        if len(numbers) < 2:
            score -= 4
            issues.append({
                'severity': 'high',
                'issue': 'لا توجد إنجازات قابلة للقياس',
                'fix': 'أضف أرقاماً: نسب التحسين، المبالغ، أعداد المشاريع'
            })
        elif len(numbers) < 4:
            score -= 1
            issues.append({
                'severity': 'medium',
                'issue': 'قليل من الإنجازات القابلة للقياس',
                'fix': 'أضف المزيد من الأرقام والنسب'
            })

        # 4. أفعال القياس
        cv_lower = cv_text.lower()
        found_verbs = [v for v in self.action_verbs if v in cv_lower]
        if len(found_verbs) < 4:
            score -= 4
            issues.append({
                'severity': 'high',
                'issue': 'استخدام محدود لأفعال القياس والإنجاز',
                'fix': 'ابدأ الجمل بأفعال قوية: حققت، طوّرت، أدارت، أنجزت...'
            })
        elif len(found_verbs) < 8:
            score -= 1
            issues.append({
                'severity': 'low',
                'issue': 'يمكن تحسين أفعال القياس',
                'fix': 'استخدم المزيد من الأفعال القوية'
            })

        # 5. نقاط قصيرة جداً (علامة على جودة رديئة)
        bullets = [l.strip() for l in cv_text.split('\n') if l.strip()]
        short_bullets = [b for b in bullets if 0 < len(b.split()) <= 3 and not b.isupper() and not re.match(r'\d{2}/\d{4}', b)]
        short_ratio = len(short_bullets) / len(bullets) if bullets else 0

        if short_ratio > 0.5 and len(bullets) > 10:
            score -= 3
            issues.append({
                'severity': 'medium',
                'issue': f'نقاط وصفية قصيرة جداً ({len(short_bullets)} من {len(bullets)})',
                'fix': 'وسّع الوصف لكل نقطة بجملة كاملة توضح الإنجاز'
            })

        score = max(0, score)

        details = {
            'word_count': word_count,
            'sentence_count': len(sentences),
            'avg_sentence_length': round(avg_sentence_length, 1),
            'numbers_found': len(numbers),
            'action_verbs_found': found_verbs[:10],
            'action_verbs_count': len(found_verbs),
            'short_bullets': len(short_bullets),
            'short_bullet_ratio': round(short_ratio * 100, 1),
            'issues': issues
        }

        return score, details

    def check_contact_info(self, cv_text: str) -> Tuple[float, Dict]:
        score = 10
        issues = []
        found = {}

        # بريد إلكتروني
        email_patterns = [
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
            r'[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
        ]
        emails = []
        for pattern in email_patterns:
            emails.extend(re.findall(pattern, cv_text))
        emails = list(set(emails))
        found['email'] = len(emails) > 0

        if not emails:
            score -= 4
            issues.append({
                'severity': 'high',
                'issue': 'لم يتم العثور على بريد إلكتروني',
                'fix': 'أضف بريدك الإلكتروني في الأعلى'
            })

        # هاتف
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}',
            r'\b\d{10,12}\b',
            r'\b\d{4}[-.\s]?\d{3}[-.\s]?\d{3}\b',
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
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

        # LinkedIn (اختياري)
        linkedin = re.search(r'linkedin\.com/\S+', cv_text, re.IGNORECASE)
        found['linkedin'] = linkedin is not None
        if not linkedin:
            score -= 1
            issues.append({
                'severity': 'low',
                'issue': 'لا يوجد رابط LinkedIn',
                'fix': 'أضف رابط LinkedIn (اختياري لكن مفيد)'
            })

        # موقع
        location_indicators = ['amman', 'jordan', 'irbid', 'aqaba', 'zarqa', 'madaba',
                               'riyadh', 'jeddah', 'mecca', 'dammam', 'saudi',
                               'dubai', 'abu dhabi', 'uae', 'cairo', 'egypt',
                               'عمان', 'الأردن', 'إربد', 'العقبة', 'الزرقاء',
                               'الرياض', 'جدة', 'مكة', 'الدمام', 'السعودية',
                               'دبي', 'أبوظبي', 'الإمارات', 'القاهرة', 'مصر']
        location_found = any(loc in cv_text.lower() for loc in location_indicators)
        found['location'] = location_found

        score = max(0, score)

        details = {
            'found': found,
            'issues': issues,
            'email': emails[0] if emails else None
        }

        return score, details

    def check_length(self, cv_text: str) -> Tuple[float, Dict]:
        words = cv_text.split()
        word_count = len(words)
        score = 10

        pages = word_count / 250

        if pages > 2.5:
            score -= 3
            recommendation = 'السيرة الذاتية طويلة جداً. حاول الاختصار.'
        elif pages < 0.4:
            score -= 5
            recommendation = 'السيرة الذاتية قصيرة جداً. أضف المزيد من التفاصيل.'
        elif pages > 2:
            score -= 1
            recommendation = 'حاول الاختصار إلى صفحتين كحد أقصى.'
        else:
            recommendation = 'الطول مثالي!'

        details = {
            'word_count': word_count,
            'estimated_pages': round(pages, 1),
            'recommendation': recommendation
        }

        return score, details

    def analyze(self, cv_text: str, job_description: str = "") -> Dict:
        keyword_score, keyword_details = self.calculate_keyword_score(cv_text, job_description)
        format_score, format_details = self.check_format(cv_text)
        readability_score, readability_details = self.check_readability(cv_text)
        contact_score, contact_details = self.check_contact_info(cv_text)
        length_score, length_details = self.check_length(cv_text)

        total_score = round(
            keyword_score + format_score + readability_score +
            contact_score + length_score, 1
        )

        # معايرة ذكية محدودة
        professional_score = 0
        if format_details.get('essential_found', 0) >= 3:
            professional_score += 1
        if readability_details.get('numbers_found', 0) >= 3:
            professional_score += 1
        if readability_details.get('action_verbs_count', 0) >= 8:
            professional_score += 1
        if keyword_details.get('action_verbs_score', 0) >= 8:
            professional_score += 1
        if not any(i['severity'] == 'high' for i in format_details.get('issues', [])):
            professional_score += 1

        # معايرة حذرة: لا نرفع كثيراً
        if professional_score >= 4 and total_score < 60:
            total_score = max(total_score, 60)
        elif professional_score >= 3 and total_score < 50:
            total_score = max(total_score, 50)

        # سقف للـ CVs السيئة
        has_critical = any(i['severity'] == 'high' for i in format_details.get('issues', []))
        has_weak = len(keyword_details.get('weak_phrases_found', [])) >= 4

        if has_critical and has_weak:
            total_score = min(total_score, 45)
        elif has_critical:
            total_score = min(total_score, 55)
        elif has_weak and readability_details.get('word_count', 0) < 300:
            total_score = min(total_score, 50)

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

        all_issues = []
        all_issues.extend(format_details.get('issues', []))
        all_issues.extend(readability_details.get('issues', []))
        all_issues.extend(contact_details.get('issues', []))

        severity_order = {'high': 0, 'medium': 1, 'low': 2, 'info': 3}
        all_issues.sort(key=lambda x: severity_order.get(x.get('severity', 'info'), 4))

        result = {
            'overall_score': total_score,
            'grade': grade,
            'status': status,
            'color': color,
            'professional_indicators': professional_score,
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
            'recommendations': self._generate_recommendations(all_issues, total_score, format_details, keyword_details)
        }

        return result

    def _generate_recommendations(self, issues: List[Dict], score: float, format_details: Dict, keyword_details: Dict) -> List[str]:
        recommendations = []

        if score < 70:
            recommendations.append('🔴 أولوية: أضف إنجازات قابلة للقياس (أرقام ونسب)')

        high_issues = [i for i in issues if i['severity'] == 'high']
        if high_issues:
            recommendations.append(f'⚠️ يوجد {len(high_issues)} مشكلة خطيرة تحتاج إصلاح فوري')

        if format_details.get('essential_found', 0) < 3:
            recommendations.append('📋 أضف الأقسام الأساسية: الخبرات، التعليم، المهارات')

        weak_phrases = keyword_details.get('weak_phrases_found', [])
        if len(weak_phrases) >= 3:
            recommendations.append('✍️ تجنب العبارات الضعيفة: "dealing with", "responsible for", "hard worker"')

        recommendations.append('🎯 ابدأ كل نقطة بفعل قوي: حققت، طوّرت، أدارت، أنجزت...')
        recommendations.append('📏 استخدم خطوطاً قياسية: Arial, Calibri, Times New Roman')
        recommendations.append('📄 احفظ الملف بصيغة PDF مع نص قابل للنسخ (لا صورة)')

        return recommendations


if __name__ == '__main__':
    engine = ATSEngine()
    print("✅ ATS Engine v3.0 (Calibrated) loaded successfully!")
