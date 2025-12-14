import json
import os
from dataclasses import dataclass, asdict

DB_PATH = r'src\resource\db.json'


@dataclass
class Word:
    no: int
    en: str
    jp: str
    ex_en: str
    ex_jp: str


class Database:

    db: list[Word]

    def add_to_db(self, source_path: str):
        self.db = self._load_db()
        self._add_to_db(source_path)
        self._save_db()
    
    def load(self):
        self.db = self._load_db()

    def _load_db(self) -> list:
        if os.path.exists(DB_PATH):
            with open(DB_PATH, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                return [Word(**d) for d in data]
        return []
    
    def _add_to_db(self, source_path: str):
        current = self.db[-1].no if self.db else 0
        with open(source_path, 'r', encoding='utf-8') as f:
            data = f.read()
        
        lines = data.split('\n')
        if len(lines) % 5 != 0:
            raise Exception('5の倍数じゃない')

        for i in range(len(lines) // 5):
            word = Word(
                current + 1,
                lines[5 * i + 0],
                lines[5 * i + 1],
                lines[5 * i + 2],
                lines[5 * i + 3],
            )
            self.db.append(word)
            current += 1
    
    def _save_db(self):
        jsonable = [asdict(word) for word in self.db]
        with open(DB_PATH, 'w', encoding='utf-8') as fp:
            json.dump(jsonable, fp, indent=2, ensure_ascii=False)


if __name__ == '__main__':

    db = Database()
    db.add_to_db(r'src\resource\source001-100.txt')
