# -*- coding: utf-8 -*-
"""Генератор статического сайта-редизайна НМБК. Печёт общий хедер/футер/меню
во все страницы и встраивает реальный контент, собранный с nmbc.ru (content/)."""
import os, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, 'content')

# ---------------------------------------------------------------- иконки
IC = {
 'doc':'<path d="M14 3v5h5M7 3h7l5 5v13H7z"/><path d="M9 13h6M9 17h4"/>',
 'users':'<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 6a3 3 0 0 1 0 6M21 20a6 6 0 0 0-4-5.6"/>',
 'building':'<path d="M3 21h18M5 21V7l7-4 7 4v14M9 21v-6h6v6"/>',
 'book':'<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M19 19H6"/>',
 'cap':'<path d="m12 3 9 4-9 4-9-4 9-4Z"/><path d="M3 9v5c0 1.7 4 3 9 3s9-1.3 9-3V9"/>',
 'money':'<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
 'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/>',
 'pin':'<path d="M21 10c0 7-9 12-9 12s-9-5-9-12a9 9 0 0 1 18 0Z"/><circle cx="12" cy="10" r="3"/>',
 'phone':'<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
 'mail':'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 7 10 6 10-6"/>',
 'cal':'<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M3 10h18M8 2v4M16 2v4"/>',
 'search':'<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
 'check':'<path d="M20 6 9 17l-5-5"/>',
 'star':'<path d="m12 2 3 6.5 7 .8-5 4.8 1.3 7-6.3-3.4L5.7 21 7 14.1 2 9.3l7-.8L12 2Z"/>',
 'flask':'<path d="M9 3h6M10 3v6L4 19a1.5 1.5 0 0 0 1.3 2.2h13.4A1.5 1.5 0 0 0 20 19l-6-10V3"/>',
 'mortar':'<path d="M19 14a7 7 0 0 1-14 0M3 14h18M12 3v6"/>',
 'heart':'<path d="M21 9c0 6-9 12-9 12S3 15 3 9a5 5 0 0 1 9.2-2.7A5 5 0 0 1 21 9Z"/>',
 'grid':'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
 'image':'<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="9" r="1.5"/><path d="m21 16-5-5L5 21"/>',
 'briefcase':'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
 'tooth':'<path d="M7 3c2 0 2 1 5 1s3-1 5-1 3 2 3 5c0 4-2 4-2.5 8-.4 3-1 4-2 4s-1.2-3-1.5-5-.7-2-1.5-2-1.2 0-1.5 2-.5 5-1.5 5-1.6-1-2-4C7 13 5 13 5 9c0-3 1-6 3-6Z" transform="scale(0.95) translate(0.6,0)"/>',
 'shield':'<path d="M12 3 5 6v6c0 4 3 7 7 9 4-2 7-5 7-9V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>',
 'plus':'<path d="M12 5v14M5 12h14"/>',
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
}
def svg(name, w=18, cls=''):
    p = IC.get(name, IC['doc'])
    c = (' class="%s"' % cls) if cls else ''
    return ('<svg%s viewBox="0 0 24 24" width="%d" height="%d" fill="none" stroke="currentColor" '
            'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">%s</svg>') % (c, w, w, p)

# ---------------------------------------------------------------- меню
ABOUT = [
 ('Основные сведения','about-osnovnye.html','Реквизиты, история, учредитель'),
 ('Структура и органы управления','about-structure.html','Корпуса, филиалы, советы'),
 ('Документы','about-documents.html','Устав, лицензия, локальные акты'),
 ('Образование','about-education.html','Программы, ГИА, численность'),
 ('Образовательные стандарты','about-standards.html','ФГОС СПО'),
 ('Руководство. Педсостав','about-rukovodstvo.html','Администрация и преподаватели'),
 ('Материально-техническое обеспечение','about-mtb.html','Кабинеты, оборудование, доступная среда'),
 ('Стипендии и меры поддержки','about-stipendii.html','Стипендии, общежитие'),
 ('Платные образовательные услуги','about-platnye.html','Договоры и стоимость'),
 ('Финансово-хозяйственная деятельность','about-finansy.html','Отчётность, госзадание'),
 ('Вакантные места для приёма','about-vakantnye.html','Приём и перевод'),
 ('Международное сотрудничество','about-mezhdunar.html','Сотрудничество'),
 ('Организация питания','about-pitanie.html','Питание обучающихся'),
]
STUDENTS = [
 ('Студенческая жизнь','student-life.html','Самоуправление и события'),
 ('Стипендии и общежитие','about-stipendii.html','Меры поддержки'),
 ('Газета «Студенческий вестник VITA»','http://nmbc.ru/studencheskaja-zhizn/gazeta-studencheskij-vestnik-vita/','Студенческое издание'),
 ('Волонтёрское движение','http://nmbc.ru/studencheskaja-zhizn/volonterskoe-dvizhenie/','Медицинские отряды'),
 ('Спортивно-оздоровительные мероприятия','http://nmbc.ru/studencheskaja-zhizn/sportivno-ozdorovitelnye-meroprijat/','Спорт и здоровье'),
 ('Навигаторы детства','http://nmbc.ru/studencheskaja-zhizn/navigatory-detstva/','Воспитательная работа'),
]
SCIENCE = [
 ('Научная деятельность','science.html','Обзор раздела'),
 ('Студенческое научное общество','http://nmbc.ru/nauchnaja-dejatelnost/studencheskoe-nauchnoe-obshhestvo/','СНО'),
 ('Научно-методическая работа','http://nmbc.ru/nauchnaja-dejatelnost/nauchno-metodicheskaja-rabota-prepodav/','Преподаватели'),
 ('Центр карьеры и трудоустройства','career.html','Выпускникам'),
 ('Наши социальные партнёры','http://nmbc.ru/nashi-socialnye-partnery/','Базы практик'),
 ('Первичная аккредитация','http://nmbc.ru/akkred/','Аккредитация специалистов'),
]
MEDIA = [
 ('Новости','news.html','Лента событий'),
 ('Фотогалерея','media.html','Фотоотчёты'),
 ('Статистика','http://nmbc.ru/statistika/','Показатели'),
 ('Мероприятия','http://nmbc.ru/meroprijatija/','Календарь'),
 ('Выпуски студентов','http://nmbc.ru/vypuski-studentov/','Архив выпусков'),
 ('Карта сайта','sitemap.html','Все разделы'),
]
MENU = [
 ('Сведения','about', ABOUT, 'doc', True),
 ('Поступающему','abiturientu.html', None, None, False),
 ('Студентам','students', STUDENTS, 'users', False),
 ('Наука и карьера','science', SCIENCE, 'cap', False),
 ('Медиа','media', MEDIA, 'image', False),
 ('Контакты','contacts.html', None, None, False),
]
def is_ext(h): return h.startswith('http')
def aattr(h):
    return ' target="_blank" rel="noopener"' if is_ext(h) else ''

# ---------------------------------------------------------------- хедер
def render_mega(items, icon, wide=False, right=False):
    cells = []
    for t in items:
        title, href, desc = t
        cells.append(
          '<a class="m-link" href="%s"%s><span class="m-ico">%s</span>'
          '<span><b>%s</b><small>%s</small></span></a>' % (href, aattr(href), svg(icon,16), title, desc))
    cls = 'mega' + (' wide' if wide else '') + (' right' if right else '')
    foot = ('<div class="mega-foot"><span>Раздел портала НМБК</span>'
            '<a href="sitemap.html">Карта сайта %s</a></div>' % svg('arrow',13))
    return '<div class="%s"><div class="mega-grid">%s</div>%s</div>' % (cls, ''.join(cells), foot)

def render_header(active_key):
    items = []
    for i,(label, key, sub, icon, wide) in enumerate(MENU):
        if sub is None:
            cls = 'nav-link' + (' active' if active_key==key else '')
            items.append('<div class="nav-item"><a href="%s" class="%s">%s</a></div>' % (key, cls, label))
        else:
            cls = 'nav-link' + (' active' if active_key==key else '')
            caret = '<svg class="caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m6 9 6 6 6-6"/></svg>'
            right = i>=4
            items.append('<div class="nav-item"><a href="#" class="%s">%s %s</a>%s</div>' %
                         (cls, label, caret, render_mega(sub, icon, wide=(key=='about'), right=right)))
    nav = '<nav class="primary" aria-label="Основное меню">%s</nav>' % ''.join(items)
    return ('<div class="topbar"><div class="container">'
            '<a href="contacts.html" class="hide-sm">'+svg('pin',14)+' Нижний Новгород, ул. Июльских дней, 8</a>'
            '<span class="spacer"></span>'
            '<a href="http://portal.nmbc.ru/" target="_blank" rel="noopener" class="hide-sm">Портал НМК · АИСТ</a>'
            '<a href="sitemap.html" class="hide-sm">Карта сайта</a>'
            '<a href="tel:+78312821979" class="tb-phone">'+svg('phone',14)+' 8 (831) 282-19-79</a>'
            '<button class="a11y-toggle" id="a11yBtn" aria-pressed="false">'+svg('globe',16)+' Версия для слабовидящих</button>'
            '</div></div>'
            '<header><div class="container head-main">'
            '<a href="index.html" class="brand" aria-label="На главную">'
            '<img class="logo-img" src="assets/img/logo.png" alt="Логотип НМБК">'
            '<span class="brand-text"><strong>Нижегородский<br>медицинский колледж</strong>'
            '<span>ГБПОУ НО «НМБК»</span></span></a>'
            + nav +
            '<a href="abiturientu.html" class="head-cta">'+svg('plus',16)+' Поступающему</a>'
            '<button class="burger" id="burger" aria-label="Открыть меню"><span></span><span></span><span></span></button>'
            '</div></header>')

def render_mobile():
    rows = []
    for label, key, sub, icon, wide in MENU:
        if sub is None:
            rows.append('<div class="mn-acc"><a href="%s">%s</a></div>' % (key, label))
        else:
            links = ''.join('<a href="%s"%s>%s</a>' % (h, aattr(h), t) for t,h,d in sub)
            rows.append('<div class="mn-acc"><button>%s <span class="pl">＋</span></button><div class="mn-sub">%s</div></div>' % (label, links))
    return ('<div class="mobile-nav" id="mobileNav"><div class="mn-panel">'
            '<div class="mn-head"><strong>Меню</strong><button class="mn-close" id="mnClose" aria-label="Закрыть">×</button></div>'
            '<div class="mn-body">%s</div>'
            '<a href="abiturientu.html" class="mn-cta">Поступающему</a>'
            '</div></div>' % ''.join(rows))

SOCIAL = ('<div class="socials">'
 '<a href="https://vk.com/nmbc_nn" target="_blank" rel="noopener" aria-label="ВКонтакте"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12.8 16.3c-5 0-8.2-3.5-8.3-9.3h2.6c.1 4.3 2 6.1 3.5 6.5V7h2.5v3.7c1.5-.2 3-1.9 3.6-3.7h2.4c-.4 2.2-2 3.9-3.1 4.6 1.1.6 3 2.1 3.7 4.7h-2.7c-.5-1.7-1.9-3-3.5-3.2v3.2z"/></svg></a>'
 '<a href="https://rutube.ru/" target="_blank" rel="noopener" aria-label="RuTube"><svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><rect x="2" y="5" width="20" height="14" rx="4"/><path d="M10 9.5v5l4.5-2.5z" fill="#0a6256"/></svg></a>'
 '<a href="http://portal.nmbc.ru/" target="_blank" rel="noopener" aria-label="Портал"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">'+IC["globe"]+'</svg></a>'
 '</div>')

def render_footer():
    about_links = ''.join('<a href="%s">%s</a>' % (h,t) for t,h,d in ABOUT[:6])
    serv = ('<a href="abiturientu.html">Поступающему</a><a href="about-education.html">Образование</a>'
            '<a href="news.html">Новости</a><a href="about-stipendii.html">Стипендии и общежитие</a>'
            '<a href="http://portal.nmbc.ru/" target="_blank" rel="noopener">Портал НМК · АИСТ</a>'
            '<a href="sitemap.html">Карта сайта</a>')
    return ('<footer><div class="container">'
      '<div class="foot-grid">'
      '<div class="foot-brand"><img class="logo-img" src="assets/img/logo.png" alt="НМБК">'
      '<div><strong>Нижегородский медицинский колледж</strong>'
      '<p>ГБПОУ НО «НМБК». Подготовка специалистов среднего медицинского и фармацевтического образования.</p>'
      + SOCIAL + '</div></div>'
      '<div class="foot-col"><h4>Сведения об ОО</h4>'+about_links+'</div>'
      '<div class="foot-col"><h4>Разделы</h4>'+serv+'</div>'
      '<div class="foot-col"><h4>Контакты</h4><ul class="foot-contacts">'
      '<li>'+svg('pin',16)+' 603011, Нижний Новгород, ул. Июльских дней, д. 8</li>'
      '<li>'+svg('phone',16)+' Канцелярия: <a href="tel:+78312821979">8 (831) 282-19-79</a></li>'
      '<li>'+svg('phone',16)+' Приёмная комиссия: <a href="tel:+78312821964">8 (831) 282-19-64</a></li>'
      '<li>'+svg('mail',16)+' <a href="mailto:nmk_suz@mail.52gov.ru">nmk_suz@mail.52gov.ru</a></li>'
      '</ul></div></div>'
      '<div class="foot-bottom"><span>© 2026 ГБПОУ НО «Нижегородский медицинский колледж». '
      'Концепт-редизайн (учебный макет).</span>'
      '<span><a href="http://nmbc.ru/" target="_blank" rel="noopener">Оригинальный сайт nmbc.ru</a> · '
      '<a href="sitemap.html">Карта сайта</a></span></div>'
      '</div></footer>')

def page(title, body, active_key=None, description='', extra_head=''):
    return ('<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">'
      '<meta name="viewport" content="width=device-width, initial-scale=1">'
      '<title>%s | Нижегородский медицинский колледж</title>'
      '<meta name="description" content="%s">'
      '<link rel="preconnect" href="http://nmbc.ru">'
      '<link rel="icon" href="assets/img/logo.png">'
      '<link rel="stylesheet" href="assets/css/style.css">%s</head><body>'
      '<a href="#main" class="skip">Перейти к содержанию</a>'
      + render_header(active_key) +
      '<main id="main">' + body + '</main>'
      + render_footer() + render_mobile() +
      '<script src="assets/js/site.js"></script></body></html>') % (title, description, extra_head)

def frag(name):
    with open(os.path.join(CONTENT, name+'.html'), encoding='utf-8') as f:
        return f.read()

# ---------------------------------------------------------------- inner (Сведения) с боковым меню
def about_sidebar(active_file):
    links = ''.join('<a href="%s"%s>%s</a>' % (h, ' class="active"' if h==active_file else '', t)
                    for t,h,d in ABOUT)
    return '<aside class="side"><h4>Сведения об ОО</h4><nav>%s</nav></aside>' % links

def breadcrumb(*pairs):
    out=['<a href="index.html">Главная</a>']
    for t,h in pairs[:-1]:
        out.append('<span class="sep">/</span><a href="%s">%s</a>'%(h,t))
    out.append('<span class="sep">/</span><span>%s</span>'%pairs[-1][0])
    return '<div class="breadcrumb">%s</div>' % ''.join(out)

def about_page(fname, title, content_name, orig_url, sub=''):
    body = ('<section class="page-hero"><div class="container">'
            + breadcrumb(('Сведения об образовательной организации','about-osnovnye.html'),(title,fname))
            + '<h1>%s</h1>%s</div></section>' % (title, ('<p class="sub">%s</p>'%sub) if sub else ''))
    src = ('<div class="src-note">Информация воспроизведена с официального сайта. '
           'Первоисточник: <a href="%s" target="_blank" rel="noopener">%s</a></div>' % (orig_url, orig_url))
    body += ('<div class="container"><div class="page-wrap">'
             + about_sidebar(fname)
             + '<div class="prose">' + frag(content_name) + src + '</div>'
             '</div></div>')
    return page(title, body, active_key='about', description=sub or title)

# ---------------------------------------------------------------- данные
SPECS = [
 ('31.02.02','Акушерское дело','Акушер / акушерка','3 г. 10 мес.'),
 ('31.02.01','Лечебное дело','Фельдшер','3 г. 10 мес.'),
 ('34.02.01','Сестринское дело','Медсестра / медбрат','очно / очно-заочно'),
 ('33.02.01','Фармация','Фармацевт','очно / заочно'),
 ('31.02.03','Лабораторная диагностика','Мед. лаб. техник','2 г. 10 мес.'),
 ('32.02.01','Медико-профилактическое дело','Санитарный фельдшер','3 г. 10 мес.'),
 ('31.02.05','Стоматология ортопедическая','Зубной техник','2 г. 10 мес.'),
 ('31.02.06','Стоматология профилактическая','Гигиенист','2 г. 10 мес.'),
 ('34.02.02','Медицинский массаж','Для лиц с ОВЗ по зрению','2 г. 10 мес.'),
]
NEWS = [
 ('25.06.2026','Международный день борьбы со злоупотреблением наркотическими средствами: «Твоя жизнь — твой выбор»','n01.jpg','http://nmbc.ru/2026/06/25/mezhdunarodnyj-den-borby-so-zloupotrebleniem-narkoticheskimi-sredstvami-i-ih-nezakonnym-oborotom-tvoja-zhizn-tvoj-vybor/'),
 ('23.06.2026','Мероприятия в День памяти и скорби','n02.jpg','http://nmbc.ru/2026/06/23/23-06-2026-meroprijatija-v-den-pamjati-i-skorbi/'),
 ('21.06.2026','Мероприятия в честь Дня медицинского работника','n03.jpg','http://nmbc.ru/2026/06/23/21-06-2026-meroprijatija-v-chest-dnja-medicinskogo-rabotnika/'),
 ('18.06.2026','Подписание соглашения о вхождении в федеральную программу «Профессионалитет»','n04.jpg','http://nmbc.ru/2026/06/19/18-06-2026-podpisanie-soglashenija-o-vhozhdenie-v-federalnuju-programmu-pobeditelej-vserossijskogo-granta-professionalitet/'),
 ('18.06.2026','Конкурс мультимедийных презентаций «Компьютеры, сохраняющие здоровье»','n05.jpg','http://nmbc.ru/2026/06/18/konkurs-multimedijnyh-prezentacij-kompjutery-sohranjajushhie-zdorove/'),
 ('17.06.2026','Встреча с выпускником колледжа — участником СВО','n06.jpg','http://nmbc.ru/2026/06/17/17-06-2026-vstrecha-s-vypusknikom-kolledzha-uchastnikom-svo/'),
 ('17.06.2026','XXIV межрегиональная конференция «Медицинская наука: вчера, сегодня, завтра»','n07.jpg','http://nmbc.ru/2026/06/17/xxiv-mezhregionalnaja-studencheskaja-nauchno-prakticheskaja-konferencija-medicinskaja-nauka-vchera-segodnja-zavtra/'),
 ('15.06.2026','Мероприятия ко Дню России','n08.jpg','http://nmbc.ru/2026/06/15/15-06-2026-meroprijatija-ko-dnju-rossii/'),
 ('11.06.2026','Участие в акции по сдаче крови на типирование в Центре крови им. Н. Я. Климовой','n09.jpg','http://nmbc.ru/2026/06/15/11-06-2026-uchastie-v-akcii-po-sdache-krovi-na-tipirovanie-v-centre-krovi-im-n-ja-klimovoj/'),
 ('11.06.2026','Подведены итоги Спартакиады СПО 2025–2026 учебного года','n10.jpg','http://nmbc.ru/2026/06/15/11-06-2026-v-ministerstve-sporta-nizhegorodskoj-oblasti-podvedeny-itogi-spartakiady-spo-v-2025-2026-uchebnom-godu/'),
]
CORP = [
 ('Корпус','Административно-учебный корпус № 1','г. Нижний Новгород, ул. Июльских дней, д. 8'),
 ('Корпус','Учебный корпус № 2','г. Нижний Новгород, ул. Родионова, д. 190'),
 ('Корпус','Учебный корпус № 3','г. Нижний Новгород, ул. Павла Мочалова, д. 9'),
 ('Отделение','Вечернее отделение','при НОКБ им. Н. А. Семашко'),
]
FILIALS = ['Богородский','Ветлужский','Городецкий','Дзержинский','Лысковский','Павловский','Семёновский']

SLIDES = ['slide_%02d.jpg' % n for n in range(1,13)]

# ---------------------------------------------------------------- ГЛАВНАЯ
def build_index():
    slides = ''.join('<div class="slide%s" style="background-image:url(assets/img/slides/%s)"></div>'
                     % (' on' if i==0 else '', s) for i,s in enumerate(SLIDES[:6]))
    hero = ('<section class="hero"><div class="container">'
      '<div>'
      '<span class="hero-badge"><span class="dot"></span> Приём 2026 открыт · бюджетные и платные места</span>'
      '<h1>Учим <em>лечить, заботиться</em><br>и помогать людям</h1>'
      '<p class="lead">ГБПОУ НО «Нижегородский медицинский колледж» — одно из крупнейших учреждений '
      'среднего медицинского образования России: учебные корпуса в Нижнем Новгороде и 7 филиалов в области.</p>'
      '<form class="search" role="search" onsubmit="return false">'
      '<input type="search" placeholder="Поиск: расписание, документы, специальности…" aria-label="Поиск">'
      '<button type="submit">'+svg('search',17)+' Найти</button></form>'
      '<div class="hero-tags"><span class="lbl">Популярное:</span>'
      '<a href="abiturientu.html">Приёмная комиссия</a>'
      '<a href="about-education.html">Специальности</a>'
      '<a href="about-stipendii.html">Стипендии</a>'
      '<a href="about-documents.html">Документы</a></div>'
      '</div>'
      '<div class="hero-media">'+slides+
      '<div class="hero-stats"><span>9 специальностей</span><span>7 филиалов</span></div>'
      '<div class="cap">Знакомство с профессией — жизнь колледжа</div></div>'
      '</div></section>')

    # audience
    aud = ('<section class="block"><div class="container"><div class="audience-grid">'
      '<div class="aud-card aud-1"><div class="aud-ico">'+svg('cap',27)+'</div><h3>Абитуриенту</h3>'
      '<p>Специальности, документы и сроки приёмной кампании 2026 года.</p>'
      '<div class="aud-links"><a href="abiturientu.html">Приёмная комиссия<span class="arr">'+svg('arrow',16)+'</span></a>'
      '<a href="abiturientu.html">Документы для поступления<span class="arr">'+svg('arrow',16)+'</span></a>'
      '<a href="about-education.html">Специальности<span class="arr">'+svg('arrow',16)+'</span></a></div></div>'
      '<div class="aud-card aud-2"><div class="aud-ico">'+svg('book',27)+'</div><h3>Студенту</h3>'
      '<p>Портал АИСТ, стипендии, общежитие и студенческая жизнь.</p>'
      '<div class="aud-links"><a href="http://portal.nmbc.ru/" target="_blank" rel="noopener">Портал НМК · АИСТ<span class="arr">'+svg('arrow',16)+'</span></a>'
      '<a href="about-stipendii.html">Стипендии и общежитие<span class="arr">'+svg('arrow',16)+'</span></a>'
      '<a href="student-life.html">Студенческая жизнь<span class="arr">'+svg('arrow',16)+'</span></a></div></div>'
      '<div class="aud-card aud-3"><div class="aud-ico">'+svg('briefcase',27)+'</div><h3>Выпускнику</h3>'
      '<p>Трудоустройство, аккредитация и социальные партнёры.</p>'
      '<div class="aud-links"><a href="career.html">Центр карьеры<span class="arr">'+svg('arrow',16)+'</span></a>'
      '<a href="http://nmbc.ru/akkred/" target="_blank" rel="noopener">Первичная аккредитация<span class="arr">'+svg('arrow',16)+'</span></a>'
      '<a href="http://nmbc.ru/nashi-socialnye-partnery/" target="_blank" rel="noopener">Социальные партнёры<span class="arr">'+svg('arrow',16)+'</span></a></div></div>'
      '</div></div></section>')

    # services
    SERV = [('cal','Расписание','http://portal.nmbc.ru/'),('book','Портал АИСТ','http://portal.nmbc.ru/'),
            ('doc','Приёмная комиссия','abiturientu.html'),('grid','Сведения об ОО','about-osnovnye.html'),
            ('money','Стипендии','about-stipendii.html'),('phone','Контакты','contacts.html')]
    serv = ''.join('<a class="serv" href="%s"%s><span class="serv-ico">%s</span><span>%s</span></a>'
                   % (h, aattr(h), svg(ic,23), t) for ic,t,h in SERV)
    services = ('<section class="block tint"><div class="container">'
      '<div class="sec-head"><div><div class="eyebrow">Быстрый доступ</div><h2>Часто используемые сервисы</h2></div>'
      '<a href="sitemap.html" class="see-all">Все разделы '+svg('arrow',15)+'</a></div>'
      '<div class="serv-grid">'+serv+'</div></div></section>')

    # specialties
    cards=[]
    for code,name,role,dur in SPECS:
        cards.append('<a class="spec" href="about-education.html"><div class="blob"></div>'
          '<div class="code">%s</div><h3>%s</h3><div class="meta"><span>%s</span><span>%s</span></div>'
          '<span class="more">Подробнее '%(code,name,role,dur)+svg('arrow',14)+'</span></a>')
    cards.append('<a class="spec cta-spec" href="abiturientu.html"><div class="code">Приём 2026</div>'
      '<h3>Подайте заявление и выберите специальность</h3>'
      '<span class="more">Поступающему '+svg('arrow',14)+'</span></a>')
    specs = ('<section class="block"><div class="container">'
      '<div class="sec-head"><div><div class="eyebrow">Чему мы учим</div><h2>Специальности колледжа</h2>'
      '<p>Программы подготовки специалистов среднего звена (ППССЗ) по медицине и фармации.</p></div>'
      '<a href="about-education.html" class="see-all">Все программы '+svg('arrow',15)+'</a></div>'
      '<div class="spec-grid">'+''.join(cards)+'</div></div></section>')

    # svedeniya tiles
    tiles=''.join('<a class="sved" href="%s"><span class="n">%d</span>%s</a>'%(h,i+1,t)
                  for i,(t,h,d) in enumerate(ABOUT))
    sved=('<section class="block tint"><div class="container">'
      '<div class="sec-head"><div><div class="eyebrow">Открытость</div>'
      '<h2>Сведения об образовательной организации</h2>'
      '<p>Обязательный раздел по приказу Рособрнадзора — все подразделы в одном месте.</p></div>'
      '<a href="about-osnovnye.html" class="see-all">Открыть раздел '+svg('arrow',15)+'</a></div>'
      '<div class="sved-grid">'+tiles+'</div></div></section>')

    # news
    nc=[]
    for d,t,img,url in NEWS[:8]:
        nc.append('<article class="news"><a href="%s" target="_blank" rel="noopener" class="ph" '
          'style="background-image:url(assets/img/news/%s)"></a><div class="body"><time>%s</time>'
          '<h3>%s</h3><a class="rd" href="%s" target="_blank" rel="noopener">Читать '%(url,img,d,t,url)+svg('arrow',13)+'</a></div></article>')
    news=('<section class="block"><div class="container">'
      '<div class="sec-head"><div><div class="eyebrow">Жизнь колледжа</div><h2>Новости и события</h2></div>'
      '<a href="news.html" class="see-all">Все новости '+svg('arrow',15)+'</a></div>'
      '<div class="news-grid">'+''.join(nc)+'</div></div></section>')

    # structure
    sc=''.join('<div class="struct"><div class="tag">%s</div><h3>%s</h3><p>%s</p></div>'%(tag,n,a) for tag,n,a in CORP)
    fil=''.join('<div class="struct"><div class="tag">Филиал</div><h3>%s филиал</h3>'
                '<p>ГБПОУ НО НМК</p></div>'%f for f in FILIALS[:4])
    structure=('<section class="block tint"><div class="container">'
      '<div class="sec-head"><div><div class="eyebrow">География</div><h2>Корпуса и филиалы</h2>'
      '<p>Учебные корпуса в Нижнем Новгороде, вечернее отделение и 7 филиалов в Нижегородской области.</p></div>'
      '<a href="about-structure.html" class="see-all">Вся структура '+svg('arrow',15)+'</a></div>'
      '<div class="struct-grid">'+sc+fil+'</div></div></section>')

    # banners
    BAN=[('credit.jpg','Образовательный кредит в СПО','abiturientu.html'),
         ('cyber.jpg','Кибергигиена','http://nmbc.ru/'),
         ('takzdorovo.jpg','Так здорово — портал о здоровье','https://www.takzdorovo.ru/')]
    bans=''.join('<a class="ban" href="%s"%s><img src="assets/img/banners/%s" alt="%s" loading="lazy"></a>'
                 %(h,aattr(h),img,t) for img,t,h in BAN)
    bans+=('<a class="ban" href="contacts.html" style="display:grid;place-items:center;min-height:150px;text-align:center;padding:18px">'
           '<span><strong style="display:block;color:var(--brand-dark);font-size:17px">Остались вопросы?</strong>'
           '<span style="color:var(--muted);font-size:13.5px">Свяжитесь с приёмной комиссией</span></span></a>')
    banners=('<section class="block"><div class="container">'
      '<div class="sec-head"><div><div class="eyebrow">Полезное</div><h2>Сервисы и партнёры</h2></div></div>'
      '<div class="ban-grid">'+bans+'</div></div></section>')

    cta=('<section class="block" style="padding-top:0"><div class="container"><div class="cta-inner">'
      '<div class="cta-text"><h2>Хотите учиться у нас? Начните прямо сейчас</h2>'
      '<p>Подайте заявление онлайн или уточните условия приёма в приёмной комиссии.</p></div>'
      '<a href="abiturientu.html" class="cta-btn">Поступающему '+svg('arrow',18)+'</a></div></div></section>')

    body = hero+aud+services+specs+sved+news+structure+banners+cta
    return page('Главная', body, active_key=None,
                description='ГБПОУ НО «Нижегородский медицинский колледж» — официальный сайт (концепт-редизайн).')

# ---------------------------------------------------------------- HUB / прочие
def hub_page(fname, title, sub, items, active_key, icon='grid'):
    cards=''.join('<a class="hub" href="%s"%s><span class="h-ico">%s</span><h3>%s</h3><p>%s</p>'
                  '<span class="go">Открыть %s</span></a>'%(h,aattr(h),svg(icon,21),t,d,svg("arrow",13))
                  for t,h,d in items)
    body=('<section class="page-hero"><div class="container">'
          +breadcrumb((title,fname))+'<h1>%s</h1><p class="sub">%s</p></div></section>'%(title,sub)
          +'<section class="block"><div class="container"><div class="hub-grid">%s</div>'%cards
          +'<div class="src-note">Подробные материалы публикуются на официальном сайте: '
           '<a href="http://nmbc.ru/" target="_blank" rel="noopener">nmbc.ru</a></div>'
          +'</div></section>')
    return page(title, body, active_key=active_key, description=sub)

def build_abiturientu():
    body=('<section class="page-hero"><div class="container">'
          +breadcrumb(('Поступающему','abiturientu.html'))
          +'<h1>Поступающему</h1><p class="sub">Приёмная кампания 2026: специальности, документы, сроки и контакты приёмной комиссии.</p></div></section>')
    info=('<div class="contact-grid" style="margin-bottom:26px">'
      '<div class="cc"><div class="t">Приёмная комиссия</div><h3>2026 год</h3>'
      '<p>'+svg('pin',15)+' г. Н. Новгород, ул. Павла Мочалова, 9</p>'
      '<p>'+svg('phone',15)+' <a href="tel:+78312821964">(831) 282-19-64</a></p>'
      '<p>'+svg('cal',15)+' Пн–Пт, 9:00–15:00 · по предварительной записи</p></div>'
      '<div class="cc"><div class="t">Подача документов</div><h3>Способы</h3>'
      '<p>'+svg('check',15)+' Онлайн (Госуслуги / сайт)</p><p>'+svg('check',15)+' Почтой РФ</p>'
      '<p>'+svg('check',15)+' Лично в приёмной комиссии</p></div>'
      '<div class="cc"><div class="t">Сроки приёма</div><h3>Ключевые даты</h3>'
      '<p>Сестринское, Лечебное дело, Стоматология ортопедическая — до 14.08.2026</p>'
      '<p>Фармация, Лаб. диагностика, Мед-проф. дело, Стоматология профилактическая — до 15.08.2026</p>'
      '<p>Оригиналы документов — до 12:00 17.08.2026</p></div></div>')
    src=('<div class="src-note">Информация воспроизведена с официального сайта. '
         'Первоисточник: <a href="http://nmbc.ru/abiturientu/" target="_blank" rel="noopener">nmbc.ru/abiturientu</a></div>')
    body+=('<section class="block"><div class="container">'+info
           +'<div class="prose">'+frag('abiturientu')+src+'</div></div></section>')
    return page('Поступающему', body, active_key='abiturientu',
                description='Приёмная кампания 2026 — Нижегородский медицинский колледж.')

def build_news():
    items=''.join('<article class="news"><a href="%s" target="_blank" rel="noopener" class="ph" '
      'style="background-image:url(assets/img/news/%s)"></a><div class="body"><time>%s</time>'
      '<h3>%s</h3><a class="rd" href="%s" target="_blank" rel="noopener">Читать полностью '%(url,img,d,t,url)+svg('arrow',13)+'</a></div></article>'
      for d,t,img,url in NEWS)
    body=('<section class="page-hero"><div class="container">'+breadcrumb(('Новости','news.html'))
      +'<h1>Новости и события</h1><p class="sub">Актуальные события Нижегородского медицинского колледжа.</p></div></section>'
      +'<section class="block"><div class="container"><div class="news-grid">'+items+'</div>'
      +'<div class="src-note">Полный архив новостей — на официальном сайте: '
       '<a href="http://nmbc.ru/" target="_blank" rel="noopener">nmbc.ru</a></div></div></section>')
    return page('Новости', body, active_key='media', description='Новости НМБК')

def build_media():
    gal=''.join('<a class="gal" href="http://nmbc.ru/fotogalereja/" target="_blank" rel="noopener">'
                '<img src="assets/img/slides/%s" alt="Фото колледжа" loading="lazy"></a>'%s for s in SLIDES)
    body=('<section class="page-hero"><div class="container">'+breadcrumb(('Медиа','media.html'),('Фотогалерея','media.html'))
      +'<h1>Фотогалерея и медиа</h1><p class="sub">Фотоотчёты о жизни колледжа, мероприятиях и буднях студентов.</p></div></section>'
      +'<section class="block"><div class="container"><div class="gal-grid">'+gal+'</div>'
      +'<div class="src-note">Полная фотогалерея: '
       '<a href="http://nmbc.ru/fotogalereja/" target="_blank" rel="noopener">nmbc.ru/fotogalereja</a></div></div></section>')
    return page('Фотогалерея', body, active_key='media', description='Фотогалерея НМБК')

def build_contacts():
    corp=''.join('<div class="cc"><div class="t">%s</div><h3>%s</h3><p>'%(tag,n)+svg('pin',15)+' %s</p></div>'%a for tag,n,a in CORP)
    fil=''.join('<div class="cc"><div class="t">Филиал</div><h3>%s филиал</h3><p>ГБПОУ НО НМК</p></div>'%f for f in FILIALS)
    body=('<section class="page-hero"><div class="container">'+breadcrumb(('Контакты','contacts.html'))
      +'<h1>Контакты</h1><p class="sub">Реквизиты, телефоны, адреса корпусов и филиалов колледжа.</p></div></section>'
      +'<section class="block"><div class="container">'
      +'<div class="contact-grid" style="margin-bottom:24px">'
      +'<div class="cc"><div class="t">Канцелярия</div><h3>Общие вопросы</h3>'
        '<p>'+svg('phone',15)+' <a href="tel:+78312821979">(831) 282-19-79</a></p>'
        '<p>'+svg('mail',15)+' <a href="mailto:nmk_suz@mail.52gov.ru">nmk_suz@mail.52gov.ru</a></p>'
        '<p>'+svg('pin',15)+' 603011, Н. Новгород, ул. Июльских дней, 8</p></div>'
      +'<div class="cc"><div class="t">Приёмная комиссия</div><h3>Поступающим</h3>'
        '<p>'+svg('phone',15)+' <a href="tel:+78312821964">(831) 282-19-64</a></p>'
        '<p>'+svg('pin',15)+' г. Н. Новгород, ул. Павла Мочалова, 9</p>'
        '<p>'+svg('cal',15)+' Пн–Пт, 9:00–15:00</p></div>'
      +'<div class="cc"><div class="t">Учредитель</div><h3>Минздрав НО</h3>'
        '<p>'+svg('pin',15)+' 603022, Н. Новгород, ул. Малая Ямская, 78а</p>'
        '<p>'+svg('phone',15)+' (831) 435-30-74</p>'
        '<p>'+svg('mail',15)+' minzdrav@nobl.ru</p></div></div>'
      +'<h2 style="font-size:22px;margin:10px 0 14px">Учебные корпуса в Нижнем Новгороде</h2>'
      +'<div class="contact-grid" style="margin-bottom:24px">'+corp+'</div>'
      +'<h2 style="font-size:22px;margin:10px 0 14px">Филиалы в Нижегородской области</h2>'
      +'<div class="contact-grid">'+fil+'</div>'
      +'<div class="src-note">Полные реквизиты и адреса всех подразделений: '
       '<a href="about-osnovnye.html">Основные сведения</a> · '
       '<a href="http://nmbc.ru/svedenija-o-nas/kontaktnye-dannye/" target="_blank" rel="noopener">оригинал</a></div>'
      +'</div></section>')
    return page('Контакты', body, active_key='contacts', description='Контакты НМБК')

def build_sitemap():
    def col(title, items):
        links=''.join('<a href="%s"%s>%s</a>'%(h,aattr(h),t) for t,h,*_ in items)
        return '<div class="map-col"><h3>%s</h3>%s</div>'%(title,links)
    cols=[]
    cols.append(col('Сведения об ОО', ABOUT))
    cols.append(col('Студентам', [('Поступающему','abiturientu.html')]+STUDENTS))
    cols.append(col('Наука и карьера', SCIENCE))
    cols.append(col('Медиа и информация', MEDIA))
    cols.append(col('Контакты и сервисы', [('Контакты','contacts.html'),('Новости','news.html'),
        ('Фотогалерея','media.html'),('Портал НМК · АИСТ','http://portal.nmbc.ru/'),
        ('Онлайн-запись на подачу документов','http://sc.nmbc.ru/'),('Оригинальный сайт','http://nmbc.ru/')]))
    body=('<section class="page-hero"><div class="container">'+breadcrumb(('Карта сайта','sitemap.html'))
      +'<h1>Карта сайта</h1><p class="sub">Все разделы портала НМБК в одном месте.</p></div></section>'
      +'<section class="block"><div class="container"><div class="map-grid">'+''.join(cols)+'</div></div></section>')
    return page('Карта сайта', body, active_key='media', description='Карта сайта НМБК')

# ---------------------------------------------------------------- запись файлов
def write(fname, content):
    with open(os.path.join(ROOT, fname),'w',encoding='utf-8') as f: f.write(content)
    return fname

ABOUT_SRC = {
 'about-osnovnye.html':('Основные сведения','kontaktnye','http://nmbc.ru/svedenija-o-nas/kontaktnye-dannye/','Полное наименование, учредитель, режим работы, реквизиты и адреса.'),
 'about-structure.html':('Структура и органы управления','structure','http://nmbc.ru/svedenija-o-nas/structure/','Органы управления, учебные корпуса и филиалы колледжа.'),
 'about-documents.html':('Документы','dokumenty','http://nmbc.ru/svedenija-o-nas/dokumenty/','Устав, лицензия, локальные нормативные акты и отчёты.'),
 'about-education.html':('Образование','obrazovanie','http://nmbc.ru/svedenija-o-nas/obrazovanie/','Реализуемые программы, ГИА, численность обучающихся, трудоустройство.'),
 'about-standards.html':('Образовательные стандарты и требования','standarty','http://nmbc.ru/svedenija-o-nas/obrazovatelnye-standarty/','Федеральные государственные образовательные стандарты СПО.'),
 'about-rukovodstvo.html':('Руководство. Педагогический состав','rukovodstvo','http://nmbc.ru/svedenija-o-nas/rukovodstvo-pedagogicheskij-sostav/','Администрация колледжа и педагогический коллектив.'),
 'about-mtb.html':('Материально-техническое обеспечение','mtb','http://nmbc.ru/svedenija-o-nas/materialno-tehnicheskoe-obespechenie/','Кабинеты, лаборатории, оборудование и доступная среда.'),
 'about-stipendii.html':('Стипендии и меры поддержки обучающихся','stipendii','http://nmbc.ru/svedenija-o-nas/stipendii-i-vidy-materialnoj-podderzhki/','Стипендиальное обеспечение и студенческое общежитие.'),
 'about-platnye.html':('Платные образовательные услуги','platnye','http://nmbc.ru/svedenija-o-nas/platnye-obrazovatelnye-uslugi/','Условия и стоимость обучения по договорам.'),
 'about-finansy.html':('Финансово-хозяйственная деятельность','finansy','http://nmbc.ru/svedenija-o-nas/finansovo-hozjajstvennaja-dejatelnost/','Бухгалтерская отчётность, государственное задание, ПФХД.'),
 'about-vakantnye.html':('Вакантные места для приёма (перевода)','vakantnye','http://nmbc.ru/svedenija-o-nas/vakantnye-mesta-dlja-priema-perevoda/','Вакантные места для приёма и перевода обучающихся.'),
 'about-mezhdunar.html':('Международное сотрудничество','mezhdunar','http://nmbc.ru/svedenija-o-nas/mezhdunarodnoe-sotrudnichestvo/','Международное сотрудничество колледжа.'),
 'about-pitanie.html':('Организация питания в образовательной организации','pitanie','http://nmbc.ru/svedenija-o-nas/organizacija-pitanija/','Организация питания обучающихся.'),
}

def main():
    written=[]
    written.append(write('index.html', build_index()))
    for fn,(title,cn,url,sub) in ABOUT_SRC.items():
        written.append(write(fn, about_page(fn,title,cn,url,sub)))
    written.append(write('abiturientu.html', build_abiturientu()))
    written.append(write('student-life.html', hub_page('student-life.html','Студенческая жизнь',
        'Самоуправление, волонтёрство, спорт, творчество и общественная жизнь студентов.', STUDENTS[2:]+[
        ('Гражданско-правовая деятельность','http://nmbc.ru/studencheskaja-zhizn/organizacija-grazhdansko-pravovoj-dejatelnosti/','Правовое воспитание'),
        ('Конкурсы, конференции, семинары','http://nmbc.ru/studencheskaja-zhizn/uchastie-studentov-v-konkursah-konferencijah-seminarah/','Участие студентов')],
        'students','users')))
    written.append(write('science.html', hub_page('science.html','Научная деятельность',
        'Научно-методическая работа, студенческое научное общество и профессиональные конкурсы.', [
        ('Студенческое научное общество','http://nmbc.ru/nauchnaja-dejatelnost/studencheskoe-nauchnoe-obshhestvo/','СНО колледжа'),
        ('Научно-методическая работа','http://nmbc.ru/nauchnaja-dejatelnost/nauchno-metodicheskaja-rabota-prepodav/','Преподаватели'),
        ('Профессиональные конкурсы','http://nmbc.ru/nauchnaja-dejatelnost/professionalnye-konkursy/','Конкурсы мастерства'),
        ('Мероприятия Совета директоров МФПОО ПФО','http://nmbc.ru/nauchnaja-dejatelnost/meroprijatija-po-planu-soveta-direktorov-mfpoo-pfo/','План мероприятий')],
        'science','cap')))
    written.append(write('career.html', hub_page('career.html','Трудоустройство и карьера',
        'Содействие трудоустройству выпускников, социальные партнёры и вакансии.', [
        ('Центр карьеры и трудоустройства','http://nmbc.ru/slujbasodtrvyp/','Служба содействия выпускникам'),
        ('Наши социальные партнёры','http://nmbc.ru/nashi-socialnye-partnery/','Базы практик и работодатели'),
        ('Вакансии для выпускников','http://nmbc.ru/vakansii-vypusknikam/','Предложения работодателей'),
        ('Вакансии колледжа','http://nmbc.ru/vakansii/','Работа в колледже'),
        ('Первичная аккредитация','http://nmbc.ru/akkred/','Аккредитация специалистов')],
        'science','briefcase')))
    written.append(write('news.html', build_news()))
    written.append(write('media.html', build_media()))
    written.append(write('contacts.html', build_contacts()))
    written.append(write('sitemap.html', build_sitemap()))
    print('WROTE %d pages:'%len(written))
    for w in written: print('  ',w)

if __name__=='__main__':
    main()
