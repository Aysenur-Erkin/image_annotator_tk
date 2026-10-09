import json, csv
from models.annotation import BoxAnnotation, PolygonAnnotation

CSV_FIELDS = ['id', 'image_path', 'type', 'label', 'x1', 'y1', 'x2', 'y2', 'points']

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
    # polygons keep their bounding box in x1..y2 and the corners in
    # "points" as "x y;x y;..."
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_FIELDS)
        for ann in annotations:
            if isinstance(ann, PolygonAnnotation):
                xs = [x for x, y in ann.points]
                ys = [y for x, y in ann.points]
                points = ';'.join(f'{x} {y}' for x, y in ann.points)
                writer.writerow([
                    ann.id, ann.image_path, 'polygon', ann.label,
                    min(xs), min(ys), max(xs), max(ys), points
                ])
            else:
                writer.writerow([
                    ann.id, ann.image_path, 'box', ann.label,
                    ann.x1, ann.y1, ann.x2, ann.y2, ''
                ])

def load_from_csv(filepath):
    annotations = []
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row.get('label') or 'default'
            # older files have no "type" column and only boxes
            if row.get('type') == 'polygon':
                points = [tuple(int(v) for v in p.split())
                          for p in row['points'].split(';')]
                annotations.append(PolygonAnnotation(
                    id=row['id'],
                    image_path=row['image_path'],
                    points=points,
                    label=label
                ))
            else:
                annotations.append(BoxAnnotation(
                    id=row['id'],
                    image_path=row['image_path'],
                    x1=int(row['x1']), y1=int(row['y1']),
                    x2=int(row['x2']), y2=int(row['y2']),
                    label=label
                ))
    return annotations
