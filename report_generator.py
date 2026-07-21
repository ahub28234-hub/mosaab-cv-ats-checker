
"""
Mosaab CV - Report Generator
=============================
مولد التقارير بصيغ HTML و Markdown
"""

import json
from datetime import datetime
from typing import Dict

class ReportGenerator:
    """مولد التقارير الاحترافية"""

    def __init__(self, logo_text: str = "Mosaab CV"):
        self.logo_text = logo_text
        self.colors = {
            'green': '#22c55e',
            'blue': '#3b82f6', 
            'orange': '#f97316',
            'red': '#ef4444',
            'darkred': '#991b1b',
            'gray': '#6b7280',
            'light': '#f3f4f6'
        }

    def generate_html(self, result: Dict, file_info: Dict, output_path: str):
        """توليد تقرير HTML"""

        score = result['overall_score']
        grade = result['grade']
        color = self.colors.get(result['color'], '#3b82f6')

        # بناء شريط التقدم
        def progress_bar(percentage, color_hex):
            return f"""
            <div style="background:#e5e7eb;border-radius:8px;height:20px;overflow:hidden;margin:5px 0;">
                <div style="background:{color_hex};width:{percentage}%;height:100%;border-radius:8px;
                            transition:width 0.5s;display:flex;align-items:center;justify-content:center;">
                    <span style="color:white;font-size:11px;font-weight:bold;">{percentage}%</span>
                </div>
            </div>
            """

        # بناء قسم المشاكل
        issues_html = ""
        severity_icons = {
            'high': '🔴',
            'medium': '🟡', 
            'low': '🔵',
            'info': 'ℹ️'
        }

        for issue in result['all_issues'][:15]:
            icon = severity_icons.get(issue['severity'], '⚪')
            issues_html += f"""
            <div style="background:#fef2f2;border-right:4px solid {color};padding:12px;margin:8px 0;border-radius:4px;">
                <div style="font-weight:bold;color:#374151;">{icon} {issue['issue']}</div>
                <div style="color:#6b7280;font-size:13px;margin-top:4px;">💡 الحل: {issue['fix']}</div>
            </div>
            """

        # التوصيات
        recs_html = ""
        for rec in result['recommendations']:
            recs_html += f"<li style='margin:8px 0;color:#374151;'>{rec}</li>"

        # الأقسام
        sections_html = ""
        for section_name, section_data in result['breakdown'].items():
            section_color = self._get_section_color(section_data['percentage'])
            sections_html += f"""
            <div style="background:white;border-radius:12px;padding:20px;margin:15px 0;box-shadow:0 1px 3px rgba(0,0,0,0.1);">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                    <h3 style="margin:0;color:#1f2937;text-transform:capitalize;">{self._translate_section(section_name)}</h3>
                    <span style="font-size:24px;font-weight:bold;color:{section_color};">{section_data['score']}/{section_data['max']}</span>
                </div>
                {progress_bar(section_data['percentage'], section_color)}
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير فحص ATS - {file_info['name']}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap');
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Tajawal', sans-serif; 
            background: #f8fafc; 
            color: #1f2937;
            line-height: 1.6;
        }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ 
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            color: white; 
            padding: 40px 30px; 
            border-radius: 16px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .score-circle {{
            width: 150px; height: 150px;
            border-radius: 50%;
            background: white;
            margin: 20px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .score-number {{ font-size: 48px; font-weight: 800; color: {color}; }}
        .score-label {{ font-size: 14px; color: #6b7280; }}
        .grade-badge {{
            display: inline-block;
            background: {color};
            color: white;
            padding: 8px 24px;
            border-radius: 20px;
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
        }}
        .section {{ margin: 25px 0; }}
        .section-title {{ 
            font-size: 20px; 
            font-weight: 700; 
            color: #1e3a5f;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e5e7eb;
        }}
        .file-info {{
            background: #eff6ff;
            border-radius: 8px;
            padding: 15px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }}
        .info-item {{ text-align: center; }}
        .info-label {{ font-size: 12px; color: #6b7280; }}
        .info-value {{ font-size: 16px; font-weight: 700; color: #1e3a5f; }}
        .footer {{
            text-align: center;
            padding: 30px;
            color: #9ca3af;
            font-size: 13px;
            margin-top: 40px;
            border-top: 1px solid #e5e7eb;
        }}
        .priority-box {{
            background: #fef3c7;
            border: 1px solid #f59e0b;
            border-radius: 8px;
            padding: 15px;
            margin: 15px 0;
        }}
        .priority-box h4 {{ color: #92400e; margin-bottom: 10px; }}
        @media print {{
            body {{ background: white; }}
            .header {{ border-radius: 0; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 تقرير فحص توافق السيرة الذاتية مع ATS</h1>
            <div class="score-circle">
                <div class="score-number">{score}</div>
                <div class="score-label">من 100</div>
            </div>
            <div class="grade-badge">{grade} - {result['status']}</div>
            <p style="margin-top:15px;opacity:0.9;">تم الفحص بتاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>

        <div class="section">
            <div class="section-title">📁 معلومات الملف</div>
            <div class="file-info">
                <div class="info-item">
                    <div class="info-label">اسم الملف</div>
                    <div class="info-value">{file_info['name']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">الحجم</div>
                    <div class="info-value">{file_info['size_kb']} KB</div>
                </div>
                <div class="info-item">
                    <div class="info-label">الصيغة</div>
                    <div class="info-value">{file_info['extension'].upper()}</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">📊 تحليل الأداء</div>
            {sections_html}
        </div>

        <div class="section">
            <div class="section-title">⚠️ المشاكل المكتشفة</div>
            {issues_html if issues_html else '<p style="color:#22c55e;text-align:center;font-size:18px;">🎉 لا توجد مشاكل خطيرة! سيرتك الذاتية في حالة ممتازة.</p>'}
        </div>

        <div class="section">
            <div class="section-title">💡 التوصيات</div>
            <ul style="padding-right:20px;">
                {recs_html}
            </ul>
        </div>

        <div class="footer">
            <p>تم إنشاء هذا التقرير بواسطة <strong>{self.logo_text}</strong></p>
            <p>للاستفسارات: تواصل معنا عبر Instagram @mosaab_cv</p>
        </div>
    </div>
</body>
</html>"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path

    def generate_markdown(self, result: Dict, file_info: Dict) -> str:
        """توليد تقرير Markdown"""

        md = f"""# 🔍 تقرير فحص توافق السيرة الذاتية مع ATS

## النتيجة الإجمالية

| المعيار | القيمة |
|---------|--------|
| النتيجة | **{result['overall_score']}/100** |
| التقدير | **{result['grade']}** |
| الحالة | {result['status']} |

---

## 📁 معلومات الملف

- **الاسم:** {file_info['name']}
- **الحجم:** {file_info['size_kb']} KB
- **الصيغة:** {file_info['extension'].upper()}

---

## 📊 تفصيل النتائج

"""

        for section_name, section_data in result['breakdown'].items():
            arabic_name = self._translate_section(section_name)
            md += f"""### {arabic_name}
- **النقاط:** {section_data['score']}/{section_data['max']}
- **النسبة:** {section_data['percentage']}%

"""

        md += "---\n\n## ⚠️ المشاكل المكتشفة\n\n"

        if result['all_issues']:
            for issue in result['all_issues']:
                severity_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🔵', 'info': 'ℹ️'}.get(issue['severity'], '⚪')
                md += f"""{severity_emoji} **{issue['issue']}**
   - 💡 الحل: {issue['fix']}

"""
        else:
            md += "🎉 لا توجد مشاكل خطيرة!\n\n"

        md += "---\n\n## 💡 التوصيات\n\n"
        for rec in result['recommendations']:
            md += f"- {rec}\n"

        md += f"""
---

*تم إنشاء هذا التقرير بواسطة {self.logo_text}*
*التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""

        return md

    def generate_json(self, result: Dict, file_info: Dict) -> str:
        """توليد تقرير JSON"""
        output = {
            'file_info': file_info,
            'analysis': result,
            'generated_at': datetime.now().isoformat()
        }
        return json.dumps(output, ensure_ascii=False, indent=2)

    def _get_section_color(self, percentage: float) -> str:
        """تحديد لون القسم حسب النسبة"""
        if percentage >= 80:
            return self.colors['green']
        elif percentage >= 60:
            return self.colors['blue']
        elif percentage >= 40:
            return self.colors['orange']
        else:
            return self.colors['red']

    def _translate_section(self, name: str) -> str:
        """ترجمة أسماء الأقسام"""
        translations = {
            'keywords': '🔑 الكلمات المفتاحية',
            'format': '📐 التنسيق والهيكل',
            'readability': '📖 سهولة القراءة',
            'contact_info': '📞 معلومات التواصل',
            'length': '📏 الطول المناسب'
        }
        return translations.get(name, name)


if __name__ == '__main__':
    gen = ReportGenerator()
    print("✅ Report Generator loaded successfully!")
