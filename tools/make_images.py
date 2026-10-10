#!/usr/bin/env python3
"""AI 영상으로 만드는 쇼츠와 유튜브 - PIL 기반 이미지 생성 스크립트."""
import os
import math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
os.makedirs(ASSETS, exist_ok=True)

BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

BG = (11, 16, 34)          # 심야 네이비
PANEL = (22, 30, 58)
CORAL = (235, 122, 80)
TEAL = (70, 200, 190)
BLUE = (100, 155, 255)
GOLD = (235, 190, 90)
WHITE = (245, 247, 250)
MUTED = (150, 163, 195)
LINE = (66, 84, 136)
LIGHT_BG = (248, 249, 252)
INK = (28, 38, 58)
SUB = (98, 114, 138)
CARD_LINE = (205, 214, 228)


def font(path, size):
    return ImageFont.truetype(path, size, index=1)


def text_center(d, cx, y, s, f, fill):
    bb = d.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0]
    d.text((cx - w / 2 - bb[0], y), s, font=f, fill=fill)


def text_left(d, x, y, s, f, fill):
    d.text((x, y), s, font=f, fill=fill)


def rrect(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(d, x1, y1, x2, y2, fill=CORAL, width=4, head=14):
    d.line([x1, y1, x2, y2], fill=fill, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    for da in (2.62, -2.62):
        d.line([x2, y2, x2 + head * math.cos(ang + da),
                y2 + head * math.sin(ang + da)], fill=fill, width=width)


def wrap_lines(d, s, f, max_w):
    lines, cur = [], ""
    for ch in s:
        if d.textlength(cur + ch, font=f) <= max_w:
            cur += ch
        else:
            lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- 표지 1000x1300
def make_cover():
    W, H = 1000, 1300
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(11 + (26 - 11) * t)
        g = int(16 + (40 - 16) * t)
        b = int(34 + (78 - 34) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    # 필름 프레임 장식
    for i in range(9):
        x = 90 + i * 95
        d.rectangle([x, 96, x + 62, 122], outline=(80, 96, 150), width=2)
    # 재생 버튼 원
    d.ellipse([400, 618, 600, 818], outline=CORAL, width=8)
    d.polygon([(468, 668), (468, 768), (556, 718)], fill=CORAL)

    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 160, "W I K I D O C S   T E C H   B O O K", fr(26), CORAL)
    d.line([(120, 208), (880, 208)], fill=LINE, width=2)

    text_center(d, W / 2, 250, "AI 영상으로", fb(92), WHITE)
    text_center(d, W / 2, 372, "만드는 쇼츠와 유튜브", fb(76), CORAL)

    text_center(d, W / 2, 500, "텍스트 한 줄로 시작하는", fb(40), WHITE)
    text_center(d, W / 2, 560, "1인 영상 제작 실전서", fb(40), WHITE)

    topics = [
        "Sora · Veo · Runway · Kling 도구 비교",
        "프롬프트 작성법과 캐릭터 일관성",
        "10초 클립 이어붙이기 워크플로우",
        "훅·전개·반전 기획과 업로드 전략",
        "실전 프로젝트: AI 드라마 파일럿 제작",
    ]
    y = 862
    text_center(d, W / 2, y, "이 책에서 다루는 내용", fr(26), MUTED)
    y += 42
    for i, t in enumerate(topics):
        rrect(d, [150, y, 850, y + 48], 24, (18, 25, 50), outline=(60, 76, 120), width=1)
        d.ellipse([174, y + 12, 208, y + 46], fill=CORAL)
        num = str(i + 1)
        bb = d.textbbox((0, 0), num, font=fb(26))
        d.text((191 - (bb[2] - bb[0]) / 2 - bb[0], y + 14), num, font=fb(26), fill=(255, 255, 255))
        d.text((224, y + 16), t, font=fr(24), fill=WHITE)
        y += 56

    d.line([(120, 1196), (880, 1196)], fill=LINE, width=2)
    text_center(d, W / 2, 1220, "저자  이준수", fr(30), MUTED)
    text_center(d, W / 2, 1260, "기준일  2026-10-09", fr(26), MUTED)

    img.save(os.path.join(ASSETS, "cover.png"))
    print("cover.png saved")


# ---------------------------------------- 텍스트-투-비디오 vs 이미지-투-비디오
def make_t2v_i2v():
    W, H = 1500, 620
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "텍스트-투-비디오 vs 이미지-투-비디오", fb(42), INK)

    boxes = [
        (60, 120, 690, 560, "텍스트-투-비디오", TEAL,
         ["텍스트 프롬프트만으로", "장면 전체를 생성",
          "장점: 아이디어를 바로 시도",
          "주의: 캐릭터·구도가", "매번 달라질 수 있음"]),
        (810, 120, 1440, 560, "이미지-투-비디오", CORAL,
         ["기준 이미지 한 장 +", "움직임 지시로 생성",
          "장점: 캐릭터·구도 고정",
          "주의: 좋은 시작 이미지가", "결과를 좌우함"]),
    ]
    for x1, y1, x2, y2, title, col, lines in boxes:
        rrect(d, [x1, y1, x2, y2], 24, (255, 255, 255), outline=CARD_LINE, width=2)
        rrect(d, [x1, y1, x2, y1 + 84], 24, col)
        rrect(d, [x1, y1 + 60, x2, y1 + 84], 0, col)
        text_center(d, (x1 + x2) / 2, y1 + 26, title, fb(36), (255, 255, 255))
        yy = y1 + 116
        for ln in lines:
            text_center(d, (x1 + x2) / 2, yy, ln, fr(28), SUB if "장점" not in ln and "주의" not in ln else INK)
            yy += 52

    text_center(d, W / 2, 596, "", fr(1), INK)
    img.save(os.path.join(ASSETS, "fig-t2v-i2v.png"))
    print("fig-t2v-i2v.png saved")


# ------------------------------------------------------ 프롬프트 4요소 구조
def make_prompt_structure():
    W, H = 1500, 640
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "영상 프롬프트의 네 가지 요소", fb(42), INK)

    items = [
        ("장면", "누가 · 어디서 · 무엇을", TEAL,
         "예: 비 오는 밤 서울 골목의\n우산 든 여성"),
        ("카메라", "앵글 · 움직임 · 렌즈", BLUE,
         "예: 로우앵글에서 시작해\n천천히 앞으로 이동"),
        ("조명", "시간대 · 광원 · 분위기", GOLD,
         "예: 네온사인 반사,\n영화 같은 색감"),
        ("움직임", "행동 · 속도 · 전환", CORAL,
         "예: 3초에 뒤돌아보고\n미소 지음"),
    ]
    bw = 330
    gap = (W - bw * 4 - 120) / 3
    x = 60
    for title, sub, col, desc in items:
        rrect(d, [x, 110, x + bw, 560], 24, (255, 255, 255), outline=CARD_LINE, width=2)
        rrect(d, [x, 110, x + bw, 110 + 130], 24, col)
        rrect(d, [x, 110 + 106, x + bw, 110 + 130], 0, col)
        text_center(d, x + bw / 2, 132, title, fb(40), (255, 255, 255))
        text_center(d, x + bw / 2, 186, sub, fr(24), (255, 255, 255))
        yy = 280
        for ln in desc.split("\n"):
            text_center(d, x + bw / 2, yy, ln, fr(27), INK)
            yy += 46
        x += bw + gap

    text_center(d, W / 2, 584, "네 요소를 한 문단으로 연결하면 모델이 이해하기 쉬운 프롬프트가 된다", fr(27), SUB)
    img.save(os.path.join(ASSETS, "fig-prompt-structure.png"))
    print("fig-prompt-structure.png saved")


# --------------------------------------------------- 10초 클립 이어붙이기
def make_clip_workflow():
    W, H = 1600, 620
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "10초 클립 이어붙이기 워크플로우", fb(42), INK)

    steps = [
        ("기획", "60초 = 클립 6개\n각 클립의 역할 지정", TEAL),
        ("생성", "클립별 프롬프트 작성\n여유분 2배 생성", BLUE),
        ("선별", "흔들림·손가락 확인\n쓸 만한 것만 남기기", GOLD),
        ("연결", "마지막 프레임을\n다음 클립의 시작으로", CORAL),
        ("후반", "자막·내레이션·BGM\n색감 통일 후 내보내기", (110, 140, 200)),
    ]
    n = len(steps)
    bw, bh = 240, 360
    total = n * bw + (n - 1) * 56
    x = (W - total) / 2
    y = 120
    centers = []
    for title, desc, col in steps:
        rrect(d, [x, y, x + bw, y + bh], 24, (255, 255, 255), outline=CARD_LINE, width=2)
        rrect(d, [x, y, x + bw, y + 96], 24, col)
        rrect(d, [x, y + 72, x + bw, y + 96], 0, col)
        text_center(d, x + bw / 2, y + 30, title, fb(36), (255, 255, 255))
        yy = y + 130
        for ln in desc.split("\n"):
            text_center(d, x + bw / 2, yy, ln, fr(26), INK)
            yy += 44
        centers.append(x + bw / 2)
        x += bw + 56
    for i in range(n - 1):
        arrow(d, centers[i] + 120, y + bh / 2, centers[i + 1] - 120, y + bh / 2, fill=SUB, width=4, head=12)

    text_center(d, W / 2, 540, "클립 사이가 어색하면 전환 효과보다 '연속된 장면'처럼 보이게 프롬프트를 맞추는 편이 낫다", fr(27), SUB)
    img.save(os.path.join(ASSETS, "fig-clip-workflow.png"))
    print("fig-clip-workflow.png saved")


# --------------------------------------------------------- 숏폼 플랫폼 규격
def make_platform_specs():
    W, H = 1500, 640
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "숏폼 플랫폼 규격 비교 (기준일 2026-10-09)", fb(40), INK)

    cols = [
        ("틱톡", TEAL, ["세로 9:16 권장", "앱 내 최대 10분", "1분 이상 원본 영상", "수익화 대상"]),
        ("유튜브 쇼츠", CORAL, ["세로 9:16 권장", "최대 3분", "광고 수익 45% 배분", "검색 노출이 강점"]),
        ("인스타그램 릴스", BLUE, ["세로 9:16 권장", "최대 3분", "직접 조회수 정산 없음", "발견 탭 노출이 강점"]),
    ]
    bw = 420
    gap = (W - bw * 3 - 120) / 2
    x = 60
    for title, col, lines in cols:
        rrect(d, [x, 100, x + bw, 570], 24, (255, 255, 255), outline=CARD_LINE, width=2)
        rrect(d, [x, 100, x + bw, 100 + 84], 24, col)
        rrect(d, [x, 100 + 60, x + bw, 100 + 84], 0, col)
        text_center(d, x + bw / 2, 124, title, fb(36), (255, 255, 255))
        yy = 220
        for ln in lines:
            text_center(d, x + bw / 2, yy, ln, fr(28), INK)
            yy += 60
            rrect(d, [x + 60, yy - 8, x + bw - 60, yy - 6], 2, (235, 239, 246))
        x += bw + gap

    text_center(d, W / 2, 596, "정책은 자주 바뀌므로 업로드 전 각 플랫폼의 공식 도움말을 다시 확인한다", fr(26), SUB)
    img.save(os.path.join(ASSETS, "fig-platform-specs.png"))
    print("fig-platform-specs.png saved")


# ----------------------------------------------------------- 훅·전개·반전
def make_hook_story():
    W, H = 1600, 600
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "조회수를 만드는 60초 구조: 훅 · 전개 · 반전", fb(42), INK)

    segs = [
        ("0-3초  훅", "질문·충격·공감", CORAL, 0.18),
        ("3-40초  전개", "기대 쌓기 · 정보 · 감정", TEAL, 0.55),
        ("40-60초  반전", "뒤집기 · 여운 · 다음 편 예고", BLUE, 0.27),
    ]
    x = 80
    bar_w = W - 160
    y = 130
    for title, desc, col, ratio in segs:
        w = bar_w * ratio
        rrect(d, [x, y, x + w, y + 300], 20, col)
        yy = y + 40
        for ln in (title + "\n" + desc).split("\n"):
            text_center(d, x + w / 2, yy, ln, fb(34) if "초" in ln else fr(28), (255, 255, 255))
            yy += 52
        x += w

    tips = [
        "훅은 첫 2초에 결론을 예고한다",
        "전개에서는 시청자가 '그래서?' 하게 만든다",
        "반전 뒤에는 팔로우·다음 편 예고를 붙인다",
    ]
    yy = 470
    for t in tips:
        d.ellipse([120, yy + 8, 142, yy + 30], fill=CORAL)
        text_left(d, 158, yy, t, fr(28), INK)
        yy += 44

    img.save(os.path.join(ASSETS, "fig-hook-story.png"))
    print("fig-hook-story.png saved")


# ------------------------------------------------------- AI 드라마 제작 파이프라인
def make_drama_pipeline():
    W, H = 1600, 660
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "AI 드라마 시리즈 제작 파이프라인", fb(42), INK)

    steps = [
        ("세계관·캐릭터", "주인공 설정집\n레퍼런스 이미지 확정", TEAL),
        ("회차 기획", "훅 2초 · 반전 1개\n60초 콘티 6컷", BLUE),
        ("이미지 생성", "캐릭터 시트 기준\n컷별 스틸 제작", GOLD),
        ("영상화", "이미지-투-비디오\n클립 6개 생성", CORAL),
        ("후반 작업", "자막 · 내레이션 · BGM\n썸네일 · 해시태그", (110, 140, 200)),
        ("연재·분석", "고정 시간 업로드\n지표 보고 다음 편 반영", (120, 170, 130)),
    ]
    n = len(steps)
    bw, bh = 210, 400
    total = n * bw + (n - 1) * 44
    x = (W - total) / 2
    y = 110
    centers = []
    for title, desc, col in steps:
        rrect(d, [x, y, x + bw, y + bh], 20, (255, 255, 255), outline=CARD_LINE, width=2)
        rrect(d, [x, y, x + bw, y + 88], 20, col)
        rrect(d, [x, y + 68, x + bw, y + 88], 0, col)
        text_center(d, x + bw / 2, y + 22, title, fb(27), (255, 255, 255))
        yy = y + 120
        for ln in desc.split("\n"):
            text_center(d, x + bw / 2, yy, ln, fr(24), INK)
            yy += 40
        centers.append(x + bw / 2)
        x += bw + 44
    for i in range(n - 1):
        arrow(d, centers[i] + 105, y + bh / 2, centers[i + 1] - 105, y + bh / 2, fill=SUB, width=4, head=11)

    text_center(d, W / 2, 566, "캐릭터 설정집을 먼저 고정하면 2편부터는 이미지 생성 단계가 절반으로 줄어든다", fr(27), SUB)
    img.save(os.path.join(ASSETS, "fig-drama-pipeline.png"))
    print("fig-drama-pipeline.png saved")


if __name__ == "__main__":
    make_cover()
    make_t2v_i2v()
    make_prompt_structure()
    make_clip_workflow()
    make_platform_specs()
    make_hook_story()
    make_drama_pipeline()
    print("done")
