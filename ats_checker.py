#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   Mosaab CV - ATS Compatibility Checker                      ║
║   أداة فحص توافق السيرة الذاتية مع أنظمة ATS                 ║
║                                                              ║
║   Usage: python ats_checker.py <cv_file> [job_description]   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import os
import argparse
from pathlib import Path

# إضافة المسار الحالي للـ import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ats_engine import ATSEngine
from file_reader import CVFileReader
from report_generator import ReportGenerator

def print_banner():
    """طباعة الشعار"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║           🔍 MOSAAB CV - ATS CHECKER v1.0                    ║
    ║                                                              ║
    ║      فحص احترافي لتوافق السيرة الذاتية مع أنظمة ATS          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_score(score: float, grade: str, status: str):
    """طباعة النتيجة بشكل جمالي"""
    color_map = {
        'A': '\033[92m',  # أخضر
        'B': '\033[94m',  # أزرق
        'C': '\033[93m',  # أصفر
        'D': '\033[91m',  # أحمر
        'F': '\033[91m\033[1m',  # أحمر غامق
    }
    reset = '\033[0m'
    color = color_map.get(grade, '\033[0m')

    print("\n" + "="*60)
    print(f"{color}                    النتيجة الإجمالية: {score}/100{reset}")
    print(f"{color}                    التقدير: {grade} - {status}{reset}")
    print("="*60 + "\n")

def print_breakdown(breakdown: dict):
    """طباعة تفصيل النتائج"""
    print("📊 تحليل الأداء:")
    print("-" * 60)

    translations = {
        'keywords': 'الكلمات المفتاحية  ',
        'format': 'التنسيق والهيكل    ',
        'readability': 'سهولة القراءة      ',
        'contact_info': 'معلومات التواصل    ',
        'length': 'الطول المناسب      '
    }

    for key, data in breakdown.items():
        name = translations.get(key, key)
        score = data['score']
        max_score = data['max']
        pct = data['percentage']

        # شريط تقدم نصي
        bar_length = 20
        filled = int((pct / 100) * bar_length)
        bar = '█' * filled + '░' * (bar_length - filled)

        print(f"  {name} │{bar}│ {score}/{max_score} ({pct}%)")

    print("-" * 60)

def print_issues(issues: list):
    """طباعة المشاكل"""
    if not issues:
        print("\n🎉 لا توجد مشاكل خطيرة! سيرتك الذاتية في حالة ممتازة.\n")
        return

    print("\n⚠️ المشاكل المكتشفة (مرتبة حسب الخطورة):")
    print("-" * 60)

    severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🔵', 'info': 'ℹ️'}

    for i, issue in enumerate(issues[:10], 1):
        icon = severity_icons.get(issue['severity'], '⚪')
        print(f"\n{i}. {icon} {issue['issue']}")
        print(f"   💡 الحل: {issue['fix']}")

    if len(issues) > 10:
        print(f"\n... و {len(issues) - 10} مشاكل إضافية")

    print("-" * 60)

def print_recommendations(recommendations: list):
    """طباعة التوصيات"""
    print("\n💡 التوصيات:")
    print("-" * 60)
    for rec in recommendations:
        print(f"  • {rec}")
    print("-" * 60)

def main():
    parser = argparse.ArgumentParser(
        description='Mosaab CV - ATS Compatibility Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ats_checker.py my_cv.pdf
  python ats_checker.py cv.docx --job "software engineer python"
  python ats_checker.py resume.pdf --job-file job_desc.txt --output report.html
        """
    )

    parser.add_argument('cv_file', help='مسار ملف السيرة الذاتية (PDF, DOCX, TXT)')
    parser.add_argument('--job', '-j', help='وصف الوظيفة (نص مباشر)')
    parser.add_argument('--job-file', '-jf', help='مسار ملف وصف الوظيفة')
    parser.add_argument('--output', '-o', help='مسار ملف التقرير (HTML)')
    parser.add_argument('--format', '-f', choices=['html', 'md', 'json', 'all'], 
                        default='html', help='صيغة التقرير (default: html)')
    parser.add_argument('--quiet', '-q', action='store_true', 
                        help='وضع صامت (بدون طباعة في الطرفية)')

    args = parser.parse_args()

    if not args.quiet:
        print_banner()

    # التحقق من وجود الملف
    cv_path = Path(args.cv_file)
    if not cv_path.exists():
        print(f"❌ خطأ: الملف غير موجود: {args.cv_file}")
        sys.exit(1)

    # قراءة وصف الوظيفة
    job_description = ""
    if args.job:
        job_description = args.job
    elif args.job_file:
        try:
            with open(args.job_file, 'r', encoding='utf-8') as f:
                job_description = f.read()
        except Exception as e:
            print(f"⚠️ تعذر قراءة ملف الوصف الوظيفي: {e}")

    # قراءة السيرة الذاتية
    try:
        reader = CVFileReader()
        file_info = reader.get_file_info(str(cv_path))
        cv_text, metadata = reader.read(str(cv_path))

        if not args.quiet:
            print(f"📁 تم قراءة الملف: {file_info['name']} ({file_info['size_kb']} KB)")
            if metadata.get('warning'):
                print(f"⚠️  تنبيه: {metadata['warning']}")
            print(f"📝 عدد الكلمات المستخرجة: ~{len(cv_text.split())}\n")

    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {e}")
        sys.exit(1)

    # تحليل ATS
    try:
        engine = ATSEngine()
        result = engine.analyze(cv_text, job_description)

        if not args.quiet:
            print_score(result['overall_score'], result['grade'], result['status'])
            print_breakdown(result['breakdown'])
            print_issues(result['all_issues'])
            print_recommendations(result['recommendations'])

            # طباعة ملخص سريع
            print("\n" + "="*60)
            print(f"📌 أولويات الإصلاح الفورية: {len(result['top_priorities'])}")
            for p in result['top_priorities']:
                print(f"   🔴 {p['issue']}")
            print("="*60)

    except Exception as e:
        print(f"❌ خطأ في التحليل: {e}")
        sys.exit(1)

    # توليد التقرير
    if args.output or args.format:
        try:
            generator = ReportGenerator()

            # تحديد مسار الإخراج
            if args.output:
                output_path = args.output
            else:
                output_path = str(cv_path.with_suffix('.html'))

            generated_files = []

            if args.format in ['html', 'all']:
                html_path = output_path if args.output else str(cv_path.with_suffix('.html'))
                generator.generate_html(result, file_info, html_path)
                generated_files.append(html_path)

            if args.format in ['md', 'all']:
                md_path = str(cv_path.with_suffix('.md'))
                md_content = generator.generate_markdown(result, file_info)
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                generated_files.append(md_path)

            if args.format in ['json', 'all']:
                json_path = str(cv_path.with_suffix('.json'))
                json_content = generator.generate_json(result, file_info)
                with open(json_path, 'w', encoding='utf-8') as f:
                    f.write(json_content)
                generated_files.append(json_path)

            if not args.quiet:
                print(f"\n✅ تم إنشاء التقرير:")
                for f in generated_files:
                    print(f"   📄 {f}")

        except Exception as e:
            print(f"⚠️ تعذر إنشاء التقرير: {e}")

    if not args.quiet:
        print("\n🎯 انتهى الفحص! حظاً موفقاً في بحثك عن عمل.\n")

    # إرجاع كود الخروج حسب النتيجة
    if result['overall_score'] >= 70:
        sys.exit(0)
    elif result['overall_score'] >= 55:
        sys.exit(1)
    else:
        sys.exit(2)

if __name__ == '__main__':
    main()
