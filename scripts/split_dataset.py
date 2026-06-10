import argparse
import os
import random
import shutil


def make_dirs(dest):
    for t in ['images/train', 'images/val', 'images/test', 'labels/train', 'labels/val', 'labels/test']:
        os.makedirs(os.path.join(dest, t), exist_ok=True)


def split(src, dest, train_ratio=0.7, val_ratio=0.2, seed=42):
    random.seed(seed)
    img_dir = os.path.join(src, 'images')
    lbl_dir = os.path.join(src, 'labels')
    assert os.path.isdir(img_dir), f"Missing {img_dir}"
    assert os.path.isdir(lbl_dir), f"Missing {lbl_dir}"

    images = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg','.jpeg','.png'))]
    images.sort()
    random.shuffle(images)

    n = len(images)
    n_train = int(n * train_ratio)
    n_val = int(n * val_ratio)

    splits = {
        'train': images[:n_train],
        'val': images[n_train:n_train+n_val],
        'test': images[n_train+n_val:]
    }

    make_dirs(dest)

    for part, files in splits.items():
        for fname in files:
            src_img = os.path.join(img_dir, fname)
            src_lbl = os.path.join(lbl_dir, os.path.splitext(fname)[0] + '.txt')
            dst_img = os.path.join(dest, 'images', part, fname)
            dst_lbl = os.path.join(dest, 'labels', part, os.path.splitext(fname)[0] + '.txt')
            shutil.copy2(src_img, dst_img)
            if os.path.exists(src_lbl):
                shutil.copy2(src_lbl, dst_lbl)

    print('Split complete:')
    for part in ['train','val','test']:
        print(part, len(splits[part]))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--src', required=True, help='Source folder with images/ and labels/')
    p.add_argument('--dest', required=True, help='Destination dataset root')
    p.add_argument('--train', type=float, default=0.7)
    p.add_argument('--val', type=float, default=0.2)
    p.add_argument('--seed', type=int, default=42)
    args = p.parse_args()
    split(args.src, args.dest, args.train, args.val, args.seed)
