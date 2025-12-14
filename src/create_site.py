from src.database import Database


DEPLOY_PATH = r'docs\index.html'
TEMPLATE_PATH = r'src\static\template.html'
REP_ORG = "'WORDS_DEF'"


def convert_to_js_text(db: Database, start: int, finish: int) -> str:
    data = db.db[start - 1: finish]
    lines = [f'{{no: {w.no}, en: "{w.en}", ja: "{w.jp}", ex_en: "{w.ex_en}", ex_jp: "{w.ex_jp}"}}' for w in data]
    joiner = ',\n' + ' ' * 10
    return joiner.join(lines)

def create_html(rep_text: str):
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        template = f.read()
    html = template.replace(REP_ORG, rep_text)
    with open(DEPLOY_PATH, 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':

    db = Database()
    db.load()
    rep_text = convert_to_js_text(db, 1, 100)
    create_html(rep_text)
