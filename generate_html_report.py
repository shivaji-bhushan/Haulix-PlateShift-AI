import os
import markdown

with open('PROJECT_REPORT.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haulix PlateShift AI — Technical Project Report</title>
    <style>
        :root {
            --bg-page: #0b0f19;
            --bg-card: #151d30;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --border: #29354f;
            --accent-green: #10b981;
            --accent-cyan: #06b6d4;
            --accent-amber: #f59e0b;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.7;
            color: var(--text-main);
            background-color: var(--bg-page);
            margin: 0;
            padding: 40px 20px;
        }
        .report-wrapper {
            max-width: 940px;
            margin: 0 auto;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 55px 65px;
            box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7);
        }
        .top-meta-badge {
            display: inline-block;
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-green);
            border: 1px solid var(--accent-green);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 16px;
        }
        h1 {
            font-size: 2.2rem;
            color: #ffffff;
            margin-top: 0;
            margin-bottom: 24px;
            letter-spacing: -0.5px;
        }
        h2 {
            font-size: 1.45rem;
            color: var(--accent-cyan);
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px;
            margin-top: 40px;
            margin-bottom: 16px;
        }
        h3 {
            font-size: 1.15rem;
            color: var(--accent-amber);
            margin-top: 24px;
            margin-bottom: 12px;
        }
        p, li {
            color: #cbd5e1;
            font-size: 15px;
        }
        hr {
            border: 0;
            border-top: 1px solid var(--border);
            margin: 30px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            font-size: 14px;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }
        th, td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }
        th {
            background: #0f172a;
            color: var(--accent-cyan);
            font-weight: 600;
        }
        tr:nth-child(even) {
            background: rgba(15, 23, 42, 0.45);
        }
        pre {
            background: #080c14;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 18px;
            overflow-x: auto;
            color: #38bdf8;
            font-family: Consolas, Monaco, 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.5;
        }
        code {
            background: #080c14;
            color: var(--accent-green);
            padding: 2px 7px;
            border-radius: 4px;
            font-family: Consolas, monospace;
            font-size: 13.5px;
        }
        pre code {
            padding: 0;
            background: none;
            color: inherit;
        }
        a {
            color: var(--accent-green);
            text-decoration: none;
            font-weight: 500;
        }
        a:hover {
            text-decoration: underline;
        }
        .print-btn-bar {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 20px;
        }
        .btn-print {
            background: var(--accent-green);
            color: #042f1a;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: opacity 0.2s;
        }
        .btn-print:hover {
            opacity: 0.9;
        }
        @media print {
            .print-btn-bar { display: none; }
            body {
                background: #ffffff;
                color: #000000;
                padding: 0;
            }
            .report-wrapper {
                border: none;
                box-shadow: none;
                padding: 0;
                background: #ffffff;
                color: #000000;
                max-width: 100%;
            }
            h1, h2, h3 { color: #000000; }
            p, li { color: #222222; }
            th { background: #f1f5f9; color: #000000; }
            pre, code {
                background: #f8fafc;
                color: #000000;
                border: 1px solid #cbd5e1;
            }
            table, th, td { border-color: #cbd5e1; }
        }
    </style>
</head>
<body>
    <div class="report-wrapper">
        <div class="print-btn-bar">
            <button class="btn-print" onclick="window.print()">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="6 9 6 2 18 2 18 9"></polyline>
                    <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                    <rect x="6" y="14" width="12" height="8"></rect>
                </svg>
                Print / Save as PDF
            </button>
        </div>
        <div class="top-meta-badge">OFFICIAL TECHNICAL REPORT &bull; HAULIX PLATESHIFT AI</div>
        {{BODY}}
    </div>
</body>
</html>
"""

full_html = html_template.replace("{{BODY}}", html_body)

with open('PROJECT_REPORT.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print('PROJECT_REPORT.html created successfully!')
