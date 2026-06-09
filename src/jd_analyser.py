# ============================================================
# JobReady AI — jd_analyser.py
# ============================================================
# Orchestrates the full JD Analyser flow:
#
#   1. Accept profile + JD text
#   2. Build prompt (prompt_builder)
#   3. Call LLM (llm_engine)
#   4. Parse response (parser)
#   5. Display results in console
#   6. Generate PDF report (ReportLab)
#
# This is the module you call from the Colab notebook.
# ============================================================

import os
from config import OUTPUT_DIR, REPORT_FILENAME, MIN_FIT_SCORE_FOR_APPLY
from prompt_builder import build_prompt
from llm_engine import llm_call
from parser import parse_response


# ── Main analyser function ───────────────────────────────────

def analyse(profile: dict, jd_text: str) -> dict:
    """
    Full end-to-end JD Analyser flow.
    Returns the parsed result dict.
    Also prints results to console and generates a PDF report.

    Args:
        profile  : dict with keys — name, years_exp, last_role,
                   target_role, skills (list), industry, achievements
        jd_text  : raw job description as a string

    Returns:
        result   : validated dict with fit_score, gaps, recommendations etc.
    """
    print("\n" + "="*60)
    print("  JobReady AI — JD Analyser")
    print("="*60)

    # Step 1 — Build prompt
    print("\n[1/4] Building prompt...")
    prompt = build_prompt(profile, jd_text)
    print(f"  Prompt assembled ({len(prompt.split())} words)")

    # Step 2 — Call LLM
    print("\n[2/4] Calling LLM...")
    raw_response = llm_call(prompt)

    # Step 3 — Parse response
    print("\n[3/4] Parsing response...")
    result = parse_response(raw_response)

    # Step 4 — Display results
    print("\n[4/4] Displaying results...")
    _display_results(profile, result)

    # Step 5 — Generate PDF
    _generate_pdf(profile, result)

    return result


# ── Console display ──────────────────────────────────────────

def _display_results(profile: dict, result: dict):
    """Prints a clean, readable summary to the Colab console."""

    if result.get("error"):
        print(f"\n  ⚠️  Analysis failed: {result.get('error_message')}")
        print("  Please try again or shorten the job description.")
        return

    score = result["fit_score"]
    score_emoji = "🟢" if score >= 80 else "🟡" if score >= 60 else "🟠" if score >= 40 else "🔴"

    print("\n" + "─"*60)
    print(f"  RESULTS FOR: {profile.get('name', 'Candidate')}")
    print(f"  TARGET ROLE: {profile.get('target_role', 'Not specified')}")
    print("─"*60)

    print(f"\n  {score_emoji}  FIT SCORE: {score}/100")
    print(f"  ROLE LEVEL MATCH: {result['role_level_match']}")
    print(f"  APPLY?: {result['apply_recommendation']}")

    if score < MIN_FIT_SCORE_FOR_APPLY:
        print(f"\n  ⚠️  Fit score is below {MIN_FIT_SCORE_FOR_APPLY}. Review gaps before applying.")

    print(f"\n  ✅ MATCHED SKILLS ({len(result['matched_skills'])}):")
    for skill in result["matched_skills"]:
        print(f"     • {skill}")

    print(f"\n  ❌ MISSING SKILLS ({len(result['missing_skills'])}):")
    for skill in result["missing_skills"]:
        print(f"     • {skill}")

    if result["partial_matches"]:
        print(f"\n  🔶 PARTIAL MATCHES ({len(result['partial_matches'])}):")
        for skill in result["partial_matches"]:
            print(f"     • {skill}")

    print(f"\n  🔑 ATS KEYWORDS TO ADD ({len(result['ats_keywords'])}):")
    for kw in result["ats_keywords"]:
        print(f"     • {kw}")

    print(f"\n  💡 RECOMMENDATIONS:")
    for i, rec in enumerate(result["recommendations"], 1):
        print(f"     {i}. {rec}")

    print("\n" + "─"*60)
    print("  PDF report saved to output folder.")
    print("─"*60 + "\n")


# ── PDF generation ───────────────────────────────────────────

def _generate_pdf(profile: dict, result: dict):
    """Generates a formatted PDF report using ReportLab."""

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    except ImportError:
        print("  [PDF] ReportLab not installed. Run: pip install reportlab")
        return

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, REPORT_FILENAME)

    NAVY     = colors.HexColor("#1B2A4A")
    TEAL     = colors.HexColor("#2A7F7F")
    TEAL_L   = colors.HexColor("#E8F4F4")
    GREEN    = colors.HexColor("#16A34A")
    GREEN_L  = colors.HexColor("#DCFCE7")
    AMBER    = colors.HexColor("#D97706")
    AMBER_L  = colors.HexColor("#FEF3C7")
    RED      = colors.HexColor("#DC2626")
    RED_L    = colors.HexColor("#FEE2E2")
    GREY_L   = colors.HexColor("#F3F4F6")
    DIVIDER  = colors.HexColor("#E5E7EB")
    GREY_MID = colors.HexColor("#6B7280")
    WHITE    = colors.white
    BLACK    = colors.HexColor("#111827")

    W, H = A4
    CW = W - 36*mm

    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    doc = SimpleDocTemplate(output_path, pagesize=A4,
        leftMargin=18*mm, rightMargin=18*mm,
        topMargin=14*mm, bottomMargin=14*mm)

    story = []

    # Header
    title = Paragraph("<font color='#2A7F7F'>JobReady AI</font>  —  JD Analyser Report",
        S("t", fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=NAVY))
    sub   = Paragraph(
        f"Candidate: <b>{profile.get('name','—')}</b> &nbsp;|&nbsp; "
        f"Target: <b>{profile.get('target_role','—')}</b> &nbsp;|&nbsp; "
        f"Experience: <b>{profile.get('years_exp','—')} years</b>",
        S("s", fontName="Helvetica", fontSize=9, leading=12, textColor=GREY_MID))
    hdr = Table([[[title, Spacer(1,4), sub]]], colWidths=[CW])
    hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),NAVY),("PADDING",(0,0),(-1,-1),14)]))
    story.append(hdr)
    story.append(Spacer(1,5*mm))

    def section_bar(text, bg=NAVY):
        t = Table([[Paragraph(f"&nbsp; {text}",
            S("sb", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=WHITE))]], colWidths=[CW])
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),
            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
        return t

    def bullet_table(items, bg, fg=BLACK):
        rows = [[Paragraph(f"\u2022  {i}", S(f"b{idx}", fontName="Helvetica",
            fontSize=8.5, leading=13, textColor=fg))] for idx, i in enumerate(items)]
        t = Table(rows, colWidths=[CW])
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),
            ("BOX",(0,0),(-1,-1),0.5,DIVIDER),
            ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),
            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
        return t

    if result.get("error"):
        story.append(Paragraph("⚠️  Analysis failed. Please retry.",
            S("err", fontName="Helvetica-Bold", fontSize=12, textColor=RED)))
        doc.build(story)
        print(f"  [PDF] Error report saved: {output_path}")
        return

    # Fit Score
    score = result["fit_score"]
    score_color = GREEN if score >= 80 else AMBER if score >= 60 else RED
    score_bg    = GREEN_L if score >= 80 else AMBER_L if score >= 60 else RED_L

    score_t = Table([[
        Paragraph("FIT SCORE", S("fsl", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=GREY_MID)),
        Paragraph(str(score), S("fsv", fontName="Helvetica-Bold", fontSize=28, leading=32, textColor=score_color, alignment=TA_CENTER)),
        Paragraph("/100", S("fsm", fontName="Helvetica", fontSize=12, leading=16, textColor=GREY_MID)),
        Paragraph(result["apply_recommendation"], S("fsa", fontName="Helvetica", fontSize=8.5, leading=13, textColor=BLACK, alignment=TA_JUSTIFY)),
    ]], colWidths=[22*mm, 20*mm, 12*mm, CW-54*mm])
    score_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),score_bg),
        ("BOX",(0,0),(-1,-1),1.5,score_color),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),10),("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    story.append(score_t)
    story.append(Spacer(1,4*mm))

    # Role level
    story.append(section_bar("ROLE LEVEL MATCH", TEAL))
    story.append(Spacer(1,1.5*mm))
    story.append(Paragraph(result["role_level_match"],
        S("rl", fontName="Helvetica", fontSize=9, leading=13, textColor=BLACK)))
    story.append(Spacer(1,4*mm))

    # Skills split: matched | missing
    col_w = CW/2
    mh = Table([[Paragraph("&nbsp; ✅  MATCHED SKILLS",
        S("mh", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=WHITE))]], colWidths=[col_w-1])
    mh.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREEN),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    xh = Table([[Paragraph("&nbsp; ❌  MISSING SKILLS",
        S("xh", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=WHITE))]], colWidths=[col_w-1])
    xh.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),RED),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))

    mc = Table([[Paragraph(f"\u2022  {s}", S(f"ms{i}", fontName="Helvetica", fontSize=8, leading=12, textColor=BLACK))]
        for i,s in enumerate(result["matched_skills"])], colWidths=[col_w-3*mm])
    mc.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GREEN_L),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    xc = Table([[Paragraph(f"\u2022  {s}", S(f"xs{i}", fontName="Helvetica", fontSize=8, leading=12, textColor=BLACK))]
        for i,s in enumerate(result["missing_skills"])], colWidths=[col_w-3*mm])
    xc.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),RED_L),("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))

    skills_t = Table([[mh,xh],[mc,xc]], colWidths=[col_w,col_w])
    skills_t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),
        ("BOX",(0,0),(-1,-1),0.5,DIVIDER),("INNERGRID",(0,0),(-1,-1),0.3,DIVIDER),
        ("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0)]))
    story.append(skills_t)
    story.append(Spacer(1,4*mm))

    # ATS Keywords
    story.append(section_bar("🔑  ATS KEYWORDS TO ADD TO YOUR RESUME & LINKEDIN", TEAL))
    story.append(Spacer(1,1.5*mm))
    story.append(bullet_table(result["ats_keywords"], TEAL_L))
    story.append(Spacer(1,4*mm))

    # Recommendations
    story.append(section_bar("💡  RECOMMENDATIONS", AMBER))
    story.append(Spacer(1,1.5*mm))
    for i, rec in enumerate(result["recommendations"], 1):
        rec_t = Table([[
            Paragraph(str(i), S(f"rn{i}", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(rec, S(f"rt{i}", fontName="Helvetica", fontSize=8.5, leading=13, textColor=BLACK, alignment=TA_JUSTIFY)),
        ]], colWidths=[10*mm, CW-10*mm])
        rec_t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,0),AMBER),("BACKGROUND",(1,0),(1,0),AMBER_L),
            ("VALIGN",(0,0),(-1,-1),"TOP"),("BOX",(0,0),(-1,-1),0.4,DIVIDER),
            ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),8),
            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
        story.append(rec_t)
        story.append(Spacer(1,1.5*mm))

    # Footer
    story.append(Spacer(1,4*mm))
    footer = Table([[
        Paragraph("JobReady AI  |  JD Analyser Report", S("fl", fontName="Helvetica", fontSize=7, leading=10, textColor=GREY_MID)),
        Paragraph("github.com/aditya-nagaria/jobready-ai", S("fr", fontName="Helvetica", fontSize=7, leading=10, textColor=GREY_MID, alignment=TA_CENTER)),
    ]], colWidths=[CW/2, CW/2])
    footer.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,0),0.5,GREY_MID),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    story.append(footer)

    doc.build(story)
    print(f"  [PDF] Report saved: {output_path}")
