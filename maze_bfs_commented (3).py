# =====================================================================
#  ملاحظة للقراءة: فوق كل سطر بهذا الملف تعليق بالعربي يشرح ما يفعله.
#  فكرة المشروع: لعبة متاهة نحلّها بخوارزمية BFS (البحث بالعرض أولاً)،
#  ومعها عرض تقديمي كامل داخل البرنامج يشرح BFS وكيف بنينا اللعبة.
#  أقسام الملف بالترتيب:
#    1) الإعدادات والألوان
#    2) المتاهة وخوارزمية BFS: كلاس BFS ودوال generate و solve و place_cats (قلب المشروع)
#    3) دوال الرسم (الفأر، القطة، الجبنة، الجدران، المسار)
#    4) كلاس Button للأزرار
#    5) العرض التقديمي: الشرائح وكلاس Deck
#    6) كلاس App: القائمة والإعدادات واللعب وشاشة النتيجة
#  لتشغيل البرنامج: افتحي الملف واضغطي زر ▶ (Run) أو اكتبي أمر py بالترمنال.
# =====================================================================
"""
Maze Runner - BFS Edition (final merged version)
------------------------------------------------
Install:  pip install pygame
Run:      python maze_bfs_final.py

Screens:  Menu -> Play (You vs BFS) / Watch BFS / Presentation / Settings
Game keys: Arrows/WASD move | H hint | SPACE run BFS | ENTER one BFS step |
           N new maze | ESC menu

Algorithms used
  * Solving    : Breadth-First Search (queue, FIFO) - the only search algorithm.
  * Generation : randomized Prim's algorithm + a few extra openings so the
                 maze has several routes (otherwise "shortest path" is trivial).
  * Cats       : obstacles. BFS treats them as blocked cells, so it finds the
                 shortest SAFE path (sometimes a detour).
"""
# نستورد مكتبة math للدوال الرياضية (جيب، جيب التمام، ...)
import math
# نستورد مكتبة random لاختيار أشياء عشوائية (نستخدمها لتوليد المتاهة)
import random
# نستورد sys لإغلاق البرنامج عند الخروج
import sys
# نستورد time لقياس زمن تنفيذ BFS (يظهر بشريحة النتائج)
import time
# نستورد deque وهي الطابور (Queue) الذي تعتمد عليه خوارزمية BFS
from collections import deque

# نستورد مكتبة pygame لرسم اللعبة والتعامل مع لوحة المفاتيح والماوس
import pygame

# إعدادات الفريق: غيّري الأسماء هنا (تظهر بشريحة العنوان وشريحة الفريق)
# ---- team names / supervisor / course (edit here) ----
# عنوان المشروع (يظهر أسفل كل شريحة)
PROJECT_TITLE = "Maze Solving with Breadth-First Search"


# قائمة أعضاء الفريق: كل عضو (الاسم، الصفة). بدّلي كلمة Team member بصفة كل شخص
TEAM = [
    # العضو 1: (الاسم، الصفة)
    ("Salsabeel Khalid", "Team member"),
    # العضو 2
    ("Tabarak Ahmed", "Team member"),
    # العضو 3
    ("Asraa Ibrahim", "Team member"),
    # العضو 4
    ("Rusul Hameed", "Team member"),
    # العضو 5
    ("Rusul Ammar", "Team member"),
    # العضو 6
    ("Rawan Mohammed", "Team member"),
    # العضو 7
    ("Hawraa Hussein", "Team member"),
    # العضو 8
    ("Ayman Nizar", "Team member"),
    # العضو 9
    ("Al-Sadeeq Amer", "Team member"),
]
# اسم المشرفة (الدكتورة) يظهر بشريحة العنوان
SUPERVISOR = "Presented to: Dr. Zahraa A. Abdalkareem"
# اسم المادة والجامعة
COURSE = "AI  |  Imam Al-A'dham University"

# نشغّل مكتبة pygame
pygame.init()
# عرض النافذة W=1000 بكسل وارتفاعها H=680 بكسل
W, H = 1000, 680
# ننشئ نافذة اللعبة بهذا الحجم (SCALED تسمح بتكبيرها لملء الشاشة)
screen = pygame.display.set_mode((W, H), pygame.SCALED)
# نكتب عنوان النافذة
pygame.display.set_caption("Maze Runner - BFS Edition")
# ساعة تتحكم بسرعة اللعبة (60 إطار بالثانية)
clock = pygame.time.Clock()

# خط العنوان الكبير جداً (حجم 72)
F_TITLE = pygame.font.SysFont("segoeui,arial", 72, bold=True)
# خط العناوين الكبيرة (حجم 40)
F_BIG = pygame.font.SysFont("segoeui,arial", 40, bold=True)
# خط الأزرار (حجم 26)
F_BTN = pygame.font.SysFont("segoeui,arial", 26, bold=True)
# خط النصوص المتوسطة (حجم 22)
F_TXT = pygame.font.SysFont("segoeui,arial", 22)
# خط نصوص الشرائح (حجم 20)
F_BODY = pygame.font.SysFont("segoeui,arial", 20)
# خط النصوص الصغيرة (حجم 18)
F_SMALL = pygame.font.SysFont("segoeui,arial", 18)

# ---------- colors ----------
# لونا بداية ونهاية الخلفية المتدرجة (أبيض مائل للوردي إلى وردي بيبي)
BG1, BG2 = (255, 250, 252), (253, 226, 238)
# لون النص الأساسي: بنفسجي غامق مريح للعين على الخلفية الفاتحة
INK = (74, 46, 84)
# لون النص الخافت
DIM = (124, 88, 128)
# لون الزر العادي ولون الزر عند وضع الماوس فوقه
BTN, BTN_HOVER = (240, 150, 186), (232, 112, 160)
# لون جدران المتاهة (بنفسجي مائل للوردي واضح على الخلفية الفاتحة)
WALL = (126, 84, 120)
# لونا خلايا BFS المستكشفة: الأزرق الفاتح للقريبة من البداية والبنفسجي الوردي للبعيدة
VIS_A, VIS_B = (140, 200, 236), (214, 150, 216)
# لون الحدود (Frontier): الخلايا المنتظرة داخل الطابور (أخضر نعناعي)
FRONTIER = (112, 214, 190)
# اللون الأصفر الذهبي (للمسار الأقصر)
GOLD = (255, 190, 80)
# لون العناوين والنصوص المميزة: وردي غامق واضح على الخلفية الفاتحة
ACCENT = (190, 48, 106)
# الأخضر لنقطة البداية والأحمر للمخرج
GREEN, RED = (110, 204, 148), (240, 100, 120)

# الاتجاهات الأربعة: كل اتجاه (تغيّر الصف، تغيّر العمود، الاتجاه المعاكس)
DIRS = {"N": (-1, 0, "S"), "S": (1, 0, "N"), "W": (0, -1, "E"), "E": (0, 1, "W")}
# أحجام المتاهة: صغير 12x12 ومتوسط 20x20 وكبير 30x30
SIZES = [("Small", 12), ("Medium", 20), ("Large", 30)]
# سرعات BFS: كم خطوة تتنفذ بكل إطار
SPEEDS = [("Slow", 1), ("Normal", 3), ("Fast", 12)]


# دالة lerp تمزج لونين حسب النسبة t (نستخدمها لتدرج الألوان)
def lerp(a, b, t):
    # تحسب كل مكوّن من RGB بين اللونين وترجع اللون الناتج
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# دالة wrap تقسّم النص الطويل إلى أسطر تناسب عرضاً معيناً
def wrap(font, text, width):
    """Split text into lines that fit inside `width` pixels."""
    # lines قائمة الأسطر الناتجة، وcur السطر الحالي
    lines, cur = [], ""
    # نمر على كل كلمة بالنص
    for word in text.split():
        # نجرّب إضافة الكلمة للسطر الحالي
        t = (cur + " " + word).strip()
        # إذا بقي السطر ضمن العرض المسموح
        if font.size(t)[0] <= width:
            # نقبل الكلمة ونكمل بنفس السطر
            cur = t
        # وإلا (السطر امتلأ)
        else:
            # نحفظ السطر الممتلئ بالقائمة
            lines.append(cur)
            # ونبدأ سطراً جديداً بهذه الكلمة
            cur = word
    # إذا بقي نص بالسطر الأخير
    if cur:
        # نضيفه للقائمة
        lines.append(cur)
    # نرجع كل الأسطر
    return lines


# دالة cell_center تحسب مركز الخلية على الشاشة (بالبكسل) من رقم الصف والعمود
def cell_center(cell, ox, oy, cs):
    # نصف حجم الخلية (cs/2) يوصلنا لمنتصف الخلية
    return (ox + cell[1] * cs + cs / 2, oy + cell[0] * cs + cs / 2)


# =====================================================================
#  MAZE + BFS
# =====================================================================
# دالة open_neighbors ترجع الخلايا المجاورة المفتوحة (ما يفصلها جدار). هذي هي "حواف" الـ graph
def open_neighbors(walls, cell):
    """Cells reachable from `cell` through an open passage."""
    # نمر على الاتجاهات الأربعة
    for d, (dr, dc, _) in DIRS.items():
        # إذا ما في جدار بهذا الاتجاه
        if d not in walls[cell]:
            # نحسب إحداثيات الخلية المجاورة
            n = (cell[0] + dr, cell[1] + dc)
            # نتأكد أنها داخل المتاهة
            if n in walls:
                # نرجعها (yield تعطي النتائج واحدة بعد الثانية)
                yield n


# دالة generate تولّد المتاهة بخوارزمية Prim العشوائية (مو DFS)
def generate(rows, cols, rng=random, loops=0.15):
    """Randomized Prim's algorithm (no DFS), then open a few extra walls."""
    # نبدأ والجدران الأربعة موجودة حول كل خلية (N,S,E,W)
    walls = {(r, c): {"N", "S", "E", "W"} for r in range(rows) for c in range(cols)}
    # البداية بأعلى المنتصف والمخرج بأسفل المنتصف
    start, end = (0, cols // 2), (rows - 1, cols // 2)
    # in_maze الخلايا التي صارت جزءاً من المتاهة، وfrontier قائمة الجدران المرشحة للفتح
    in_maze, frontier = {start}, []

    # دالة صغيرة add تضيف جدران الخلية المجاورة لقائمة المرشحين
    def add(cell):
        # نمر على اتجاهات الخلية
        for d, (dr, dc, opp) in DIRS.items():
            # نحسب الجار
            n = (cell[0] + dr, cell[1] + dc)
            # إذا الجار موجود وما دخل المتاهة بعد
            if n in walls and n not in in_maze:
                # نضيف (الخلية، الجار، الاتجاه، الاتجاه المعاكس) للمرشحين
                frontier.append((cell, n, d, opp))

    # نبدأ من خلية البداية
    add(start)
    # نكرر حتى تنتهي قائمة المرشحين
    while frontier:
        # نختار رقماً عشوائياً من القائمة
        i = rng.randrange(len(frontier))
        # نبدّل المختار مع آخر عنصر حتى نسحبه بسرعة
        frontier[i], frontier[-1] = frontier[-1], frontier[i]
        # نسحب العنصر المختار
        cell, n, d, opp = frontier.pop()
        # إذا الجار صار جزءاً من المتاهة سابقاً
        if n in in_maze:
            # نتجاهله ونكمل (حتى ما تنشأ حلقات)
            continue
        # نهدم جدار الخلية باتجاه الجار
        walls[cell].discard(d)
        # ونهدم جدار الجار من الجهة المقابلة
        walls[n].discard(opp)
        # نضم الجار للمتاهة
        in_maze.add(n)
        # ونضيف جدرانه المجاورة للمرشحين
        add(n)
    # نفتح عدداً إضافياً من الجدران عشوائياً (حوالي 15%) لتصير هناك طرق بديلة
    for _ in range(int(rows * cols * loops)):  # extra openings = alternative routes
        # نختار خلية عشوائية
        cell = (rng.randrange(rows), rng.randrange(cols))
        # ونختار اتجاهاً عشوائياً
        d = rng.choice(list(DIRS))
        # نجلب تغيّر الصف والعمود والاتجاه المعاكس
        dr, dc, opp = DIRS[d]
        # نحسب الجار
        n = (cell[0] + dr, cell[1] + dc)
        # إذا الجار داخل المتاهة
        if n in walls:
            # نهدم الجدار بين الخليتين
            walls[cell].discard(d)
            # ونهدمه من الجهة الثانية أيضاً
            walls[n].discard(opp)
    # نفتح مدخل المتاهة (جدار الشمال لخلية البداية)
    walls[start].discard("N")
    # ونفتح المخرج (جدار الجنوب لخلية النهاية)
    walls[end].discard("S")
    # نرجع الجدران والبداية والنهاية
    return walls, start, end


# كلاس BFS: قلب المشروع، ينفذ بحث BFS خطوة وحدة كل مرة حتى نقدر نحركه
class BFS:
    """Breadth-First Search, one expansion per step() so we can animate it."""

    # دالة البناء: تجهّز كل المتغيرات قبل بداية البحث
    def __init__(self, walls, start, end, blocked=()):
        # نحفظ الجدران والمخرج والخلايا الممنوعة (القطط)
        self.walls, self.end, self.blocked = walls, end, set(blocked)
        # self.q هو الطابور (FIFO) ونضع فيه خلية البداية
        self.q = deque([start])          # the queue (FIFO)
        # parent يحفظ "من أين جاءت" كل خلية لنستعيد المسار بالنهاية
        self.parent = {start: None}      # "came from" links
        # dist يحفظ بُعد كل خلية عن البداية (عدد الخطوات)
        self.dist = {start: 0}
        # maxd أكبر بُعد وجدناه (نستخدمه بالألوان)
        self.maxd = 1
        # عدد الخلايا التي استكشفناها
        self.explored = 0
        # هل انتهى البحث؟
        self.done = False
        # المسار الأقصر (يتعبّأ عند الوصول للمخرج)
        self.path = []
        # reveal لتحريك ظهور المسار الذهبي تدريجياً
        self.reveal = 0.0
        # cur آخر خلية أخرجناها من الطابور
        self.cur = None                  # cell taken out of the queue last step
        # added كم جاراً أضفنا بالخطوة الأخيرة
        self.added = 0                   # neighbors added last step

    # دالة step تنفذ خطوة BFS واحدة
    def step(self):
        # إذا انتهى البحث
        if self.done:
            # ما نسوي شي
            return
        # إذا الطابور فاضي (ما بقى شي نستكشفه)
        if not self.q:                   # queue empty: no route exists
            # نعلن انتهاء البحث (ما في طريق)
            self.done = True
            # ونخرج
            return
        # نسحب أول خلية من الطابور (الداخل أولاً يخرج أولاً - FIFO)
        cur = self.q.popleft()
        # نسجلها كخلية حالية ونصفّر عدّاد الجيران
        self.cur, self.added = cur, 0
        # نزيد عدّاد الخلايا المستكشفة
        self.explored += 1
        # إذا هذي الخلية هي المخرج
        if cur == self.end:
            # نبدأ من المخرج
            node = cur
            # نرجع للخلف عبر روابط parent حتى نصل للبداية
            while node is not None:      # walk back through the parent links
                # نضيف الخلية للمسار
                self.path.append(node)
                # وننتقل لـ "الخلية التي جئنا منها"
                node = self.parent[node]
            # نعكس المسار ليصير من البداية إلى النهاية
            self.path.reverse()
            # ننهي البحث
            self.done = True
            # ونخرج
            return
        # وإلا: نمر على الجيران المفتوحين للخلية الحالية
        for n in open_neighbors(self.walls, cur):
            # إذا الجار ما زرناه قبل وليس فيه قطة
            if n not in self.parent and n not in self.blocked:
                # نسجل أننا وصلناه من الخلية الحالية
                self.parent[n] = cur
                # بُعده = بُعد الخلية الحالية + 1
                self.dist[n] = self.dist[cur] + 1
                # نحدّث أكبر بُعد
                self.maxd = max(self.maxd, self.dist[n])
                # نضيف الجار لنهاية الطابور
                self.q.append(n)
                # نزيد عدّاد الجيران المضافين
                self.added += 1

    # دالة run_all تكمل كل الخطوات دفعة واحدة بدون حركة
    def run_all(self):
        # نكرر حتى ينتهي البحث
        while not self.done:
            # كل مرة نعمل خطوة
            self.step()


# دالة solve تحل المتاهة بسرعة وترجع أقصر مسار
def solve(walls, start, end, blocked=()):
    # ننشئ بحث BFS
    b = BFS(walls, start, end, blocked)
    # ونشغّله للنهاية
    b.run_all()
    # نرجع المسار
    return b.path


# دالة place_cats تضع القطط (العوائق) في المتاهة
def place_cats(walls, start, end, count, rng=random):
    """Cats are obstacles.
    (a) some sit ON the shortest route (only if a detour still exists),
    (b) the rest are traps on side branches away from the safe route."""
    # إذا طُلب صفر قطط
    if count <= 0:
        # نرجع مجموعة فارغة
        return set()
    # نحسب أقصر طريق بدون قطط
    base = solve(walls, start, end)
    # مجموعة القطط تبدأ فارغة
    cats = set()
    # نأخذ خلايا وسط الطريق (نتجنب أول 3 وآخر 3 حتى ما نسد البداية والنهاية)
    mid = base[3:-3]
    # نخلطها عشوائياً
    rng.shuffle(mid)
    # نجرّب وضع ثلث القطط تقريباً على الطريق الأقصر نفسه
    for cell in mid[:max(1, count // 3)]:
        # نتأكد أنه ما زال هناك طريق بديل بعد وضع القطة
        if solve(walls, start, end, cats | {cell}):
            # إذا نعم نثبّت القطة هنا (فيضطر BFS لتحويلة)
            cats.add(cell)
    # نحسب أقصر طريق آمن بعد وضع القطط
    safe = solve(walls, start, end, cats)
    # on خلايا الطريق الآمن، وcand مرشحات القطط الباقية
    on, cand = set(safe), []
    # نمر على خلايا الطريق الآمن (بدون أول 3 وآخر 2)
    for cell in safe[3:-2]:
        # نمر على جيران كل خلية
        for a in open_neighbors(walls, cell):
            # إذا الجار على الطريق أو فيه قطة
            if a in on or a in cats:
                # نتجاهله
                continue
            # أحياناً (50%) ندخل أعمق بالفرع الجانبي
            if rng.random() < .5:                    # sometimes deeper in the branch
                # نبحث عن خلية بعده
                for b in open_neighbors(walls, a):
                    # بشرط أنها ليست على الطريق ولا فيها قطة ولا هي الخلية السابقة
                    if b not in on and b not in cats and b != cell:
                        # نعتمدها
                        a = b
                        # ونتوقف
                        break
            # نضيف المكان لقائمة المرشحين (فخاخ بعيدة عن الطريق الآمن)
            cand.append(a)
    # نخلط المرشحين
    rng.shuffle(cand)
    # نمر على المرشحين بدون تكرار
    for a in dict.fromkeys(cand):
        # إذا وصلنا للعدد المطلوب
        if len(cats) >= count:
            # نتوقف
            break
        # نتأكد أنها ليست البداية ولا النهاية
        if a != start and a != end:
            # نضع القطة
            cats.add(a)
    # نرجع مجموعة القطط
    return cats


# =====================================================================
#  DRAWING HELPERS
# =====================================================================
# دالة make_glow ترسم هالة ناعمة ملونة (للقطط والجبنة)
def make_glow(r, col):
    # سطح شفاف بحجم الهالة
    s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    # نرسم 10 دوائر من الأكبر للأصغر
    for i in range(10, 0, -1):
        # كل دائرة أغمق قليلاً فنحصل على توهج ناعم
        pygame.draw.circle(s, (*col, 8 * (11 - i)), (r, r), max(1, int(r * i / 10)))
    # نرجع الهالة
    return s


# دالة draw_mouse ترسم الفأر
def draw_mouse(x, y, k):
    # ألوان الجسم والحواف
    body, dark = (170, 170, 190), (90, 90, 110)
    # نرسم ذيل الفأر بخط منكسر
    pygame.draw.lines(screen, (240, 150, 170), False,
                      [(x + k * .8, y + k * .5), (x + k * 1.4, y + k * .6), (x + k * 1.7, y + k * .1)], 2)
    # نمر على الجانبين (يسار ويمين)
    for g in (-1, 1):
        # نحسب مكان الأذن
        c = (x + g * k * .75, y - k * .75)
        # نرسم الأذن الخارجية
        pygame.draw.circle(screen, body, c, max(1, k * .55))
        # وداخلها الوردي
        pygame.draw.circle(screen, (255, 175, 195), c, max(1, k * .32))
    # نرسم رأس الفأر
    pygame.draw.circle(screen, body, (x, y), max(2, k))
    # وحوافه
    pygame.draw.circle(screen, dark, (x, y), max(2, k), 2)
    # نكرر للعينين (يسار ويمين)
    for g in (-1, 1):
        # نحسب مكان العين
        ex = x + g * k * .38
        # نرسم بياض العين
        pygame.draw.circle(screen, (255, 255, 255), (ex, y - k * .2), max(1, k * .25))
        # ونرسم بؤبؤها الأسود
        pygame.draw.circle(screen, (0, 0, 0), (ex, y - k * .17), max(1, k * .13))
    # نرسم أنف الفأر الوردي
    pygame.draw.circle(screen, (255, 110, 150), (x, y + k * .35), max(1, k * .16))


# دالة draw_cat ترسم قطة الفخ (الخطر)
def draw_cat(x, y, k):
    # لون القطة داكن
    d = (84, 46, 64)
    # نكرر للأذنين
    for g in (-1, 1):
        # نرسم الأذن كمثلث
        pygame.draw.polygon(screen, d, [(x + g * k, y - k * .2), (x + g * k * .8, y - k * 1.4),
                                        (x + g * k * .15, y - k * .8)])
    # نرسم رأس القطة
    pygame.draw.circle(screen, d, (x, y), max(2, k))
    # نكرر للعينين
    for g in (-1, 1):
        # نرسم عيناً حمراء بيضاوية (تعطي إحساس الخطر)
        pygame.draw.ellipse(screen, (226, 96, 88),
                            (x + g * k * .45 - k * .22, y - k * .25, k * .44, k * .3))
        # نرسم شارب القطة
        pygame.draw.line(screen, (200, 200, 210), (x + g * k * .2, y + k * .35),
                         (x + g * k * 1.1, y + k * .3), 1)


# دالة draw_cheese ترسم الجبنة (المخرج) مع أشعة تدور حولها
def draw_cheese(x, y, k, t, gl=None):
    # إذا أعطيناها هالة توهج
    if gl:
        # نرسمها خلف الجبنة
        screen.blit(gl, (int(x - gl.get_width() / 2), int(y - gl.get_height() / 2)))
    # نرسم 8 أشعة تدور حول الجبنة
    for i in range(8):  # spinning rays
        # نحسب زاوية الشعاع (تتغير مع الوقت فتدور)
        a = t * .8 + i * math.pi / 4
        # نرسم الشعاع كخط قصير
        pygame.draw.line(screen, (255, 205, 100),
                         (x + math.cos(a) * k * 1.4, y + math.sin(a) * k * 1.4),
                         (x + math.cos(a) * k * 1.9, y + math.sin(a) * k * 1.9), 2)
    # نقاط مثلث الجبنة
    pts = [(x - k, y + k * .7), (x + k, y + k * .7), (x + k, y - k * .7)]
    # نملأ الجبنة باللون الأصفر
    pygame.draw.polygon(screen, (255, 214, 92), pts)
    # ونرسم حافتها الداكنة
    pygame.draw.polygon(screen, (200, 150, 40), pts, 2)
    # نمر على ثقوب الجبنة (موقع ونصف قطر)
    for hx, hy, hr in ((.35, .25, .18), (.62, -.1, .12), (-.1, .45, .12)):
        # نرسم كل ثقب بدائرة
        pygame.draw.circle(screen, (226, 170, 50), (x + hx * k, y + hy * k), max(1, hr * k))


# دالة draw_layers تلوّن الخلايا حسب حالة BFS: مستكشفة (أزرق إلى بنفسجي) أو حدود (سماوي)
def draw_layers(sv, ox, oy, cs):
    """BFS colors: blue->purple = explored (by distance), cyan = frontier (in queue)."""
    # إذا ما في بحث فلا نرسم شي
    if not sv:
        # نخرج
        return
    # نمر على كل خلية استكشفناها مع بُعدها
    for (r, c), d in sv.dist.items():
        # نحسب لونها حسب بُعدها عن البداية (الأقرب أزرق والأبعد بنفسجي)
        col = lerp(VIS_A, VIS_B, d / sv.maxd)
        # نرسم مربعاً ملوناً للخلية
        pygame.draw.rect(screen, col, (ox + c * cs + 1, oy + r * cs + 1, cs - 1, cs - 1))
    # نمر على الخلايا الموجودة داخل الطابور (الحدود)
    for (r, c) in sv.q:
        # نرسمها باللون السماوي
        pygame.draw.rect(screen, FRONTIER, (ox + c * cs + 1, oy + r * cs + 1, cs - 1, cs - 1))


# دالة draw_markers ترسم مربع البداية (أخضر) ومربع المخرج (أحمر)
def draw_markers(start, end, ox, oy, cs):
    # نمر على الخليتين ولون كل منهما
    for cell, col in ((start, GREEN), (end, RED)):
        # نفصل رقم الصف والعمود
        r, c = cell
        # نرسم مربعاً بزوايا مدورة
        pygame.draw.rect(screen, col, (ox + c * cs + 2, oy + r * cs + 2, cs - 3, cs - 3), border_radius=4)


# دالة draw_walls ترسم جدران المتاهة
def draw_walls(walls, ox, oy, cs):
    # نمر على كل خلية وجدرانها
    for (r, c), ws in walls.items():
        # نحسب مكان الخلية على الشاشة
        x, y = ox + c * cs, oy + r * cs
        # إذا فيه جدار شمالي
        if "N" in ws:
            # نرسمه كخط أعلى الخلية
            pygame.draw.line(screen, WALL, (x, y), (x + cs, y), 2)
        # إذا فيه جدار جنوبي
        if "S" in ws:
            # نرسمه أسفل الخلية
            pygame.draw.line(screen, WALL, (x, y + cs), (x + cs, y + cs), 2)
        # إذا فيه جدار غربي
        if "W" in ws:
            # نرسمه يسار الخلية
            pygame.draw.line(screen, WALL, (x, y), (x, y + cs), 2)
        # إذا فيه جدار شرقي
        if "E" in ws:
            # نرسمه يمين الخلية
            pygame.draw.line(screen, WALL, (x + cs, y), (x + cs, y + cs), 2)


# دالة draw_path ترسم المسار الأقصر الذهبي ويظهر تدريجياً بعد انتهاء BFS
def draw_path(sv, ox, oy, cs, tick):
    """Glowing shortest path, revealed progressively once BFS is done."""
    # إذا البحث لم ينته أو ما في مسار
    if not sv or not sv.done or not sv.path:
        # نخرج
        return
    # نزيد جزء المسار الظاهر شوي كل إطار
    sv.reveal = min(len(sv.path), sv.reveal + 0.8)
    # نحوّل خلايا المسار الظاهرة إلى نقاط على الشاشة
    pts = [cell_center(p, ox, oy, cs) for p in sv.path[:int(sv.reveal) + 1]]
    # إذا في نقطتين أو أكثر
    if len(pts) > 1:
        # نرسم ظلاً برتقالياً غامقاً عريضاً تحت الخط
        pygame.draw.lines(screen, (214, 150, 50), False, pts, max(6, int(cs // 2)))
        # ثم الخط الذهبي فوقه
        pygame.draw.lines(screen, GOLD, False, pts, max(3, int(cs // 4)))
    # نبض بسيط لحجم النقطة المتحركة
    pulse = 3 + 2 * math.sin(tick * 0.2)
    # نرسم نقطة غامقة بنهاية المسار الظاهر
    pygame.draw.circle(screen, INK, pts[-1], int(cs * 0.22 + pulse))


# دالة make_background ترسم الخلفية المتدرجة مرة واحدة
def make_background():
    # نصنع سطحاً بحجم النافذة
    surf = pygame.Surface((W, H))
    # نمر على كل صف بكسل
    for y in range(H):
        # نرسم خطاً بلون مختلط بين اللونين (فيصير تدرجاً)
        pygame.draw.line(surf, lerp(BG1, BG2, y / H), (0, y), (W, y))
    # نرجع الخلفية
    return surf


# نرسم الخلفية مرة واحدة ونخزنها (أسرع من رسمها كل إطار)
BACKGROUND = make_background()
# نصنع 60 نقطة ضوء عشوائية تطفو بالخلفية (موقعها وسرعتها)
PARTICLES = [[random.uniform(0, W), random.uniform(0, H), random.uniform(0.2, 1.0)]
             for _ in range(60)]


# دالة draw_background ترسم الخلفية مع النقاط الطائرة
def draw_background(tick):
    # نرسم الخلفية المخزنة
    screen.blit(BACKGROUND, (0, 0))
    # نمر على كل نقطة ضوء
    for p in PARTICLES:
        # نحركها للأعلى
        p[1] -= p[2] * 0.6
        # إذا خرجت من أعلى الشاشة
        if p[1] < -5:
            # نعيدها من الأسفل بمكان عشوائي
            p[0], p[1] = random.uniform(0, W), H + 5
        # نحسب لمعانها (يتغير مع الوقت)
        glow = 0.5 + 0.5 * math.sin(tick * 0.03 + p[0])
        # نحسب لونها حسب اللمعان
        c = lerp((250, 205, 225), (236, 172, 206), glow * p[2])
        # نرسم النقطة
        pygame.draw.circle(screen, c, (int(p[0]), int(p[1])), max(1, int(p[2] * 3)))


# دالة text_center تكتب نصاً في منتصف الشاشة أفقياً
def text_center(font, s, y, color=INK):
    # نحوّل النص إلى صورة
    img = font.render(s, True, color)
    # ونرسمها في المنتصف
    screen.blit(img, img.get_rect(center=(W // 2, y)))


# دالة draw_star ترسم نجمة (تظهر بشاشة النتيجة)
def draw_star(cx, cy, r, filled):
    # قائمة نقاط النجمة
    pts = []
    # النجمة لها 10 نقاط (5 خارجية و5 داخلية)
    for i in range(10):
        # نحسب زاوية كل نقطة
        ang = -math.pi / 2 + i * math.pi / 5
        # النقطة الخارجية بعيدة والداخلية قريبة
        rad = r if i % 2 == 0 else r * 0.45
        # نضيف النقطة بعد تحويلها إلى إحداثيات
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    # إذا النجمة ممتلئة (مكتسبة)
    if filled:
        # نلوّنها ذهبياً
        pygame.draw.polygon(screen, GOLD, pts)
    # نرسم حدودها (ذهبية أو رمادية إذا فارغة)
    pygame.draw.polygon(screen, GOLD if filled else (222, 200, 215), pts, 3)


# =====================================================================
#  UI
# =====================================================================
# كلاس Button يمثل زراً بالقائمة
class Button:
    # دالة البناء: النص والموقع والحجم والفعل الذي ينفذه الزر
    def __init__(self, text, cx, cy, w, h, action):
        # نحفظ النص والفعل
        self.text, self.action = text, action
        # نصنع مستطيل الزر
        self.rect = pygame.Rect(0, 0, w, h)
        # ونضع مركزه بالمكان المطلوب
        self.rect.center = (cx, cy)
        # t رقم من 0 إلى 1 لحركة تغيّر لون الزر عند مرور الماوس
        self.t = 0.0

    # دالة label ترجع نص الزر
    def label(self):
        # النص قد يكون ثابتاً أو دالة (مثل: حجم المتاهة الحالي)
        return self.text() if callable(self.text) else self.text

    # دالة update تتابع هل الماوس فوق الزر
    def update(self, mouse):
        # نتحقق إن كان الماوس داخل الزر
        hover = self.rect.collidepoint(mouse)
        # نزيد t تدريجياً إذا الماوس فوقه وننقصه إذا لا (حركة ناعمة)
        self.t = max(0.0, min(1.0, self.t + (0.18 if hover else -0.18)))

    # دالة draw ترسم الزر
    def draw(self):
        # نكبّر الزر قليلاً عند مرور الماوس
        r = self.rect.inflate(int(14 * self.t), int(6 * self.t))
        # نرسم ظل الزر
        pygame.draw.rect(screen, (232, 196, 212), r.move(0, 5), border_radius=16)
        # نرسم جسم الزر بلون يمزج العادي والمميز
        pygame.draw.rect(screen, lerp(BTN, BTN_HOVER, self.t), r, border_radius=16)
        # نرسم إطار الزر
        pygame.draw.rect(screen, lerp((240, 160, 194), INK, self.t), r, 2, border_radius=16)
        # نحوّل نص الزر إلى صورة
        img = F_BTN.render(self.label(), True, INK)
        # ونرسمها في منتصف الزر
        screen.blit(img, img.get_rect(center=r.center))


# =====================================================================
#  PRESENTATION  (menu -> "Presentation (What is BFS?)")
#  Arrows / click = navigate | F = full screen | P = play | Esc = menu
# =====================================================================
# دالة ease تجعل الحركة تبدأ سريعة وتنتهي ببطء (حركة ناعمة)
def ease(x):
    # نحصر القيمة بين 0 و1
    x = max(0.0, min(1.0, x))
    # نرجع القيمة بعد تطبيق المنحنى
    return 1 - (1 - x) ** 3


# دالة appear تحسب تقدّم ظهور عنصر بالشريحة (0 مخفي إلى 1 ظاهر) بعد تأخير معين
def appear(t, delay, dur=24):
    """0 -> 1 animation progress that starts `delay` frames after the slide opens."""
    # نحسب التقدم حسب الوقت بعد التأخير
    return ease((t - delay) / dur)


# دالة draw_text تكتب نصاً يظهر تدريجياً ويصعد للأعلى
def draw_text(font, s, x, y, color=INK, a=1.0, center=False):
    """Text that fades in and slides up. `center` centers it horizontally."""
    # إذا النص ما بدأ بالظهور
    if a <= 0:
        # ما نرسم شي
        return
    # نحوّل النص إلى صورة
    img = font.render(s, True, color)
    # إذا ما زال يظهر
    if a < 1:
        # نجعله شفافاً حسب التقدم
        img.set_alpha(int(255 * a))
    # نحسب مكان البداية (أو المنتصف إذا طلبنا التوسيط)
    px = x - img.get_width() / 2 if center else x
    # نرسم النص مع إزاحة بسيطة للأسفل تختفي مع الظهور
    screen.blit(img, (int(px), int(y + (1 - a) * 14)))


# دالة draw_para تكتب فقرة طويلة على عدة أسطر
def draw_para(font, text, x, y, width, color=INK, a=1.0, lh=26):
    # نقسم النص إلى أسطر تناسب العرض
    for line in wrap(font, text, width):
        # نكتب كل سطر
        draw_text(font, line, x, y, color, a)
        # وننزل للسطر التالي
        y += lh
    # نرجع مكان نهاية الفقرة
    return y


# دالة draw_items تكتب قائمة عناوين وفقرات ونقاط تظهر واحدة بعد الأخرى
def draw_items(items, x, y, width, t, delay=14, gap=16):
    """Heading / paragraph / bullet list that appears line by line."""
    # نمر على كل عنصر بالقائمة
    for k, (style, txt) in enumerate(items):
        # نحسب وقت ظهور هذا العنصر (كل عنصر بعد الذي قبله)
        a = appear(t, delay + k * gap)
        # إذا العنصر عنوان فرعي
        if style == "h":
            # نترك مسافة صغيرة
            y += 4
            # نكتبه بالذهبي
            draw_text(F_BTN, txt, x, y, ACCENT, a)
            # وننزل للأسفل
            y += 34
            # وننتقل للعنصر التالي
            continue
        # إذا نقطة نضع قبلها شرطة (إلا إذا كانت خطوة مرقمة)
        prefix = "- " if style == "b" and not txt[0].isdigit() else ""
        # نكتب الفقرة وننزل لما بعدها
        y = draw_para(F_BODY, prefix + txt, x, y, width, INK, a, 27) + 8
    # نرجع مكان النهاية
    return y


# دالة card_box ترسم بطاقة ملونة تصعد وتظهر
def card_box(x, y, w, h, col, t, delay):
    # نحسب تقدم ظهورها
    a = appear(t, delay)
    # إذا لم تبدأ بالظهور
    if a <= 0:
        # ما نرسمها
        return
    # نزيحها للأسفل وهي تظهر (تصعد لمكانها)
    y += int((1 - a) * 30)
    # نصنع مستطيل البطاقة
    r = pygame.Rect(x, y, w, h)
    # نرسم ظلها
    pygame.draw.rect(screen, (232, 196, 212), r.move(0, 6), border_radius=18)
    # نرسم جسمها الأبيض
    pygame.draw.rect(screen, (255, 255, 255), r, border_radius=18)
    # نرسم الشريط الملوّن أعلاها
    pygame.draw.rect(screen, col, (x, y, w, 9), border_top_left_radius=18, border_top_right_radius=18)
    # نرسم إطارها
    pygame.draw.rect(screen, lerp(col, INK, 0.3), r, 2, border_radius=18)


# دالة icon ترسم أيقونة صغيرة حسب نوعها
def icon(kind, cx, cy):
    # أيقونة الموقع (GPS)
    if kind == "gps":
        # نرسم رأس السهم السفلي
        pygame.draw.polygon(screen, RED, [(cx - 11, cy - 1), (cx + 11, cy - 1), (cx, cy + 22)])
        # ودائرته الحمراء
        pygame.draw.circle(screen, RED, (cx, cy - 8), 14)
        # ونقطته الغامقة
        pygame.draw.circle(screen, INK, (cx, cy - 8), 5)
    # أيقونة الفأر
    elif kind == "mouse":
        # نستخدم دالة رسم الفأر
        draw_mouse(cx, cy, 18)
    # أيقونة القطة
    elif kind == "cat":
        # نستخدم دالة رسم القطة
        draw_cat(cx, cy, 16)
    # أيقونة الروبوت
    elif kind == "robot":
        # هوائي الروبوت
        pygame.draw.line(screen, DIM, (cx, cy - 16), (cx, cy - 26), 3)
        # رأس الهوائي
        pygame.draw.circle(screen, GOLD, (cx, cy - 28), 4)
        # جسم الروبوت
        pygame.draw.rect(screen, (190, 170, 215), (cx - 20, cy - 16, 40, 34), border_radius=8)
        # نكرر للعينين
        for g in (-1, 1):
            # نرسم العين
            pygame.draw.circle(screen, (74, 46, 84), (cx + g * 9, cy - 3), 5)
    # أيقونة الشبكة
    elif kind == "net":
        # ثلاث نقاط تمثل أجهزة
        pts = [(cx - 26, cy + 12), (cx, cy - 16), (cx + 26, cy + 12)]
        # نرسم خطوطاً تربط بينها
        pygame.draw.lines(screen, DIM, True, pts, 3)
        # نمر على النقاط
        for p in pts:
            # نرسم كل جهاز بدائرة سماوية
            pygame.draw.circle(screen, FRONTIER, p, 8)
    # أيقونة الطبقات (مثل BFS)
    elif kind == "layers":
        # نمر على ثلاثة ألوان
        for k, col in enumerate((VIS_A, VIS_B, FRONTIER)):
            # نرسم مربعاً لكل طبقة
            pygame.draw.rect(screen, col, (cx - 32 + k * 24, cy - 16 + (k % 2) * 10, 20, 20), border_radius=5)
    # أيقونة زر الخطوة
    elif kind == "step":
        # نرسم مثلث التشغيل
        pygame.draw.polygon(screen, GOLD, [(cx - 16, cy - 18), (cx - 16, cy + 18), (cx + 12, cy)])
        # ونرسم عمود التوقف بجانبه
        pygame.draw.rect(screen, GOLD, (cx + 16, cy - 18, 7, 36), border_radius=3)
    # أيقونة التلميح (Hint)
    elif kind == "hint":
        # نمر على مواقع النقاط
        for k, (dx, dy) in enumerate(((-30, 12), (-15, 0), (0, 10), (15, -6), (30, -16))):
            # نرسم نقطة غامقة بكل موقع (مسار)
            pygame.draw.circle(screen, INK, (cx + dx, cy + dy), 5)
    # أيقونة النجمة
    elif kind == "star":
        # نرسم نجمة ذهبية
        draw_star(cx, cy, 24, True)


# دالة ripple ترسم طبقات BFS على شبكة بشكل ثابت بدون حركة (خلفية العنوان والشكر)
def ripple(tick, cx=12, cy=8):
    """BFS-like wave spreading over a grid (title / thank-you background)."""
    # نمر على 17 صفاً
    for r in range(17):
        # وعلى 25 عموداً
        for c in range(25):
            # نحسب بُعد الخلية عن المركز (مثل بُعد BFS)
            dd = abs(r - cy) + abs(c - cx)
            # نحسب شدة اللون (ثابتة وما تتحرك حتى ما تتعب العين)
            v = max(0.0, math.sin(1.0 - dd * 0.38)) ** 2
            # نحسب لون الخلية حسب شدة الموجة
            col = lerp((255, 238, 246), lerp(VIS_A, VIS_B, (dd % 12) / 12), v * 0.35)
            # نرسم الخلية بشكل مربع بزوايا مدورة
            pygame.draw.rect(screen, col, (c * 40 + 2, r * 40 + 2, 36, 36), border_radius=8)


# متغير يحفظ لوحة العنوان بعد رسمها أول مرة
_PANEL = None


# دالة title_panel ترجع لوحة شفافة تظهر خلف نص العنوان
def title_panel():
    # نسمح بتغيير المتغير الخارجي
    global _PANEL
    # إذا ما رسمناها بعد
    if _PANEL is None:
        # نصنع سطحاً شفافاً
        _PANEL = pygame.Surface((780, 400), pygame.SRCALPHA)
        # نرسم اللوحة البيضاء الشفافة بزوايا مدورة
        pygame.draw.rect(_PANEL, (255, 255, 255, 235), _PANEL.get_rect(), border_radius=30)
        # ونرسم إطارها
        pygame.draw.rect(_PANEL, (240, 160, 194, 255), _PANEL.get_rect(), 2, border_radius=30)
    # نرجع اللوحة
    return _PANEL


# دالة frame ترسم إطار الشريحة العادية: الخلفية والعنوان والشريط الذهبي
def frame(d, title, t):
    # نرسم الخلفية
    draw_background(d.tick)
    # نحسب تقدم ظهور العنوان
    a = appear(t, 0, 20)
    # نرسم شريطاً ذهبياً ينمو بجانب العنوان
    pygame.draw.rect(screen, GOLD, (40, 36, 8, int(48 * a)), border_radius=4)
    # نكتب عنوان الشريحة
    draw_text(F_BIG, title, 62, 32, INK, a)


# كلاس Demo: متاهة صغيرة يشتغل فيها BFS ببطء مع رسم الطابور تحتها (تستخدم بالشرائح)
class Demo:
    """Small maze where BFS runs slowly, with the queue drawn below it."""

    # دالة البناء: هل فيها قطط، رقم المتاهة، حجمها، مكانها
    def __init__(self, cats=False, seed=1, n=7, cs=46, ox=50, oy=120, ncats=3):
        # نصنع مولد أرقام عشوائية ثابت (حتى تطلع نفس المتاهة كل مرة)
        rng = random.Random(seed)
        # نحفظ الحجم والمكان
        self.N, self.cs, self.ox, self.oy = n, cs, ox, oy
        # نولّد المتاهة الصغيرة
        self.walls, self.start, self.end = generate(n, n, rng, 0.2)
        # نضع القطط إذا طُلبت
        self.cats = place_cats(self.walls, self.start, self.end, ncats, rng) if cats else set()
        # نبدأ البحث من الصفر
        self.reset()

    # دالة reset تعيد تشغيل العرض التوضيحي من البداية
    def reset(self):
        # ننشئ بحث BFS جديد على نفس المتاهة
        self.bfs = BFS(self.walls, self.start, self.end, self.cats)
        # نصفّر المؤقت وعدّاد الانتظار
        self.timer = self.hold = 0

    # دالة update تُستدعى كل إطار لتحريك العرض
    def update(self):
        # نزيد المؤقت
        self.timer += 1
        # إذا انتهى البحث
        if self.bfs.done:
            # نعدّ فترة انتظار (حتى يتمكن الحضور من رؤية النتيجة)
            self.hold += 1
            # بعد حوالي 3 ثوانٍ
            if self.hold > 160:      # replay the same maze
                # نعيد العرض من البداية
                self.reset()
        # وإلا: كل 14 إطاراً تقريباً
        elif self.timer % 14 == 0:
            # ننفذ خطوة BFS واحدة (بطيئة حتى يُفهم الشرح)
            self.bfs.step()

    # دالة caption ترجع الجملة التي تشرح ما يحدث الآن
    def caption(self):
        # نختصر اسم البحث بـ b
        b = self.bfs
        # إذا انتهى البحث ووجدنا المسار
        if b.done and b.path:
            # نكتب عدد الخلايا المستكشفة وطول أقصر مسار
            return (f"Exit reached! BFS explored {b.explored} cells and the shortest path "
                    f"is {len(b.path) - 1} steps.")
        # إذا لم نبدأ بعد
        if b.explored == 0:
            # نشرح أن البداية وُضعت بالطابور
            return "Start: the green cell is put in the queue."
        # وإلا نشرح الخطوة الحالية: أي خلية خرجت من الطابور وكم جاراً أضفنا
        return f"Took {b.cur} out of the queue and added {b.added} new neighbor(s) to its end."

    # دالة draw ترسم المتاهة الصغيرة والطابور وشرح الخطوة
    def draw(self):
        # نجمع القيم التي سنحتاجها: حجم الخلية ومكان الرسم والبحث وحجم المتاهة
        cs, ox, oy, b, n = self.cs, self.ox, self.oy, self.bfs, self.N
        # نرسم خلفية المتاهة الفاتحة
        pygame.draw.rect(screen, (255, 252, 254), (ox, oy, cs * n, cs * n), border_radius=6)
        # نلوّن الخلايا المستكشفة والحدود
        draw_layers(b, ox, oy, cs)
        # نرسم مربعي البداية والمخرج
        draw_markers(self.start, self.end, ox, oy, cs)
        # نرسم الجدران
        draw_walls(self.walls, ox, oy, cs)
        # نمر على القطط (إن وُجدت)
        for cat in self.cats:
            # نحسب مكان القطة
            x, y = cell_center(cat, ox, oy, cs)
            # ونرسمها
            draw_cat(x, y, cs * .3)
        # نحسب مكان المخرج
        ex, ey = cell_center(self.end, ox, oy, cs)
        # ونرسم الجبنة فيه
        draw_cheese(ex, ey, cs * .22, self.timer / 60)
        # إذا في خلية خرجت للتو من الطابور
        if b.cur and not b.done:
            # نأخذ مكانها
            r, c = b.cur
            # ونرسم حولها إطاراً غامقاً لنلفت النظر لها
            pygame.draw.rect(screen, INK, (ox + c * cs, oy + r * cs, cs, cs), 3)
        # نرسم المسار الذهبي إذا انتهى البحث
        draw_path(b, ox, oy, cs, self.timer)
        # نحدد مكان رسم الطابور تحت المتاهة
        qy = oy + cs * n + 20      # the queue
        # نكتب عنوان الطابور (من الأمام للخلف)
        screen.blit(F_SMALL.render("QUEUE  (front -> back)", True, ACCENT), (ox, qy))
        # نأخذ أول 9 عناصر من الطابور فقط للعرض
        shown = list(b.q)[:9]
        # نمر على كل عنصر
        for k, cell in enumerate(shown):
            # نصنع مربعاً صغيراً له
            rect = pygame.Rect(ox + k * 37, qy + 28, 32, 32)
            # نلونه حسب بُعد الخلية عن البداية
            pygame.draw.rect(screen, lerp(VIS_A, VIS_B, b.dist[cell] / b.maxd), rect, border_radius=6)
            # نرسم إطاره (الأول ذهبي لأنه سيخرج أولاً)
            pygame.draw.rect(screen, GOLD if k == 0 else (240, 160, 194), rect, 3 if k == 0 else 1,
                             border_radius=6)
            # نكتب رقم البُعد داخل المربع
            img = F_SMALL.render(str(b.dist[cell]), True, INK)
            # ونرسمه بالمنتصف
            screen.blit(img, (rect.x + (32 - img.get_width()) // 2, rect.y + (32 - img.get_height()) // 2))
        # إذا الطابور فاضي
        if not shown:
            # نكتب (empty)
            screen.blit(F_SMALL.render("(empty)", True, DIM), (ox, qy + 34))
        # إذا فيه أكثر من 9 عناصر
        if len(b.q) > 9:
            # نكتب كم عنصراً إضافياً بالطابور
            screen.blit(F_SMALL.render(f"+{len(b.q) - 9}", True, DIM), (ox + 9 * 37, qy + 34))
        # نشرح معنى الأرقام
        screen.blit(F_SMALL.render("number = distance from start", True, DIM), (ox, qy + 66))
        # نكتب جملة الشرح على أسطر
        for k, line in enumerate(wrap(F_SMALL, self.caption(), 330)):
            # ونرسم كل سطر
            screen.blit(F_SMALL.render(line, True, INK), (ox, qy + 92 + k * 22))


# ---------- small graph for the "BFS by hand" slide ----------
# مواقع عقد الرسم الصغير (الأحرف A إلى G) على الشاشة
G_POS = {"A": (110, 300), "B": (230, 200), "C": (230, 400), "D": (360, 130),
         "E": (360, 270), "F": (360, 410), "G": (480, 340)}
# الحواف: أي حرفين مرتبطين ببعض
G_EDGES = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("E", "G"), ("F", "G"), ("E", "F")]


# دالة build_trace تنفذ BFS على الرسم الصغير وتسجل كل خطوة لعرضها بشريحة "BFS by hand"
def build_trace():
    # نصنع قائمة جيران لكل عقدة
    adj = {k: [] for k in G_POS}
    # نمر على كل حافة
    for a, b in G_EDGES:
        # نضيف الجار الأول
        adj[a].append(b)
        # ونضيف الجار الثاني (الحافة بالاتجاهين)
        adj[b].append(a)
    # نرتب الجيران ترتيباً أبجدياً
    for k in adj:
        # ليكون الترتيب ثابتاً
        adj[k].sort()
    # نجهز الطابور والخلايا المزورة وروابط "من أين جاء"
    q, seen, parent = deque(["A"]), {"A"}, {"A": None}
    # نسجل الخطوة الأولى: الطابور فيه A فقط
    steps = [("-", ["A"], ["A"])]
    # نكرر مادام الطابور فيه عناصر
    while q:
        # نسحب أول عنصر (FIFO)
        cur = q.popleft()
        # إذا ما وصلنا للهدف G بعد
        if cur != "G":
            # نمر على جيرانه
            for n in adj[cur]:
                # إذا ما زرناه من قبل
                if n not in seen:
                    # نسجله كمزور
                    seen.add(n)
                    # ونحفظ من أين جاء
                    parent[n] = cur
                    # ونضيفه لنهاية الطابور
                    q.append(n)
        # نسجل حالة الخطوة (العنصر والطابور والمزورين) لنعرضها بالجدول
        steps.append((cur, list(q), sorted(seen)))
        # إذا وصلنا للهدف G
        if cur == "G":
            # نتوقف
            break
    # نبدأ ببناء المسار من الهدف
    path, node = [], "G"
    # نرجع للخلف عبر روابط parent
    while node:
        # نضيف العقدة للمسار
        path.append(node)
        # وننتقل لمن جاءت منه
        node = parent[node]
    # نرجع الخطوات والمسار بعد عكسه
    return steps, path[::-1]


# ننفذ build_trace مرة واحدة ونحفظ النتيجة
TRACE = build_trace()
# متغير لحفظ نتائج القياس
RESULTS = None


# دالة compute_results تقيس أداء BFS الحقيقي على متاهات عشوائية (لشريحة النتائج)
def compute_results():
    """Real measurements with the game's own code (BFS only)."""
    # نسمح بتعديل المتغير الخارجي
    global RESULTS
    # إذا ما قسنا من قبل
    if RESULTS is None:
        # قائمة النتائج
        out = []
        # نجرّب 3 أحجام: 12 و20 و30
        for n in (12, 20, 30):
            # مولد عشوائي ثابت لكل حجم
            rng = random.Random(100 + n)
            # مجاميع: الخلايا المستكشفة وطول المسار والزمن
            ex = pl = tm = 0.0
            # نكرر القياس 25 مرة
            trials = 25
            # كل مرة نكرر القياس
            for _ in range(trials):
                # نولّد متاهة جديدة
                w, s_, e_ = generate(n, n, rng)
                # نبدأ ساعة القياس
                t0 = time.perf_counter()
                # ننشئ بحث BFS
                b = BFS(w, s_, e_)
                # ونشغّله للنهاية
                b.run_all()
                # نحسب الزمن بالميلي ثانية ونضيفه
                tm += (time.perf_counter() - t0) * 1000
                # نضيف عدد الخلايا المستكشفة
                ex += b.explored
                # ونضيف طول أقصر مسار
                pl += len(b.path) - 1
            # نحسب المتوسطات لهذا الحجم ونحفظها
            out.append((n, n * n, ex / trials, pl / trials, tm / trials))
        # نحفظ النتائج
        RESULTS = out
    # نرجع النتائج
    return RESULTS


# دالة make_layers تحسب كم خلية على كل بُعد من البداية (لرسم الأعمدة)
def make_layers():
    # مولد عشوائي ثابت
    rng = random.Random(5)
    # نولّد متاهة 20x20
    w, s_, e_ = generate(20, 20, rng)
    # نشغّل BFS بهدف غير موجود حتى يستكشف كل شي
    full = BFS(w, s_, (-1, -1))      # unreachable goal = explore everything
    # ننفذه للنهاية
    full.run_all()
    # قاموس يعدّ الخلايا لكل بُعد
    counts = {}
    # نمر على أبعاد كل الخلايا
    for dd in full.dist.values():
        # نزيد عدّاد هذا البُعد
        counts[dd] = counts.get(dd, 0) + 1
    # أكبر بُعد
    maxd = max(counts)
    # نجمّع الأبعاد بمجموعات (حتى لا تزيد الأعمدة عن 40)
    binsize = max(1, math.ceil((maxd + 1) / 40))
    # نصنع قائمة الأعمدة
    bins = [0] * (maxd // binsize + 1)
    # نمر على كل بُعد وعدده
    for dd, c in counts.items():
        # نضيفه للعمود المناسب
        bins[dd // binsize] += c
    # نرجع الأعمدة وحجم المجموعة وبُعد المخرج
    return bins, binsize, full.dist[e_]


# ---------- slides ----------
# نصوص شريحة "ما هو BFS": (النوع، النص) حيث p فقرة وh عنوان وb نقطة
ITEMS_BFS = [
    # فقرة (p): تعريف BFS وأنه يستكشف طبقة بعد طبقة
    ("p", "BFS = Breadth-First Search. It explores a graph level by level, "
          "always finishing the closest cells before moving farther."),
    # فقرة (p): BFS يتوسع مثل الموج في الماء
    ("p", "BFS visits all cells 1 step from the start, then all cells 2 steps away, "
          "then 3... like ripples spreading in water."),
    # عنوان فرعي (h): الألوان التي ستظهر
    ("h", "Colors you will see"),
    # نقطة (b): الأزرق إلى البنفسجي = خلايا مستكشفة
    ("b", "Blue to purple = explored (darker = closer to the start)."),
    # نقطة: السماوي = الحدود (الخلايا المنتظرة بالطابور)
    ("b", "Cyan = frontier: cells waiting in the queue."),
    # نقطة: الخط الذهبي = أقصر مسار
    ("b", "Gold line = the shortest path."),
]
# نصوص شريحة "كيف يعمل BFS" (خطوات الخوارزمية)
ITEMS_QUEUE = [
    # فقرة: BFS يستخدم طابوراً FIFO (الداخل أولاً يخرج أولاً)
    ("p", "BFS uses a QUEUE: First In, First Out (FIFO). Watch it on the left."),
    # عنوان فرعي: الخوارزمية
    ("h", "The algorithm"),
    # الخطوة 1: نضع خلية البداية بالطابور
    ("b", "1. Put the start cell in the queue."),
    # الخطوة 2: نسحب أول خلية من الطابور
    ("b", "2. Take the FIRST cell out of the queue."),
    # الخطوة 3: نضيف جيرانها الجدد لنهاية الطابور ونتذكر من أين جاؤوا
    ("b", "3. Add its unvisited neighbors to the END of the queue, and remember "
          "where each one came from."),
    # الخطوة 4: نكرر حتى يخرج المخرج من الطابور
    ("b", "4. Repeat until the exit is taken out of the queue."),
    # الخطوة 5: نتتبع روابط "من أين جاء" لنستعيد المسار
    ("b", "5. Follow the 'came from' links backwards to rebuild the path."),
]
# مزايا اللعبة: (العنوان، الوصف، الأيقونة، اللون)
FEATURES = [
    # الميزة 1: اللعب ضد BFS (الفأر والجبنة)
    ("Play: You vs BFS", "Guide the mouse to the cheese; your steps are compared with BFS.", "mouse", GREEN),
    # الميزة 2: مشاهدة BFS وهو يتوسع طبقة بطبقة
    ("Watch BFS", "See the search spread layer by layer, then the shortest path lights up.", "layers", VIS_B),
    # الميزة 3: القطط عوائق يلتف حولها BFS
    ("Cats = obstacles", "BFS routes around them, so the shortest safe path can be a detour.", "cat", RED),
    # الميزة 4: زر الخطوة الواحدة لشرح الخوارزمية
    ("Step BFS", "One press = one BFS step: perfect for explaining the algorithm.", "step", GOLD),
    # الميزة 5: التلميح (BFS من مكان اللاعب)
    ("Hint", "Runs BFS from where you stand and shows the way.", "hint", FRONTIER),
    # الميزة 6: النجوم والإعدادات
    ("Stars and settings", "Efficiency stars, 3 maze sizes, 3 speeds, cats on or off.", "star", (180, 150, 230)),
]


# دالة s_title ترسم شريحة العنوان
def s_title(d, t, i):
    # نثبّت الوقت حتى تظهر الشريحة كاملة بدون حركة ظهور
    t = 999
    # نرسم خلفية طبقات BFS الثابتة (بدون حركة)
    ripple(d.tick)
    # نرسم اللوحة البيضاء خلف النص
    screen.blit(title_panel(), (110, 140))
    # نرسم الفأر
    draw_mouse(195, 300, 26)
    # ونرسم الجبنة
    draw_cheese(805, 300, 24, 0)
    # نكتب عنوان المشروع الكبير
    draw_text(F_TITLE, "MAZE SOLVING", W // 2, 170, ACCENT, appear(t, 5), center=True)
    # نكتب العنوان الفرعي
    draw_text(F_BIG, "with Breadth-First Search (BFS)", W // 2, 262, INK, appear(t, 18), center=True)
    # نحسب تقدم ظهور الخط الذهبي
    k = appear(t, 30)
    # نرسم الخط الذهبي يتوسع من المنتصف
    pygame.draw.rect(screen, GOLD, (W // 2 - int(120 * k), 328, int(240 * k), 4), border_radius=2)
    # نكتب عدد أعضاء الفريق
    draw_text(F_BTN, f"A team of {len(TEAM)} students", W // 2, 355, (150, 92, 148), appear(t, 40), center=True)
    # نكتب اسم المشرفة
    draw_text(F_TXT, SUPERVISOR, W // 2, 402, DIM, appear(t, 50), center=True)
    # نكتب المادة والجامعة
    draw_text(F_TXT, COURSE, W // 2, 436, DIM, appear(t, 58), center=True)
    # نكتب "اضغط للبدء" بلون ثابت (بدون وميض)
    draw_text(F_SMALL, "Press  ->  or click to start", W // 2, 492,
              ACCENT, appear(t, 70), center=True)


# دالة fit تقصّ النص إذا كان أطول من المكان المخصص له
def fit(font, s, width):
    # إذا النص يكفي
    if font.size(s)[0] <= width:
        # نرجعه كما هو
        return s
    # وإلا نحذف حرفاً حرفاً حتى يكفي
    while s and font.size(s + "..")[0] > width:
        # نحذف آخر حرف
        s = s[:-1]
    # ونضيف نقطتين للدلالة على القص
    return s + ".."


# دالة s_team ترسم شريحة فريق العمل
def s_team(d, t, i):
    # نرسم إطار الشريحة والعنوان
    frame(d, "Our Team", t)
    # عدد أعضاء الفريق
    n = len(TEAM)
    # نحسب عدد الصفوف (3 بطاقات بكل صف)
    rows = (n + 2) // 3
    # المسافة بين البطاقات
    gap = 16
    # نحسب ارتفاع البطاقة بحيث تتسع كل الصفوف
    h = min(120, (520 - (rows - 1) * gap) // rows)
    # ألوان البطاقات المتناوبة
    cols = (FRONTIER, GOLD, GREEN, RED, (180, 150, 230))
    # نمر على كل عضو (الاسم والصفة)
    for k, (name, role) in enumerate(TEAM):
        # نحسب مكان بطاقته وتأخير ظهورها
        x, y, delay = 45 + (k % 3) * 310, 105 + (k // 3) * (h + gap), 6 + k * 6
        # نرسم البطاقة
        card_box(x, y, 290, h, cols[k % len(cols)], t, delay)
        # نحسب تقدم ظهور النص
        a = appear(t, delay + 8)
        # نكتب اسم العضو
        draw_text(F_TXT, fit(F_TXT, name, 262), x + 145, y + h // 2 - 24, INK, a, center=True)
        # ونكتب صفته تحت الاسم
        draw_text(F_SMALL, fit(F_SMALL, role, 262), x + 145, y + h // 2 + 8, DIM, a, center=True)


# دالة s_problem ترسم شريحة المشكلة
def s_problem(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "The Problem", t)
    # نكتب السؤال الرئيسي
    draw_para(F_BTN, "How can a program find the way out of a maze - and be sure the path "
                     "it found is the SHORTEST?", 60, 115, 880, INK, appear(t, 10), 36)
    # نكتب أن الفكرة تُستخدم بأماكن كثيرة
    draw_text(F_TXT, "The same idea is used everywhere:", 60, 250, ACCENT, appear(t, 40))
    # قائمة التطبيقات الأربعة (الاسم والوصف والأيقونة واللون)
    cards = [("GPS and Maps", "Shortest route between two places.", "gps", FRONTIER),
             # التطبيق 2: ألعاب الكمبيوتر (الذكاء الاصطناعي)
             ("Game AI", "Characters find paths across the map.", "mouse", GREEN),
             # التطبيق 3: الروبوتات
             ("Robots", "A robot plans a route through a room.", "robot", GOLD),
             # التطبيق 4: الشبكات
             ("Networks", "Data hops through the fewest routers.", "net", (180, 150, 230))]
    # نمر على كل تطبيق
    for k, (title, body, ic, col) in enumerate(cards):
        # نحسب مكان بطاقته وتأخير ظهورها
        x, y, delay = 60 + k * 225, 295, 55 + k * 12
        # نرسم البطاقة
        card_box(x, y, 205, 230, col, t, delay)
        # نحسب تقدم ظهور المحتوى
        a = appear(t, delay + 8)
        # إذا بدأ بالظهور
        if a > 0:
            # نرسم الأيقونة
            icon(ic, x + 102, y + 70)
            # نكتب العنوان
            draw_text(F_BTN, title, x + 102, y + 112, INK, a, center=True)
            # ونكتب الوصف
            draw_para(F_SMALL, body, x + 16, y + 154, 175, DIM, a, 22)


# دالة s_graph ترسم شريحة "المتاهة = graph"
def s_graph(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "A Maze Is a Graph", t)
    # حجم الخلية ومكان رسم المتاهة
    cs, oy = 44, 130
    # ننشئ متاهة صغيرة (مرة واحدة)
    m = d.obj(i, "m", lambda: Demo(False, 11, 7, cs, 60, oy))
    # نحسب كل الحواف (كل ممر مفتوح بين خليتين) مرة واحدة
    edges = d.obj(i, "e", lambda: sorted((a, b) for a in m.walls
                                         for b in open_neighbors(m.walls, a) if a < b))
    # نرسم خلفية المتاهة
    pygame.draw.rect(screen, (255, 252, 254), (60, oy, cs * 7, cs * 7), border_radius=6)
    # نرسم البداية والمخرج
    draw_markers(m.start, m.end, 60, oy, cs)
    # نرسم الجدران
    draw_walls(m.walls, 60, oy, cs)
    # نحسب تقدم ظهور السهم
    a = appear(t, 25)
    # إذا بدأ بالظهور
    if a > 0:
        # نرسم سهماً ذهبياً بين الرسمين
        pygame.draw.polygon(screen, GOLD, [(410, 285), (450, 285), (450, 268), (488, 300),
                                           (450, 332), (450, 315), (410, 315)])
    # مكان الرسم الثاني (الـ graph)
    ox = 520
    # نرسم خلفيته
    pygame.draw.rect(screen, (255, 252, 254), (ox, oy, cs * 7, cs * 7), border_radius=6)
    # بعد ثانية تقريباً
    if t > 35:
        # نرسم الحواف تدريجياً
        for p, q in edges[:int((t - 35) * 1.6)]:
            # نرسم الحافة كخط بين مركزي خليتين
            pygame.draw.line(screen, (214, 170, 200), cell_center(p, ox, oy, cs),
                             cell_center(q, ox, oy, cs), 3)
        # ثم نرسم العقد
        for cell in m.walls:
            # لون العقدة: أخضر للبداية وأحمر للمخرج وسماوي للباقي
            col = GREEN if cell == m.start else RED if cell == m.end else FRONTIER
            # نرسم العقدة كدائرة
            pygame.draw.circle(screen, col, cell_center(cell, ox, oy, cs), 9 if col != FRONTIER else 6)
    # نكتب تعليق الرسم الأول
    draw_text(F_SMALL, "The maze (walls)", 60, 450, DIM, appear(t, 10))
    # ونكتب تعليق الرسم الثاني
    draw_text(F_SMALL, "The same maze as a graph", ox, 450, DIM, appear(t, 40))
    # نصوص البطاقات الصغيرة (عدد العقد V وعدد الحواف E)
    chips = [f"Cell = Node   (V = {len(m.walls)})", f"Open passage = Edge   (E = {len(edges)})",
             "Neighbors = connected nodes"]
    # نمر على النصوص الثلاثة
    for k, txt in enumerate(chips):
        # نحسب مكان البطاقة
        x, y = 50 + k * 305, 495
        # نرسم البطاقة
        card_box(x, y, 290, 70, (GOLD, FRONTIER, GREEN)[k], t, 70 + k * 12)
        # نكتب النص داخلها
        draw_text(F_SMALL, txt, x + 145, y + 28, INK, appear(t, 80 + k * 12), center=True)


# دالة s_bfs ترسم شريحة "ما هو BFS"
def s_bfs(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "What Is BFS?", t)
    # ننشئ المتاهة التوضيحية (مرة واحدة)
    demo = d.obj(i, "demo", lambda: Demo(False, 3))
    # نحرّكها خطوة
    demo.update()
    # ونرسمها
    demo.draw()
    # نكتب الشرح على اليمين
    draw_items(ITEMS_BFS, 440, 115, 520, t)


# دالة s_queue ترسم شريحة "الطابور"
def s_queue(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "How BFS Works: the Queue", t)
    # ننشئ متاهة توضيحية أخرى
    demo = d.obj(i, "demo", lambda: Demo(False, 8))
    # نحرّكها
    demo.update()
    # ونرسمها
    demo.draw()
    # نكتب خطوات الخوارزمية على اليمين
    draw_items(ITEMS_QUEUE, 440, 115, 520, t)


# دالة s_trace ترسم شريحة "BFS بالإيد" (مثال صغير بجدول)
def s_trace(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "BFS by Hand: a Small Example", t)
    # نجلب الخطوات المسجلة والمسار
    steps, path = TRACE
    # نحسب أي خطوة نعرضها الآن (كل 1.25 ثانية خطوة)
    k = min(len(steps) - 1, int(t // 75))
    # نأخذ بيانات هذه الخطوة: العنصر الحالي والطابور والمزورين
    cur, queue, seen = steps[k]
    # هل وصلنا للخطوة الأخيرة؟
    final = k == len(steps) - 1
    # نمر على كل حافة بالرسم
    for a, b in G_EDGES:
        # هل الحافة جزء من المسار النهائي؟
        on = final and a in path and b in path and abs(path.index(a) - path.index(b)) == 1
        # نرسمها (ذهبية وسميكة إذا كانت من المسار)
        pygame.draw.line(screen, GOLD if on else (214, 170, 200), G_POS[a], G_POS[b], 6 if on else 3)
    # نمر على العقد
    for name, pos in G_POS.items():
        # إذا هذي العقدة هي الحالية (التي خرجت من الطابور)
        if name == cur:
            # نلونها ذهبياً
            col = GOLD
        # وإذا هي داخل الطابور
        elif name in queue:
            # نلونها سماوياً
            col = FRONTIER
        # وإذا زرناها سابقاً
        elif name in seen:
            # نلونها بنفسجياً
            col = VIS_B
        # وإلا (ما وصلنا لها بعد)
        else:
            # نلونها رمادياً وردياً فاتحاً
            col = (238, 228, 236)
        # نرسم ظل العقدة
        pygame.draw.circle(screen, (232, 196, 212), (pos[0], pos[1] + 4), 26)
        # نرسم جسم العقدة بلونها
        pygame.draw.circle(screen, col, pos, 25)
        # نرسم إطارها الغامق
        pygame.draw.circle(screen, INK, pos, 25, 2)
        # نحوّل حرف العقدة إلى صورة
        img = F_BTN.render(name, True, (74, 46, 84) if col in (GOLD, FRONTIER) else INK)
        # ونرسمه بمنتصف العقدة
        screen.blit(img, (pos[0] - img.get_width() // 2, pos[1] - img.get_height() // 2))
    # نحدد بداية الجدول على اليمين
    x0 = 560
    # مواقع الأعمدة الأربعة بالجدول
    cols = [x0, x0 + 55, x0 + 125, x0 + 245]
    # نكتب عناوين الأعمدة: الخطوة، الخارج، الطابور، المزورة
    for cx_, h in zip(cols, ("Step", "Out", "Queue", "Visited")):
        # نكتب العنوان بلون ذهبي
        draw_text(F_SMALL, h, cx_, 118, ACCENT, appear(t, 5))
    # نرسم خطاً تحت العناوين
    pygame.draw.line(screen, (240, 170, 200), (x0 - 10, 145), (W - 40, 145), 2)
    # نمر على كل خطوة حتى الخطوة الحالية
    for r in range(k + 1):
        # نجلب بيانات الخطوة ونحسب مكان صفها
        st, y = steps[r], 155 + r * 38
        # إذا هذا الصف هو الحالي
        if r == k:
            # نرسم خلفية مميزة له
            pygame.draw.rect(screen, (252, 222, 236), (x0 - 12, y - 4, W - 40 - (x0 - 12), 34), border_radius=8)
        # نجهز قيم الصف: رقم الخطوة والعنصر الخارج والطابور والمزورين
        vals = [str(r), st[0], " ".join(st[1]) or "-", " ".join(st[2])]
        # نمر على كل خانة
        for cx_, v in zip(cols, vals):
            # نكتبها (الصف الحالي غامق والباقي خافت)
            draw_text(F_TXT, v, cx_, y, INK if r == k else DIM)
    # إذا بالخطوة الأولى
    if k == 0:
        # نشرح أن A دخلت الطابور
        msg = "Start: put A (the start) in the queue."
    # وإذا بالخطوة الأخيرة
    elif final:
        # نشرح أننا وصلنا للمخرج ونتتبع روابط "من أين جاء" للخلف
        msg = ("G leaves the queue: the exit is reached! Follow the 'came from' links back: "
               + " -> ".join(path) + f"  ({len(path) - 1} steps).")
    # وإلا
    else:
        # نشرح الخطوة العادية: العنصر الخارج من مقدمة الطابور وإضافة جيرانه للنهاية
        msg = f"Take {cur} out of the queue (the front). Add its new neighbors to the back."
    # نكتب جملة الشرح
    draw_para(F_BODY, msg, 60, 500, 450, INK, 1.0, 27)
    # نرسم دليل الألوان: الحالي والموجود بالطابور والمزور
    for n_, (lab, col) in enumerate((("current", GOLD), ("in queue", FRONTIER), ("visited", VIS_B))):
        # نرسم دائرة اللون
        pygame.draw.circle(screen, col, (70 + n_ * 130, 600), 9)
        # ونكتب اسمه بجانبها
        screen.blit(F_SMALL.render(lab, True, DIM), (86 + n_ * 130, 590))


# دالة s_layers ترسم شريحة "ليش أقصر طريق" مع الرسم البياني
def s_layers(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "Why Is It the Shortest Path?", t)
    # نحسب بيانات الأعمدة (مرة واحدة) من متاهة حقيقية
    bins, binsize, exit_d = d.obj(i, "L", make_layers)
    # ثلاث بطاقات تشرح السبب (الاسم والنص واللون)
    cards = [("Distance order", "BFS handles all cells at distance d before any cell at d + 1.", FRONTIER),
             # البطاقة 2: أول وصول للمخرج = أقصر طريق
             ("First arrival wins", "The first time the exit comes out of the queue, no shorter path exists.", GOLD),
             # البطاقة 3: التعقيد O(V + E)
             ("Cost: O(V + E)", "Every cell and passage is checked once. Memory: O(V).", GREEN)]
    # نمر على البطاقات
    for k, (title, body, col) in enumerate(cards):
        # نحسب مكان البطاقة وتأخير ظهورها
        x, y, delay = 60 + k * 300, 100, 8 + k * 10
        # نرسم البطاقة
        card_box(x, y, 280, 135, col, t, delay)
        # نحسب تقدم ظهور النص
        a = appear(t, delay + 8)
        # نكتب عنوان البطاقة
        draw_text(F_BTN, title, x + 18, y + 22, INK, a)
        # ونكتب شرحها
        draw_para(F_SMALL, body, x + 18, y + 62, 245, DIM, a, 21)
    # نكتب عنوان الرسم البياني
    draw_text(F_SMALL, "Cells discovered at each distance from the start (a real 20 x 20 maze)",
              60, 250, DIM, appear(t, 40))
    # نحدد مكان وحجم الرسم البياني
    x0, base, maxh, width = 80, 585, 240, 840
    # نحسب عرض العمود وأعلى قيمة
    bw, peak = width / len(bins), max(bins)
    # نمر على كل عمود
    for b, count in enumerate(bins):
        # نحسب ارتفاعه (ينمو تدريجياً مع الوقت)
        h = int(maxh * count / peak * appear(t, 50 + b * 1.5, 22))
        # إذا ما بدأ بالظهور
        if h < 1:
            # نتخطاه
            continue
        # نلوّنه (متدرج قبل المخرج ورمادي بعده)
        col = lerp(VIS_A, VIS_B, b / len(bins)) if b * binsize <= exit_d else (236, 224, 232)
        # نرسم العمود
        pygame.draw.rect(screen, col, (int(x0 + b * bw) + 1, base - h, max(1, int(bw) - 2), h))
    # نرسم خط القاعدة
    pygame.draw.line(screen, DIM, (x0, base), (x0 + width, base), 2)
    # نحسب مكان خط المخرج الأحمر
    mx = int(x0 + (exit_d / binsize + .5) * bw)
    # بعد حوالي ثانيتين
    if t > 130:
        # نرسم خطاً أحمر متقطعاً عند المخرج
        for y in range(base - maxh - 10, base, 14):
            # كل قطعة من الخط
            pygame.draw.line(screen, RED, (mx, y), (mx, y + 8), 3)
        # نكتب "وجدنا المخرج عند البُعد كذا"
        draw_text(F_SMALL, f"Exit found at distance {exit_d}", min(max(mx, 160), W - 160),
                  base - maxh - 36, (200, 48, 78), appear(t, 130), center=True)
    # نكتب كلمة start أسفل يسار الرسم
    draw_text(F_SMALL, "start", x0, base + 8, DIM)
    # ونكتب كلمة "أبعد عن البداية" أسفل يمينه
    draw_text(F_SMALL, "farther from the start  ->", x0 + width - 190, base + 8, DIM)


# دالة s_results ترسم شريحة "النتائج المقاسة"
def s_results(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "Measured Results", t)
    # نجلب نتائج القياس الحقيقية
    rows = compute_results()
    # نكتب أن القياس بكود اللعبة نفسها على 25 متاهة
    draw_text(F_SMALL, "Measured live on 25 random mazes per size, using the game's own BFS code.",
              60, 98, DIM, appear(t, 5))
    # مواقع أعمدة الجدول
    xs = [80, 230, 390, 600, 800]
    # نكتب عناوين الجدول
    for hx, h in zip(xs, ("Maze", "Cells (V)", "Explored (avg)", "Shortest path (avg)", "BFS time (avg)")):
        # نكتب العنوان
        draw_text(F_SMALL, h, hx, 138, ACCENT, appear(t, 10))
    # نمر على صف النتائج لكل حجم
    for r, (n, V, ex, pl, tm) in enumerate(rows):
        # نحسب تقدم ظهور الصف ومكانه
        a, y = appear(t, 20 + r * 12), 168 + r * 46
        # إذا بدأ بالظهور
        if a > 0:
            # نرسم خلفية الصف
            pygame.draw.rect(screen, (255, 255, 255), (60, y, 880, 38), border_radius=10)
            # نجهز النصوص: الحجم وعدد الخلايا والمستكشف ومتوسط المسار والزمن
            vals = [f"{n} x {n}", str(V), f"{ex:.0f}", f"{pl:.0f} steps", f"{tm:.2f} ms"]
            # نمر على الخانات
            for hx, v in zip(xs, vals):
                # نكتب كل خانة
                draw_text(F_TXT, v, hx, y + 6, INK, a)
    # نكتب سؤال الأعمدة السفلية
    draw_text(F_BTN, "How much of the maze does BFS explore before it finds the exit?", 60, 335,
              INK, appear(t, 60))
    # نمر على الأحجام الثلاثة للأعمدة الأفقية
    for r, (n, V, ex, pl, tm) in enumerate(rows):
        # نحسب مكان العمود وتقدم ظهوره
        y, a = 395 + r * 60, appear(t, 70 + r * 14, 40)
        # نكتب حجم المتاهة بجانبه
        draw_text(F_TXT, f"{n} x {n}", 60, y + 4, DIM, appear(t, 70 + r * 14))
        # نرسم خلفية العمود
        pygame.draw.rect(screen, (255, 255, 255), (170, y, 520, 34), border_radius=10)
        # نحسب طول العمود (نسبة الخلايا المستكشفة من كل الخلايا)
        wbar = int(520 * (ex / V) * a)
        # إذا العمود ظاهر
        if wbar > 4:
            # نرسمه ملوّناً
            pygame.draw.rect(screen, lerp(VIS_A, VIS_B, r / 2), (170, y, wbar, 34), border_radius=10)
        # نكتب النسبة المئوية وعدد الخلايا
        draw_text(F_TXT, f"{ex / V * 100:.0f}%  ({ex:.0f} of {V} cells)", 702, y + 4, INK, a)
    # نكتب ملاحظة أن BFS يزور كل خلية مرة واحدة: O(V+E)
    draw_text(F_BODY, "In the worst case BFS visits each cell once: time O(V + E).", 60, 585,
              ACCENT, appear(t, 110))


# دالة s_design ترسم شريحة "كيف بنينا اللعبة"
def s_design(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "How We Built the Game", t)
    # خطوات بناء اللعبة الخمس (الاسم والوصف واللون)
    steps = [("Generate", "Prim's algorithm + extra openings (loops).", FRONTIER),
             # الخطوة 2: وضع القطط كعوائق
             ("Place cats", "Cats are obstacles; a safe route must exist.", RED),
             # الخطوة 3: حركة اللاعب بين الخلايا المجاورة
             ("Player moves", "The mouse moves between neighboring cells.", GREEN),
             # الخطوة 4: حل المتاهة بـ BFS
             ("BFS solver", "Queue + 'came from' links = shortest safe path.", GOLD),
             # الخطوة 5: حساب النقاط بمقارنة خطوات اللاعب بـ BFS
             ("Score", "Your steps vs BFS = stars.", (180, 150, 230))]
    # نمر على كل خطوة
    for k, (title, body, col) in enumerate(steps):
        # نحسب مكان البطاقة وتأخير ظهورها
        x, y, delay = 40 + k * 188, 110, 8 + k * 14
        # نرسم البطاقة
        card_box(x, y, 168, 230, col, t, delay)
        # نحسب تقدم ظهور المحتوى
        a = appear(t, delay + 8)
        # إذا بدأ بالظهور
        if a > 0:
            # مركز البطاقة الأفقي
            cx_ = x + 84
            # نرسم دائرة الرقم
            pygame.draw.circle(screen, col, (cx_, y + 52), 24)
            # نكتب رقم الخطوة
            draw_text(F_BTN, str(k + 1), cx_, y + 37, (74, 46, 84), a, center=True)
            # نكتب اسم الخطوة
            draw_text(F_TXT, title, cx_, y + 90, INK, a, center=True)
            # نكتب وصفها
            draw_para(F_SMALL, body, x + 12, y + 126, 144, DIM, a, 20)
            # إذا ليست الخطوة الأخيرة
            if k < 4:
                # نرسم سهماً صغيراً للخطوة التالية
                pygame.draw.polygon(screen, GOLD, [(x + 172, y + 44), (x + 185, y + 52), (x + 172, y + 60)])
    # نكتب عنوان "هياكل البيانات التي استخدمناها"
    draw_text(F_BTN, "Data structures we used", 40, 372, ACCENT, appear(t, 80))
    # هياكل البيانات الأربعة: dict للمتاهة وdeque للطابور وdict للأهل وset للقطط
    chips = [("dict  walls", "the graph: cells and open passages", FRONTIER),
             # الهيكل 2: deque للطابور
             ("deque", "the BFS queue (First In, First Out)", GOLD),
             # الهيكل 3: dict لروابط "من أين جاء"
             ("dict  parent", "'came from' links to rebuild the path", GREEN),
             # الهيكل 4: set للخلايا الممنوعة (القطط)
             ("set  cats", "blocked cells that BFS must skip", RED)]
    # نمر على الهياكل
    for k, (name, desc, col) in enumerate(chips):
        # نحسب مكان البطاقة وتأخير ظهورها
        x, y, delay = 40 + (k % 2) * 460, 418 + (k // 2) * 78, 90 + k * 10
        # نرسم البطاقة
        card_box(x, y, 440, 64, (255, 255, 255), t, delay)
        # نحسب تقدم ظهور المحتوى
        a = appear(t, delay + 6)
        # إذا بدأ بالظهور
        if a > 0:
            # نرسم الشريط الملوّن على جانب البطاقة
            pygame.draw.rect(screen, col, (x, y, 8, 64), border_top_left_radius=18, border_bottom_left_radius=18)
            # نكتب اسم الهيكل
            draw_text(F_TXT, name, x + 24, y + 6, INK, a)
            # ونكتب وظيفته
            draw_text(F_SMALL, desc, x + 24, y + 36, DIM, a)


# دالة s_features ترسم شريحة "مزايا اللعبة"
def s_features(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "Game Features", t)
    # نمر على المزايا الست
    for k, (title, body, ic, col) in enumerate(FEATURES):
        # نحسب مكان البطاقة (3 بكل صف) وتأخير ظهورها
        x, y, delay = 45 + (k % 3) * 310, 110 + (k // 3) * 230, 8 + k * 10
        # نرسم البطاقة
        card_box(x, y, 290, 215, col, t, delay)
        # نحسب تقدم ظهور المحتوى
        a = appear(t, delay + 8)
        # إذا بدأ بالظهور
        if a > 0:
            # نرسم الأيقونة
            icon(ic, x + 145, y + 62)
            # نكتب اسم الميزة
            draw_text(F_BTN, title, x + 145, y + 105, INK, a, center=True)
            # ونكتب وصفها
            draw_para(F_SMALL, body, x + 16, y + 142, 258, DIM, a, 21)


# دالة s_live ترسم شريحة "العرض الحي" (BFS حول القطط)
def s_live(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "Live Demo: BFS Around the Cats", t)
    # ننشئ متاهة العرض (فيها 4 قطط)
    demo = d.obj(i, "demo", lambda: Demo(True, 21, 9, 40, 50, 100, 4))
    # نحرّكها خطوة
    demo.update()
    # ونرسمها
    demo.draw()
    # نختصر اسم البحث ونحدد مكان الكلام على اليمين
    b, x = demo.bfs, 500
    # نكتب عنوان "شاهدي البحث"
    draw_text(F_BTN, "Watch the search", x, 108, ACCENT, appear(t, 10))
    # نجهز إحصائيات حية: الخلايا المستكشفة وحجم الطابور وطول المسار الآمن
    stats = [("Cells explored", str(b.explored)),
             # الإحصائية 2: حجم الطابور
             ("Queue size", "0" if b.done else str(len(b.q))),
             # الإحصائية 3: طول أقصر مسار آمن
             ("Shortest safe path", str(len(b.path) - 1) if b.done and b.path else "...")]
    # نمر على الإحصائيات
    for k, (lab, val) in enumerate(stats):
        # نحسب تقدم ظهورها
        a = appear(t, 20 + k * 10)
        # نكتب اسم الإحصائية
        draw_text(F_SMALL, lab, x, 155 + k * 62, DIM, a)
        # نكتب قيمتها بخط كبير
        draw_text(F_BIG, val, x, 175 + k * 62, INK, a)
    # نكتب ثلاث نقاط تشرح ما يحدث
    draw_items([("b", "Red cats are obstacles: BFS never enters them."),
                # النقطة 2: BFS يلتف حول القطط
                ("b", "If a cat blocks the shortest route, BFS finds the detour."),
                # النقطة 3: المسار الذهبي هو الأقصر الآمن
                ("b", "The gold path is the shortest SAFE path.")], x, 355, 440, t, 40)
    # نحسب تقدم ظهور زر "اضغط P"
    a = appear(t, 90)
    # إذا بدأ بالظهور
    if a > 0:
        # نرسم الصندوق الذهبي
        pygame.draw.rect(screen, GOLD, (x, 540, 440, 56), border_radius=16)
        # نكتب "اضغط P للعب"
        draw_text(F_BTN, "Press  P  to play the game now", x + 220, 551, (74, 46, 84), a, center=True)


# دالة s_future ترسم شريحة الخلاصة والتطوير المستقبلي
def s_future(d, t, i):
    # نرسم الإطار والعنوان
    frame(d, "Conclusion and Future Work", t)
    # قائمة ما تعلمناه
    learned = ["A maze is naturally a graph: cells are nodes, passages are edges.",
               # النقطة 2: الطابور يجعل البحث طبقة بعد طبقة
               "A queue (FIFO) makes the search go level by level.",
               # النقطة 3: أول مسار يجده BFS هو الأقصر
               "With equal step costs, the first path BFS finds is the shortest.",
               # النقطة 4: العوائق سهلة (نتخطى الخلايا الممنوعة)
               "Obstacles are easy: BFS just skips blocked cells."]
    # قائمة التطوير المستقبلي
    future = ["Weighted terrain (mud, water): use Dijkstra's algorithm.",
              # الفكرة 2: خوارزمية A* تستكشف خلايا أقل
              "A* search: a heuristic explores fewer cells.",
              # الفكرة 3: عدة مخارج أو قطط متحركة
              "Several exits or moving cats.",
              # الفكرة 4: متاهات أكبر ونسخة ويب أو موبايل
              "Bigger mazes and a web or mobile version."]
    # نمر على بطاقتين: ما تعلمناه والتطوير
    for ci, (title, col, items) in enumerate((("What we learned", GREEN, learned),
                                              ("Future work", FRONTIER, future))):
        # نحسب مكان البطاقة
        x = 45 + ci * 460
        # نرسم البطاقة
        card_box(x, 110, 430, 440, col, t, 5 + ci * 10)
        # نكتب عنوانها
        draw_text(F_BTN, title, x + 24, 140, INK, appear(t, 15 + ci * 10))
        # نبدأ كتابة النقاط من الأعلى
        y = 195
        # نمر على كل نقطة
        for k, txt in enumerate(items):
            # نحسب تقدم ظهورها
            a = appear(t, 30 + ci * 10 + k * 14)
            # إذا بدأت بالظهور
            if a > 0:
                # نرسم نقطة دائرية قبل النص
                pygame.draw.circle(screen, col, (x + 36, y + 13), 6)
            # نكتب النقطة وننزل لما بعدها
            y = draw_para(F_BODY, txt, x + 56, y, 350, INK, a, 27) + 18


# دالة s_thanks ترسم شريحة الشكر والأسئلة
def s_thanks(d, t, i):
    # نثبّت الوقت حتى تظهر الشريحة كاملة بدون حركة ظهور
    t = 999
    # نرسم خلفية طبقات BFS الثابتة (بدون حركة)
    ripple(d.tick)
    # نرسم اللوحة البيضاء
    screen.blit(title_panel(), (110, 140))
    # نرسم الفأر
    draw_mouse(195, 300, 26)
    # ونرسم الجبنة
    draw_cheese(805, 300, 24, 0)
    # نكتب "شكراً لكم"
    draw_text(F_TITLE, "Thank You!", W // 2, 175, ACCENT, appear(t, 5), center=True)
    # نكتب "أي أسئلة؟"
    draw_text(F_BIG, "Questions?", W // 2, 270, INK, appear(t, 20), center=True)
    # نحسب تقدم الخط الذهبي
    k = appear(t, 30)
    # نرسم الخط الذهبي
    pygame.draw.rect(screen, GOLD, (W // 2 - int(120 * k), 335, int(240 * k), 4), border_radius=2)
    # نكتب عدد أعضاء الفريق
    draw_text(F_BTN, f"A team of {len(TEAM)} students", W // 2, 365, (150, 92, 148), appear(t, 40), center=True)
    # نكتب اسم المشرفة
    draw_text(F_TXT, SUPERVISOR, W // 2, 410, DIM, appear(t, 50), center=True)
    # نكتب تعليمات اللعب والخروج
    draw_text(F_SMALL, "Press  P  to play the game      Esc for the menu", W // 2, 480,
              ACCENT, appear(t, 65), center=True)


# قائمة الشرائح بالترتيب الذي تظهر به
SLIDES = [s_title, s_team, s_problem, s_graph, s_bfs, s_queue, s_trace, s_layers, s_results,
          s_design, s_features, s_live, s_future, s_thanks]


# دالة render_to ترسم شريحة على سطح آخر (لتأثير انزلاق الشرائح)
def render_to(target, fn, *args):
    """Run a drawing function on another surface (used for slide transitions)."""
    # نسمح بتغيير متغير الشاشة الأساسي
    global screen
    # نحفظ الشاشة الأصلية
    saved = screen
    # نجعل الرسم يذهب للسطح الجديد
    screen = target
    # نجرّب الرسم
    try:
        # ننفذ دالة رسم الشريحة
        fn(*args)
    # وبكل الأحوال
    finally:
        # نرجع الشاشة الأصلية
        screen = saved


# كلاس Deck يدير العرض: التنقل بين الشرائح وانتقالاتها وأسفل الصفحة
class Deck:
    """The presentation: slide navigation, slide-in transitions, footer."""

    # دالة البناء: تجهز العرض
    def __init__(self):
        # نقيس نتائج BFS مرة واحدة (تختفي بالتعتيم عند الدخول)
        compute_results()                   # measure once (hidden by the fade)
        # رقم الشريحة الحالية والوقت منذ فتحها وعدّاد الإطارات
        self.idx, self.t, self.tick = 0, 0, 0
        # متغيرات انتقال الشرائح: السابقة وتقدم الانتقال والاتجاه
        self.old, self.old_t, self.trans, self.dir = 0, 0, 1.0, 1
        # قاموس لحفظ الأشياء الخاصة بكل شريحة
        self.objs = {}
        # سطح لرسم الشريحة السابقة
        self.surf_a = pygame.Surface((W, H))
        # وسطح لرسم الشريحة الجديدة
        self.surf_b = pygame.Surface((W, H))

    # دالة obj تنشئ كائن الشريحة مرة واحدة وتعيده كل مرة
    def obj(self, i, name, factory):
        # إذا ما أنشأناه بعد
        if (i, name) not in self.objs:
            # ننشئه ونخزنه
            self.objs[(i, name)] = factory()
        # نرجع الكائن المخزن
        return self.objs[(i, name)]

    # دالة goto تنتقل لشريحة معينة
    def goto(self, new):
        # نمنع الخروج عن عدد الشرائح
        new = max(0, min(len(SLIDES) - 1, new))
        # إذا هي نفس الشريحة
        if new == self.idx:
            # ما نسوي شي
            return
        # نحفظ الشريحة القديمة ووقتها لعرض انتقالها
        self.old, self.old_t = self.idx, self.t
        # نحدد اتجاه الانزلاق (للأمام أو للخلف)
        self.dir = 1 if new > self.idx else -1
        # نضبط الشريحة الجديدة ونبدأ الانتقال
        self.idx, self.t, self.trans = new, 0, 0.0
        # نمسح كائنات الشريحة الجديدة لتبدأ حركتها من جديد
        for k in [k for k in self.objs if k[0] == new]:
            # نحذف كل كائن
            del self.objs[k]

    # دالة render ترسم شريحة برقمها
    def render(self, i, t):
        # نستدعي دالة الشريحة المناسبة
        SLIDES[i](self, t, i)

    # دالة draw ترسم العرض كل إطار
    def draw(self):
        # نزيد عدّاد الإطارات العام
        self.tick += 1
        # ونزيد وقت الشريحة الحالية
        self.t += 1
        # إذا فيه انتقال جارٍ بين شريحتين
        if self.trans < 1:
            # نقدّم الانتقال شوي
            self.trans = min(1.0, self.trans + 0.05)
            # ونزيد وقت الشريحة القديمة
            self.old_t += 1
            # نحسب سلاسة الحركة
            e = ease(self.trans)
            # نرسم الشريحة القديمة على سطحها
            render_to(self.surf_a, self.render, self.old, self.old_t)
            # ونرسم الجديدة على سطحها
            render_to(self.surf_b, self.render, self.idx, self.t)
            # نزلق القديمة للخارج
            screen.blit(self.surf_a, (int(-self.dir * e * W), 0))
            # ونزلق الجديدة للداخل
            screen.blit(self.surf_b, (int(self.dir * (1 - e) * W), 0))
        # وإلا (لا انتقال)
        else:
            # نرسم الشريحة الحالية مباشرة
            self.render(self.idx, self.t)
        # عدد الشرائح الكلي
        n = len(SLIDES)
        # نرسم خلفية شريط التقدم أسفل الشاشة
        pygame.draw.rect(screen, (246, 214, 228), (0, H - 6, W, 6))
        # ونرسم الجزء المكتمل منه بالذهبي
        pygame.draw.rect(screen, GOLD, (0, H - 6, int(W * (self.idx + 1) / n), 6))
        # نكتب عنوان المشروع بالأسفل يسار
        screen.blit(F_SMALL.render(PROJECT_TITLE, True, (130, 92, 132)), (20, H - 32))
        # نجهز نص "رقم الشريحة" وتعليمات التنقل
        hint = f"{self.idx + 1} / {n}     click or arrows: navigate     F: full screen     Esc: menu"
        # نحوّله إلى صورة
        img = F_SMALL.render(hint, True, (130, 92, 132))
        # ونرسمه بالأسفل يمين
        screen.blit(img, (W - img.get_width() - 20, H - 32))


# =====================================================================
#  THE APP
# =====================================================================
# كلاس App هو برنامج اللعبة كله: القائمة والإعدادات واللعب والعرض
class App:
    # دالة البناء: تجهّز متغيرات البرنامج عند تشغيله
    def __init__(self):
        # المشهد الحالي: نبدأ بالقائمة
        self.scene = "menu"
        # المشهد التالي عند الانتقال
        self.next_scene = None
        # التعتيم: نبدأ معتماً ثم يظهر تدريجياً
        self.fade, self.fade_dir = 255, -1
        # الإعدادات: حجم المتاهة (المتوسط) وسرعة BFS (عادية) والقطط (مفعّلة)
        self.size_i, self.speed_i, self.cats_on = 1, 1, True
        # وضع اللعب: نلعب أو نشاهد BFS
        self.mode = "play"          # "play" or "watch"
        # عدّاد الإطارات
        self.tick = 0
        # نتيجة اللعبة الأخيرة
        self.result = ("win", 0, 0, 0)
        # هل نعيد نفس المتاهة عند الدخول للعبة؟
        self.keep_maze = False
        # كائن العرض التقديمي (يُنشأ عند فتحه)
        self.deck = None
        # قائمة الأزرار الحالية
        self.buttons = []
        # نبني أزرار المشهد الأول
        self.build()

    # ----- scene switching with fade -----
    # دالة go تبدأ الانتقال لمشهد آخر مع تعتيم
    def go(self, scene):
        # فقط إذا ما فيه انتقال جارٍ
        if self.fade_dir == 0:
            # نحفظ المشهد المطلوب ونبدأ التعتيم
            self.next_scene, self.fade_dir = scene, 1

    # دالة start_game تبدأ اللعب بنوع معين (لعب أو مشاهدة)
    def start_game(self, mode):
        # نحفظ نوع الوضع
        self.mode = mode
        # ننتقل لمشهد اللعبة
        self.go("game")

    # دالة retry تعيد المحاولة على نفس المتاهة
    def retry(self):
        # نسجل أننا نريد نفس المتاهة
        self.keep_maze = True
        # وننتقل لمشهد اللعبة
        self.go("game")

    # دالة present_key تتعامل مع أزرار الكيبورد داخل العرض التقديمي
    def present_key(self, key):
        # نختصر اسم كائن العرض بـ dk
        dk = self.deck
        # الأسهم اليمين أو المسافة أو Enter أو PageDown
        if key in (pygame.K_RIGHT, pygame.K_SPACE, pygame.K_RETURN, pygame.K_PAGEDOWN):
            # ننتقل للشريحة التالية
            dk.goto(dk.idx + 1)
        # السهم الأيسر أو Backspace أو PageUp
        elif key in (pygame.K_LEFT, pygame.K_BACKSPACE, pygame.K_PAGEUP):
            # ننتقل للشريحة السابقة
            dk.goto(dk.idx - 1)
        # زر Home
        elif key == pygame.K_HOME:
            # نذهب لأول شريحة
            dk.goto(0)
        # زر End
        elif key == pygame.K_END:
            # نذهب لآخر شريحة
            dk.goto(len(SLIDES) - 1)
        # زر F
        elif key == pygame.K_f:
            # نبدّل بين النافذة وملء الشاشة
            pygame.display.toggle_fullscreen()
        # زر P
        elif key == pygame.K_p:
            # نبدأ اللعبة مباشرة
            self.start_game("play")

    # دالة build تبني أزرار كل مشهد (قائمة، إعدادات، لعبة، نتيجة)
    def build(self):
        # نعرف المشهد الحالي ومنتصف الشاشة
        s, cx = self.scene, W // 2
        # نختصر اسم كلاس الزر بـ B
        B = Button
        # إذا المشهد هو القائمة الرئيسية
        if s == "menu":
            # نصنع قائمة أزرار القائمة
            self.buttons = [
                # زر اللعب: أنت ضد BFS
                B("Play  (You vs BFS)", cx, 300, 420, 58, lambda: self.start_game("play")),
                # زر مشاهدة BFS يحل المتاهة
                B("Watch BFS Solve", cx, 372, 420, 58, lambda: self.start_game("watch")),
                # زر العرض التقديمي (ما هو BFS)
                B("Presentation (What is BFS?)", cx, 444, 420, 58, lambda: self.go("present")),
                # زر الإعدادات
                B("Settings", cx, 516, 420, 58, lambda: self.go("settings")),
                # زر الخروج من البرنامج
                B("Quit", cx, 588, 420, 58, lambda: (pygame.quit(), sys.exit())),
            ]
        # وإذا المشهد هو الإعدادات
        elif s == "settings":
            # نصنع أزرار الإعدادات
            self.buttons = [
                # زر حجم المتاهة (يتغير نصه حسب الاختيار)
                B(lambda: f"Maze size:  {SIZES[self.size_i][0]}", cx, 290, 440, 60, self.cycle_size),
                # زر سرعة BFS
                B(lambda: f"BFS speed:  {SPEEDS[self.speed_i][0]}", cx, 370, 440, 60, self.cycle_speed),
                # زر تشغيل أو إيقاف القطط
                B(lambda: f"Cats (obstacles):  {'On' if self.cats_on else 'Off'}", cx, 450, 440, 60,
                  self.toggle_cats),
                # زر الرجوع للقائمة
                B("Back", cx, 560, 260, 58, lambda: self.go("menu")),
            ]
        # وإذا المشهد هو العرض التقديمي
        elif s == "present":
            # ما فيه أزرار (التنقل بالكيبورد والماوس)
            self.buttons = []
        # وإذا المشهد هو اللعبة
        elif s == "game":
            # مكان الأزرار على اليمين
            px = 850
            # أزرار اللعبة
            self.buttons = [
                # زر متاهة جديدة
                B("New Maze", px, 458, 220, 38, self.new_maze),
                # زر تشغيل BFS متحرك
                B("Run BFS", px, 500, 220, 38, self.run_bfs),
                # زر خطوة BFS واحدة
                B("Step BFS", px, 542, 220, 38, self.step_bfs),
                # زر التلميح
                B("Hint", px, 584, 220, 38, self.toggle_hint),
                # زر العودة للقائمة
                B("Menu", px, 626, 220, 38, lambda: self.go("menu")),
            ]
            # إذا طلبنا إعادة نفس المتاهة
            if self.keep_maze:
                # نلغي الطلب
                self.keep_maze = False
                # ونعيد اللاعب للبداية فقط
                self.reset_player()
            # وإلا
            else:
                # ننشئ متاهة جديدة
                self.new_maze()
        # وإذا المشهد هو النتيجة
        elif s == "result":
            # إذا ربح اللاعب
            if self.result[0] == "win":
                # أزرار شاشة الفوز
                self.buttons = [
                    # زر اللعب مرة ثانية
                    B("Play Again", cx, 470, 320, 58, lambda: self.start_game("play")),
                    # زر العودة للقائمة
                    B("Main Menu", cx, 545, 320, 58, lambda: self.go("menu")),
                ]
            # وإذا خسر (أكلته قطة)
            else:
                # أزرار شاشة الخسارة
                self.buttons = [
                    # زر إعادة المحاولة على نفس المتاهة
                    B("Retry (same maze)", cx, 440, 360, 58, self.retry),
                    # زر متاهة جديدة
                    B("New Maze", cx, 510, 360, 58, lambda: self.start_game("play")),
                    # زر القائمة
                    B("Main Menu", cx, 580, 360, 58, lambda: self.go("menu")),
                ]

    # دالة cycle_size تنتقل لحجم المتاهة التالي (صغير، متوسط، كبير ثم تعود للأول)
    def cycle_size(self):
        # نزيد الرقم ونعود للصفر عند النهاية (باقي القسمة %)
        self.size_i = (self.size_i + 1) % len(SIZES)

    # دالة cycle_speed تنتقل لسرعة BFS التالية
    def cycle_speed(self):
        # نفس الفكرة: نزيد الرقم ونعود للأول
        self.speed_i = (self.speed_i + 1) % len(SPEEDS)

    # دالة toggle_cats تشغّل القطط أو تطفيها
    def toggle_cats(self):
        # نعكس القيمة (صح تصير خطأ والعكس)
        self.cats_on = not self.cats_on

    # ----- game logic -----
    # دالة new_maze تنشئ متاهة جديدة وتجهز كل شي للعبة
    def new_maze(self):
        # نجلب حجم المتاهة المختار
        n = SIZES[self.size_i][1]
        # عدد الصفوف والأعمدة متساوي
        self.rows = self.cols = n
        # نولّد المتاهة بخوارزمية Prim
        self.walls, self.start, self.end = generate(n, n)
        # نحسب حجم الخلية بالبكسل (المتاهة تملأ 640 بكسل)
        self.cell = 640 // n
        # نحسب مكان بداية الرسم أفقياً (لتكون بالمنتصف)
        self.ox = 20 + (680 - self.cell * n) // 2
        # ومكانها عمودياً
        self.oy = 20 + (640 - self.cell * n) // 2
        # نحسب عدد القطط (70% من حجم الضلع) أو صفر إذا القطط مطفأة
        count = round(n * 0.7) if self.cats_on else 0
        # نضع القطط بالمتاهة
        self.cats = place_cats(self.walls, self.start, self.end, count)
        # نصنع هالة القطط الحمراء
        self.glow_red = make_glow(max(6, int(self.cell * 0.9)), (255, 120, 140))
        # ونصنع هالة الجبنة الذهبية
        self.glow_gold = make_glow(max(8, int(self.cell * 1.3)), (255, 215, 120))
        # نعيد اللاعب للبداية
        self.reset_player()
        # إذا الوضع مشاهدة
        if self.mode == "watch":
            # نشغّل BFS تلقائياً
            self.run_bfs()

    # دالة reset_player تعيد اللاعب لنقطة البداية وتصفّر كل شي
    def reset_player(self):
        # اللاعب عند خلية البداية
        self.player = self.start
        # الموقع المرئي للفأر (يتحرك بنعومة نحو الموقع الحقيقي)
        self.vis = [float(self.start[0]), float(self.start[1])]
        # سجل الخلايا التي مشى عليها
        self.trail = [self.start]
        # عدد الخطوات صفر
        self.steps = 0
        # لا يوجد بحث BFS شغّال
        self.solver, self.auto = None, False
        # نطفئ التلميح
        self.hint, self.hint_path = False, []

    # دالة run_bfs تبدأ بحث BFS متحرك من البداية
    def run_bfs(self):
        """Animated BFS from the start."""
        # ننشئ بحثاً جديداً (القطط ممنوعة عليه)
        self.solver = BFS(self.walls, self.start, self.end, self.cats)
        # ونجعله يتحرك تلقائياً
        self.auto = True

    # دالة step_bfs تنفذ خطوة BFS واحدة فقط (ممتازة للشرح)
    def step_bfs(self):
        """Advance BFS by exactly one step (great for explaining)."""
        # إذا ما في بحث أو انتهى
        if self.solver is None or self.solver.done:
            # نبدأ بحثاً جديداً
            self.solver = BFS(self.walls, self.start, self.end, self.cats)
        # نوقف الحركة التلقائية
        self.auto = False
        # ننفذ خطوة واحدة
        self.solver.step()

    # دالة toggle_hint تشغّل أو تطفي التلميح
    def toggle_hint(self):
        # نعكس حالة التلميح
        self.hint = not self.hint
        # ونحدّث مسار التلميح
        self.refresh_hint()

    # دالة refresh_hint تحسب مسار التلميح من مكان اللاعب الحالي
    def refresh_hint(self):
        # نشغّل BFS من مكان اللاعب (مع تجنب القطط) إذا التلميح شغّال وإلا القائمة فاضية
        self.hint_path = solve(self.walls, self.player, self.end, self.cats) if self.hint else []

    # دالة move تحرك اللاعب خطوة باتجاه معين
    def move(self, d):
        # إذا مو وضع اللعب أو يوجد جدار بهذا الاتجاه
        if self.mode != "play" or d in self.walls[self.player]:
            # نخرج ولا نتحرك
            return
        # نجلب تغيّر الصف والعمود للاتجاه
        dr, dc, _ = DIRS[d]
        # نحسب الخلية الجديدة
        n = (self.player[0] + dr, self.player[1] + dc)
        # إذا خارج المتاهة
        if n not in self.walls:
            # نخرج
            return
        # ننقل اللاعب للخلية الجديدة
        self.player = n
        # نسجلها بسجل المشي
        self.trail.append(n)
        # نزيد عدد الخطوات
        self.steps += 1
        # نحدّث التلميح
        self.refresh_hint()
        # إذا الخلية فيها قطة
        if n in self.cats:
            # نسجل خسارة اللاعب
            self.result = ("lose", self.steps, 0, 0)
            # وننتقل لشاشة النتيجة
            self.go("result")
        # وإذا الخلية هي المخرج
        elif n == self.end:
            # ننشئ بحث BFS مرجعي لنقارن به
            ref = BFS(self.walls, self.start, self.end, self.cats)
            # ونشغّله للنهاية
            ref.run_all()
            # نسجل الفوز: خطوات اللاعب وأقصر مسار آمن وعدد الخلايا التي استكشفها BFS
            self.result = ("win", self.steps, len(ref.path) - 1, ref.explored)
            # وننتقل لشاشة النتيجة
            self.go("result")

    # ----- drawing -----
    # دالة draw_game ترسم شاشة اللعبة كاملة
    def draw_game(self):
        # نجمع القيم: حجم الخلية ومكان الرسم والبحث الحالي
        cs, ox, oy, sv = self.cell, self.ox, self.oy, self.solver
        # نرسم خلفية المتاهة
        pygame.draw.rect(screen, (255, 252, 254), (ox, oy, cs * self.cols, cs * self.rows), border_radius=6)
        # نلوّن خلايا BFS
        draw_layers(sv, ox, oy, cs)
        # نرسم مربعي البداية والمخرج
        draw_markers(self.start, self.end, ox, oy, cs)
        # نجلب هالة القطط
        gl = self.glow_red
        # نجعل لمعانها ينبض مع الوقت
        gl.set_alpha(max(0, min(255, 170 + int(70 * math.sin(self.tick * 0.1)))))
        # نمر على القطط
        for cat in self.cats:
            # نحسب مكان القطة
            x, y = cell_center(cat, ox, oy, cs)
            # نرسم هالتها الحمراء
            screen.blit(gl, (int(x - gl.get_width() / 2), int(y - gl.get_height() / 2)))
        # نرسم الجدران
        draw_walls(self.walls, ox, oy, cs)
        # نمر على خلايا التلميح
        for p in self.hint_path:
            # نرسم نقطة غامقة على كل خلية
            pygame.draw.circle(screen, INK, cell_center(p, ox, oy, cs), max(2, int(cs * .12)))
        # نرسم المسار الذهبي إذا انتهى BFS
        draw_path(sv, ox, oy, cs, self.tick)
        # نمر على القطط مرة ثانية
        for cat in self.cats:
            # نحسب مكانها
            x, y = cell_center(cat, ox, oy, cs)
            # ونرسم القطة نفسها
            draw_cat(x, y, cs * .3)
        # نحسب مكان المخرج
        ex, ey = cell_center(self.end, ox, oy, cs)
        # ونرسم الجبنة
        draw_cheese(ex, ey, cs * .27, self.tick / 60, self.glow_gold)
        # إذا وضع اللعب
        if self.mode == "play":
            # نرسم آخر 40 خلية مشى عليها اللاعب
            for p in self.trail[-40:]:
                # كل خلية بنقطة وردية
                pygame.draw.circle(screen, (240, 120, 165), cell_center(p, ox, oy, cs), max(2, int(cs // 8)))
            # نحرك موقع الفأر المرئي قليلاً نحو موقعه الحقيقي (حركة ناعمة) للصفوف
            self.vis[0] += (self.player[0] - self.vis[0]) * 0.28   # smooth movement
            # وللأعمدة
            self.vis[1] += (self.player[1] - self.vis[1]) * 0.28
            # نحسب مكان الفأر على الشاشة
            mx, my = cell_center(self.vis, ox, oy, cs)
            # ونرسمه مع اهتزاز بسيط
            draw_mouse(mx, my + math.sin(self.tick * 0.3) * 1.5, cs * .3)
        # side panel
        # نرسم اللوحة الجانبية
        pygame.draw.rect(screen, (255, 255, 255), (725, 20, 250, 410), border_radius=16)
        # ونرسم إطارها
        pygame.draw.rect(screen, (240, 170, 200), (725, 20, 250, 410), 2, border_radius=16)
        # نكتب كلمة BFS أعلاها
        screen.blit(F_BIG.render("BFS", True, ACCENT), (750, 28))
        # نجهز الإحصائيات: الوضع وحجم المتاهة وعدد القطط
        lines = [("Mode", "You vs BFS" if self.mode == "play" else "Watching BFS"),
                 ("Maze", f"{self.rows}x{self.cols}  |  {len(self.cats)} cats")]
        # إذا وضع اللعب
        if self.mode == "play":
            # نضيف عدد خطوات اللاعب
            lines.append(("Your steps", str(self.steps)))
        # نضيف عدد الخلايا التي استكشفها BFS
        lines.append(("BFS explored", str(sv.explored) if sv else "-"))
        # نضيف حجم الطابور الحالي
        lines.append(("Queue size", str(len(sv.q)) if sv and not sv.done else "-"))
        # نضيف طول أقصر مسار آمن (بعد انتهاء BFS)
        lines.append(("Safe shortest path", str(len(sv.path) - 1) if sv and sv.done and sv.path else "-"))
        # نبدأ الكتابة من الأعلى
        y = 84
        # نمر على كل إحصائية
        for k, v in lines:
            # نكتب اسمها
            screen.blit(F_SMALL.render(k, True, DIM), (750, y))
            # ونكتب قيمتها بخط أكبر
            screen.blit(F_TXT.render(v, True, INK), (750, y + 19))
            # وننزل للسطر التالي
            y += 46
        # نجهز تعليمات التحكم حسب الوضع
        hints = (["Arrows/WASD: move", "H: hint   SPACE: run BFS", "ENTER: one BFS step"]
                 if self.mode == "play" else
                 ["SPACE: restart BFS", "ENTER: one BFS step", "N: new maze"])
        # نمر على التعليمات
        for i, h in enumerate(hints):
            # ونكتب كل تعليمة بأسفل اللوحة
            screen.blit(F_SMALL.render(h, True, DIM), (750, 366 + i * 20))

    # دالة draw ترسم أي مشهد حالي كل إطار
    def draw(self):
        # نرسم الخلفية المتحركة
        draw_background(self.tick)
        # نعرف المشهد الحالي
        s = self.scene
        # إذا القائمة
        if s == "menu":
            # نحسب اهتزازاً بسيطاً للعنوان
            bob = math.sin(self.tick * 0.05) * 6
            # نكتب عنوان اللعبة
            text_center(F_TITLE, "MAZE RUNNER", 120 + bob, ACCENT)
            # نكتب العنوان الفرعي
            text_center(F_BTN, "Breadth-First Search Edition", 195, (150, 92, 148))
            # نكتب جملة تنصح بفتح العرض
            text_center(F_SMALL, "New here? Open the Presentation to see how BFS works", 240, DIM)
            # ونكتب عنوان المشروع بالأسفل
            text_center(F_SMALL, "Maze Solving with Breadth-First Search", H - 24, (130, 92, 132))
        # وإذا الإعدادات
        elif s == "settings":
            # نكتب عنوان الإعدادات
            text_center(F_BIG, "Settings", 150, ACCENT)
            # ونكتب تعليمة التغيير
            text_center(F_SMALL, "Click an option to change it", 215, (150, 92, 148))
        # وإذا العرض التقديمي
        elif s == "present":
            # نرسم العرض
            self.deck.draw()
        # وإذا اللعبة
        elif s == "game":
            # إذا BFS يشتغل تلقائياً ولم ينته
            if self.solver and self.auto and not self.solver.done:
                # ننفذ عدداً من الخطوات حسب السرعة المختارة
                for _ in range(SPEEDS[self.speed_i][1]):
                    # كل خطوة تتنفذ
                    self.solver.step()
            # ثم نرسم اللعبة
            self.draw_game()
        # وإذا شاشة النتيجة
        elif s == "result":
            # نفصل بيانات النتيجة
            outcome, steps, best, explored = self.result
            # إذا فاز اللاعب
            if outcome == "win":
                # نكتب "نجحت"
                text_center(F_TITLE, "You made it!", 110, ACCENT)
                # نحسب الكفاءة: أقصر مسار ÷ خطوات اللاعب
                ratio = best / max(1, steps)
                # ونحدد عدد النجوم من الكفاءة (3 للممتاز و2 للجيد و1 للمقبول)
                stars = 3 if ratio >= 0.9 else 2 if ratio >= 0.6 else 1
                # نمر على 3 نجوم
                for i in range(3):
                    # نرسم النجمة ممتلئة إذا كسبتها
                    draw_star(W // 2 - 90 + i * 90, 215, 34, i < stars)
                # نكتب خطوات اللاعب
                text_center(F_BTN, f"Your steps: {steps}", 300)
                # نكتب أقصر مسار آمن حسب BFS
                text_center(F_BTN, f"BFS shortest safe path: {best}", 345)
                # نكتب عدد الخلايا التي استكشفها BFS
                text_center(F_TXT, f"BFS explored {explored} cells to prove it", 390, DIM)
                # نكتب نسبة الكفاءة
                text_center(F_TXT, f"Efficiency: {int(min(1, ratio) * 100)}%", 425, (150, 92, 148))
            # وإلا (خسر)
            else:
                # نكتب "أكلتك القطة"
                text_center(F_TITLE, "The cat got you!", 120, (200, 48, 78))
                # نكتب عدد خطواته
                text_center(F_BTN, f"You walked {steps} steps", 230)
                # نشرح أن القطط عوائق يتجنبها BFS
                text_center(F_TXT, "Cats are obstacles - BFS routes around them.", 290, DIM)
                # ننصحه بزر التلميح
                text_center(F_TXT, "Try the Hint button (H) to see the safe BFS path.", 325, DIM)

        # نجلب مكان الماوس
        mouse = pygame.mouse.get_pos()
        # نمر على أزرار المشهد
        for b in self.buttons:
            # نحدّث حالة الزر
            b.update(mouse)
            # ونرسمه
            b.draw()

        # إذا في تعتيم جارٍ
        if self.fade > 0:  # fade transition
            # نصنع طبقة وردية فاتحة
            veil = pygame.Surface((W, H))
            veil.fill((255, 240, 246))
            # نضبط شفافيتها حسب مقدار التعتيم
            veil.set_alpha(self.fade)
            # ونرسمها فوق الشاشة
            screen.blit(veil, (0, 0))

    # دالة update_fade تحرك التعتيم عند الانتقال بين المشاهد
    def update_fade(self):
        # إذا نعتّم الشاشة (نخرج من مشهد)
        if self.fade_dir == 1:
            # نزيد التعتيم
            self.fade += 22
            # إذا صارت الشاشة معتمة تماماً
            if self.fade >= 255:
                # نبدأ إظهار المشهد الجديد
                self.fade, self.fade_dir = 255, -1
                # ننتقل فعلياً للمشهد الجديد
                self.scene = self.next_scene
                # إذا هو العرض التقديمي
                if self.scene == "present":
                    # ننشئ العرض من جديد (يبدأ من الشريحة الأولى)
                    self.deck = Deck()
                # نبني أزرار المشهد الجديد
                self.build()
        # وإلا إذا نكشف الشاشة (ندخل المشهد)
        elif self.fade_dir == -1:
            # نقلل التعتيم
            self.fade -= 22
            # إذا زال التعتيم
            if self.fade <= 0:
                # نعلن انتهاء الانتقال
                self.fade, self.fade_dir = 0, 0

    # دالة run هي الحلقة الرئيسية للبرنامج: تعمل بلا توقف حتى نغلق النافذة
    def run(self):
        # خريطة أزرار الاتجاه والحروف (WASD) إلى الاتجاهات الأربعة
        keymap = {pygame.K_UP: "N", pygame.K_w: "N", pygame.K_DOWN: "S", pygame.K_s: "S",
                  pygame.K_LEFT: "W", pygame.K_a: "W", pygame.K_RIGHT: "E", pygame.K_d: "E"}
        # حلقة لا نهائية (كل دورة = إطار واحد)
        while True:
            # نمر على كل حدث (ضغط زر أو حركة ماوس)
            for e in pygame.event.get():
                # إذا ضغطنا إغلاق النافذة
                if e.type == pygame.QUIT:
                    # نغلق pygame
                    pygame.quit()
                    # ونخرج من البرنامج
                    sys.exit()
                # إذا يوجد انتقال جارٍ
                if self.fade_dir != 0:
                    # نتجاهل الأحداث
                    continue
                # إذا ضغط ماوس أثناء العرض التقديمي
                if e.type == pygame.MOUSEBUTTONDOWN and self.scene == "present":
                    # الزر الأيسر يتقدم والأيمن يرجع
                    step = 1 if e.button == 1 else -1 if e.button == 3 else 0
                    # وننتقل للشريحة المطلوبة
                    self.deck.goto(self.deck.idx + step)
                # وإلا إذا ضغط ماوس بالزر الأيسر
                elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    # نمر على الأزرار
                    for b in self.buttons:
                        # إذا الضغطة داخل زر
                        if b.rect.collidepoint(e.pos):
                            # ننفذ فعله
                            b.action()
                            # ونتوقف عن البحث
                            break
                # إذا ضغط زر كيبورد
                if e.type == pygame.KEYDOWN:
                    # زر Esc يرجعنا للقائمة
                    if e.key == pygame.K_ESCAPE and self.scene != "menu":
                        self.go("menu")
                    # وإذا نحن بمشهد اللعبة
                    elif self.scene == "game":
                        # إذا هو زر اتجاه
                        if e.key in keymap:
                            # نحرك الفأر
                            self.move(keymap[e.key])
                        # وإذا هو المسافة
                        elif e.key == pygame.K_SPACE:
                            # نشغّل BFS متحرك
                            self.run_bfs()
                        # وإذا هو Enter
                        elif e.key == pygame.K_RETURN:
                            # ننفذ خطوة BFS واحدة
                            self.step_bfs()
                        # وإذا هو H
                        elif e.key == pygame.K_h:
                            # نشغّل أو نطفي التلميح
                            self.toggle_hint()
                        # وإذا هو N
                        elif e.key == pygame.K_n:
                            # ننشئ متاهة جديدة
                            self.new_maze()
                    # وإذا نحن بالعرض التقديمي
                    elif self.scene == "present":
                        # نمرر الزر لدالة التنقل بين الشرائح
                        self.present_key(e.key)
            # نزيد عدّاد الإطارات
            self.tick += 1
            # نحرّك التعتيم
            self.update_fade()
            # نرسم الشاشة
            self.draw()
            # نعرض ما رسمناه على النافذة
            pygame.display.flip()
            # نحدد سرعة 60 إطار بالثانية
            clock.tick(60)


if __name__ == "__main__":
    # نشغّل البرنامج: ننشئ التطبيق ونبدأ حلقته الرئيسية
    App().run()
