"""Generate index.html, about.html, and courses.html for the site root."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WA = {"Mentakab": "60177717900", "Setapak": "60173663800", "Wangsa": "60122467900"}


def wa(b, t):
    import urllib.parse as u

    return f"https://wa.me/{WA[b]}?text=" + u.quote(t)


def canonical_path(cur: str) -> str:
    if cur == "index.html":
        return "https://chengyi-education.com/"
    return f"https://chengyi-education.com/{cur}"


GA = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S00FG8N2L4"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-S00FG8N2L4');
</script>"""


def nav_links(cur: str) -> str:
    items = [
        ("index.html", "首页", "Home", "Utama"),
        ("about.html", "关于我们", "About", "Tentang"),
        ("courses.html", "课程", "Courses", "Kursus"),
        ("index.html#contact", "联系", "Contact", "Hubungi"),
    ]
    return "".join(
        f'<a href="{h}"{" aria-current=page" if h == cur else ""} data-en="{e}" data-ms="{m}">{z}</a>'
        for h, z, e, m in items
    )


def header_block(cur: str) -> str:
    links = nav_links(cur)
    return f"""<header><div class="wrap nav"><a class="brand" href="index.html"><img src="logo.png" alt="诚意补习学院 logo"><span>诚意补习学院</span></a>
<nav class="links" aria-label="主导航">{links}</nav>
<button type="button" class="nav-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="打开菜单"><span class="nav-toggle-bar"></span><span class="nav-toggle-bar"></span><span class="nav-toggle-bar"></span></button>
<div class="lang" aria-label="语言"><button class="on" type="button" data-l="zh">中</button><button type="button" data-l="ms">MS</button><button type="button" data-l="en">EN</button></div>
<a class="btn btn-wa btn-sm nav-book" href="index.html#contact" data-en="Book" data-ms="Tempah">预约</a></div>
<nav id="mobile-nav" class="mobile-nav" hidden aria-label="手机导航"><div class="wrap">{links}</div></nav></header>"""


def head(title, desc, cur):
    canon = canonical_path(cur)
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{GA}
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{canon}">
<link rel="icon" type="image/png" href="logo.png">
<link href="https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
<meta property="og:url" content="{canon}"><meta property="og:image" content="https://chengyi-education.com/logo.png"><link rel="stylesheet" href="site.css"></head><body>
{header_block(cur)}<main>"""


FOOT = """</main><footer><div class="wrap"><div class="grid">
<div><h3>诚意补习学院</h3><p>诚意育人，精益求精</p><p>Sincere Education, Excellence</p>
<ul style="margin-top:10px"><li>Mentakab · 017-7717900</li><li>Setapak · 017-3663800</li><li>Wangsa · 012-2467900</li></ul></div>
<div><h3 data-en="Pages" data-ms="Halaman">导航</h3><ul><li><a href="index.html">首页</a></li><li><a href="about.html">关于我们</a></li><li><a href="courses.html">课程</a></li><li><a href="index.html#contact">联系我们</a></li></ul></div>
<div><h3 data-en="Opening hours" data-ms="Waktu operasi">营业时间</h3><ul><li>周一 – 周五：10:30 AM – 9:00 PM</li><li>周六：9:00 AM – 5:00 PM</li><li>周日：休息</li></ul></div>
</div><p class="copy">© 2024 诚意补习学院 · ChengYi Tuition Academy. All rights reserved.</p></div></footer><script src="site.js"></script></body></html>"""

BR = [
    ("Mentakab", "mentakab.jpg", "61-1, Jalan Temerloh, Mentakab", "017-7717900", "mentakab.html"),
    ("Setapak", "setapak.jpg", "Jalan 1/23f, Taman Teratai Mewah, KL", "017-3663800", "setapak.html"),
    (
        "Wangsa Maju",
        "wangsa.jpg",
        "123-1, Jalan 3/23A, Taman Danau Kota, Wangsa Maju, 53000 KL",
        "012-2467900",
        "wangsa.html",
    ),
]


def branches():
    s = ""
    for i, (n, img, a, p, h) in enumerate(BR):
        k = "Wangsa" if n.startswith("W") else n
        s += f"""<article class="card wob tape" style="transform:rotate({[-1, 0.6, -0.4][i]}deg)"><img src="{img}" alt="{n} 分校外观" style="width:100%;height:170px;object-fit:cover;border:2px solid #2d2d2d;border-radius:6px">
<h3 style="font-size:26px;margin-top:14px">{n}</h3><p style="margin:6px 0">{a}</p><p style="margin:0 0 14px;font-weight:700">{p}</p>
<a class="btn btn-wa btn-sm" href="{wa(k, f'您好！我想了解诚意补习学院{k}的课程信息。')}" target="_blank" rel="noopener">WhatsApp {n}</a> <a href="{h}" style="font-size:14px;margin-left:8px">分校页 →</a></article>"""
    return s


GROUPS = [
    (
        "小学【低年组】",
        "Primary (lower)",
        [
            "Bahasa Melayu Pemahaman",
            "Bahasa Melayu Karangan",
            "English (BI)",
            "Bahasa Cina (BC)",
            "Mathematics (MM)",
            "Science (SC)",
        ],
    ),
    (
        "小学【高年组】",
        "Primary (upper)",
        [
            "Bahasa Melayu Pemahaman",
            "Bahasa Melayu Karangan",
            "English (BI)",
            "Bahasa Cina Pemahaman",
            "Bahasa Cina Karangan",
            "Mathematics (MM)",
            "Science (SC)",
            "Sejarah (SEJ)",
        ],
    ),
    (
        "中学【F1 - F3】",
        "Form 1 – 3",
        [
            "Bahasa Melayu Pemahaman (BMP)",
            "Bahasa Melayu Karangan (BMK)",
            "Mathematics (MM)",
            "Science (SC)",
            "Sejarah (SEJ)",
            "Bahasa Cina (BC)",
            "English (BI)",
            "ASK/RBT + Geografi",
        ],
    ),
    (
        "中学【F4 - F5】",
        "Form 4 – 5 (SPM)",
        [
            "Bahasa Melayu Karangan",
            "Bahasa Melayu Pemahaman",
            "English (BI) Karangan",
            "English (BI) Pemahaman",
            "Mathematics (MM)",
            "Science (SC)",
            "Sejarah (SEJ)",
            "Add Maths (AM)",
            "Physics (PHY)",
            "Chemistry (CHE)",
            "Bahasa Cina (BC)",
            "Account (ACC)",
            "Pendidikan (PN)",
            "Ekonomi (EKO)",
        ],
    ),
    (
        "安亲班",
        "Day care",
        [
            "完成学校功课与听写",
            "健康妈妈餐",
            "品格塑造，心灵疗法",
            "免费考前复习",
            "营业至晚上9时，加时不加价",
        ],
    ),
]

WHY = [
    ("常年不换专业教师团队", "超过二十位硕士毕业老师，深研幼儿班、安亲班、小学和中学课程"),
    ("成绩跟踪", "定期评估，及时调整教学方案，为每一位学生量身定制教学方案"),
    ("Newton Memory 有趣漫画教学", "我们遵循 UASA 教育制度，并采用漫画与课本知识结合，让课程简单易懂"),
    ("全面减轻家长负担", "成立家长与老师私人群组，让家长随时可以联系老师，关心孩子的成长与安全"),
]


def why():
    return "".join(
        f'<div class="card wob {"note" if i % 2 else ""}"><h3 style="font-size:22px">{t}</h3><p style="margin:8px 0 0">{d}</p></div>'
        for i, (t, d) in enumerate(WHY)
    )


def awards():
    items = [
        ("asean-records.webp", "ASEAN Records", "全马最多培训中心"),
        ("asia-pacific-brand.jpg", "Asia Pacific Excellence Brand", "亚太卓越品牌大奖"),
        ("malaysia-records.webp", "Malaysia Book of Records", "大马记录大全"),
    ]
    return "".join(
        f'<figure class="card wob tape" style="margin:0;text-align:center"><img src="{i}" alt="{a}" style="height:110px;object-fit:contain;margin:0 auto"><figcaption style="margin-top:12px"><b>{t}</b></figcaption></figure>'
        for i, a, t in items
    )


_GRADES = ["K1", "K2"] + [f"Year {i}" for i in range(1, 7)] + [f"F{i}" for i in range(1, 6)]
FORM = (
    """<form id="bookForm" class="card wob" style="max-width:560px">
<h3 style="font-size:26px" data-en="Book a trial class" data-ms="Tempah kelas percubaan">预约 / 咨询</h3><p style="margin:0;color:#666;font-size:14px">填写后将以 WhatsApp 发送至所选分校</p>
<label for="b">选择分校 *</label><select id="b" name="branch" required><option value="">—</option><option value="60177717900">Mentakab · 017-7717900</option><option value="60173663800">Setapak · 017-3663800</option><option value="60122467900">Wangsa · 012-2467900</option></select>
<label for="n">学生姓名 *</label><input id="n" name="name" required>
<label for="p">电话 / WhatsApp *</label><input id="p" name="phone" type="tel" required>
<label for="g">年级</label><select id="g" name="grade"><option value="">—</option>"""
    + "".join(f"<option>{g}</option>" for g in _GRADES)
    + """</select>
<label for="m">咨询内容</label><textarea id="m" name="msg" rows="3"></textarea>
<button class="btn btn-wa" style="margin-top:16px" data-en="Send via WhatsApp" data-ms="Hantar melalui WhatsApp">通过 WhatsApp 发送</button><p style="font-size:13px;color:#777">您的信息将严格保密</p></form>"""
)


def write(name: str, html: str):
    if "示例" in html or "待补" in html:
        raise RuntimeError(f"{name} still contains placeholder markers")
    (ROOT / name).write_text(html, encoding="utf-8")


def main():
    idx = (
        head(
            "诚意补习学院 ChengYi · Mentakab / Setapak / Wangsa Maju 中小学补习",
            "诚意补习学院在 Mentakab、Setapak、Wangsa Maju 三校提供小学至中学（F1–F5）补习及安亲班。",
            "index.html",
        )
        + f"""
<section style="padding-top:56px"><div class="wrap grid hero" style="align-items:center">
<div class="card wob tape" style="transform:rotate(-1.5deg);padding:28px;box-shadow:8px 8px 0 #2d2d2d"><img src="logo.png" alt="诚意教育 logo" style="width:100%;max-width:340px;margin:0 auto" width="340" height="340"></div>
<div><span class="kicker">诚意育人，精益求精</span>
<h1 style="font-size:clamp(36px,6vw,60px);margin:10px 0 16px" data-en="Primary &amp; secondary tuition in Mentakab, Setapak &amp; Wangsa Maju" data-ms="Tuisyen rendah &amp; menengah di Mentakab, Setapak &amp; Wangsa Maju">吉隆坡 Wangsa Maju 中小学补习 · 诚意补习学院</h1>
<p class="lead" style="font-family:Kalam;font-size:20px;color:#2d2d2d">Mentakab · Setapak · Wangsa Maju 三校</p><p class="lead">从小学低年组到 F4–F5，再到安亲班，三校提供相同课程体系。十余年专注本地中小学生的课后辅导。</p>
<p style="display:flex;gap:14px;flex-wrap:wrap;margin-top:24px"><a class="btn btn-wa" href="#contact" data-en="Book a trial class on WhatsApp" data-ms="Tempah kelas percubaan">WhatsApp 预约试听</a><a class="btn" href="courses.html" data-en="See courses" data-ms="Lihat kursus">查看课程</a></p></div>
</div></section>
<section style="background:#fff;border-block:2px dashed var(--line)"><div class="wrap"><span class="kicker">Courses</span><h2>年级与科目</h2>
<div class="grid g3" style="margin-top:24px">"""
        + "".join(
            f'<a href="courses.html" class="card wob" style="text-decoration:none"><h3 style="font-size:22px">{z}</h3><p style="margin:4px 0 0;color:#666">{e} · {len(s)} {"项服务" if z == "安亲班" else "科"}</p></a>'
            for z, e, s in GROUPS
        )
        + """
<a href="courses.html" class="card wob note" style="text-decoration:none;display:flex;align-items:center"><h3 style="font-size:22px">查看全部科目 →</h3></a></div></div></section>
<section><div class="wrap"><span class="kicker">Why us</span><h2>为什么选择诚意？</h2><div class="grid g2" style="margin-top:24px">"""
        + why()
        + f"""</div></div></section>
<section><div class="wrap"><span class="kicker">Branches</span><h2>三所分校</h2><div class="grid g3" style="margin-top:28px">{branches()}</div></div></section>
<section id="contact" style="background:#fff;border-block:2px dashed var(--line)"><div class="wrap grid g2"><div><span class="kicker">Contact</span><h2>预约试听</h2>
<p class="lead">选好分校，填写后会直接打开 WhatsApp 发给该分校。</p><p><b>营业时间</b><br>周一 – 周五 10:30 AM – 9:00 PM<br>周六 9:00 AM – 5:00 PM<br>周日 休息</p></div>{FORM}</div></section>"""
        + FOOT
    )
    write("index.html", idx)

    ab = (
        head(
            "关于我们 · 诚意补习学院 ChengYi",
            "诚意补习学院秉承「诚意育人，精益求精」，在 Mentakab、Setapak 与 Wangsa Maju 设立三所分校。",
            "about.html",
        )
        + f"""
<section style="padding-top:56px"><div class="wrap" style="max-width:720px"><span class="kicker">About Us</span>
<h1 style="font-size:clamp(34px,5vw,52px);margin:8px 0 14px" data-en="Three branches, serving more families" data-ms="Tiga cawangan, lebih banyak keluarga">三校联动，服务更多家庭</h1>
<p class="lead">诚意补习学院秉承「诚意育人，精益求精」的办学宗旨，在 Mentakab、Setapak 与 Wangsa Maju 设立三所分校，十余年来专注为本地中小学生提供高质量、个性化的课后辅导服务。</p>
<a class="btn btn-wa" href="index.html#contact" style="margin-top:14px">WhatsApp 预约试听</a></div></section>
<section style="background:#fff;border-block:2px dashed var(--line)"><div class="wrap"><span class="kicker">Awards</span><h2>权威认证</h2>
<div class="grid g3" style="margin-top:24px">{awards()}</div></div></section>
<section><div class="wrap"><span class="kicker">Why us</span><h2>为什么选择诚意？</h2><div class="grid g2" style="margin-top:24px">{why()}</div></div></section>
<section style="background:#fff;border-block:2px dashed var(--line)"><div class="wrap"><span class="kicker">Branches</span><h2>三所分校</h2><div class="grid g3" style="margin-top:28px">{branches()}</div></div></section>"""
        + FOOT
    )
    write("about.html", ab)

    cs = (
        head(
            "课程 · 诚意补习学院 ChengYi",
            "小学低年组、高年组、F1–F3、F4–F5（SPM）各科补习及安亲班，三校课程相同。",
            "courses.html",
        )
        + """
<section style="padding-top:56px;padding-bottom:24px"><div class="wrap"><span class="kicker">Courses</span>
<h1 style="font-size:clamp(34px,5vw,52px);margin:8px 0 12px" data-en="Courses for every grade" data-ms="Kursus untuk semua tahap">全面课程，覆盖各年级</h1>
<p class="lead">三校提供相同课程体系，涵盖小学至中学及安亲班。直接点每一组的按钮，就能用 WhatsApp 询问上课时间与学费。</p>
<nav style="display:flex;flex-wrap:wrap;gap:8px;margin-top:18px">"""
        + "".join(f'<a class="btn btn-sm" href="#g{i}">{z}</a>' for i, (z, e, s) in enumerate(GROUPS))
        + """</nav></div></section>
<section style="padding-top:24px"><div class="wrap grid g2">"""
        + "".join(
            f"""<article id="g{i}" class="card wob {"note" if z == "安亲班" else ""}" style="display:flex;flex-direction:column"><h2 style="font-size:28px;margin:0">{z}</h2><p style="margin:0;color:#666;font-size:15px">{e} · {len(s)} {"项服务" if z == "安亲班" else "科"}</p>
<ul class="chips">{"".join(f"<li>{x}</li>" for x in s)}</ul>
<div style="margin-top:auto;padding-top:18px"><a class="btn btn-wa btn-sm" href="{wa("Wangsa", f"您好！我想了解{z}的上课时间和学费。")}" target="_blank" rel="noopener">WhatsApp 问{z}</a></div></article>"""
            for i, (z, e, s) in enumerate(GROUPS)
        )
        + """
<div class="card wob" style="display:flex;flex-direction:column;justify-content:center"><h3 style="font-size:24px">不确定选哪一科？</h3><p>告诉我们孩子的年级和学校，老师会给建议。</p><a class="btn btn-wa" href="index.html#contact">WhatsApp 预约试听</a></div>
</div></div></section>"""
        + FOOT
    )
    write("courses.html", cs)


if __name__ == "__main__":
    main()
