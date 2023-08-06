from collections import defaultdict
import imagehash
from io import BytesIO
import json
import numpy as np
import os
from PIL import Image
import urllib
import cv2


def fail(reason):
  def func(*args, **kwargs):
    raise Exception(reason)
  return func

try:
  from django.core.files.base import ContentFile
except ImportError:
  Contentfile = fail("You must install django.")

from .max_rect import max_rect

def _get_format(img):
  if isinstance(img, np.ndarray):
    return "np"
  return "pil"

def _coerce(img, format_):
  if type(img) == str:
    if img.startswith('data:'):
      if format_ == 'dataurl':
        # currently the only way to output a dataurl is this idempotent action
        return format_
      with urllib.request.urlopen(img) as response:
        with open('/tmp/sprite.png', 'wb') as f:
          f.write(response.read())
        img = Image.open('/tmp/sprite.png', mode="RGBA")

    else:
      img = Image.open(img).convert('RGBA')

  if format_ == "np":
    return np.array(img)

  if format_ == "pil":
    if isinstance(img, Image.Image):
      return img
    if isinstance(img, np.ndarray):
      mode = 'RGBA' if img.shape[-1] == 4 else 'RGB'
      return Image.fromarray(img, mode=mode)
    raise ValueError(f"Unknown image source of type: {type(img)}")

  raise ValueError(f"Unknown image format requested: {format_}")


def make_content_file(img, name):
  img = _coerce(img, "pil")
  img_io = BytesIO()
  img.save(img_io, format=name.split('.')[-1])
  return ContentFile(img_io.getvalue(), name)


def replace_color(data, color1, color2):
  r1, g1, b1 = color1
  r2, g2, b2 = color2

  red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
  mask = (red == r1) & (green == g1) & (blue == b1)
  data[:,:,:3][mask] = [r2, g2, b2]

  return data


def paste_image(back, front, x, y):
  # replaces the pixels of front with back, treating alpha like just another channel
  bh, bw = back.shape[:2]
  fh, fw = front.shape[:2]
  x1, x2 = max(x, 0), min(x+fw, bw)
  y1, y2 = max(y, 0), min(y+fh, bh)
  front_cropped = front[y1-y:y2-y, x1-x:x2-x]
  back_cropped = back[y1:y2, x1:x2]

  result = back.copy()
  result[y1:y2, x1:x2] = front_cropped
  return result


def merge_image(back, front, x, y):
  # like paste image but respects alpha channel (if it exists)
  needs_revert = False
  if back.shape[2] == 3:
    needs_revert = True
    back = cv2.cvtColor(back, cv2.COLOR_BGR2BGRA)
  if front.shape[2] == 3:
    front = cv2.cvtColor(front, cv2.COLOR_BGR2BGRA)

  # crop the overlay from both images
  bh,bw = back.shape[:2]
  fh,fw = front.shape[:2]
  x1, x2 = max(x, 0), min(x+fw, bw)
  y1, y2 = max(y, 0), min(y+fh, bh)
  front_cropped = front[y1-y:y2-y, x1-x:x2-x]
  back_cropped = back[y1:y2, x1:x2]

  alpha_front = front_cropped[:,:,3:4] / 255
  alpha_back = back_cropped[:,:,3:4] / 255

  # replace an area in result with overlay
  result = back.copy()
  result[y1:y2, x1:x2, :3] = alpha_front * front_cropped[:,:,:3] + (1-alpha_front) * back_cropped[:,:,:3]
  result[y1:y2, x1:x2, 3:4] = (alpha_front + alpha_back) / (1 + alpha_front*alpha_back) * 255

  if needs_revert:
    result = cv2.cvtColor(result, cv2.COLOR_BGRA2BGR)
  return result


def get_or_create(image_name, function, path="", force=False):
  target_path = os.path.join(path, image_name)
  if not force and os.path.exists(target_path):
    return Image.open(target_path), False

  image = function()
  image.save(target_path)
  return image, True


# ideally we should do something more like this: https://stackoverflow.com/a/43111221/266564
def analyze_colors(img, ignore_clear=True):
  img = _coerce(img, 'np')
  counts = defaultdict(int)
  ignore_clear = ignore_clear and img.shape[2] == 4
  all_colors = []
  for row in img:
    for color in row:
      if ignore_clear and color[3] == 0:
        continue
      counts[tuple(color)] += 1
      all_colors.append(color[:3])
  average = np.round(np.sum(all_colors, axis=0) / len(all_colors))
  return { 'counts': counts, 'average': average }

def int_to_64bit_array(value):
  array = [int(i) for i in bin(value)[2:]]
  while len(array) < 64:
    array.insert(0, 0)
  return array


def int_to_imagehash(value):
  if isinstance(value, imagehash.ImageHash):
    return value
  hash_ = np.array(int_to_64bit_array(value)).reshape((8, 8))
  return imagehash.ImageHash(hash_)


def imagehash_to_int(value):
  if isinstance(value, int):
    return value
  res = 0
  for row in value.hash:
    for boolean in row:
      res = (res << 1) | int(boolean)
  return res


def color_distance(color1, color2):
  return np.sum(np.abs(np.array(color1) - np.array(color2)))


class NpEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, np.integer):
      return int(obj)
    if isinstance(obj, np.floating):
      return float(obj)
    if isinstance(obj, np.ndarray):
      return obj.tolist()
    return super().default(obj)


def make_holes(image, holes, color=(0,0,0,0)):
    format_ = _get_format(image)
    image = _coerce(image, 'np')
    for x, y in holes:
        image[y*256:(y+1) * 256,x*256:(x+1) * 256,:] = [0,0,0,0]
    return _coerce(image, format_)
