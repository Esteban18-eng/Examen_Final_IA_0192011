#!/usr/bin/env python3
"""Uso:
  python scripts/download_images.py --classes "celular,teclado" --num 200

Esto descargará imágenes en `dataset/raw/images` nombradas como <clase>_0001.jpg, etc.
"""
import argparse
import os
import tempfile
import shutil
from icrawler.builtin import BingImageCrawler


def download_for_class(cls, num, out_dir):
    tmp = tempfile.mkdtemp()
    crawler = BingImageCrawler(storage={'root_dir': tmp})
    try:
        crawler.crawl(keyword=cls, max_num=num)
    except Exception as e:
        print(f"Error descargando {cls}: {e}")
    # move and rename
    files = []
    for root, _, fnames in os.walk(tmp):
        for f in fnames:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                files.append(os.path.join(root, f))
    files.sort()
    os.makedirs(out_dir, exist_ok=True)
    i = 1
    for src in files:
        ext = os.path.splitext(src)[1]
        dst_name = f"{cls.replace(' ','_')}_{i:04d}{ext}"
        dst = os.path.join(out_dir, dst_name)
        try:
            shutil.move(src, dst)
            i += 1
        except Exception as e:
            print(f"No se pudo mover {src}: {e}")
    shutil.rmtree(tmp, ignore_errors=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--classes', required=True, help='Clases separadas por coma, ej: "celular,teclado"')
    p.add_argument('--num', type=int, default=200, help='Número máximo de imágenes por clase')
    p.add_argument('--out', default='dataset', help='Carpeta raíz del dataset')
    args = p.parse_args()

    classes = [c.strip() for c in args.classes.split(',') if c.strip()]
    img_out = os.path.join(args.out, 'raw', 'images')
    os.makedirs(img_out, exist_ok=True)

    for cls in classes:
        print(f'Descargando {args.num} imágenes para clase: {cls}')
        download_for_class(cls, args.num, img_out)
        print(f'Hecho: {cls}')

    print(f'Terminado. Imágenes guardadas en {img_out}')


if __name__ == '__main__':
    main()
