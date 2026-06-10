#!/usr/bin/env python3
"""Valida que cada imagen en dataset/raw/images tenga su .txt en dataset/raw/labels

Ejecutar desde la raíz del proyecto:
  python scripts/validate_dataset.py --src dataset/raw
"""
import os
import argparse


def validate(src):
    img_dir = os.path.join(src, 'images')
    lbl_dir = os.path.join(src, 'labels')
    imgs = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg','.jpeg','.png'))]
    imgs.sort()
    missing = []
    for f in imgs:
        base = os.path.splitext(f)[0]
        lbl = os.path.join(lbl_dir, base + '.txt')
        if not os.path.exists(lbl):
            missing.append(f)
    print(f'Total images: {len(imgs)}')
    print(f'Missing labels: {len(missing)}')
    if missing:
        print('Ejemplos de imágenes sin etiqueta:')
        for m in missing[:20]:
            print(' -', m)
    else:
        print('Todas las imágenes tienen etiquetas.')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--src', default='dataset/raw')
    args = p.parse_args()
    validate(args.src)
