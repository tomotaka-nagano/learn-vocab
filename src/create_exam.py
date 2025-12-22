import os
from src.database import Database


DEPLOY_ROOT = r'exams'
TEMPLATE_PATH = r'src\static\exam.html'
REP_E2J = '{{e2j}}'
REP_J2E = '{{j2e}}'
REP_E2J_EX = '{{e2j_ex}}'

exclude_nos: list[int] = []


def _row(no: int, q: str, a: str) -> tuple[str, str]:
    return (
        f'<tr><td>({no})</td><td>{q}</td><td></td></tr>',
        f'<tr><td>({no})</td><td>{q}</td><td>{a}</td></tr>'
    )


def create_exam_e2j(db: Database, start: int, finish: int) -> tuple[str, str]:
    global exclude_nos
    words = db.get_ramdom_words(20, exclude_nos, start, finish)
    rows = []
    anss = []
    for i in enumerate(words):
        q, a = _row(i[0] + 1, i[1].en, i[1].ja)
        rows.append(q)
        anss.append(a)
    exclude_nos += [word.no for word in words]
    return ('\n'.join(rows), '\n'.join(anss))


def create_exam_j2e(db: Database, start: int, finish: int) -> tuple[str, str]:
    global exclude_nos
    words = db.get_ramdom_words(20, exclude_nos, start, finish)
    rows = []
    anss = []
    for i in enumerate(words):
        q, a = _row(i[0] + 21, i[1].ja, i[1].en)
        rows.append(q)
        anss.append(a)
    exclude_nos += [word.no for word in words]
    return ('\n'.join(rows), '\n'.join(anss))


def create_exam_e2j_ex(db: Database, start: int, finish: int) -> str:
    global exclude_nos
    words = db.get_ramdom_words(5, exclude_nos, start, finish)
    rows = []
    anss = []
    for i in enumerate(words):
        q, a = _row(i[0] + 41, i[1].ex_en, i[1].ex_ja)
        rows.append(q)
        anss.append(a)
    exclude_nos += [word.no for word in words]
    return ('\n'.join(rows), '\n'.join(anss))


def create_exam_body(db: Database, start: int, finish: int) -> tuple[str, str]:
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()
    
    e2j, e2j_ans = create_exam_e2j(db, start, finish)
    j2e, j2e_ans = create_exam_j2e(db, start, finish)
    e2j_ex, e2j_ex_ans = create_exam_e2j_ex(db, start, finish)

    html = template
    ans_html = template.replace('回答', '正解')

    html = html.replace(REP_E2J, e2j)
    html = html.replace(REP_J2E, j2e)
    html = html.replace(REP_E2J_EX, e2j_ex)

    ans_html = ans_html.replace(REP_E2J, e2j_ans)
    ans_html = ans_html.replace(REP_J2E, j2e_ans)
    ans_html = ans_html.replace(REP_E2J_EX, e2j_ex_ans)

    return html, ans_html


def get_exam_path(start: int, finish: int) -> tuple[str, str]:
    deploy_dir = os.path.join(DEPLOY_ROOT, f'exam-{start:04}-{finish:04}')
    num_files = len(os.listdir(deploy_dir)) if os.path.exists(deploy_dir) else 0
    index = num_files // 2 + 1
    return (
        os.path.join(deploy_dir, f'exam-{index:03}.html'),
        os.path.join(deploy_dir, f'ans-{index:03}.html')
    )


def save_exam(body_html: str, path: str):
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(body_html)


def create_exam(db: Database, start: int, finish: int):
    body_html, ans_html = create_exam_body(db, start, finish)
    path, ans_path = get_exam_path(start, finish)
    save_exam(body_html, path)
    save_exam(ans_html, ans_path)


if __name__ == '__main__':
    
    db = Database()
    db.load()
    create_exam(db, 1, 100)
