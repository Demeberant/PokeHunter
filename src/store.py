import json
from pathlib import Path

class AlertStore:
    def __init__(self, path="data/alerts.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.items = self._load()

    def _load(self):
        try:
            return json.loads(self.path.read_text("utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self):
        self.path.write_text(json.dumps(self.items, ensure_ascii=False, indent=2), "utf-8")

    def add(self, item):
        next_id = max([x.get("id", 0) for x in self.items], default=0) + 1
        item = {**item, "id": next_id}
        self.items.append(item)
        self.save()
        return item

    def remove(self, alert_id, user_id):
        old = len(self.items)
        self.items = [x for x in self.items if not (x.get("id") == alert_id and x.get("user_id") == user_id)]
        self.save()
        return len(self.items) < old
