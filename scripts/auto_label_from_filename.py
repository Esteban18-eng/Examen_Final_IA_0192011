#!/usr/bin/env python3
"""Genera etiquetas YOLO simples basadas en el nombre de archivo.

Regla: si el nombre contiene 'celular' -> class 0, 'teclado' -> class 1.
La caja generada cubrirá gran parte de la imagen (centro, 90% ancho/alto).
Usar solo para pruebas/demo; se recomienda anotar manualmente para entrenamiento real.
"""
import os
from PIL import Image


def process_folder(folder):
    if not os.path.isdir(folder):
        return
    img_files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg','.jpeg','.png'))]
    for f in img_files:
        base = os.path.splitext(f)[0]
        img_path = os.path.join(folder, f)
        # Compute labels folder parallel to images: replace '/images/' with '/labels/'
        if '/images/' in folder.replace('\\','/'):
            lbl_root = folder.replace('images', 'labels')
        else:
            # fallback to dataset/labels/<same-subpath>
            parts = folder.split(os.sep)
            if 'images' in parts:
                idx = parts.index('images')
                parts[idx] = 'labels'
                lbl_root = os.sep.join(parts)
            else:
                lbl_root = os.path.join(os.path.dirname(folder), 'labels')
        lbl_dir = os.path.join(lbl_root)
        os.makedirs(lbl_dir, exist_ok=True)
        lbl_path = os.path.join(lbl_dir, base + '.txt')
        lf = f.lower()
        if 'celular' in lf or 'telefono' in lf or 'phone' in lf:
            cls = 0
        elif 'teclado' in lf or 'keyboard' in lf:
            cls = 1
        else:
            # skip unknown
            continue
        try:
            with Image.open(img_path) as im:
                w, h = im.size
        except Exception:
            continue
        cx = 0.5
        cy = 0.5
        bw = 0.9
        bh = 0.9
        line = f"{cls} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n"
        with open(lbl_path, 'w') as out:
            out.write(line)


def main():
    base = 'dataset'
    parts = ['raw/images', 'images/train', 'images/val', 'images/test']
    for p in parts:
        folder = os.path.join(base, p)
        if os.path.isdir(folder):
            print('Processing', folder)
            process_folder(folder)


if __name__ == '__main__':
    main()
