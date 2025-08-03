import json, csv
from models.annotation import BoxAnnotation, PolygonAnnotation

def save_to_json(annotations, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump([ann.to_dict() for ann in annotations],
                  f, ensure_ascii=False, indent=2)

def load_from_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    result = []
    for item in data:
        t = item.get("type", "box")
        if t == "box":
            result.append(BoxAnnotation.from_dict(item))
        elif t == "polygon":
            result.append(PolygonAnnotation.from_dict(item))
    return result

def save_to_csv(annotations, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id','image_path','x1','y1','x2','y2','label'])
        for ann in annotations:
            if isinstance(ann, BoxAnnotation):
                writer.writerow([
                    ann.id, ann.image_path,
                    ann.x1, ann.y1, ann.x2, ann.y2,
                    ann.label
                ])

def load_from_csv(filepath):
    annotations = []
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            annotations.append(BoxAnnotation(
                id=row['id'],
                image_path=row['image_path'],
                x1=int(row['x1']), y1=int(row['y1']),
                x2=int(row['x2']), y2=int(row['y2']),
                label=row.get('label', 'default')
            ))
    return annotations
